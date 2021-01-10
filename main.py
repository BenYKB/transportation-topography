import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
    layout_title_text="Native Plotly rendering in Dash"
)

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.COSMO])

main_page = html.Div([
    html.H1('Commuter Transportation Topography'),
    html.P('Generates a visualization of transportation times for locations around you.'),
    html.Div([
        html.P('Enter your mode of transportation: '),
        dcc.Dropdown(
            options=[
                {'label': 'Driving', 'value':'drive'},
                {'label': 'Cycling', 'value':'cylce'},
                {'label': 'Walking', 'value':'walk'},
                {'label': 'Transit', 'value':'transit'}
            ],
            value='drive', id='mode')
    ]),
    html.Hr(),
    html.Div([
        html.H3('Enter your address below'),
        dcc.Input(id="address", value="123 Road Ave City", type='text')]
    ),
    dbc.Button('Go!', id='go_button', color="Secondary", className='b1'),

])

display_page = html.Div([
    dcc.Graph(id="graph", figure=fig)
])

no_display = html.Div([])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    main_page,
    html.Div(id='visual-content')
])

@app.callback(dash.dependencies.Output('visual-content', 'children'),
              [dash.dependencies.Input('go_button', 'n_clicks')],
              [dash.dependencies.State('address', 'value')],
              [dash.dependencies.State('mode', 'value')])
def load_map(n_clicks, value_a, value_m):
    print(value_a)
    print(value_m)
    return display_page if n_clicks else no_display


if __name__ == '__main__':
    app.run_server(debug=True)
