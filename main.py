import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import api_calls


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
        dbc.Button("Neighbourhood", color="secondary", className="mr-1", id='nbhd'), # value 12, ~6.6 km
        dbc.Button("District", color="secondary", className="mr-1", id='district'), # value 11, ~6.6 km
        dbc.Button("City", color="secondary", className="mr-1", id='city'), # value 10, ~6.6 km
        dbc.Button("Region", color="secondary", className="mr-1", id='region'), # value 9, ~6.6 km
    ], style={'margin-bottom':'20px'}),
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
    html.Div(id='visual-content')
], style={'background-color':'MintCream'})

@app.callback(dash.dependencies.Output('visual-content', 'children'),
              [dash.dependencies.Input('go_button', 'n_clicks')],
              [dash.dependencies.State('address', 'value')],
              [dash.dependencies.State('mode', 'value')],
              [dash.dependencies.State('grid', 'value')])
def load_map(n_clicks, address, mode, grid):
    print(address)
    print(mode)
    print(grid)
    return get_visual(address,mode, grid) if n_clicks else no_display


def get_visual(address, mode, grid):
    # TODO: add option for radius/distance
    # TODO: add option (slider) for grid size
    if not address or not mode:
        return no_display

    # f = open(image_cache_filename, 'wb')
    # for chunk in api_calls.get_map_iterator(address, api_calls.DEFAULT_ZOOM):
    #     if chunk:
    #         f.write(chunk)
    # f.close()

    lat, lng = api_calls.origin_coordinates(address)
    radius = api_calls.zoom_to_radius(api_calls.DEFAULT_ZOOM, lat) 

    x, y, z = api_calls.data(address, radius, mode, grid)

    fig = go.Figure(
        data=[go.Surface(z=z, x=x, y=y)],
        layout_title_text=f"From {address} by {mode}"
    )
    # fig.update_layout(title=f'From {address} by {mode}', autosize=False,
    #               width=500, height=500,
    #               margin=dict(l=65, r=50, b=65, t=90))

    return html.Div([dcc.Graph(id="graph", figure=fig)])


if __name__ == '__main__':
    app.run_server(debug=True)
