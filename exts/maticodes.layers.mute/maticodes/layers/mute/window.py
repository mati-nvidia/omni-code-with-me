from functools import partial

import carb
import omni.kit.commands
import omni.kit.usd.layers as usd_layers
import omni.ui as ui
import omni.usd


class LayerMuteWindow(ui.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame.set_build_fn(self.build_frame)

        self.layers: usd_layers.Layers = usd_layers.get_layers()
        self.layers_state: usd_layers.LayersState = self.layers.get_layers_state()

        self._event_subs = []
        events_stream = omni.usd.get_context().get_stage_event_stream()
        self._event_subs.append(
            events_stream.create_subscription_to_pop_by_type(
                omni.usd.StageEventType.OPENED, self._on_stage_opened
            )
        )
        self._event_subs.append(
            self.layers.get_event_stream().create_subscription_to_pop(self._on_layers_changed)
        )

    def build_frame(self):
        with ui.ScrollingFrame():
            with ui.VStack():
                layer_ids = self.layers_state.get_local_layer_identifiers()
                if len(layer_ids) < 2:
                    ui.Label("There are currently no sublayers in this Stage.", alignment=ui.Alignment.CENTER)
                for layer_id in layer_ids:
                    layer_name = self.layers_state.get_layer_name(layer_id)
                    if layer_name != "Root Layer":
                        is_muted = self.layers_state.is_layer_locally_muted(layer_id)
                        button = ui.Button(layer_name, height=25, checked=not is_muted)
                        button.set_clicked_fn(partial(self._on_clicked, layer_id, button))

    def _on_clicked(self, layer_id, button):
        button.checked = not button.checked
        omni.kit.commands.execute("SetLayerMuteness", layer_identifier=layer_id, muted=not button.checked)

    def _on_stage_opened(self, event: carb.events.IEvent):
        self.frame.rebuild()

    def _on_layers_changed(self, event: carb.events.IEvent):
        self.frame.rebuild()

    def destroy(self) -> None:
        for sub in self._event_subs:
            sub.unsubscribe()
        return super().destroy()
