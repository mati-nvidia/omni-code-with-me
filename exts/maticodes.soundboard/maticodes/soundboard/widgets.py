# SPDX-License-Identifier: Apache-2.0

import copy
from functools import partial

import omni.kit.app
import omni.kit.uiaudio
from omni import ui

from .config import ConfigManager, Settings, SettingsManager
from .constants import REORDER_EVENT, GUTTER_WIDTH


class ButtonSlot:
    def __init__(self, sound_name, sound, button_width) -> None:
        self.settings = SettingsManager()
        self.edit_sub = self.settings._settings.subscribe_to_node_change_events(Settings.EDIT_MODE, self._on_mode_changed)
        self.color_sub = None
        self.sound_name = sound_name
        self.sound = sound
        self.button_width = button_width
        self._audio_iface = omni.kit.uiaudio.get_ui_audio_interface()
        self.msg_bus = omni.kit.app.get_app().get_message_bus_event_stream()
        self.color_model = None
        self.frame = ui.Frame()
        self.frame.set_build_fn(self.build_frame)
        self.button_frame = None
        
    def build_frame(self):
        with ui.HStack():
            if self.settings.get(Settings.EDIT_MODE):
                with ui.VStack():
                    with ui.ZStack(width=0, height=0):
                        move_rect = ui.Rectangle(width=GUTTER_WIDTH, 
                            height=GUTTER_WIDTH, 
                            style={"background_color":ui.color(.04)}
                        )
                        def drag(sound_name):
                            return sound_name
                        
                        move_rect.set_drag_fn(lambda: drag(self.sound_name))
                        ui.Label(
                            f'{omni.kit.ui.get_custom_glyph_code("${glyphs}/toolbar_move_global.svg")}',
                            alignment=ui.Alignment.CENTER)
                    with ui.HStack():
                        ui.Spacer()
                        color = ConfigManager.resolved_config()["sounds_repo"][self.sound_name].get("color", [0.1, 0.1, 0.1])
                        self.color_model = ui.ColorWidget(*color, width=0, height=0, style={"margin_height":5}).model
                        self.color_sub = self.color_model.subscribe_end_edit_fn(self._on_color_changed)
                        ui.Spacer()
            self.button_frame = ui.Frame(width=self.button_width, height=self.button_width)
            self.button_frame.set_build_fn(self.build_button)
            # self.build_button()

    def _on_color_changed(self, model, item):
        sound_data = ConfigManager.resolved_config()["sounds_repo"][self.sound_name]
        color = []
        for child in model.get_item_children():
            component = model.get_item_value_model(child)
            color.append(component.as_float)
        sound_data["color"] = color[:3]
        ConfigManager.user_config["sounds_repo"][self.sound_name] = sound_data
        self.button_frame.rebuild()

    def build_button(self):
        color = ConfigManager.resolved_config()["sounds_repo"][self.sound_name].get("color", [0.1, 0.1, 0.1])
        style = {
            "background_color": ui.color(*color)
        }
        def on_click():
            self._audio_iface.play_sound(self.sound)
        if self.settings.get(Settings.EDIT_MODE):
            
            button = ui.Button(
                self.sound_name,
                height=self.button_width,
                width=self.button_width,
                clicked_fn=on_click,
                style=style
            )
            def can_drop(path: str) -> bool:
                return True
            
            def on_drop(button, sound_name, e):
                if sound_name == e.mime_data:
                    return
                active_sounds = copy.deepcopy(ConfigManager.resolved_config()["active_sounds"])
                moved_id = active_sounds.index(e.mime_data)
                active_sounds.pop(moved_id)
                insert_index = active_sounds.index(sound_name)
                button_width = button.computed_width
                button_pos_x = button.screen_position_x
                button_center = button_pos_x + button_width / 2
                if e.x > button_center:
                    insert_index += 1
                active_sounds.insert(insert_index, e.mime_data)
                ConfigManager.user_config["active_sounds"] = active_sounds
                self.msg_bus.push(REORDER_EVENT)
            
            button.set_accept_drop_fn(can_drop)
            button.set_drop_fn(partial(on_drop, button, self.sound_name))
        else:
            ui.Button(
                self.sound_name,
                height=self.button_width,
                width=self.button_width,
                clicked_fn=on_click,
                style=style
            )

    def _on_mode_changed(self, value, event_type):
        self.frame.rebuild()
    