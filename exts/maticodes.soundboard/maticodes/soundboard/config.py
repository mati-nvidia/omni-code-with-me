
# SPDX-License-Identifier: Apache-2.0

import json
from pathlib import Path

import omni.kit.app


class ConfigManager:
    resolved_config = {}
    default_config = {}
    user_config = {}
    default_config_path = "data/default_config.json"

    @classmethod
    def _read_json(cls, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        return data

    @classmethod
    def load_default_config(cls, ext_id):
        manager = omni.kit.app.get_app().get_extension_manager()
        ext_root_path = Path(manager.get_extension_path(ext_id))
        filepath = ext_root_path / cls.default_config_path
        data = cls._read_json(filepath)
        for sound_name in data["sounds_repo"]:
            abs_path = Path(ext_root_path) / data["sounds_repo"][sound_name]["uri"]
            data["sounds_repo"][sound_name]["uri"] = str(abs_path)
        cls.default_config = data
        cls.resolved_config.update(data)

    @classmethod
    def load_user_config(cls, filepath):
        data = cls._read_json(filepath)
        cls.user_config = data
        cls.resolved_config.update(data)
