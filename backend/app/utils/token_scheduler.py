"""
定時任務 - 清理過期的JWT token
"""

import threading
import time
import logging
from app.utils.token_blacklist import token_blacklist


class TokenCleanupScheduler:
    def __init__(self, interval_minutes=60):
        """
        初始化清理調度器

        Args:
            interval_minutes: 清理間隔（分鐘）
        """
        self.interval = interval_minutes * 60  # 轉換為秒
        self.running = False
        self.thread = None

    def start(self):
        """啟動定時清理"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.thread.start()
        logging.info(
            f"Token cleanup scheduler started (interval: {self.interval/60} minutes)"
        )

    def stop(self):
        """停止定時清理"""
        self.running = False
        if self.thread:
            self.thread.join()
        logging.info("Token cleanup scheduler stopped")

    def _cleanup_loop(self):
        """清理循環"""
        while self.running:
            try:
                cleaned_count = token_blacklist.cleanup_expired_tokens()
                if cleaned_count > 0:
                    logging.info(
                        f"Cleaned {cleaned_count} expired tokens from blacklist"
                    )

                # 獲取統計信息
                stats = token_blacklist.get_blacklist_stats()
                logging.debug(f"Blacklist stats: {stats}")

            except Exception as e:
                logging.error(f"Error during token cleanup: {e}")

            # 等待下次清理
            time.sleep(self.interval)


# 全局清理調度器實例
cleanup_scheduler = TokenCleanupScheduler(interval_minutes=30)  # 每30分鐘清理一次
