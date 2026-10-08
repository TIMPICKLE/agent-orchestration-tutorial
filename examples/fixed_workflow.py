"""01: 固定流程。候选实现早已写好，不会真的让模型修改文件。"""
import re
from decimal import Decimal

WORK_ITEM = "demo-1042"
# 接受非负 ASCII 数字；逗号必须三位分组；小数若出现则恰好两位。
AMOUNT = re.compile(r"(?:[0-9]+|[1-9][0-9]{0,2}(?:,[0-9]{3})+)(?:\.[0-9]{2})?")


def original(text):
    return Decimal(text)  # 原来的缺陷：不接受千位逗号。


def tempting_fix(text):
    return Decimal(text.replace(",", ""))  # 看似修好了，却放过错误分组。


def parse_amount(text):
    if not isinstance(text, str) or AMOUNT.fullmatch(text) is None:
        raise ValueError("amount does not match the documented grammar")
    return Decimal(text.replace(",", ""))


def acceptance_failures(parser):
    """测试是完成证据；模型说‘完成’不是。返回便于阅读的失败列表。"""
    failures = []
    for text, expected in [("1,234.50", "1234.50"), ("0.00", "0.00"),
                           ("12", "12"), ("1234.50", "1234.50")]:
        try:
            if parser(text) != Decimal(expected):
                failures.append("wrong value: " + text)
        except Exception:
            failures.append("rejected valid input: " + text)
    for text in ["12,34.50", "1,,234.50", "-1.00", "1e3", " 1.00", "NaN", "1.2"]:
        try:
            parser(text)
        except (ValueError, ArithmeticError):
            pass
        else:
            failures.append("accepted invalid input: " + text)
    return failures


def run_workflow():
    # 程序预先决定顺序，没有模型决策。
    before = acceptance_failures(original)
    after = acceptance_failures(parse_amount)
    return {"work_item": WORK_ITEM, "initial_failed": bool(before),
            "tests_passed": not after, "status": "ready_for_review" if not after else "blocked"}


if __name__ == "__main__":
    result = run_workflow()
    print(f"{result['work_item']}: initial_failed={result['initial_failed']}")
    print(f"tests_passed={result['tests_passed']}; status={result['status']}")
    print(f"tempting_fix rejected by regression suite={bool(acceptance_failures(tempting_fix))}")
