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
    html.Div([
        html.H5('How do you get around?'),
        dcc.Dropdown(
            options=[
                {'label': 'Driving', 'value':'driving'},
                {'label': 'Cycling', 'value':'bicycling'},
                {'label': 'Walking', 'value':'walking'},
                {'label': 'Transit', 'value':'transit'}
            ],
            placeholder='Select a mode of transportation', id='mode')
    ], style={'margin-top':'20px', 'margin-bottom':'20px'}),
    html.Div([
        html.H5('Where would you like to start from?'),
        dcc.Input(id="address", placeholder='My Street, City, Province, Country', type='text', size='30')
    ]),
    dbc.Button('Go!', id='go_button', color="primary", className='mr-1', outline=False, style={'margin':'20px', 'border-radius':'5px'}),

], style={'text-align':'center'})

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
              [dash.dependencies.State('mode', 'value')])
def load_map(n_clicks, address, mode):
    print(address)
    print(mode)
    return get_visual(address,mode) if n_clicks else no_display


def get_visual(address, mode):
    # TODO: add option for radius/distance
    # TODO: add option (slider) for grid size
    if not address or not mode:
        return no_display

    x, y, z = api_calls.data(address, 10, mode, grid=10)

    fig = go.Figure(
        data=[go.Surface(z=z, x=x, y=y)],
        layout_title_text=f"From {address} by {mode}"
    )
    fig.update_layout(title=f'From {address} by {mode}', autosize=False,
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))

    return html.Div([dcc.Graph(id="graph", figure=fig)])


if __name__ == '__main__':
    app.run_server(debug=True)
