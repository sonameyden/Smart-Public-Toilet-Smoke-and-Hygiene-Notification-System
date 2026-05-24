from enum import Enum


class ActivityType(str, Enum):
    RESOLVE = "resolve"
    MAINTENANCE = "maintenance"
    LOGIN = "login"
    SETTINGS = "settings"
