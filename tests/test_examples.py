"""Offline assertions and deterministic fault injection; no third-party services."""
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from examples.fixed_workflow import parse_amount, tempting_fix, acceptance_failures, run_workflow
from examples.bounded_loop import Action, ScriptedFakeModel, run_agent, demo_model
from examples.message_delivery import Delivery, FakeProvider
from examples.approval_resume import (new_state, grant_simulated_approval, save_state,
                                     load_state, resume, version_of, FakeReviewProvider)


class WorkflowTests(unittest.TestCase):
    def test_original_failure_and_fixed_success(self):
        result = run_workflow()
        self.assertTrue(result["initial_failed"])
        self.assertTrue(result["tests_passed"])
        self.assertEqual(result["status"], "ready_for_review")

    def test_valid_grammar(self):
        for text in ("0", "0012", "1,234", "12,345,678.90", "1234.50"):
            with self.subTest(text=text):
                self.assertEqual(parse_amount(text), Decimal(text.replace(",", "")))

    def test_invalid_grammar(self):
        for text in ("12,34.50", "01,234.50", "1,2345", "1.2", "1.234", "1.",
                     "-1.00", "+1.00", "1e3", "NaN", "Infinity", "１.００", "1.00\n",
                     " 1.00", "$1.00", "", None):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_amount(text)

    def test_false_positive_repair(self):
        self.assertEqual(tempting_fix("1,234.50"), Decimal("1234.50"))
        self.assertIn("accepted invalid input: 12,34.50", acceptance_failures(tempting_fix))

    def test_decimal_avoids_float_rounding(self):
        self.assertEqual(parse_amount("0.10") + parse_amount("0.20"), Decimal("0.30"))


class AgentTests(unittest.TestCase):
    def test_repair_after_feedback(self):
        model = demo_model()
        result = run_agent(model)
        self.assertEqual(result["status"], "ready_for_review")
        self.assertEqual(result["steps"], 5)
        self.assertTrue(model.observations[2]["failures"])
        self.assertFalse(model.observations[4]["failures"])

    def test_budget_exhausted(self):
        result = run_agent(demo_model(), max_steps=2)
        self.assertEqual(result["status"], "budget_exhausted")
        self.assertEqual(result["steps"], 2)

    def test_zero_budget(self):
        self.assertEqual(run_agent(demo_model(), max_steps=0)["steps"], 0)

    def test_unverified_finish(self):
        result = run_agent(ScriptedFakeModel([Action("finish")]))
        self.assertEqual(result["status"], "unverified_finish")

    def test_new_patch_invalidates_old_test(self):
        model = ScriptedFakeModel([Action("select_patch", "validated"), Action("test"),
                                   Action("select_patch", "strip_commas"), Action("finish")])
        self.assertEqual(run_agent(model)["status"], "unverified_finish")

    def test_unknown_tool_denied(self):
        self.assertEqual(run_agent(ScriptedFakeModel([Action("send_real_email")]))["status"], "denied_action")

    def test_unknown_patch_denied(self):
        model = ScriptedFakeModel([Action("select_patch", "untrusted_path")])
        self.assertEqual(run_agent(model)["status"], "denied_action")

    def test_invalid_action(self):
        self.assertEqual(run_agent(ScriptedFakeModel(["oops"]))["status"], "invalid_action")


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.delivery = Delivery(self.root / "local.db")
        self.provider = FakeProvider(self.root / "provider.db")

    def tearDown(self):
        self.delivery.close()
        self.provider.close()
        self.directory.cleanup()

    def test_duplicate_message(self):
        self.assertTrue(self.delivery.receive("e1", "ready"))
        self.assertFalse(self.delivery.receive("e1", "ready"))
        self.assertEqual(self.delivery.deliver("notify:e1", self.provider), "sent")
        self.assertEqual(self.delivery.deliver("notify:e1", self.provider), "already_sent")
        self.assertEqual(self.provider.count(), 1)

    def test_lost_response_and_reopened_databases(self):
        self.delivery.receive("e1", "ready")
        self.provider.lose_next_response = True
        self.assertEqual(self.delivery.deliver("notify:e1", self.provider), "unknown")
        self.assertEqual(self.provider.count(), 1)  # 响应丢了，副作用仍然存在。
        self.delivery.close()
        self.provider.close()
        self.delivery = Delivery(self.root / "local.db")
        self.provider = FakeProvider(self.root / "provider.db")
        self.assertEqual(self.delivery.deliver("notify:e1", self.provider), "reconciled")
        self.assertEqual(self.provider.count(), 1)

    def test_event_payload_collision(self):
        self.delivery.receive("e1", "ready")
        with self.assertRaises(ValueError):
            self.delivery.receive("e1", "changed")

    def test_provider_idempotency_and_collision(self):
        self.provider.send("k1", "ready")
        self.provider.send("k1", "ready")
        self.assertEqual(self.provider.count(), 1)
        with self.assertRaises(ValueError):
            self.provider.send("k1", "changed")

    def test_reconciliation_payload_mismatch(self):
        self.delivery.receive("e1", "ready")
        self.provider.send("notify:e1", "wrong")
        with self.assertRaises(ValueError):
            self.delivery.deliver("notify:e1", self.provider)

    def test_unknown_outbox_key(self):
        with self.assertRaises(KeyError):
            self.delivery.deliver("missing", self.provider)


class ApprovalTests(unittest.TestCase):
    def test_missing_approval_has_no_effect(self):
        provider = FakeReviewProvider()
        self.assertEqual(resume(new_state("v1"), provider), "approval_required")
        self.assertEqual(provider.drafts, {})

    def test_save_load_and_approved_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            state, provider = new_state("v1"), FakeReviewProvider()
            grant_simulated_approval(state)
            save_state(path, state)
            loaded = load_state(path)
            self.assertEqual(loaded, state)
            self.assertEqual(resume(loaded, provider), "published_simulated")
            self.assertEqual(resume(loaded, provider), "published_simulated")
            self.assertEqual(len(provider.drafts), 1)

    def test_changed_version_invalidates_approval(self):
        state, provider = new_state("v1"), FakeReviewProvider()
        grant_simulated_approval(state)
        state.update(content="v2", version=version_of("v2"))
        self.assertEqual(resume(state, provider), "approval_required")
        self.assertEqual(provider.drafts, {})

    def test_tampered_content(self):
        state, provider = new_state("v1"), FakeReviewProvider()
        grant_simulated_approval(state)
        state["content"] = "v2"
        self.assertEqual(resume(state, provider), "invalid_artifact_version")
        self.assertEqual(provider.drafts, {})

    def test_changed_scope_invalidates_approval(self):
        for field in ("task", "action", "target"):
            state, provider = new_state("v1"), FakeReviewProvider()
            grant_simulated_approval(state)
            state[field] = "different"
            with self.subTest(field=field):
                self.assertEqual(resume(state, provider), "approval_required")
                self.assertEqual(provider.drafts, {})


if __name__ == "__main__":
    unittest.main()
