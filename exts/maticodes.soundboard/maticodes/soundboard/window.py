# SPDX-License-Identifier: Apache-2.0

import copy
import shutil
from pathlib import Path
from typing import List

import carb.tokens
import omni.kit.app
import omni.kit.uiaudio
import omni.ui as ui
from omni.kit.window.drop_support import ExternalDragDrop

from .config import ConfigManager, SettingKeys
from .constants import REORDER_EVENT
from .widgets import ButtonSlot

DATA_DIR = Path("${omni_data}/exts/maticodes.soundboard")
USER_CONFIG_PATH = DATA_DIR / "user.config"


class Soundboard(ui.Window):
    def __init__(self, title, ext_id, settings, **kwargs):
        super().__init__(title, **kwargs)
        self.ext_id = ext_id
        
        self._sounds = {}
        ConfigManager.load_default_config(self.ext_id)
        ConfigManager.load_user_config(USER_CONFIG_PATH)
        self._audio_iface = omni.kit.uiaudio.get_ui_audio_interface()
        self.load_sounds()
        self._setting_man = settings
        self._settings_sub = self._setting_man._settings.subscribe_to_node_change_events(SettingKeys.BUTTON_WIDTH, self._on_settings_changed)
        ConfigManager.user_config["foo"] = "bar"
        ConfigManager.save_user_config(USER_CONFIG_PATH)
        self._external_drag_and_drop = None
        bus = omni.kit.app.get_app().get_message_bus_event_stream()
        self._reorder_sub = bus.create_subscription_to_push_by_type(REORDER_EVENT, self._on_reorder)
        self.frame.set_build_fn(self.build_window)

    def _on_reorder(self, e):
        self.frame.rebuild()

    def build_window(self):
        button_width = self._setting_man.get(SettingKeys.BUTTON_WIDTH)
        with ui.VStack():
            # def slider_changed(model):
            #     self._setting_man._settings.set("/exts/maticodes.soundboard/button_width", model.as_float)
            # model = ui.SimpleFloatModel(self._setting_man._settings.get("/exts/maticodes.soundboard/button_width"))
            # self._sub_slider = model.subscribe_value_changed_fn(slider_changed)
            # ui.FloatSlider(model, min=50, max=400, step=1)
            with ui.VGrid(column_width=button_width + 10):
                
                for sound_name in ConfigManager.resolved_config()["active_sounds"]:
                    ButtonSlot(sound_name, 
                        self._sounds[sound_name],
                        button_width, edit=True)

                if self._external_drag_and_drop:
                    self._external_drag_and_drop.destroy()
                    self._external_drag_and_drop = None
                self._external_drag_and_drop = ExternalDragDrop(window_name=self.title,
                                                            drag_drop_fn=self._on_ext_drag_drop)

    def load_sounds(self):
        for sound_name in ConfigManager.resolved_config()["active_sounds"]:
            conf = ConfigManager.resolved_config()
            sound_data = ConfigManager.resolved_config()["sounds_repo"][sound_name]
            self.load_sound(sound_name, sound_data["uri"])
    
    def load_sound(self, name, filepath):
        sound = self._audio_iface.create_sound(filepath)
        self._sounds[name] = sound
    
    def _on_settings_changed(self, item, event_type):
        self.frame.rebuild()
    
    def _on_ext_drag_drop(self, edd: ExternalDragDrop, payload: List[str]):
        paths = edd.expand_payload(payload)
        if paths:
            for p in paths:
                filepath = Path(p)
                if filepath.suffix in [".mp3", ".wav"]:
                    dest = DATA_DIR / filepath.name
                    dest = carb.tokens.get_tokens_interface().resolve(str(dest))
                    shutil.copy(filepath, dest)
                    self.load_sound(filepath.stem, dest)
                    active_sounds = copy.deepcopy(ConfigManager.resolved_config()["active_sounds"])
                    active_sounds.append(filepath.stem)
                    ConfigManager.user_config["active_sounds"] = active_sounds
                    if not ConfigManager.user_config.get("sounds_repo"):
                        ConfigManager.user_config["sounds_repo"] = {}
                    ConfigManager.user_config["sounds_repo"][filepath.stem] = {
                        "uri": dest
                    }
        ConfigManager.save_user_config(USER_CONFIG_PATH)
        self.frame.rebuild()


    def destroy(self) -> None:
        self._settings_sub = None
        self._sub_slider = None
        self._setting_man = None
        self._reorder_sub = None
        if self._external_drag_and_drop:
            self._external_drag_and_drop.destroy()
            self._external_drag_and_drop = None
        super().destroy()
