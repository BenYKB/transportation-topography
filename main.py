import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import api_calls
import numpy as np
import skimage.io as sio
import requests


image_cache_filename = "img.png"

fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
    layout_title_text="Native Plotly rendering in Dash"
)

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX])

main_page = html.Div([
    html.Div([
        html.H1('\n\rCommuter Transportation Topography')
    ]),
    html.P('A visualization of transportation times for locations around you'),
    html.Hr(),
    html.H5('How do you get around?'),
    html.Div([
        dcc.Dropdown(
            options=[
                {'label': 'Driving', 'value':'driving'},
                {'label': 'Cycling', 'value':'bicycling'},
                {'label': 'Walking', 'value':'walking'},
                {'label': 'Transit', 'value':'transit'}
            ],
            placeholder='Select a mode of transportation', 
            id='mode',
            style={
                'width':'400px', 
                'justify-content': 'center', 'align-text':'center'
            },
        )    
    ], 
    style={
        'margin-bottom':'20px',
        'display': 'flex', 'align-items': 'center', 
        'justify-content': 'center', 'align-text':'center'
    }),
    html.Div([
        html.H5('Where would you like to start from?'),
        dcc.Input(
            id="address", 
            placeholder='My Street, City, Province, Country', 
            type='text', 
            size='30',
            style={'margin-bottom':'20px'}
        ),
    ]), 
    html.Div([
        html.H5('How far would you like to go?'),
        dbc.ButtonGroup([
            dbc.Button("Neighbourhood", color="info",  outline=True, className="mr-1", id='nbhd', n_clicks_timestamp=-1), # value 12, ~6.6 km
            dbc.Button("District", color="info", outline=True, className="mr-1", id='district', n_clicks_timestamp=-1), # value 11, ~6.6 km
            dbc.Button("City", color="info", outline=True, className="mr-1", id='city', n_clicks_timestamp=-1), # value 10, ~6.6 km
            dbc.Button("Region", color="info", outline=True, className="mr-1", id='region', n_clicks_timestamp=-1)] # value 9, ~6.6 km)
        , id='zoom-buttons')
    ], style={'margin-bottom':'20px'}, id='distance-buttons'),
    html.Div([
        html.H5('Resolution'),
        dcc.Slider(
            id='grid', 
            min=5, 
            max=30,
            value=5,
            step=1,
            dots=True,
            marks={i: '{}'.format(i) for i in range(5,31,5)}
        ),
    ], style={'margin-left':'300px', 'margin-right': '300px'}),
    dbc.Button(
        'Go!', 
        id='go_button', 
        color="primary", 
        className='mr-1', 
        outline=False, 
        style={'margin':'20px', 'border-radius':'5px'}
    ),
], 
style={'text-align':'center'})

display_page = html.Div([
    dcc.Graph(id="graph", figure=fig)
])

no_display = html.Div([])

app.layout = html.Div([
    html.Title("Transportation Topography"),
    dcc.Location(id='url', refresh=False),
    main_page,
    html.Div(id='visual-content',style={'text-align':'center'})
], style={'background-color':'MintCream'})

@app.callback([dash.dependencies.Output('visual-content', 'children'),
              dash.dependencies.Output('nbhd', 'active'),
              dash.dependencies.Output('district', 'active'),
              dash.dependencies.Output('city', 'active'),
              dash.dependencies.Output('region', 'active')],
              [dash.dependencies.Input('go_button', 'n_clicks')],
              [dash.dependencies.State('nbhd', 'n_clicks_timestamp')],
              [dash.dependencies.State('district', 'n_clicks_timestamp')],
              [dash.dependencies.State('city', 'n_clicks_timestamp')],
              [dash.dependencies.State('region', 'n_clicks_timestamp')],
              [dash.dependencies.State('address', 'value')],
              [dash.dependencies.State('mode', 'value')],
              [dash.dependencies.State('grid', 'value')])
def load_map(n_clicks, nbhd, district, city, region, address, mode, grid):
    click_ts = np.array([nbhd, district, city, region])
    latest_click = np.amax(click_ts)

    if latest_click == -1:
        print("no button")
        return no_display, False, False, False, False

    i = np.argmax(click_ts)

    button_to_zoom = [12,11,10,9]
    zoom = button_to_zoom[i]

    activations = [False, False, False, False]
    activations[i] = True

    print(address)
    print(mode)
    print(grid)
    print(zoom)

    if n_clicks and address and mode:
        return get_visual(address, mode, grid, zoom), activations[0], activations[1], activations[2], activations[3]
    else:
        return no_display, False, False, False, False


def get_visual(address, mode, grid, zoom):
    if not address or not mode:
        return no_display

    # f = open(image_cache_filename, 'wb')
    # for chunk in api_calls.get_map_iterator(address, api_calls.DEFAULT_ZOOM):
    #     if chunk:
    #         f.write(chunk)
    #f.close()
    lat, lng = api_calls.origin_coordinates(address)
    print(lat)
    print(lng)
#52.520103, 13.404871

    my_zoom = zoom
    my_grid = grid
    my_img_side = 320

    f = open(image_cache_filename, 'wb')
    for chunk in api_calls.gmaps.static_map(size=(my_img_side, my_img_side),
                                   center=(lat, lng),
                                   zoom=my_zoom):
        if chunk:
            f.write(chunk)
    f.close()

    radius = api_calls.zoom_to_radius(my_zoom, lat, my_img_side)

    x, y, z = api_calls.data(address, radius, mode, grid=my_grid)

    fig = go.Figure(
        data=[go.Surface(z=z, x=x, y=y, opacity=0.5, showscale=False)]
        # layout_title_text=f"From {address} by {mode}"
    )
    fig.update_traces(colorbar_thickness=50,
                      contours_z=dict(show=True, usecolormap=True,
                                      project_z=True),
                      colorscale='Turbo')

    img = sio.imread(image_cache_filename, as_gray=True)
    img = np.flipud(img)

    canvas = np.zeros((my_img_side, my_img_side))
    x_max = np.amax(x)
    x_min = np.amin(x)
    y_max = np.amax(y)
    y_min = np.amin(y)

    x = np.linspace(x_min, x_max, num=my_img_side)
    y = np.linspace(y_min, y_max, num=my_img_side)

    fig.add_surface(x=x, y=y, z=canvas, surfacecolor=img, colorscale='gray', showscale=False)

    fig.update_layout(title_font_size=30,
                      autosize=False,
                      height=900, width=1200,
                      margin=dict(l=60, r=60, b=60, t=100, pad=50),
                      scene=dict(
                          xaxis_title='Longitude (degrees)',
                          yaxis_title='Latitude (degrees)',
                          zaxis_title='Travel time (minutes)'))

    return html.Div([dcc.Graph(id="graph", figure=fig)], style={
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center',
        'align-text':'center'})


if __name__ == '__main__':
    app.run_server(debug=True)
