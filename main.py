import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
    layout_title_text="Native Plotly rendering in Dash"
)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Markdown('''
    # Commuter Transportation Topography
    
    Generates a visualization of transportation times for locations around you.
    
    ### Enter your address below:
    
    '''),
    dcc.Input(id="address", value="What is your address?", type='text'),
    html.Button('Go!', id='go_button'),
    dcc.Graph(id="graph", figure=fig),
])

if __name__ == '__main__':
    app.run_server(debug=True)
