"""
JWT黑名單管理
"""

from datetime import datetime, timezone
from flask_jwt_extended import decode_token
from app.extensions import jwt
import logging


class TokenBlacklist:
    def __init__(self):
        # 存儲格式: {jti: {'exp': expiration_timestamp, 'type': 'access'/'refresh'}}
        self._blacklisted_tokens = {}

    def add_token(self, jti, exp_timestamp, token_type="access"):
        """添加token到黑名單"""
        self._blacklisted_tokens[jti] = {
            "exp": exp_timestamp,
            "type": token_type,
            "blacklisted_at": datetime.now(timezone.utc).timestamp(),
        }
        logging.info(f"Token {jti} ({token_type}) added to blacklist")

    def is_token_revoked(self, jti):
        """檢查token是否在黑名單中"""
        return jti in self._blacklisted_tokens

    def cleanup_expired_tokens(self):
        """清理已過期的token（定期維護）"""
        current_time = datetime.now(timezone.utc).timestamp()
        expired_tokens = []

        for jti, token_info in self._blacklisted_tokens.items():
            # 如果token已經過期，從黑名單中移除（因為過期的token自然無效）
            if token_info["exp"] < current_time:
                expired_tokens.append(jti)

        for jti in expired_tokens:
            del self._blacklisted_tokens[jti]
            logging.info(f"Removed expired token {jti} from blacklist")

        return len(expired_tokens)

    def auto_blacklist_expired_refresh_tokens(self):
        """自動將過期的refresh token加入黑名單（這個方法需要與實際的token存儲結合）"""
        # 這個方法更多是概念性的，實際實現需要根據你的token存儲策略
        pass

    def get_blacklist_stats(self):
        """獲取黑名單統計信息"""
        current_time = datetime.now(timezone.utc).timestamp()
        total = len(self._blacklisted_tokens)
        expired = sum(
            1
            for info in self._blacklisted_tokens.values()
            if info["exp"] < current_time
        )
        active = total - expired

        return {"total": total, "active": active, "expired": expired}


# 全局黑名單實例
token_blacklist = TokenBlacklist()
