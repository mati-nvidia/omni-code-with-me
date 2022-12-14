# SPDX-License-Identifier: Apache-2.0

import copy
import shutil
from functools import partial
from pathlib import Path
from typing import List

import carb.tokens
import omni.kit.app
import omni.kit.uiaudio
import omni.ui as ui
from omni.kit.window.drop_support import ExternalDragDrop

from .config import ConfigManager, Settings
from .constants import DATA_DIR, REORDER_EVENT, SOUNDS_CHANGED_EVENT, USER_CONFIG_PATH, GUTTER_WIDTH
from .widgets import ButtonSlot, PaletteSlot


class Soundboard(ui.Window):
    def __init__(self, title, ext_id, **kwargs):
        super().__init__(title, **kwargs)
        self.ext_id = ext_id

        self._sounds = {}
        self._buttons_frame = None
        self._slider_sub = None
        ConfigManager.load_default_config(self.ext_id)
        ConfigManager.load_user_config(USER_CONFIG_PATH)
        self._audio_iface = omni.kit.uiaudio.get_ui_audio_interface()
        self._load_sounds()
        self._settings = carb.settings.get_settings()
        self._settings_sub = self._settings.subscribe_to_node_change_events(
            Settings.BUTTON_WIDTH, self._on_settings_changed
        )
        self._edit_sub = self._settings.subscribe_to_node_change_events(Settings.EDIT_MODE, self._on_edit_changed)
        self._external_drag_and_drop = None
        bus = omni.kit.app.get_app().get_message_bus_event_stream()
        reorder_event_type = carb.events.type_from_string(REORDER_EVENT)
        self._reorder_sub = bus.create_subscription_to_push_by_type(reorder_event_type, self._on_reorder)
        self._sounds_changed_sub = bus.create_subscription_to_push_by_type(
            carb.events.type_from_string(SOUNDS_CHANGED_EVENT), self._on_sounds_changed
        )
        self.frame.set_build_fn(self._build_window)
        

    def _on_reorder(self, e):
        self._buttons_frame.rebuild()

    def _on_sounds_changed(self, e):
        self._load_sounds()
        self._buttons_frame.rebuild()

    def _on_edit_changed(self, item, event_type):
        self.frame.rebuild()

    def _build_window(self):
        edit_mode = self._settings.get(Settings.EDIT_MODE)
        with ui.VStack():
            with ui.HStack(height=0):
                if edit_mode:
                    ui.Label("Button Width: ", width=0)

                    def slider_changed(model):
                        self._settings.set(Settings.BUTTON_WIDTH, model.as_float)

                    model = ui.SimpleFloatModel(self._settings.get(Settings.BUTTON_WIDTH))
                    self._slider_sub = model.subscribe_value_changed_fn(slider_changed)
                    ui.FloatSlider(model, min=50, max=400, step=1)
                ui.Spacer()

                def set_edit_mode(button):
                    button.checked = not button.checked
                    if not button.checked:
                        ConfigManager.save_user_config(USER_CONFIG_PATH)
                    self._settings.set(Settings.EDIT_MODE, button.checked)

                button = ui.Button(text="Edit", height=0, width=0, checked=edit_mode)
                button.set_clicked_fn(partial(set_edit_mode, button))
            self._buttons_frame = ui.Frame()
            self._buttons_frame.set_build_fn(self._build_buttons_frame)

    def _build_buttons_frame(self):
        button_width = self._settings.get(Settings.BUTTON_WIDTH)
        edit_mode = self._settings.get(Settings.EDIT_MODE)
        gutter_offset = GUTTER_WIDTH if edit_mode else 0
        with ui.VStack():
            with ui.ScrollingFrame(
                horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON,
            ):
            
                with ui.VGrid(column_width=button_width + gutter_offset):
                    for sound_name in ConfigManager.resolved_config()["active_sounds"]:
                        ButtonSlot(sound_name, self._sounds[sound_name], width=button_width, height=button_width)

            if edit_mode:
                with ui.ScrollingFrame(
                    horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON,
                    vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                    height=75,
                ):
                    with ui.ZStack():
                        ui.Rectangle(style={"background_color": ui.color.black})
                        with ui.VStack():
                            # ui.Spacer(height=5)
                            with ui.HStack(style={"margin": 2}):
                                for sound_name, sound_data in ConfigManager.resolved_config()[
                                    "sounds_repo"
                                ].items():
                                    sound = self._load_sound(sound_data["uri"])
                                    PaletteSlot(sound_name, sound, width=button_width, height=50)

                if self._external_drag_and_drop:
                    self._external_drag_and_drop.destroy()
                    self._external_drag_and_drop = None
                self._external_drag_and_drop = ExternalDragDrop(
                    window_name=self.title, drag_drop_fn=self._on_ext_drag_drop
                )
            elif self._external_drag_and_drop:
                self._external_drag_and_drop.destroy()
                self._external_drag_and_drop = None

    def _load_sounds(self):
        self._sounds = {}
        for sound_name in ConfigManager.resolved_config()["active_sounds"]:
            sound_data = ConfigManager.resolved_config()["sounds_repo"][sound_name]
            sound = self._load_sound(sound_data["uri"])
            self._sounds[sound_name] = sound

    def _load_sound(self, filepath):
        return self._audio_iface.create_sound(filepath)

    def _on_settings_changed(self, item, event_type):
        if self._buttons_frame:
            self._buttons_frame.rebuild()

    def _on_ext_drag_drop(self, edd: ExternalDragDrop, payload: List[str]):
        paths = edd.expand_payload(payload)
        if paths:
            for p in paths:
                filepath = Path(p)
                if filepath.suffix in [".mp3", ".wav"]:
                    dest = DATA_DIR / filepath.name
                    dest = carb.tokens.get_tokens_interface().resolve(str(dest))
                    shutil.copy(filepath, dest)
                    self._sounds[filepath.stem] = self._load_sound(dest)
                    self._add_sound_to_config(filepath.stem, dest)

        ConfigManager.save_user_config(USER_CONFIG_PATH)
        self.frame.rebuild()

    def _add_sound_to_config(self, sound_name, file_path):
        active_sounds = copy.deepcopy(ConfigManager.resolved_config()["active_sounds"])
        active_sounds.append(sound_name)
        ConfigManager.user_config["active_sounds"] = active_sounds
        if not ConfigManager.user_config.get("sounds_repo"):
            ConfigManager.user_config["sounds_repo"] = {}
        ConfigManager.user_config["sounds_repo"][sound_name] = {"uri": file_path}

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False
    
    def destroy(self) -> None:
        self._slider_sub = None
        if self._settings_sub:
            self._settings.unsubscribe_to_change_events(self._settings_sub)
            self._settings_sub = None
        if self._edit_sub:
            self._settings.unsubscribe_to_change_events(self._edit_sub)
            self._edit_sub = None
        if self._reorder_sub:
            self._reorder_sub.unsubscribe()
            self._reorder_sub = None
        if self._sounds_changed_sub:
            self._sounds_changed_sub.unsubscribe()
            self._sounds_changed_sub = None
        if self._external_drag_and_drop:
            self._external_drag_and_drop.destroy()
            self._external_drag_and_drop = None
        if self._buttons_frame:
            self._buttons_frame.destroy()
            self._buttons_frame = None
        super().destroy()
