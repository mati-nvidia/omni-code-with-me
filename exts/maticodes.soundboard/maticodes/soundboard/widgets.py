# SPDX-License-Identifier: Apache-2.0

import asyncio
import copy
from functools import partial

import carb
import omni.kit.app
import omni.kit.uiaudio
from omni import ui

from .config import ConfigManager, Settings
from .constants import REORDER_EVENT, GUTTER_WIDTH, USER_CONFIG_PATH
from .style import slot_style


class ButtonSlot:
    def __init__(self, sound_name, sound, width, height) -> None:
        self._settings = carb.settings.get_settings()
        self.edit_sub = self._settings.subscribe_to_node_change_events(Settings.EDIT_MODE, self._on_mode_changed)
        self.color_sub = None
        self.sound_name = sound_name
        self.sound = sound
        self.width = width
        self.height = height
        self._audio_iface = omni.kit.uiaudio.get_ui_audio_interface()
        self.msg_bus = omni.kit.app.get_app().get_message_bus_event_stream()
        self.color_model = None
        self.frame = ui.Frame(width=self.width, height=self.height)
        self.frame.set_build_fn(self._build_frame)
        self.button_frame = None
        
    def _build_frame(self):
        with ui.HStack(style=slot_style):
            if self._settings.get(Settings.EDIT_MODE):
                with ui.ZStack(width=0, height=0):
                    ui.Rectangle(width=GUTTER_WIDTH, 
                        height=100, 
                        name="edit_bar"
                    )
                    with ui.VStack():
                        def drag(sound_name):
                            return sound_name
                        img = ui.Image(carb.tokens.get_tokens_interface().resolve("${glyphs}/toolbar_move_global.svg"), 
                            width=GUTTER_WIDTH, height=GUTTER_WIDTH)
                        img.set_drag_fn(lambda: drag(self.sound_name))
                        with ui.HStack():
                            ui.Spacer()
                            color = ConfigManager.resolved_config()["sounds_repo"][self.sound_name].get("color", [0.1, 0.1, 0.1])
                            self.color_model = ui.ColorWidget(*color, width=0, height=0).model
                            self.color_sub = self.color_model.subscribe_end_edit_fn(self._on_color_changed)
                            ui.Spacer()
                        ui.Button("E", width=GUTTER_WIDTH, height=GUTTER_WIDTH, clicked_fn=self._rename_button)
                        ui.Button("X", width=GUTTER_WIDTH, height=GUTTER_WIDTH, clicked_fn=self._remove_button)
            self.button_frame = ui.Frame(width=self.width, height=self.height)
            self.button_frame.set_build_fn(self._build_button)
    
    def _rename_button(self):
        RenameWindow(self.sound_name)
    
    def _remove_button(self):
        active_sounds = copy.deepcopy(ConfigManager.resolved_config()["active_sounds"])
        active_sounds.remove(self.sound_name)
        ConfigManager.user_config["active_sounds"] = active_sounds
        ConfigManager.save_user_config(USER_CONFIG_PATH)
        self.msg_bus.push(REORDER_EVENT)

    def _on_color_changed(self, model, item):
        sound_data = ConfigManager.resolved_config()["sounds_repo"][self.sound_name]
        color = []
        for child in model.get_item_children():
            component = model.get_item_value_model(child)
            color.append(component.as_float)
        sound_data["color"] = color[:3]
        ConfigManager.user_config["sounds_repo"][self.sound_name] = sound_data
        self.button_frame.rebuild()

    def _build_button(self):
        color = ConfigManager.resolved_config()["sounds_repo"][self.sound_name].get("color", [0.1, 0.1, 0.1])
        button_color = {
            "background_color": ui.color(*color)
        }
        def on_click():
            self._audio_iface.play_sound(self.sound)
        if self._settings.get(Settings.EDIT_MODE):
            
            button = ui.Button(
                self.sound_name,
                height=self.height,
                width=self.width,
                clicked_fn=on_click,
                style=button_color
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
                height=self.height,
                width=self.width,
                clicked_fn=on_click,
                style=button_color
            )

    def _on_mode_changed(self, value, event_type):
        self.frame.rebuild()

class RenameWindow(ui.Window):
    title = "Rename Sound"
    def __init__(self, sound_name, **kwargs) -> None:
        super().__init__(self.title, flags=ui.WINDOW_FLAGS_MODAL, width=300, height=200, **kwargs)
        self.sound_name = sound_name
        self.name_model = None
        self.msg_bus = omni.kit.app.get_app().get_message_bus_event_stream()
        self.frame.set_build_fn(self._build_frame)
    
    def _build_frame(self):
        with ui.VStack():
            self.name_model = ui.StringField().model
            self.name_model.set_value(self.sound_name)
            def close_window():
                async def close_async():
                    self.destroy()
                asyncio.ensure_future(close_async())

            def rename_button():
                sounds_repo = copy.deepcopy(ConfigManager.resolved_config()["sounds_repo"])
                new_name = self.name_model.as_string
                if new_name in sounds_repo:
                    return
                active_sounds = copy.deepcopy(ConfigManager.resolved_config()["active_sounds"])
                active_sounds.remove(self.sound_name)
                active_sounds.append(new_name)
                data = sounds_repo[self.sound_name]
                user_sounds_repo = copy.deepcopy(ConfigManager.user_config["sounds_repo"])
                if self.sound_name in ConfigManager.default_config["sounds_repo"]:
                    data["active"] = False
                if self.sound_name in user_sounds_repo:
                    del user_sounds_repo[self.sound_name]

                ConfigManager.user_config["active_sounds"] = active_sounds
                user_sounds_repo[new_name] = data
                ConfigManager.user_config["sounds_repo"] = user_sounds_repo
                ConfigManager.save_user_config(USER_CONFIG_PATH)
                self.msg_bus.push(REORDER_EVENT)
                close_window()
            
            with ui.HStack():
                ui.Button("Ok", clicked_fn=rename_button)
                ui.Button("Cancel", clicked_fn=close_window)

class PaletteSlot:
    def __init__(self, sound_name, sound, width, height) -> None:
        self._settings = carb.settings.get_settings()
        self.sound_name = sound_name
        self.sound = sound
        self.width = width
        self.height = height
        self._audio_iface = omni.kit.uiaudio.get_ui_audio_interface()
        self.msg_bus = omni.kit.app.get_app().get_message_bus_event_stream()
        self.frame = ui.Frame(width=self.width, height=self.height)
        self.frame.set_build_fn(self._build_frame)
        
    def _build_frame(self):
        color = ConfigManager.resolved_config()["sounds_repo"][self.sound_name].get("color", [0.1, 0.1, 0.1])
        style = {
            "background_color": ui.color(*color),
            "border_radius": 5
        }
        with ui.ZStack():
            ui.Rectangle(style=style)
            with ui.HStack(style=slot_style):
                def on_click():
                    self._audio_iface.play_sound(self.sound)
                ui.Label(self.sound_name, alignment=ui.Alignment.CENTER)
                with ui.VStack():
                    ui.Spacer(height=12)
                    with ui.HStack():
                        ui.Button("Play", width=0, height=0, clicked_fn=on_click)
                        ui.Button("Add", width=0, height=0, clicked_fn=self._add_active_sound)


    def _add_active_sound(self):
        active_sounds = copy.deepcopy(ConfigManager.resolved_config()["active_sounds"])
        if self.sound_name not in active_sounds:
            active_sounds.append(self.sound_name)
            ConfigManager.user_config["active_sounds"] = active_sounds
            ConfigManager.save_user_config(USER_CONFIG_PATH)
            self.msg_bus.push(REORDER_EVENT)
            
        
