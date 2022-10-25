# SPDX-License-Identifier: Apache-2.0

import copy
from functools import partial

import omni.kit.app
import omni.kit.uiaudio
from omni import ui

from .config import ConfigManager
from .constants import REORDER_EVENT


class ButtonSlot:
    def __init__(self, sound_name, sound, button_width, edit=False) -> None:
        self.edit = edit
        self.sound_name = sound_name
        self.sound = sound
        self.button_width = button_width
        self._audio_iface = omni.kit.uiaudio.get_ui_audio_interface()
        self.msg_bus = omni.kit.app.get_app().get_message_bus_event_stream()

        with ui.HStack():
            if self.edit:
                move_rect = ui.Rectangle(width=10, 
                    height=10, 
                    style={"background_color":ui.color.red}
                )
                def drag(sound_name):
                    return sound_name
                
                move_rect.set_drag_fn(lambda: drag(self.sound_name))
            self.build_button()
    
    def build_button(self):
        def on_click():
            self._audio_iface.play_sound(self.sound)
        if self.edit:
            button = ui.Button(
                self.sound_name,
                height=self.button_width,
                width=self.button_width,
                clicked_fn=on_click
            )
            def can_drop(path: str) -> bool:
                return True
            
            def on_drop(button, e):
                active_sounds = copy.deepcopy(ConfigManager.resolved_config()["active_sounds"])
                moved_id = active_sounds.index(e.mime_data)
                active_sounds.pop(moved_id)
                insert_before = active_sounds.index(button.sound_name)
                active_sounds.insert(insert_before, e.mime_data)
                ConfigManager.user_config["active_sounds"] = active_sounds
                self.msg_bus.push(REORDER_EVENT)
                print(type(e))
                # e.x and e.y
                # e.mime_data
            
            button.set_accept_drop_fn(can_drop)
            button.set_drop_fn(partial(on_drop, self))
        else:
            ui.Button(
                self.sound_name,
                height=self.button_width,
                width=self.button_width,
                clicked_fn=on_click
            )
