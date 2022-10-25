# SPDX-License-Identifier: Apache-2.0

from .config import SettingsManager
import omni.ext
import omni.kit.app

from .window import Soundboard


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[maticodes.soundboard] MyExtension startup")

        self.setting_man = SettingsManager()
        self._window = Soundboard("Soundboard4", ext_id, settings=self.setting_man, width=500, height=500)
        
    def on_shutdown(self):
        print("[maticodes.soundboard] MyExtension shutdown")
        self.setting_man.save_settings()
        self.setting_man = None
        self._window.destroy()
        self._window = None
