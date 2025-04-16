from trame.app import get_server
from trame.widgets import html, client
from trame.ui.html import DivLayout
from trame_image_tools.widgets import (
    TrameImage,
    TrameImageRoi,
    TrameImageLine,
    TrameImageCircle,
    TrameImagePolygon,
    TrameImageGrid,
)


class ExampleApp:
    def __init__(self, server=None):
        self._server = get_server(server, client_type="vue3")
        self.ui = None
        self._build_ui()

    @property
    def server(self):
        return self._server

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    def _build_ui(self):
        with DivLayout(self.server) as layout:
            self._ui = layout

            layout.root.style = "height: 100%;"

            client.Style("""
                            html { height: 100%; overflow: hidden;}
                            body { height: 100%; margin: 0;}
                            #app { height: 100%; }
                         """)

            with html.Div(style="width: 100%; height: 100%; background-color: black;"):
                with TrameImage(
                    src="https://www.kitware.com/main/wp-content/uploads/2023/10/logo-trame.png",
                    size=("[800, 210]",),
                    v_model_scale=("scale", 0.9),
                    v_model_center=("center", [0.5, 0.5]),
                ):
                    TrameImageGrid(
                        spacing=("grid_spacing", [50, 25]),
                    )

                    TrameImageLine(
                        v_model=("line", [200, 50, 300, 150]),
                        color="lime",
                        thickness=3,
                        handle_size=12,
                    )

                    TrameImageRoi(
                        v_model=("roi", [350, 50, 100, 100]),
                        border_color="yellow",
                        border_size=3,
                        handle_size=12,
                    )

                    TrameImageCircle(
                        v_model=("circle", [550, 100, 50]),
                        border_color="cyan",
                        border_size=3,
                        handle_size=12,
                    )

                    TrameImagePolygon(
                        v_model=("polygon", [650, 90, 670, 150, 730, 150, 750, 90, 700, 50]),
                        border_color="fuchsia",
                        border_size=3,
                        handle_size=12,
                    )

                html.Button(
                    "Reset Camera",
                    style="position: absolute; left: 1rem; top: 1rem;",
                    click="scale = 0.9; center = [0.5, 0.5];",
                )


def main(server=None, **kwargs):
    app = ExampleApp(server)
    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
