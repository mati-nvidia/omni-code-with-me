# SPDX-License-Identifier: Apache-2.0

import copy
import json
import os
from pathlib import Path

import carb.settings
import carb.tokens
import omni.kit.app


class ConfigManager:
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

    @classmethod
    def load_user_config(cls, filepath: Path):
        filepath = cls._resolve_path(filepath)
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        else:
            data = cls._read_json(filepath)
            cls.user_config = data
        
        if not cls.user_config:
            cls.user_config = {"sounds_repo": {}}


    @classmethod
    def save_user_config(cls, filepath: Path):
        filepath = cls._resolve_path(filepath)
        with open(filepath, "w") as f:
            json.dump(cls.user_config, f, indent=4)

    @classmethod
    def _resolve_path(cls, filepath):
        return carb.tokens.get_tokens_interface().resolve(str(filepath))

    @classmethod
    def resolved_config(cls):
        resolved_config = {}
        resolved_config.update(cls.default_config)
        resolved_config.update(cls.user_config)
        sounds_repo = copy.deepcopy(cls.default_config["sounds_repo"])
        sounds_repo.update(cls.user_config["sounds_repo"])
        resolved_config["sounds_repo"] = sounds_repo
        return resolved_config


class TransientSettings:
    EDIT_MODE = "/exts/maticodes.soundboard.window/edit_mode"


class PersistentSettings:
    BUTTON_WIDTH = "/exts/maticodes.soundboard.window/button_width"

    @classmethod
    def get_persistent_keys(cls):
        attrs = [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]
        return [getattr(cls, attr) for attr in attrs]


class Settings(PersistentSettings, TransientSettings):
    pass


class SettingsManager:
    PERSISTENT = "/persistent"

    def __init__(self):
        self._settings = carb.settings.get_settings()
        self._load_settings()

    def _load_settings(self):
        for key in PersistentSettings.get_persistent_keys():
            value = self._settings.get(self.PERSISTENT + key)
            if value is not None:
                self._settings.set(key, value)

    def save_settings(self):
        for key in PersistentSettings.get_persistent_keys():
            value = self._settings.get(key)
            self._settings.set(self.PERSISTENT + key, value)

    @property
    def settings(self):
        return self._settings
