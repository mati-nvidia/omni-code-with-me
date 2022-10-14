# SPDX-License-Identifier: Apache-2.0

import carb.settings
import omni.kit.commands
import omni.kit.uiaudio
import omni.ui as ui

from .config import ConfigManager


class Soundboard(ui.Window):
    def __init__(self, title, ext_id, **kwargs):
        super().__init__(title, **kwargs)
        self.ext_id = ext_id
        self._settings = carb.settings.get_settings()
        self._sounds = {}
        ConfigManager.load_default_config(self.ext_id)
        self.frame.set_build_fn(self.build_window)
        self._audio_iface = omni.kit.uiaudio.get_ui_audio_interface()
        self.load_sounds()

    def build_window(self):
        button_width = self._settings.get("exts/maticodes.soundboard/button_width")
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

    def load_sounds(self):
        for sound_name in ConfigManager.resolved_config["active_sounds"]:
            sound_data = ConfigManager.resolved_config["sounds_repo"][sound_name]
            sound = self._audio_iface.create_sound(sound_data["uri"])

            prim_path = f"/World/{sound_name}"
            omni.kit.commands.execute(
                "CreatePrimWithDefaultXform",
                prim_type="Sound",
                prim_path=prim_path,
                attributes={"auralMode": "nonSpatial", "filePath": sound_data["uri"]},
            )

            self._sounds[sound_name] = prim_path
