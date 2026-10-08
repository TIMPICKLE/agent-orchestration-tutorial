"""03: 收件箱/发件箱 + 丢失响应后的对账。两个 SQLite 文件模拟两个系统。"""
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory


class FakeProvider:
    """模拟支持幂等键和查询的外部服务；绝不发送真实通知。"""
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS effects (key TEXT PRIMARY KEY, body TEXT NOT NULL)")
        self.lose_next_response = False

    def lookup(self, key):
        row = self.db.execute("SELECT body FROM effects WHERE key=?", (key,)).fetchone()
        return row[0] if row else None

    def send(self, key, body):
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO effects VALUES (?, ?)", (key, body))
            # 插入/去重后在同一事务中核对，避免只在写入前检查旧内容。
            if self.lookup(key) != body:
                raise ValueError("idempotency key reused for different payload")
        # 注入最危险的窗口：外部副作用已成功，但本地没收到响应。
        if self.lose_next_response:
            self.lose_next_response = False
            raise TimeoutError("side effect committed; response lost")

    def count(self):
        return self.db.execute("SELECT COUNT(*) FROM effects").fetchone()[0]

    def close(self):
        self.db.close()


class Delivery:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS inbox (event_id TEXT PRIMARY KEY, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS outbox
              (key TEXT PRIMARY KEY, body TEXT NOT NULL, status TEXT NOT NULL);
        """)

    def receive(self, event_id, body):
        # inbox 和 outbox 在同一事务中落盘：没有‘收到却忘了安排’的窗口。
        with self.db:
            row = self.db.execute("SELECT body FROM inbox WHERE event_id=?", (event_id,)).fetchone()
            if row:
                if row[0] != body:
                    raise ValueError("event ID reused for different payload")
                return False
            self.db.execute("INSERT INTO inbox VALUES (?, ?)", (event_id, body))
            self.db.execute("INSERT INTO outbox VALUES (?, ?, 'pending')", ("notify:" + event_id, body))
        return True

    def deliver(self, key, provider):
        row = self.db.execute("SELECT body, status FROM outbox WHERE key=?", (key,)).fetchone()
        if row is None:
            raise KeyError(key)
        body, status = row
        if status == "sent":
            return "already_sent"
        observed = provider.lookup(key)  # 先查外部事实，不能把超时当成失败。
        if observed is not None and observed != body:
            raise ValueError("provider payload conflict; manual reconciliation needed")
        outcome = "reconciled" if observed is not None else "sent"
        if observed is None:
            try:
                provider.send(key, body)
            except TimeoutError:
                return "unknown"  # 保留待对账状态；不谎报成功/失败。
        with self.db:
            self.db.execute("UPDATE outbox SET status='sent' WHERE key=?", (key,))
        return outcome

    def close(self):
        self.db.close()


if __name__ == "__main__":
    with TemporaryDirectory() as directory:
        root = Path(directory)
        delivery, provider = Delivery(root / "local.db"), FakeProvider(root / "provider.db")
        print(f"first_event={delivery.receive('event-1042', 'demo-1042 ready for review')}")
        print(f"duplicate_event={delivery.receive('event-1042', 'demo-1042 ready for review')}")
        provider.lose_next_response = True
        print("first_attempt=" + delivery.deliver("notify:event-1042", provider))
        delivery.close()
        delivery = Delivery(root / "local.db")  # 重建对象，读取已持久化的 outbox。
        print("after_reopen=" + delivery.deliver("notify:event-1042", provider))
        print(f"external_effects={provider.count()}")
        delivery.close()
        provider.close()
