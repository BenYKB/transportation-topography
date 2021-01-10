import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
    layout_title_text="Native Plotly rendering in Dash"
)

app = dash.Dash(__name__, suppress_callback_exceptions=True)

main_page = html.Div([
    dcc.Markdown('''
# Commuter Transportation Topography

Generates a visualization of transportation times for locations around you.

### Enter your address below:

'''),
    dcc.Input(id="address", value="What is your address?", type='text'),
    html.Button('Go!', id='go_button')
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
              [dash.dependencies.State('address', 'value')])
def load_map(n_clicks, value):
    return display_page if n_clicks else no_display



if __name__ == '__main__':
    app.run_server(debug=True)
