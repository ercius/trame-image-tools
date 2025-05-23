from trame.decorators import TrameApp, change
from trame.app import get_server
from trame.widgets import html, client
from trame.ui.html import DivLayout
from trame_image_tools.widgets import TrameImage, TrameImageRoi

from pathlib import Path

import base64
from io import BytesIO

from PIL import Image

import numpy as np
from matplotlib import cm

@TrameApp()
class ExampleApp:
    def __init__(self, server=None):
        self._server = get_server(server, client_type="vue3")
        self.ui = None
        self.load_image()
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
    
    def load_image(self):
        image_path = Path(__file__).parent /  Path("trame_logo_800x210.png")
        self.image = Image.open(image_path)
        self.state.image = self.convert_to_base64(self.image)
        self.state.image_size = self.image.size
        roi_size = min(self.image.size) // 2
        self.state.roi = [
            self.image.size[0] // 2 - roi_size // 2,
            self.image.size[1] // 2 - roi_size // 2,
            roi_size, roi_size
        ]

    @change("roi")
    def update_fft(self, *args, **kwargs):
        roi = self.state.roi
        cropped_image = self.image.crop((
            roi[0], roi[1], roi[0] + roi[2], roi[1] + roi[3]
        ))
        fft = np.real(np.abs(np.fft.fftshift(np.fft.fft2(np.asarray(cropped_image).sum(axis=-1))))) # FFT gray scale image
        fft_c = self.apply_colormap(fft, fft.shape, cm.cividis, True)
        image = Image.fromarray(fft_c)
        self.state.zoomed_image = self.convert_to_base64(image)
        self.state.zoomed_image_size = image.size

    def _build_ui(self):
        with DivLayout(self.server) as layout:
            self._ui = layout

            layout.root.style = "height: 100%;"

            client.Style("""
                            html { height: 100%; overflow: hidden;}
                            body { height: 100%; margin: 0;}
                            #app { height: 100%; }
                         """)

            with html.Div(style="position: absolute; width: 50%; height: 100%; background-color: black;"):
                with TrameImage(
                    src=("image",),
                    size=("image_size",),
                    v_model_scale=("scale_left", 0.9),
                    v_model_center=("center_left", [0.5, 0.5]),
                ):
                    TrameImageRoi(
                        v_model=("roi",),
                    )

                html.Button(
                    "Reset Camera", style="position: absolute; left: 1rem; top: 1rem;",
                    click="scale_left = 0.9; center_left = [0.5, 0.5];"
                )

            with html.Div(style="position: absolute; left: 50%; width: 50%; height: 100%; background-color: black; border-left-style: solid; border-left-color: grey;"):
                TrameImage(
                    src=("zoomed_image",),
                    size=("zoomed_image_size",),
                    v_model_scale=("scale_right", 0.9),
                    v_model_center=("center_right", [0.5, 0.75]),
                )

                html.Button(
                    "Reset Camera", style="position: absolute; left: 1rem; top: 1rem;",
                    click="scale_right = 0.9; center_right = [0.5, 0.5];"
                )
    def apply_colormap(self, data, shape, colormap, log):
        if log:
            data = np.log(data + 1)

        fdata = np.empty(shape=data.shape, dtype=np.float32)
        min_val = np.min(data)
        max_val = np.max(data)
        delta = max_val - min_val
        fdata[:] = (data[:] - min_val) / delta
        fdata = fdata.reshape(shape)

        return np.uint8(colormap(fdata) * 255)
        
    @staticmethod
    def convert_to_base64(img: Image.Image) -> str:
        """Convert image to base64 string"""
        buf = BytesIO()
        img.save(buf, format="png")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def main(server=None, **kwargs):
    app = ExampleApp(server)
    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
