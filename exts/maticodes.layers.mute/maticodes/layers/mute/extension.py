import carb
import omni.ext

from .window import LayerMuteWindow


class LayersVisibilityExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        self._window = LayerMuteWindow("Layers Mute Window", width=300, height=300)

    def on_shutdown(self):
        self._window.destroy()
