import plotly.graph_objects as go
import skimage.io as sio
import numpy as np
import metrotown
x = metrotown.X
y = metrotown.Y
z = metrotown.Z
title = 'Transportation Topology'

fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, opacity=0.5)])
fig.update_traces(colorbar_thickness=50,
                  contours_z=dict(show=True, usecolormap=True,
                                  project_z=True),
                  colorscale='Bluered')
fig.update_layout(title_text=title,
                  title_font_size=30,
                  autosize=False,
                  height=800, width=1200,
                  margin=dict(l=60, r=60, b=60, t=100, pad=50),
                  scene=dict(
                      xaxis_title='Longitude (degrees)',
                      yaxis_title='Latitude (degrees)',
                      zaxis_title='Travel time (minutes)'))

Z = np.ones((x.shape[0], y.shape[0])) * np.amin(z)
img = sio.imread("https://raw.githubusercontent.com/empet/Discrete-Arnold-map/master/Images/cat-128.jpg")
# img2 = img[50:55, 60:65]
# if image has shape (x.shape[0], y.shape[0], something)
img2 = img[:, :, 1]

fig.add_surface(x=x, y=y, z=Z,
                surfacecolor=img2,
                colorscale='matter_r',
                showscale=False)

fig.show()
