from dash.dependencies import Input, Output
import plotly.graph_objects as go
from app import app
import pandas as pd
from utilities import (exponential_hourly_filter_pg1, excess_weekdayHR_table_pg1, exponential_daily_filter_pg1,
                       excess_weekday_table_pg1, exponential_weekly_filter_pg1, excess_weekly_table_pg1,
                       exponential_monthly_filter_pg1, excess_monthly_table_pg1,
                       figure1_1dt_pg1, figure2_2dt_pg1, weekly_figure1_1dt_pg1, weekly_figure2_2dt_pg1,
                       monthly_figure1_1dt_pg1, monthly_figure2_2dt_pg1)
from utilities import (exponential_hourly_filter_pg2, excess_weekdayHR_table_pg2, exponential_daily_filter_pg2,
                       excess_weekday_table_pg2, exponential_weekly_filter_pg2, excess_weekly_table_pg2,
                       exponential_monthly_filter_pg2, excess_monthly_table_pg2,
                       figure1_1dt_pg2, figure2_2dt_pg2, weekly_figure1_1dt_pg2, weekly_figure2_2dt_pg2,
                       monthly_figure1_1dt_pg2, monthly_figure2_2dt_pg2)
from utilities import (page3_graph_1, page3_graph_2, page3_graph_3, filter_data_page3)

#####################################################################################################################
house_dt = pd.read_csv('Cleaned House Water Data.csv')
house_dt['DateTime'] = pd.to_datetime(house_dt.DateTime, format='%Y-%m-%d  %H:%M:%S.%f')
house_min_dt = pd.read_csv('house_in_min.csv')
house_min_dt['DateTime'] = pd.to_datetime(house_min_dt.DateTime, format='%Y-%m-%d  %H:%M:%S')
house_hr_dt = pd.read_csv('house_in_hour.csv')
house_hr_dt['DateTime'] = pd.to_datetime(house_hr_dt.DateTime, format='%Y-%m-%d  %H:%M:%S')

condo_dt = pd.read_csv('Cleaned Condo Water Data.csv')
condo_dt['DateTime'] = pd.to_datetime(condo_dt.DateTime, format='%Y-%m-%d %H:%M:%S.%f')
condo_min_dt = pd.read_csv('condo_in_min.csv')
condo_min_dt['DateTime'] = pd.to_datetime(condo_min_dt.DateTime, format='%Y-%m-%d  %H:%M:%S')
condo_hr_dt = pd.read_csv('condo_in_hour.csv')
condo_hr_dt['DateTime'] = pd.to_datetime(condo_hr_dt.DateTime, format='%Y-%m-%d  %H:%M:%S')

sim_dt = pd.read_csv('SimData.csv')
sim_dt['DateTime'] = pd.to_datetime(sim_dt.DateTime, format='%Y-%m-%d %H:%M:%S')
sim_min_dt = pd.read_csv('sim_in_min.csv')
sim_min_dt['DateTime'] = pd.to_datetime(sim_min_dt.DateTime, format='%Y-%m-%d  %H:%M:%S')
sim_hr_dt = pd.read_csv('sim_in_hour.csv')
sim_hr_dt['DateTime'] = pd.to_datetime(sim_hr_dt.DateTime, format='%Y-%m-%d  %H:%M:%S')

df_dict = {'house_dt': house_dt.copy(deep=True), 'condo_dt': condo_dt.copy(deep=True), 'sim_dt': sim_dt.copy(deep=True)}
df_dict2 = {'house_min_dt': house_min_dt.copy(deep=True), 'condo_min_dt': condo_min_dt.copy(deep=True),
            'sim_min_dt': sim_min_dt.copy(deep=True)}
df_dict3 = {'house_hr_dt': house_hr_dt.copy(deep=True), 'condo_hr_dt': condo_hr_dt.copy(deep=True),
            'sim_hr_dt': sim_hr_dt.copy(deep=True)}

# Load the water data we got from Live Systems
main_water_dt = pd.read_csv('main water.csv')
main_water_dt['DateTime'] = pd.to_datetime(main_water_dt.DateTime, format='%m/%d/%Y  %H:%M')
live_riser_dt = pd.read_csv('live risers.csv')
live_riser_dt['DateTime'] = pd.to_datetime(live_riser_dt.DateTime, format='%m/%d/%Y %H:%M')
df_dict4 = {'main_water_dt': main_water_dt.copy(deep=True), 'live_riser_dt': live_riser_dt.copy(deep=True)}

# Load the gas data we got from Live Systems
gas_dt = pd.read_csv('gas_dt.csv')
gas_dt['DateTime'] = pd.to_datetime(gas_dt.DateTime, format='%m/%d/%Y %H:%M')
df_dict5 = {'gas_dt': gas_dt.copy(deep=True)}


#######################################################################################################################
#######################################################################################################################
# PAGE 1 CallBACKS: Live Systems Water Data
# Top Figure: Per Day Per Hour
@app.callback(
    [Output('page1-graph1', 'figure'),
     Output('page1-table1', 'columns'),
     Output('page1-table1', 'data'),
     Output('page1-table2', 'columns'),
     Output('page1-table2', 'data')],
    [Input('page1-drop-down', 'value'),
     Input('page1-range-picker', 'start_date'),
     Input('page1-range-picker', 'end_date'),
     Input('page1-slider', 'value')])
def update_graph1(value, start_date, end_date, slider_page2):
    start_point = slider_page2[0]
    end_point = slider_page2[1]
    if len(value) < 1:  # if not datasets are selected return empty figure and table
        figure = go.Figure()
        empty_dt = pd.DataFrame()
        # Table 1
        data = empty_dt.to_dict('records')
        columns = [{"name": i, "id": i} for i in empty_dt.columns]
        # Table 2
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    if len(value) == 1:
        df1_name = value[0]  # df1 name
        df1 = df_dict4.get(df1_name)
        # apply date, hour and EMA filters
        df1 = exponential_hourly_filter_pg1(df1, start_date, end_date, start_point, end_point)
        # get the graph per day per hour
        figure = figure1_1dt_pg1(df1, df1_name)
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_weekdayHR_table_pg1(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    elif len(value) == 2:
        df1_name = value[0]  # df1 name
        df1 = df_dict4.get(df1_name)
        # apply date, hour and EMA filters
        df1 = exponential_hourly_filter_pg1(df1, start_date, end_date, start_point, end_point)
        # df2
        df2_name = value[1]  # df2 name
        df2 = df_dict4.get(df2_name)
        # get the graph per day per hour
        df2 = exponential_hourly_filter_pg1(df2, start_date, end_date, start_point, end_point)
        # get the graph per day per hour
        figure = figure2_2dt_pg1(df1, df1_name, df2, df2_name)
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_weekdayHR_table_pg1(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        df2 = excess_weekdayHR_table_pg1(df2)
        columns2 = [{"name": i, "id": i} for i in df2.columns]
        data2 = df2.to_dict('records')
        return [figure, columns, data, columns2, data2]


# Second Figure: Per Day
@app.callback(
    [Output('page1-graph2', 'figure'),
     Output('page1-table3', 'columns'),
     Output('page1-table3', 'data'),
     Output('page1-table4', 'columns'),
     Output('page1-table4', 'data')],
    [Input('page1-drop-down', 'value'),
     Input('page1-range-picker', 'start_date'),
     Input('page1-range-picker', 'end_date')])
def update_graph2(value, start_date, end_date):
    if len(value) < 1:  # if not datasets are selected return empty figure and table
        figure = go.Figure()
        empty_dt = pd.DataFrame()
        # Table 1
        data = empty_dt.to_dict('records')
        columns = [{"name": i, "id": i} for i in empty_dt.columns]
        # Table 2
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    if len(value) == 1:
        df1_name = value[0]  # df1 name
        df1 = df_dict4.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_daily_filter_pg1(df1, start_date, end_date)
        # get the graph per day
        figure = figure1_1dt_pg1(df1, df1_name)
        figure.update_layout(title={'text': "Water Usage: Gallons Consumed per Day"})
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_weekday_table_pg1(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    elif len(value) == 2:
        # df1
        df1_name = value[0]  # df1 name
        df1 = df_dict4.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_daily_filter_pg1(df1, start_date, end_date)
        df2_name = value[1]  # df2 name
        df2 = df_dict4.get(df2_name)
        # apply date and EMA filters
        df2 = exponential_daily_filter_pg1(df2, start_date, end_date)
        # get the graph per day
        figure = figure2_2dt_pg1(df1, df1_name, df2, df2_name)
        figure.update_layout(title={'text': "Water Usage: Gallons Consumed per Day"})
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_weekday_table_pg1(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        df2 = excess_weekday_table_pg1(df2)
        columns2 = [{"name": i, "id": i} for i in df2.columns]
        data2 = df2.to_dict('records')
        return [figure, columns, data, columns2, data2]


# Third Figure: Per Week
@app.callback(
    [Output('page1-graph3', 'figure'),
     Output('page1-table5', 'columns'),
     Output('page1-table5', 'data'),
     Output('page1-table6', 'columns'),
     Output('page1-table6', 'data')],
    [Input('page1-drop-down', 'value'),
     Input('page1-range-picker', 'start_date'),
     Input('page1-range-picker', 'end_date')])
def update_graph3(value, start_date, end_date):
    if len(value) < 1:  # if not datasets are selected return empty figure and table
        figure = go.Figure()
        empty_dt = pd.DataFrame()
        # Table 1
        data = empty_dt.to_dict('records')
        columns = [{"name": i, "id": i} for i in empty_dt.columns]
        # Table 2
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    if len(value) == 1:
        df1_name = value[0]  # df1 name
        df1 = df_dict4.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_weekly_filter_pg1(df1, start_date, end_date)
        # get the graph per week
        figure = weekly_figure1_1dt_pg1(df1, df1_name)
        figure.update_layout(title={'text': "Water Usage: Gallons Consumed per Week"})
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_weekly_table_pg1(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    elif len(value) == 2:
        # df1
        df1_name = value[0]
        df1 = df_dict4.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_weekly_filter_pg1(df1, start_date, end_date)
        # df2
        df2_name = value[1]
        df2 = df_dict4.get(df2_name)
        # apply date and EMA filters
        df2 = exponential_weekly_filter_pg1(df2, start_date, end_date)
        # get the graph per week
        figure = weekly_figure2_2dt_pg1(df1, df1_name, df2, df2_name)
        figure.update_layout(title={'text': "Water Usage: Gallons Consumed per Week"})
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_weekly_table_pg1(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 1: apply filters to show only data points above EMA
        df2 = excess_weekly_table_pg1(df2)
        columns2 = [{"name": i, "id": i} for i in df2.columns]
        data2 = df2.to_dict('records')
        return [figure, columns, data, columns2, data2]


# Fourth Figure: Per Month
@app.callback(
    [Output('page1-graph4', 'figure'),
     Output('page1-table7', 'columns'),
     Output('page1-table7', 'data'),
     Output('page1-table8', 'columns'),
     Output('page1-table8', 'data')],
    [Input('page1-drop-down', 'value'),
     Input('page1-range-picker', 'start_date'),
     Input('page1-range-picker', 'end_date')])
def update_graph4(value, start_date, end_date):
    if len(value) < 1:  # if no datasets are selected return empty figure and table
        figure = go.Figure()
        empty_dt = pd.DataFrame()
        # Table 1
        data = empty_dt.to_dict('records')
        columns = [{"name": i, "id": i} for i in empty_dt.columns]
        # Table 2
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    if len(value) == 1:
        df1_name = value[0]  # df1 name
        df1 = df_dict4.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_monthly_filter_pg1(df1, start_date, end_date)
        # get the graph per month
        figure = monthly_figure1_1dt_pg1(df1, df1_name)
        figure.update_layout(title={'text': "Water Usage: Gallons Consumed per Month"})
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_monthly_table_pg1(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    elif len(value) == 2:
        df1_name = value[0]  # df1 name
        df1 = df_dict4.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_monthly_filter_pg1(df1, start_date, end_date)
        df2_name = value[1]  # df2 name
        df2 = df_dict4.get(df2_name)
        # apply date and EMA filters
        df2 = exponential_monthly_filter_pg1(df2, start_date, end_date)
        # get graph per month
        figure = monthly_figure2_2dt_pg1(df1, df1_name, df2, df2_name)
        figure.update_layout(title={'text': "Water Usage: Gallons Consumed per Month"})
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_monthly_table_pg1(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        df2 = excess_monthly_table_pg1(df2)
        columns2 = [{"name": i, "id": i} for i in df2.columns]
        data2 = df2.to_dict('records')
        return [figure, columns, data, columns2, data2]


#######################################################################################################################
#######################################################################################################################
# PAGE 2 CallBACKS: Live Systems Gas Data
# Top Figure: Per Day Per Hour
@app.callback(
    [Output('page2-graph1', 'figure'),
     Output('page2-table1', 'columns'),
     Output('page2-table1', 'data'),
     Output('page2-table2', 'columns'),
     Output('page2-table2', 'data')],
    [Input('page2-drop-down', 'value'),
     Input('page2-range-picker', 'start_date'),
     Input('page2-range-picker', 'end_date'),
     Input('page2-slider', 'value')])
def update_graph5(value, start_date, end_date, slider_page2):
    start_point = slider_page2[0]
    end_point = slider_page2[1]
    if len(value) < 1:  # if no datasets are selected return empty figure and table
        figure = go.Figure()
        empty_dt = pd.DataFrame()
        # Table 1
        data = empty_dt.to_dict('records')
        columns = [{"name": i, "id": i} for i in empty_dt.columns]
        # Table 2
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    if len(value) == 1:
        df1_name = value[0]  # df1 name
        df1 = df_dict5.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_hourly_filter_pg2(df1, start_date, end_date, start_point, end_point)
        # get the graph per day per hour
        figure = figure1_1dt_pg2(df1, df1_name)
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_weekdayHR_table_pg2(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    elif len(value) == 2:
        df1_name = value[0]  # df1 name
        df1 = df_dict5.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_hourly_filter_pg2(df1, start_date, end_date, start_point, end_point)
        df2_name = value[1]  # df2 name
        df2 = df_dict5.get(df2_name)
        # apply date and EMA filters
        df2 = exponential_hourly_filter_pg2(df2, start_date, end_date, start_point, end_point)
        # get graph per per day per hour
        figure = figure2_2dt_pg2(df1, df1_name, df2, df2_name)
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_weekdayHR_table_pg2(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        df2 = excess_weekdayHR_table_pg2(df2)
        columns2 = [{"name": i, "id": i} for i in df2.columns]
        data2 = df2.to_dict('records')
        return [figure, columns, data, columns2, data2]


# Second Figure: Per Day
@app.callback(
    [Output('page2-graph2', 'figure'),
     Output('page2-table3', 'columns'),
     Output('page2-table3', 'data'),
     Output('page2-table4', 'columns'),
     Output('page2-table4', 'data')],
    [Input('page2-drop-down', 'value'),
     Input('page2-range-picker', 'start_date'),
     Input('page2-range-picker', 'end_date')])
def update_graph6(value, start_date, end_date):
    if len(value) < 1:  # if no datasets are selected return empty figure and table
        figure = go.Figure()
        empty_dt = pd.DataFrame()
        # Table 1
        data = empty_dt.to_dict('records')
        columns = [{"name": i, "id": i} for i in empty_dt.columns]
        # Table 2
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    if len(value) == 1:
        df1_name = value[0]  # df1 name
        df1 = df_dict5.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_daily_filter_pg2(df1, start_date, end_date)
        # get the graph per day
        figure = figure1_1dt_pg2(df1, df1_name)
        figure.update_layout(title={'text': "Gas Usage: Therms Consumed per Day"})
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_weekday_table_pg2(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    elif len(value) == 2:
        df1_name = value[0]  # df1 name
        df1 = df_dict5.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_daily_filter_pg2(df1, start_date, end_date)
        df2_name = value[1]  # df2 name
        df2 = df_dict5.get(df2_name)
        # apply date and EMA filters
        df2 = exponential_daily_filter_pg2(df2, start_date, end_date)
        # Get Graph per Day
        figure = figure2_2dt_pg2(df1, df1_name, df2, df2_name)
        figure.update_layout(title={'text': "Gas Usage: Therms Consumed per Day"})
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_weekday_table_pg2(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        df2 = excess_weekday_table_pg2(df2)
        columns2 = [{"name": i, "id": i} for i in df2.columns]
        data2 = df2.to_dict('records')
        return [figure, columns, data, columns2, data2]


# Third Figure: Per Week
@app.callback(
    [Output('page2-graph3', 'figure'),
     Output('page2-table5', 'columns'),
     Output('page2-table5', 'data'),
     Output('page2-table6', 'columns'),
     Output('page2-table6', 'data')],
    [Input('page2-drop-down', 'value'),
     Input('page2-range-picker', 'start_date'),
     Input('page2-range-picker', 'end_date')])
def update_graph7(value, start_date, end_date):
    if len(value) < 1:  # if no datasets are selected return empty figure and table
        figure = go.Figure()
        empty_dt = pd.DataFrame()
        # Table 1
        data = empty_dt.to_dict('records')
        columns = [{"name": i, "id": i} for i in empty_dt.columns]
        # Table 2
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    if len(value) == 1:
        df1_name = value[0]  # df1`name
        df1 = df_dict5.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_weekly_filter_pg2(df1, start_date, end_date)
        # get the graph per week
        figure = weekly_figure1_1dt_pg2(df1, df1_name)
        figure.update_layout(title={'text': "Gas Usage: Therms Consumed per Week"})
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_weekly_table_pg2(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    elif len(value) == 2:
        df1_name = value[0]  # df1 name
        df1 = df_dict5.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_weekly_filter_pg2(df1, start_date, end_date)
        df2_name = value[1]  # df2 name
        df2 = df_dict4.get(df2_name)
        # apply date and EMA filters
        df2 = exponential_weekly_filter_pg2(df2, start_date, end_date)
        # Get Graph per Day per Hour
        figure = weekly_figure2_2dt_pg2(df1, df1_name, df2, df2_name)
        figure.update_layout(title={'text': "Gas Usage: Therms Consumed per Week"})
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_weekly_table_pg2(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        df2 = excess_weekly_table_pg2(df2)
        columns2 = [{"name": i, "id": i} for i in df2.columns]
        data2 = df2.to_dict('records')
        return [figure, columns, data, columns2, data2]


# Fourth Figure: Per Month
@app.callback(
    [Output('page2-graph4', 'figure'),
     Output('page2-table7', 'columns'),
     Output('page2-table7', 'data'),
     Output('page2-table8', 'columns'),
     Output('page2-table8', 'data')],
    [Input('page2-drop-down', 'value'),
     Input('page2-range-picker', 'start_date'),
     Input('page2-range-picker', 'end_date')])
def update_graph8(value, start_date, end_date):
    if len(value) < 1:  # if no datasets are selected return empty figure and table
        figure = go.Figure()
        empty_dt = pd.DataFrame()
        # Table 1
        data = empty_dt.to_dict('records')
        columns = [{"name": i, "id": i} for i in empty_dt.columns]
        # Table 2
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    if len(value) == 1:
        df1_name = value[0]  # df1 name
        df1 = df_dict5.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_monthly_filter_pg2(df1, start_date, end_date)
        # get the graph
        figure = monthly_figure1_1dt_pg2(df1, df1_name)
        figure.update_layout(title={'text': "Gas Usage: Therms Consumed per Month"})
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_monthly_table_pg2(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        empty_dt2 = pd.DataFrame()
        data2 = empty_dt2.to_dict('records')
        columns2 = [{"name": i, "id": i} for i in empty_dt2.columns]
        return [figure, columns, data, columns2, data2]
    elif len(value) == 2:
        df1_name = value[0]  # df1 name
        df1 = df_dict5.get(df1_name)
        # apply date and EMA filters
        df1 = exponential_monthly_filter_pg2(df1, start_date, end_date)
        # df2
        df2_name = value[1]  # df2 name
        df2 = df_dict5.get(df2_name)
        # apply date and EMA filters
        df2 = exponential_monthly_filter_pg2(df2, start_date, end_date)
        # Get Graph per month
        figure = monthly_figure2_2dt_pg2(df1, df1_name, df2, df2_name)
        figure.update_layout(title={'text': "Gas Usage: Therms Consumed per Month"})
        # Table 1: apply filters to show only data points above EMA
        df1 = excess_monthly_table_pg2(df1)
        columns = [{"name": i, "id": i} for i in df1.columns]
        data = df1.to_dict('records')
        # Table 2: apply filters to show only data points above EMA
        df2 = excess_monthly_table_pg2(df2)
        columns2 = [{"name": i, "id": i} for i in df2.columns]
        data2 = df2.to_dict('records')
        return [figure, columns, data, columns2, data2]


#######################################################################################################################
#######################################################################################################################
# PAGE 3 CallBACKS: Vata VerksAggregated Water Comparison
# Top Figure: Per Day Per Hour
@app.callback(
    Output('page3-graph1', 'figure'),
    [Input('page3-drop-down1', 'value'),
     Input('page3-range-picker1', 'start_date'),
     Input('page3-range-picker1', 'end_date'),
     Input('page3_slider1', 'value')])
def update_graph9(value, start_date, end_date, slider_house):
    start_point = slider_house[0]
    end_point = slider_house[1]
    if len(value) < 1:  # if no datasets are selected return empty figure
        figure = go.Figure()
        return figure
    if len(value) == 1:
        df1_name = value[0]  # df1 name
        df1 = df_dict.get(df1_name, df1_name)
        # apply the other filters
        df1 = filter_data_page3(df1, start_date, end_date, start_point, end_point)
        # get the graph
        figure = page3_graph_1(df1, df1_name)
        return figure
    elif len(value) == 2:
        # df1
        df1_name = value[0]
        df1 = df_dict.get(df1_name, df1_name)
        # apply the other filters
        df1 = filter_data_page3(df1, start_date, end_date, start_point, end_point)
        # df2
        df2_name = value[1]
        df2 = df_dict.get(df2_name, df2_name)
        # apply the other filters
        df2 = filter_data_page3(df2, start_date, end_date, start_point, end_point)
        # get the graph
        figure = page3_graph_2(df1, df1_name, df2, df2_name)
        return figure
    elif len(value) == 3:
        # df1
        df1_name = value[0]
        df1 = df_dict.get(df1_name, df1_name)
        # apply the other filters
        df1 = filter_data_page3(df1, start_date, end_date, start_point, end_point)
        # df2
        df2_name = value[1]
        df2 = df_dict.get(df2_name, df2_name)
        # apply the other filters
        df2 = filter_data_page3(df2, start_date, end_date, start_point, end_point)
        # df3
        df3_name = value[2]
        df3 = df_dict.get(df3_name, df3_name)
        # apply the other filters
        df3 = filter_data_page3(df3, start_date, end_date, start_point, end_point)
        # get the graph
        figure = page3_graph_3(df1, df1_name, df2, df2_name, df3, df3_name)
        return figure


# Middle figure: by minute
@app.callback(
    Output('page3-graph2', 'figure'),
    [Input('page3-drop-down2', 'value'),
     Input('page3-range-picker2', 'start_date'),
     Input('page3-range-picker2', 'end_date'),
     Input('page3_slider2', 'value')])
def update_graph10(dropdown, start_date, end_date, slider2_page1):
    start_point = slider2_page1[0]
    end_point = slider2_page1[1]
    if len(dropdown) < 1:
        figure = go.Figure()
        return figure
    if len(dropdown) == 1:
        # df1
        df1_name = dropdown[0]
        df1 = df_dict2.get(df1_name, df1_name)
        # apply the other filters
        df1 = filter_data_page3(df1, start_date, end_date, start_point, end_point)
        # get the graph
        figure = page3_graph_1(df1, df1_name)
        figure.update_layout(title={'text': "Water Usage: Volume Per Minute"})
        return figure
    elif len(dropdown) == 2:
        # df1
        df1_name = dropdown[0]
        df1 = df_dict2.get(df1_name, df1_name)
        # apply the other filters
        df1 = filter_data_page3(df1, start_date, end_date, start_point, end_point)
        # df2
        df2_name = dropdown[1]
        df2 = df_dict2.get(df2_name, df2_name)
        # apply the other filters
        df2 = filter_data_page3(df2, start_date, end_date, start_point, end_point)
        # get the graph
        figure = page3_graph_2(df1, df1_name, df2, df2_name)
        figure.update_layout(title={'text': "Water Usage: Volume Per Minute"})
        return figure
    elif len(dropdown) == 3:
        # df1
        df1_name = dropdown[0]
        df1 = df_dict2.get(df1_name, df1_name)
        # apply the other filters
        df1 = filter_data_page3(df1, start_date, end_date, start_point, end_point)
        # df2
        df2_name = dropdown[1]
        df2 = df_dict2.get(df2_name, df2_name)
        # apply the other filters
        df2 = filter_data_page3(df2, start_date, end_date, start_point, end_point)
        # df3
        df3_name = dropdown[2]
        df3 = df_dict2.get(df3_name, df3_name)
        # apply the other filters
        df3 = filter_data_page3(df3, start_date, end_date, start_point, end_point)
        # get the graph
        figure = page3_graph_3(df1, df1_name, df2, df2_name, df3, df3_name)
        figure.update_layout(title={'text': "Water Usage: Volume Per Minute"})
        return figure


# Bottom figure: by hour
@app.callback(
    Output('page3-graph3', 'figure'),
    [Input('page3-drop-down3', 'value'),
     Input('page3-range-picker3', 'start_date'),
     Input('page3-range-picker3', 'end_date'),
     Input('page3_slider3', 'value')])
def update_graph11(dropdown3, start_date, end_date, slider3_page1):
    start_point = slider3_page1[0]
    end_point = slider3_page1[1]
    if len(dropdown3) < 1:
        figure = go.Figure()
        return figure
    if len(dropdown3) == 1:
        # df1
        df1_name = dropdown3[0]
        df1 = df_dict3.get(df1_name, df1_name)
        # apply the other filters
        df1 = filter_data_page3(df1, start_date, end_date, start_point, end_point)
        # get the graph
        figure = page3_graph_1(df1, df1_name)
        figure.update_layout(title={'text': "Water Usage: Volume Per Hour"})
        return figure
    elif len(dropdown3) == 2:
        # df1
        df1_name = dropdown3[0]
        df1 = df_dict3.get(df1_name, df1_name)
        # apply the other filters
        df1 = filter_data_page3(df1, start_date, end_date, start_point, end_point)
        # df2
        df2_name = dropdown3[1]
        df2 = df_dict3.get(df2_name, df2_name)
        # apply the other filters
        df2 = filter_data_page3(df2, start_date, end_date, start_point, end_point)
        # get the graph
        figure = page3_graph_2(df1, df1_name, df2, df2_name)
        figure.update_layout(title={'text': "Water Usage: Volume Per Hour"})
        return figure
    elif len(dropdown3) == 3:
        # df1
        df1_name = dropdown3[0]
        df1 = df_dict3.get(df1_name, df1_name)
        # apply the other filters
        df1 = filter_data_page3(df1, start_date, end_date, start_point, end_point)
        # df2
        df2_name = dropdown3[1]
        df2 = df_dict3.get(df2_name, df2_name)
        # apply the other filters
        df2 = filter_data_page3(df2, start_date, end_date, start_point, end_point)
        # df3
        df3_name = dropdown3[2]
        df3 = df_dict3.get(df3_name, df3_name)
        # apply the other filters
        df3 = filter_data_page3(df3, start_date, end_date, start_point, end_point)
        # get the graph
        figure = page3_graph_3(df1, df1_name, df2, df2_name, df3, df3_name)
        figure.update_layout(title={'text': "Water Usage: Volume Per Hour"})
        return figure
