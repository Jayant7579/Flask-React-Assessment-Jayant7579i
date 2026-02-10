import os
from typing import Any, Optional, cast

from modules.config.internals.config_utils import ConfigUtil
from modules.config.internals.types import Config


class CustomEnvConfig:

    FILENAME: str = "custom-environment-variables.yml"

    @staticmethod
    def load() -> Config:
        custom_env_config = ConfigUtil.read_yml_from_config_dir(CustomEnvConfig.FILENAME)
        custom_env_dict = CustomEnvConfig._apply_environment_overrides(custom_env_config)
        result = cast(Config, custom_env_dict)
        return result

    @staticmethod
    def _apply_environment_overrides(data: dict[str, Any]) -> dict[str, Any]:

        if not isinstance(data, dict):
            result = data
            return result

        updated_data = {}

        for key, value in data.items():
            if isinstance(value, dict):
                updated_data[key] = CustomEnvConfig._search_and_replace_dict_value_with_env(value)
            elif isinstance(value, str):
                result = CustomEnvConfig._search_and_get_str_value_from_env(value)
                if result is not None:
                    updated_data[key] = result

        result = updated_data
        return result

    @staticmethod
    def _search_and_replace_dict_value_with_env(value: dict[str, Any]) -> Any:
        if "__name" in value:
            env_var_name = value["__name"]
            env_var_value = os.getenv(env_var_name)
            value_format = value.get("__format")
            result = CustomEnvConfig._parse_value(env_var_value, value_format) if value_format else env_var_value
            return result
        result = CustomEnvConfig._apply_environment_overrides(value)
        return result

    @staticmethod
    def _search_and_get_str_value_from_env(key: str) -> Optional[str]:
        result = os.getenv(key)
        return result

    @staticmethod
    def _parse_value(value: Optional[str], value_format: str) -> int | float | bool | None:
        if value is None:
            return None

        parsers = {
            "boolean": lambda x: x.lower() in ["true", "1"],
            "number": lambda x: int(x) if x.isdigit() else float(x),
        }

        parser = parsers.get(value_format)
        if not parser:
            raise ValueError(f"Unsupported format: {value_format}")

        try:
            result = parser(value)
            return result
        except Exception as e:
            raise ValueError(f"Error parsing value '{value}' as {value_format}: {e}") from e
