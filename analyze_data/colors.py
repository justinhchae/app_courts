
import plotly.express as px
# import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
import numpy as np

from textwrap import wrap

class Colors():
    def __init__(self):
        pass

    def make_scales(self):
        # https: // plotly.com / python / builtin - colorscales /
        scales = px.colors.named_colorscales()
        print("\n".join(wrap("".join('{:<12}'.format(c) for c in scales), 96)))
        return px.colors.cyclical.Twilight

    def discrete_cmap(self, N, base_cmap=None, as_hex=True):
        """
        N = number of values
        base_cmap = the color scale by names

        Create an N-bin discrete colormap from the specified input map"""

        # Note that if base_cmap is a string or None, you can simply do
        #    return plt.cm.get_cmap(base_cmap, N)
        # The following works for string, None, or a colormap instance:

        # https://gist.github.com/jakevdp/91077b0cae40f8f8244a
        np.random.seed(0)
        base = plt.cm.get_cmap(base_cmap)
        color_list = base(np.linspace(0, 1, N))
        if as_hex:
            color_list = [clrs.to_hex(i) for i in color_list]
        # cmap_name = base.name + str(N)
        # print(color_list)
        # return base.from_list(cmap_name, color_list, N)

        return color_list

