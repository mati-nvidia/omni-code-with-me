# SPDX-License-Identifier: Apache-2.0

from .config import SettingsManager
import omni.ext
import omni.kit.app

from .window import Soundboard


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class SoundboardWindowExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.

    MENU_PATH = "Window/Soundboard"

    def on_startup(self, ext_id):
        self.ext_id = ext_id
        self.settings_mgr = SettingsManager()
        editor_menu = omni.kit.ui.get_editor_menu()

        self._window = None
        self._menu = editor_menu.add_item(SoundboardWindowExtension.MENU_PATH, self._on_menu_click, 
            toggle=True, value=True)
        self.show_window(True)

    def _on_menu_click(self, menu, toggled):
        self.show_window(toggled)

    def show_window(self, toggled):
        if toggled:
            if self._window is None:
                self._window = Soundboard("Soundboard", self.ext_id, width=800, height=500)
                self._window.set_visibility_changed_fn(self._visibility_changed_fn)
            else:
                self._window.show()
        else:
            if self._window is not None:
                self._window.hide()

    def _visibility_changed_fn(self, visible: bool):
        """Toggles window visibility and Window menu item checked state.
        Args:
            visible (bool): Whether the window is visible or not
        """
        if self._menu:
            omni.kit.ui.get_editor_menu().set_value(SoundboardWindowExtension.MENU_PATH, visible)
            self.show_window(visible)

    def on_shutdown(self):
        if self._menu:
            omni.kit.ui.get_editor_menu().remove_item(self._menu)
        self.settings_mgr.save_settings()
        if self._window is not None:
            self._window.destroy()
            self._window = None
