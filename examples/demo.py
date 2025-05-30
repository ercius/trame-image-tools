from trame.app import TrameApp

from trame.widgets import html, image_tools
from trame.ui.html import DivLayout


class ExampleApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            self.ui.root.style = "position: absolute; top:0;left:0;width: 100vw; height: 100vh; background-color: gray;"

            image_tools.TrameImage(
                src="https://www.kitware.com/main/wp-content/uploads/2023/10/logo-trame.png",
                size=("[800, 210]",),
                v_model_scale=("scale", 0.2),
                v_model_center=("center", [0.5, 0.5]),
            )

            html.Button(
                "Reset Camera",
                style="position: absolute; left: 1rem; top: 1rem;color: white",
                click="scale = 0.9; center = [0.5, 0.5];",
            )


def main():
    app = ExampleApp()
    app.server.start()


if __name__ == "__main__":
    main()
