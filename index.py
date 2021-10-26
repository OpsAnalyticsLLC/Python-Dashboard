import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages import page1, page2, page3
from callbacks import *
from app import app


# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False),
     html.Div(id="page-content")]
)


# CALLBACK: to Update Selected Tab
@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash-VataVerks-Dashboard/Water-Analysis":
        return page1.create_layout(app)
    elif pathname == "/dash-VataVerks-Dashboard/Gas-Analysis":
        return page2.create_layout(app)
    elif pathname == "/dash-VataVerks-Dashboard/aggregated-water-data":
        return page3.create_layout(app)
    else:
        return page1.create_layout(app)


if __name__ == "__main__":
    app.run_server(debug=True)
