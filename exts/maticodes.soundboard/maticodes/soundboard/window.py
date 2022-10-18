# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
from typing import List

import carb.settings
from omni.kit.window.drop_support import ExternalDragDrop
import omni.kit.uiaudio
import omni.ui as ui

from .config import ConfigManager, SettingKeys


DATA_DIR = Path("${omni_data}/exts/maticodes.soundboard")
USER_CONFIG_PATH = DATA_DIR / "user.config"


class Soundboard(ui.Window):
    def __init__(self, title, ext_id, settings, **kwargs):
        super().__init__(title, **kwargs)
        self.ext_id = ext_id
        
        self._sounds = {}
        ConfigManager.load_default_config(self.ext_id)
        ConfigManager.load_user_config(USER_CONFIG_PATH)
        self.frame.set_build_fn(self.build_window)
        self._audio_iface = omni.kit.uiaudio.get_ui_audio_interface()
        self.load_sounds()
        self._setting_man = settings
        print(SettingKeys.get_keys())
        self._settings_sub = self._setting_man._settings.subscribe_to_node_change_events(SettingKeys.BUTTON_WIDTH, self._on_settings_changed)
        ConfigManager.user_config["foo"] = "bar"
        ConfigManager.save_user_config(USER_CONFIG_PATH)

    def build_window(self):
        button_width = self._setting_man.get(SettingKeys.BUTTON_WIDTH)
        with ui.VStack():
            def slider_changed(model):
                self._setting_man._settings.set("/exts/maticodes.soundboard/button_width", model.as_float)
            model = ui.SimpleFloatModel(self._setting_man._settings.get("/exts/maticodes.soundboard/button_width"))
            self._sub_slider = model.subscribe_value_changed_fn(slider_changed)
            ui.FloatSlider(model, min=50, max=400, step=1)
            with ui.VGrid(column_width=button_width):
                
                
                def on_click(sound_name):
                    self._audio_iface.play_sound(self._sounds[sound_name])

                for sound_name in ConfigManager.resolved_config["active_sounds"]:
                    ui.Button(
                        sound_name,
                        height=button_width,
                        width=button_width,
                        clicked_fn=lambda sound_name=sound_name: on_click(sound_name),
                    )
                self._external_drag_and_drop = ExternalDragDrop(window_name="Soundboard",
                                                            drag_drop_fn=self._on_ext_drag_drop)

    def load_sounds(self):
        for sound_name in ConfigManager.resolved_config["active_sounds"]:
            sound_data = ConfigManager.resolved_config["sounds_repo"][sound_name]
            sound = self._audio_iface.create_sound(sound_data["uri"])
            self._sounds[sound_name] = sound
    
    def _on_settings_changed(self, item, event_type):
        self.frame.rebuild()
    
    def _on_ext_drag_drop(self, edd: ExternalDragDrop, payload: List[str]):
        paths = edd.expand_payload(payload)
        if paths:
            self._browser_model.image_search(paths[0])

    # def destroy(self) -> None:
    #     self._settings_sub = None
    #     return super().destroy()
