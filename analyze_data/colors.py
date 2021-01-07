
import plotly.express as px
# import plotly.graph_objects as go

# from textwrap import wrap

class Colors():
    def __init__(self):
        pass

    def make_scales(self):
        # https: // plotly.com / python / builtin - colorscales /
        scales = px.colors.named_colorscales()
        # print("\n".join(wrap("".join('{:<12}'.format(c) for c in scales), 96)))
        return px.colors.cyclical.Edge


