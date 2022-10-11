# SPDX-License-Identifier: Apache-2.0
from pathlib import Path

import omni.ext
import omni.kit.uiaudio
import omni.ui as ui
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
        
        self._window = Soundboard("Soundboard", ext_id, width=500, height=500)


    def on_shutdown(self):
        print("[maticodes.soundboard] MyExtension shutdown")
        self._window.destroy()
        self._window = None
