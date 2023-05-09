# SPDX-License-Identifier: Apache-2.0

import omni.ui as ui


class TutorialWindow(ui.Window):
    def __init__(self):
        super().__init__("Tutorial", width=300, height=300)
        self.frame.set_build_fn(self._build_window)
        step1 = Step(50, "Step 1", "This is step 1")
        step2 = Step(60, "Step 2", "This is step 2")
        step3 = Step(70, "Step 3", "This is step 3")
        self.steps = [step1, step2, step3]
        self.step_index = 0


    
    def _build_window(self):
        with ui.VStack():
            self.step_frame = ui.Frame()
            self.step_frame.set_build_fn(self._build_step_frame)
            with ui.HStack(height=20):
                ui.Button("Reset", width=0)
                ui.Spacer()
                ui.Button("Validate", width=0)
            with ui.HStack(height=0):
                def prev_func():
                    self.step_index -= 1
                    self.step_frame.rebuild()
                ui.Button("Previous", clicked_fn=prev_func)
                ui.Spacer()
                def next_func():
                    self.step_index += 1
                    self.step_frame.rebuild()
                ui.Button("Next", clicked_fn=next_func)
    
    def _build_step_frame(self):
        step = self.steps[self.step_index]
        step.build()


class Step():
    def __init__(self, num_lines=10, title="Step", text="Hello World"):
        self.num_lines = num_lines
        self.text = text
        self.title = title

    def build_title(self):
        ui.Label(self.title, height=0, alignment=ui.Alignment.CENTER)
    
    def build_content(self):
        with ui.VStack():
            for x in range(self.num_lines):
                ui.Label(self.text)

    def build(self):
        with ui.VStack():
            self.build_title()
            with ui.ScrollingFrame():
                self.build_content()
