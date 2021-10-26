import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from utilities import Header
layout = dict(
    autosize=True,
    height=300,
    overflowY='scroll',
    padding='0px 20px 20px 20px'  # Ignore cutoffs
)


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
                                    id='page3-drop-down1',
                                    options=[
                                        {'label': 'house_dt', 'value': 'house_dt'},
                                        {'label': 'condo_dt', 'value': 'condo_dt'},
                                        {'label': 'sim_dt', 'value': 'sim_dt'}
                                    ],
                                    value=['sim_dt', 'condo_dt'],
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
                                    id='page3-range-picker1',
                                    stay_open_on_select=False,
                                    min_date_allowed=pd.Timestamp(2019, 1, 1),
                                    max_date_allowed=pd.Timestamp.now(),
                                    initial_visible_month=pd.Timestamp(2020, 1, 1),
                                    start_date=pd.Timestamp(2020, 1, 1),
                                    end_date=pd.Timestamp(2020, 1, 3),
                                    day_size=45,
                                ),
                            ],
                            className="six columns",
                        ),
                    ],
                    className="row "
                ),
                # row 5 has large graph
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='page3-graph1'),
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
                                    id='page3_slider1',
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
                # Row 7 with data description and date range picker
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6('Pick 1 or more datasets to compare'),
                                dcc.Dropdown(
                                    id='page3-drop-down2',
                                    options=[
                                        {'label': 'house_min_dt', 'value': 'house_min_dt'},
                                        {'label': 'condo_min_dt', 'value': 'condo_min_dt'},
                                        {'label': 'sim_min_dt', 'value': 'sim_min_dt'}
                                    ],
                                    value=['sim_min_dt', 'condo_min_dt'],
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
                                    id='page3-range-picker2',
                                    stay_open_on_select=False,
                                    min_date_allowed=pd.Timestamp(2019, 1, 1),
                                    max_date_allowed=pd.Timestamp.now(),
                                    initial_visible_month=pd.Timestamp(2020, 1, 1),
                                    start_date=pd.Timestamp(2020, 1, 1),
                                    end_date=pd.Timestamp(2020, 1, 3),
                                    day_size=45,
                                ),
                            ],
                            className="six columns",
                        ),
                    ],
                    className="row "
                ),
                # row 8 has large graph
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='page3-graph2'),
                            ],
                            className="twelve columns",
                        ),
                    ],
                    className="row ",
                ),
                # Row 9 with slider picker
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Drag the slider to select the hour range you would like to see"),
                                dcc.RangeSlider(
                                    id='page3_slider2',
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
                # Row 10 with data description and date range picker
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6('Pick 1 or more datasets to compare'),
                                dcc.Dropdown(
                                    id='page3-drop-down3',
                                    options=[
                                        {'label': 'house_hr_dt', 'value': 'house_hr_dt'},
                                        {'label': 'condo_hr_dt', 'value': 'condo_hr_dt'},
                                        {'label': 'sim_hr_dt', 'value': 'sim_hr_dt'}
                                    ],
                                    value=['sim_hr_dt', 'condo_hr_dt'],
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
                                    id='page3-range-picker3',
                                    stay_open_on_select=False,
                                    min_date_allowed=pd.Timestamp(2019, 1, 1),
                                    max_date_allowed=pd.Timestamp.now(),
                                    initial_visible_month=pd.Timestamp(2020, 1, 1),
                                    start_date=pd.Timestamp(2020, 1, 1),
                                    end_date=pd.Timestamp(2020, 1, 3),
                                    day_size=45,
                                ),
                            ],
                            className="six columns",
                        ),
                    ],
                    className="row "
                ),
                # row 11 has large graph
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='page3-graph3'),
                            ],
                            className="twelve columns",
                        ),
                    ],
                    className="row ",
                ),
                # Row 12 with slider picker
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Drag the slider to select the hour range you would like to see"),
                                dcc.RangeSlider(
                                    id='page3_slider3',
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
            ],
                className="sub_page",
            ),
        ],
        className='page',
    )
