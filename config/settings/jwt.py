from datetime import timedelta

from config.env import env

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": env("ACCESS_TOKEN_LIFETIME", default=timedelta(minutes=15)),
    "REFRESH_TOKEN_LIFETIME": env("REFRESH_TOKEN_LIFETIME", default=timedelta(days=1)),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}