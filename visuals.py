import plotly.graph_objects as go
import skimage.io as sio
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import metrotown
x = metrotown.X
y = metrotown.Y
z = metrotown.Z

fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
fig.update_layout(title='Mt Bruno Elevation', autosize=False,
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))

Z = np.ones((x.shape[0], y.shape[0])) * np.amin(z)

img = sio.imread ("https://raw.githubusercontent.com/empet/Discrete-Arnold-map/master/Images/cat-128.jpg")
img2 = img[50:55, 60:65]
img3 = img2[:,:, 1]
print(img3.shape)

fig.add_surface(x=x, y=y, z=Z,
                surfacecolor=img3,
                colorscale='matter_r',
                showscale=False)
fig.update_layout(width=600, height=600,
                  scene_camera_eye_z=0.6,
                  scene_aspectratio=dict(x=0.9, y=1, z=1))

fig.show()
