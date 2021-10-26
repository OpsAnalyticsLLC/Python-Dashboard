import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table as dash_table
from utilities import Header
layout = dict(
    autosize=True,
    height=300,
    overflowY='scroll',
    padding='0px 20px 20px 20px'  # Ignore cutoffs
)


#####################################################################################################################
def create_layout(app):
    return html.Div(
        [
            Header(app),  # contains three rows
            # Subpage
            html.Div([
                # Row 4 with data description and date range picker
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6('Pick 1 or more datasets to compare'),
                                dcc.Dropdown(
                                    id='page2-drop-down',
                                    options=[
                                        {'label': 'gas_dt', 'value': 'gas_dt'},
                                    ],
                                    value=['gas_dt'],
                                    placeholder="Select Data Sets",
                                    multi=True,
                                ),
                            ],
                            className="six columns",
                        ),
                        html.Div(
                            [
                                html.H6('Pick Date Range'),
                                dcc.DatePickerRange(
                                    id='page2-range-picker',
                                    stay_open_on_select=False,
                                    min_date_allowed=pd.Timestamp(2019, 1, 1),
                                    max_date_allowed=pd.Timestamp.now(),
                                    initial_visible_month=pd.Timestamp(2020, 1, 1),
                                    start_date=pd.Timestamp(2020, 1, 31),
                                    end_date=pd.Timestamp(2020, 2, 20),
                                    day_size=45,
                                ),
                            ],
                            className="six columns",
                        ),
                    ],
                    className="row "
                ),
                # Row 5: GRAPH PER HOUR PER DAY
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='page2-graph1'),
                            ],
                            className="twelve columns",
                        ),
                    ],
                    className="row ",
                ),
                # Row 6 with slider picker
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Drag the slider to select the hour range you would like to see"),
                                dcc.RangeSlider(
                                    id='page2-slider',
                                    marks={i: '{}'.format(i) for i in range(0, 24)},
                                    min=0,
                                    max=23,
                                    value=[0, 23],
                                    step=1,
                                    updatemode='drag'
                                ),
                                html.Br([]),
                            ],
                            className="twelve columns",
                            style={'textAlign': 'center'},
                        ),
                    ],
                    className="row ",
                ),
                # Row 7 Dynamic DataTable
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6("Therms by Hour Table 1"),
                                dash_table.DataTable(
                                    id='page2-table1',
                                    style_cell={'fontSize': 12, 'font-family': 'sans-serif'},
                                ),
                            ],
                            className="six columns",
                            style=layout,
                        ),
                        html.Div(
                            [
                                html.H6("Therms by Hour Table 2"),
                                dash_table.DataTable(
                                    id='page2-table2',
                                    style_cell={'fontSize': 12, 'font-family': 'sans-serif'},
                                ),
                            ],
                            className="six columns",
                            style=layout,
                        ),
                    ],
                    className="row ",
                ),
                # Row 8: GRAPH PER DAY
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='page2-graph2'),
                            ],
                            className="twelve columns",
                        ),
                    ],
                    className="row ",
                ),
                # Row 9 Dynamic DataTable
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6("Therms by Day Table 1"),
                                dash_table.DataTable(
                                    id='page2-table3',
                                    style_cell={'fontSize': 12, 'font-family': 'sans-serif'},
                                ),
                            ],
                            className="six columns",
                            style=layout,
                        ),
                        html.Div(
                            [
                                html.H6("Therms by Day Table 2"),
                                dash_table.DataTable(
                                    id='page2-table4',
                                    style_cell={'fontSize': 12, 'font-family': 'sans-serif'},
                                ),
                            ],
                            className="six columns",
                            style=layout,
                        ),
                    ],
                    className="row ",
                ),
                # Row 10: GRAPH PER Week
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='page2-graph3'),
                            ],
                            className="twelve columns",
                        ),
                    ],
                    className="row ",
                ),
                # Row 11 Dynamic DataTable
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6("Therms by Week Table 1"),
                                dash_table.DataTable(
                                    id='page2-table5',
                                    style_cell={'fontSize': 12, 'font-family': 'sans-serif'},
                                ),
                            ],
                            className="six columns",
                            style=layout,
                        ),
                        html.Div(
                            [
                                html.H6("Therms by Week Table 2"),
                                dash_table.DataTable(
                                    id='page2-table6',
                                    style_cell={'fontSize': 12, 'font-family': 'sans-serif'},
                                ),
                            ],
                            className="six columns",
                            style=layout,
                        ),
                    ],
                    className="row ",
                ),
                # Row 12: GRAPH PER Month
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='page2-graph4'),
                            ],
                            className="twelve columns",
                        ),
                    ],
                    className="row ",
                ),
                # Row 13 Dynamic DataTable
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6("Therms by Month Table 1"),
                                dash_table.DataTable(
                                    id='page2-table7',
                                    style_cell={'fontSize': 12, 'font-family': 'sans-serif'},
                                ),
                            ],
                            className="six columns",
                            style=layout,
                        ),
                        html.Div(
                            [
                                html.H6("Therms by Month Table 2"),
                                dash_table.DataTable(
                                    id='page2-table8',
                                    style_cell={'fontSize': 12, 'font-family': 'sans-serif'},
                                ),
                            ],
                            className="six columns",
                            style=layout,
                        ),
                    ],
                    className="row ",
                ),
            ],
                className="sub_page",
            ),
        ],
        className='page',
    )
