import numpy as np
import plotly.graph_objects as go
from PIL import Image


def draw_raw(extracted_strokes):
    fig = go.Figure()
    for stroke in extracted_strokes:
        tx = np.array([p[1] for p in stroke.points])
        ty = np.array([-p[0] for p in stroke.points])
        fig.add_trace(go.Scatter(x=tx, y=ty, mode='lines+markers'))
    return fig


def draw_approximated(extracted_strokes):
    fig = go.Figure()
    for stroke in extracted_strokes:
        tt = np.linspace(0, 1, num=17)
        tx = np.polyval(stroke.poly_y, tt)
        ty = -np.polyval(stroke.poly_x, tt)
        fig.add_trace(go.Scatter(x=tx, y=ty, mode='lines'))
    return fig


def prepare_plots(extracted_strokes, background_image_path):
    fig1 = draw_raw(extracted_strokes)
    fig2 = draw_approximated(extracted_strokes)
    pil_image = Image.open(background_image_path)
    image_dict = dict(
        source=pil_image,
        xref="x",
        yref="y",
        x=0,
        y=0,
        sizex=pil_image.width,
        sizey=pil_image.height,
        sizing="stretch",
        opacity=0.5,
        layer="below"
    )
    fig1.add_layout_image(image_dict)
    fig2.add_layout_image(image_dict)
    return fig1, fig2
