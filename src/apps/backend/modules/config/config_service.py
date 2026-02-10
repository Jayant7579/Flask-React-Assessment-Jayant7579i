from typing import Generic, Optional, cast

from modules.config.errors import MissingKeyError
from modules.config.internals.config_manager import ConfigManager
from modules.config.types import ConfigType, ErrorCode


class ConfigService(Generic[ConfigType]):
    config_manager: ConfigManager = ConfigManager()

    @classmethod
    def get_value(cls, key: str, default: Optional[ConfigType] = None) -> ConfigType:
        value: Optional[ConfigType] = cls.config_manager.get(key, default=default)
        if value is None:
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY)
        result = cast(ConfigType, value)
        return result

    @classmethod
    def has_value(cls, key: str) -> bool:
        result = cls.config_manager.has(key)
        return result
