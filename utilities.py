import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import calendar


#######################################################################################################################
#######################################################################################################################
# PAGE 1 FUNCTIONS #############################################################################################
# Hourly Analysis #############################################################################################
# This function will apply date and hour filters, apply EMA, and get the Excess Number of Gallons used
def exponential_hourly_filter_pg1(df, startdate, enddate, hour1, hour2):
    df1 = pd.DataFrame(df[(df.DateTime >= startdate) & (df.DateTime <= enddate)])
    df1["Hour"] = pd.to_datetime(df1["DateTime"]).dt.hour
    df1 = pd.DataFrame(df1[(df1.Hour >= hour1) & (df1.Hour <= hour2)])
    df1 = df1.drop(['Hour'], axis=1)
    # apply Exponential Moving Average
    df1['EMA'] = df1.iloc[:, 1].ewm(span=7, adjust=True).mean().round(2)
    df1['Excess Expected Gallons'] = round(df1.Gallons - df1.EMA, 2)
    return df1


# This function will create a table from the function above that will only display data points
# above the EMA. It will also get the Day of week spelled out and show the hour of each data point
def excess_weekdayHR_table_pg1(df1):
    # create day of week column
    daysofweek = []
    for day in df1['DateTime']:
        daysofweek.append(day.strftime("%A"))
    df1['WeekDay'] = daysofweek
    # get table with only data points that are above the EMA
    df1 = df1[df1.Gallons > df1.EMA].reset_index()
    df1 = df1.drop(['index'], axis=1)
    df1["Hour"] = df1["DateTime"].dt.hour
    df1["DateTime"] = df1["DateTime"].dt.date
    df1['WeekDay'] = pd.Categorical(df1['WeekDay'], ordered=True,
                                    categories=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                                                'Saturday'])
    # rearrange table and sort by day of week
    df1 = df1[['DateTime', 'WeekDay', 'Hour', 'Gallons', 'EMA', 'Excess Expected Gallons']]
    df1 = df1.sort_values(by=['WeekDay', 'DateTime', 'Hour'], ascending=True)
    return df1


# Daily Analysis #############################################################################################
# This function will apply date and hour filters, apply EMA, and get the Excess Number of Gallons used
def exponential_daily_filter_pg1(df, startdate, enddate):
    df1 = pd.DataFrame(df[(df.DateTime >= startdate) & (df.DateTime <= enddate)])
    df1["DateTime"] = pd.to_datetime(df1["DateTime"]).dt.date
    df1 = pd.DataFrame(df1.groupby(['DateTime'])['Gallons'].sum().round(2)).reset_index().sort_values(by=['DateTime'],
                                                                                                      ascending=True)
    # apply Exponential Moving Average
    df1['EMA'] = df1.iloc[:, 1].ewm(span=7, adjust=True).mean().round(2)
    df1['Excess Expected Gallons'] = round(df1.Gallons - df1.EMA, 2)
    return df1


# This function will create a table from the function above that will only display data points
# above the EMA. It will also get the Day of week spelled out and show the hour of each data point
def excess_weekday_table_pg1(df1):
    # create day of week column
    daysofweek = []
    for day in df1['DateTime']:
        daysofweek.append(day.strftime("%A"))
    df1['WeekDay'] = daysofweek
    # get table with only data points that are above the EMA
    df1 = df1[df1.Gallons > df1.EMA].reset_index()
    df1 = df1.drop(['index'], axis=1)
    df1['WeekDay'] = pd.Categorical(df1['WeekDay'], ordered=True,
                                    categories=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                                                'Saturday'])
    # rearrange table and sort by day of week
    df1 = df1[['DateTime', 'WeekDay', 'Gallons', 'EMA', 'Excess Expected Gallons']]
    df1 = df1.sort_values(by=['WeekDay', 'DateTime'], ascending=True)
    return df1


# Weekly Analysis #############################################################################################
# This function will apply date and hour filters, apply EMA, and get the Excess Number of Gallons used
def exponential_weekly_filter_pg1(df, startdate, enddate):
    df1 = pd.DataFrame(df[(df.DateTime >= startdate) & (df.DateTime <= enddate)])
    df1["Week"] = pd.to_datetime(df1["DateTime"]).dt.week
    df1 = pd.DataFrame(df1.groupby(['Week'])['Gallons'].sum().round(2)).reset_index().sort_values(by=['Week'],
                                                                                                  ascending=True)
    # apply Exponential Moving Average
    df1['EMA'] = df1.iloc[:, 1].ewm(span=2, adjust=True).mean().round(2)
    df1['Excess Expected Gallons'] = round(df1.Gallons - df1.EMA, 2)
    return df1


# This function will create a table from the function above that will only display data points
# above the EMA. It will also get the Day of week spelled out and show the hour of each data point
def excess_weekly_table_pg1(df1):
    # get table with only data points that are above the EMA
    df1 = df1[df1.Gallons > df1.EMA].reset_index()
    df1 = df1.drop(['index'], axis=1)
    df1 = df1[['Week', 'Gallons', 'EMA', 'Excess Expected Gallons']]
    df1 = df1.sort_values(by=['Week'], ascending=True)
    return df1


# Monthly Analysis #############################################################################################
# This function will apply date and hour filters, apply EMA, and get the Excess Number of Gallons used
def exponential_monthly_filter_pg1(df, startdate, enddate):
    df1 = pd.DataFrame(df[(df.DateTime >= startdate) & (df.DateTime <= enddate)])
    df1["Month"] = pd.to_datetime(df1["DateTime"]).dt.month
    df1 = pd.DataFrame(df1.groupby(['Month'])['Gallons'].sum().round(2)).reset_index().sort_values(by=['Month'],
                                                                                                   ascending=True)
    # apply Exponential Moving Average
    df1['EMA'] = df1.iloc[:, 1].ewm(span=2, adjust=True).mean().round(2)
    df1['Excess Expected Gallons'] = round(df1.Gallons - df1.EMA, 2)
    month_list = []
    for month in df1['Month']:
        month_list.append(calendar.month_name[month])
    df1['Month'] = month_list
    return df1


# This function will create a table from the function above that will only display data points
# above the EMA. It will also get the Day of week spelled out and show the hour of each data point
def excess_monthly_table_pg1(df1):
    # get table with only data points that are above the EMA
    df1 = df1[df1.Gallons > df1.EMA].reset_index()
    df1 = df1.drop(['index'], axis=1)
    df1 = df1[['Month', 'Gallons', 'EMA', 'Excess Expected Gallons']]
    df1 = df1.sort_values(by=['Month'], ascending=True)
    return df1


# Page 1: Hourly and Daily Figures #########################################################################
# This function will create the graph for the data per Day per Hour and per Day. It will show
# in Red points those data points above EMA and in green those below. It takes two arguments. The dataset
# name and the filtered dataset. This function is for one dataset selected
def figure1_1dt_pg1(df1, df1name):
    expo1name = df1name + " Exponential MA"
    fig = go.Figure()
    fig = fig.add_trace(go.Scatter(x=df1.DateTime, y=df1.Gallons, line=dict(color='darkgray'), name=df1name,
                                   marker=dict(size=6, color=(df1.Gallons >= df1.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df1.DateTime, y=df1.EMA, line=dict(color='lightseagreen'), name=expo1name))
    fig.update_layout(showlegend=True, legend=dict(x=-.1, y=1.2, font=dict(size=12)),
                      title={
                          'text': "Water Usage: Gallons Consumed per Day per Hour",
                          'y': 0.93,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})
    fig.update_traces(mode='lines+markers')
    return fig


# This function will create the graph for the data per Day per Hour and per Day. It will show
# in Red points those data points above EMA and in green those below. It takes two arguments. The dataset
# name and the filtered dataset. This function is for two dataset selected
def figure2_2dt_pg1(df1, df1name, df2, df2name):
    expo1name = df1name + " Exponential MA"
    expo2name = df2name + " Exponential MA"
    fig = go.Figure()
    # Add dataset one
    fig = fig.add_trace(go.Scatter(x=df1.DateTime, y=df1.Gallons, line=dict(color='darkgray'), name=df1name,
                                   marker=dict(size=6, color=(df1.Gallons >= df1.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df1.DateTime, y=df1.EMA, line=dict(color='lightseagreen'), name=expo1name))
    # Add dataset two
    fig = fig.add_trace(go.Scatter(x=df2.DateTime, y=df2.Gallons, line=dict(color='bisque'), name=df2name,
                                   marker=dict(size=6, color=(df2.Gallons >= df2.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df2.DateTime, y=df2.EMA, line=dict(color='darkorchid'), name=expo2name))
    fig.update_layout(showlegend=True, legend=dict(x=-.1, y=1.2, font=dict(size=12)),
                      title={
                          'text': "Water Usage: Gallons Consumed per Day per Hour",
                          'y': 0.93,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})
    fig.update_traces(mode='lines+markers')
    return fig


# Page 1: Weekly Analysis Figures #################################################################################
# This function will create the graph for the data per Week. It will show
# in Red points those data points above EMA and in green those below. It takes two arguments. The dataset
# name and the filtered dataset. This function is for one dataset selected
def weekly_figure1_1dt_pg1(df1, df1name):
    expo1name = df1name + " Exponential MA"
    fig = go.Figure()
    fig = fig.add_trace(go.Scatter(x=df1.Week, y=df1.Gallons, line=dict(color='darkgray'), name=df1name,
                                   marker=dict(size=6, color=(df1.Gallons >= df1.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df1.Week, y=df1.EMA, line=dict(color='lightseagreen'), name=expo1name))
    fig.update_layout(showlegend=True, xaxis=dict(dtick=1), legend=dict(x=-.1, y=1.2, font=dict(size=12)),
                      title={
                          'text': "Water Usage: Gallons Consumed per Week",
                          'y': 0.93,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})
    fig.update_traces(mode='lines+markers')
    return fig


# This function will create the graph for the data per Week. It will show
# in Red points those data points above EMA and in green those below. It takes two arguments. The dataset
# name and the filtered dataset. This function is for two dataset selected
def weekly_figure2_2dt_pg1(df1, df1name, df2, df2name):
    expo1name = df1name + " Exponential MA"
    expo2name = df2name + " Exponential MA"
    fig = go.Figure()
    # Add dataset one
    fig = fig.add_trace(go.Scatter(x=df1.Week, y=df1.Gallons, line=dict(color='darkgray'), name=df1name,
                                   marker=dict(size=6, color=(df1.Gallons >= df1.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df1.Week, y=df1.EMA, line=dict(color='lightseagreen'), name=expo1name))
    # Add dataset two
    fig = fig.add_trace(go.Scatter(x=df2.Week, y=df2.Gallons, line=dict(color='bisque'), name=df2name,
                                   marker=dict(size=6, color=(df2.Gallons >= df2.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df2.Week, y=df2.EMA, line=dict(color='darkorchid'), name=expo2name))
    fig.update_layout(showlegend=True, xaxis=dict(dtick=1), legend=dict(x=-.1, y=1.2, font=dict(size=12)),
                      title={
                          'text': "Water Usage: Gallons Consumed per Week",
                          'y': 0.93,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})
    fig.update_traces(mode='lines+markers')
    return fig


# Page 1: Monthly Analysis Figures ##############################################################################
# This function will create the graph for the data per Month. It will show
# in Red points those data points above EMA and in green those below. It takes two arguments. The dataset
# name and the filtered dataset. This function is for one dataset selected
def monthly_figure1_1dt_pg1(df1, df1name):
    expo1name = df1name + " Exponential MA"
    fig = go.Figure()
    fig = fig.add_trace(go.Scatter(x=df1.Month, y=df1.Gallons, line=dict(color='darkgray'), name=df1name,
                                   marker=dict(size=6, color=(df1.Gallons >= df1.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df1.Month, y=df1.EMA, line=dict(color='lightseagreen'), name=expo1name))
    fig.update_layout(showlegend=True, xaxis=dict(dtick=1), legend=dict(x=-.1, y=1.2, font=dict(size=12)),
                      title={
                          'text': "Water Usage: Gallons Consumed per Month",
                          'y': 0.93,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})
    fig.update_traces(mode='lines+markers')
    return fig


# This function will create the graph for the data per Month. It will show
# in Red points those data points above EMA and in green those below. It takes two arguments. The dataset
# name and the filtered dataset. This function is for two dataset selected
def monthly_figure2_2dt_pg1(df1, df1name, df2, df2name):
    expo1name = df1name + " Exponential MA"
    expo2name = df2name + " Exponential MA"
    fig = go.Figure()
    # Add dataset one
    fig = fig.add_trace(go.Scatter(x=df1.Month, y=df1.Gallons, line=dict(color='darkgray'), name=df1name,
                                   marker=dict(size=6, color=(df1.Gallons >= df1.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df1.Month, y=df1.EMA, line=dict(color='lightseagreen'), name=expo1name))
    # Add dataset two
    fig = fig.add_trace(go.Scatter(x=df2.Month, y=df2.Gallons, line=dict(color='bisque'), name=df2name,
                                   marker=dict(size=6, color=(df2.Gallons >= df2.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df2.Month, y=df2.EMA, line=dict(color='darkorchid'), name=expo2name))
    fig.update_layout(showlegend=True, xaxis=dict(dtick=1), legend=dict(x=-.1, y=1.2, font=dict(size=12)),
                      title={
                          'text': "Water Usage: Gallons consumed per Month",
                          'y': 0.93,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})
    fig.update_traces(mode='lines+markers')
    return fig


#######################################################################################################################
#######################################################################################################################
# Page 2 Functions
# Hourly Analysis #############################################################################################
# This function will apply date and hour filters, apply EMA, and get the Excess Number of Therms used
def exponential_hourly_filter_pg2(df, startdate, enddate, hour1, hour2):
    df1 = pd.DataFrame(df[(df.DateTime >= startdate) & (df.DateTime <= enddate)])
    df1["Hour"] = pd.to_datetime(df1["DateTime"]).dt.hour
    df1 = pd.DataFrame(df1[(df1.Hour >= hour1) & (df1.Hour <= hour2)])
    df1 = df1.drop(['Hour'], axis=1)
    # apply Exponential Moving Average
    df1['EMA'] = df1.iloc[:, 1].ewm(span=7, adjust=True).mean().round(2)
    df1['Excess Expected Therms'] = round(df1.Therms - df1.EMA, 2)
    return df1


# This function will create a table from the function above that will only display data points
# above the EMA. It will also get the Day of week spelled out and show the hour of each data point
def excess_weekdayHR_table_pg2(df1):
    # create day of week column
    daysofweek = []
    for day in df1['DateTime']:
        daysofweek.append(day.strftime("%A"))
    df1['WeekDay'] = daysofweek
    # get table with only data points that are above the EMA
    df1 = df1[df1.Therms > df1.EMA].reset_index()
    df1 = df1.drop(['index'], axis=1)
    df1["Hour"] = df1["DateTime"].dt.hour
    df1["DateTime"] = df1["DateTime"].dt.date
    df1['WeekDay'] = pd.Categorical(df1['WeekDay'], ordered=True,
                                    categories=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                                                'Saturday'])
    # rearrange table and sort by day of week
    df1 = df1[['DateTime', 'WeekDay', 'Hour', 'Therms', 'EMA', 'Excess Expected Therms']]
    df1 = df1.sort_values(by=['WeekDay', 'DateTime', 'Hour'], ascending=True)
    return df1


# Daily Analysis #############################################################################################
# This function will apply date and hour filters, apply EMA, and get the Excess Number of Therms used
def exponential_daily_filter_pg2(df, startdate, enddate):
    df1 = pd.DataFrame(df[(df.DateTime >= startdate) & (df.DateTime <= enddate)])
    df1["DateTime"] = pd.to_datetime(df1["DateTime"]).dt.date
    df1 = pd.DataFrame(df1.groupby(['DateTime'])['Therms'].sum().round(2)).reset_index().sort_values(by=['DateTime'],
                                                                                                     ascending=True)
    # apply Exponential Moving Average
    df1['EMA'] = df1.iloc[:, 1].ewm(span=7, adjust=True).mean().round(2)
    df1['Excess Expected Therms'] = round(df1.Therms - df1.EMA, 2)
    return df1


# This function will create a table from the function above that will only display data points
# above the EMA. It will also get the Day of week spelled out and show the hour of each data point
def excess_weekday_table_pg2(df1):
    # create day of week column
    daysofweek = []
    for day in df1['DateTime']:
        daysofweek.append(day.strftime("%A"))
    df1['WeekDay'] = daysofweek
    # get table with only data points that are above the EMA
    df1 = df1[df1.Therms > df1.EMA].reset_index()
    df1 = df1.drop(['index'], axis=1)
    df1['WeekDay'] = pd.Categorical(df1['WeekDay'], ordered=True,
                                    categories=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                                                'Saturday'])
    # rearrange table and sort by day of week
    df1 = df1[['DateTime', 'WeekDay', 'Therms', 'EMA', 'Excess Expected Therms']]
    df1 = df1.sort_values(by=['WeekDay', 'DateTime'], ascending=True)
    return df1


# Weekly Analysis #############################################################################################
# This function will apply date filters, apply EMA, get the Excess Number of Therms used, and get the Week number
def exponential_weekly_filter_pg2(df, startdate, enddate):
    df1 = pd.DataFrame(df[(df.DateTime >= startdate) & (df.DateTime <= enddate)])
    df1["Week"] = pd.to_datetime(df1["DateTime"]).dt.week
    df1 = pd.DataFrame(df1.groupby(['Week'])['Therms'].sum().round(2)).reset_index().sort_values(by=['Week'],
                                                                                                 ascending=True)
    # apply Exponential Moving Average
    df1['EMA'] = df1.iloc[:, 1].ewm(span=2, adjust=True).mean().round(2)
    df1['Excess Expected Therms'] = round(df1.Therms - df1.EMA, 2)
    return df1


# This function will create a table from the function above that will only display data points above the EMA
def excess_weekly_table_pg2(df1):
    # get table with only data points that are above the EMA
    df1 = df1[df1.Therms > df1.EMA].reset_index()
    df1 = df1.drop(['index'], axis=1)
    df1 = df1[['Week', 'Therms', 'EMA', 'Excess Expected Therms']]
    df1 = df1.sort_values(by=['Week'], ascending=True)
    return df1


# Monthly Analysis #############################################################################################
# This function will apply date filters, apply EMA, get the Excess Number of Therms used, and the month spelled out
def exponential_monthly_filter_pg2(df, startdate, enddate):
    df1 = pd.DataFrame(df[(df.DateTime >= startdate) & (df.DateTime <= enddate)])
    df1["Month"] = pd.to_datetime(df1["DateTime"]).dt.month
    df1 = pd.DataFrame(df1.groupby(['Month'])['Therms'].sum().round(2)).reset_index().sort_values(by=['Month'],
                                                                                                  ascending=True)
    # apply Exponential Moving Average
    df1['EMA'] = df1.iloc[:, 1].ewm(span=2, adjust=True).mean().round(2)
    df1['Excess Expected Therms'] = round(df1.Therms - df1.EMA, 2)
    month_list = []
    for month in df1['Month']:
        month_list.append(calendar.month_name[month])
    df1['Month'] = month_list
    return df1


# This function will create a table from the function above that will only display data points above the EMA
def excess_monthly_table_pg2(df1):
    # get table with only data points that are above the EMA
    df1 = df1[df1.Therms > df1.EMA].reset_index()
    df1 = df1.drop(['index'], axis=1)
    df1 = df1[['Month', 'Therms', 'EMA', 'Excess Expected Therms']]
    df1 = df1.sort_values(by=['Month'], ascending=True)
    return df1


# Page 2: Hourly and Daily Figures #########################################################################
# This function will create the graph for the data per Month. It will show
# in Red points those data points above EMA and in green those below. It takes two arguments. The dataset
# name and the filtered dataset. This function is for one dataset selected
def figure1_1dt_pg2(df1, df1name):
    expo1name = df1name + " Exponential MA"
    fig = go.Figure()
    fig = fig.add_trace(go.Scatter(x=df1.DateTime, y=df1.Therms, line=dict(color='darkgray'), name=df1name,
                                   marker=dict(size=6, color=(df1.Therms >= df1.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df1.DateTime, y=df1.EMA, line=dict(color='lightseagreen'), name=expo1name))
    fig.update_layout(showlegend=True, legend=dict(x=-.1, y=1.2, font=dict(size=12)),
                      title={
                          'text': "Gas Usage: Therms Consumed per Day per Hour",
                          'y': 0.93,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})
    fig.update_traces(mode='lines+markers')
    return fig


# This function will create the graph for the data per Month. It will show
# in Red points those data points above EMA and in green those below. It takes two arguments. The dataset
# name and the filtered dataset. This function is for one dataset selected
def figure2_2dt_pg2(df1, df1name, df2, df2name):
    expo1name = df1name + " Exponential MA"
    expo2name = df2name + " Exponential MA"
    fig = go.Figure()
    # Add dataset one
    fig = fig.add_trace(go.Scatter(x=df1.DateTime, y=df1.Therms, line=dict(color='darkgray'), name=df1name,
                                   marker=dict(size=6, color=(df1.Therms >= df1.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df1.DateTime, y=df1.EMA, line=dict(color='lightseagreen'), name=expo1name))
    # Add dataset two
    fig = fig.add_trace(go.Scatter(x=df2.DateTime, y=df2.Therms, line=dict(color='bisque'), name=df2name,
                                   marker=dict(size=6, color=(df2.Therms >= df2.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df2.DateTime, y=df2.EMA, line=dict(color='darkorchid'), name=expo2name))
    fig.update_layout(showlegend=True, legend=dict(x=-.1, y=1.2, font=dict(size=12)),
                      title={
                          'text': "Gas Usage: Therms Consumed per Day per Hour",
                          'y': 0.93,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})
    fig.update_traces(mode='lines+markers')
    return fig


# Page 2: Weekly Analysis Figures #################################################################################
# This function will create the graph for the data per Week. It will show
# in Red points those data points above EMA and in green those below. It takes two arguments. The dataset
# name and the filtered dataset. This function is for one dataset selected
def weekly_figure1_1dt_pg2(df1, df1name):
    expo1name = df1name + " Exponential MA"
    fig = go.Figure()
    fig = fig.add_trace(go.Scatter(x=df1.Week, y=df1.Therms, line=dict(color='darkgray'), name=df1name,
                                   marker=dict(size=6, color=(df1.Therms >= df1.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df1.Week, y=df1.EMA, line=dict(color='lightseagreen'), name=expo1name))
    fig.update_layout(showlegend=True, xaxis=dict(dtick=1), legend=dict(x=-.1, y=1.2, font=dict(size=12)),
                      title={
                          'text': "Gas Usage: Therms Consumed per Week",
                          'y': 0.93,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})
    fig.update_traces(mode='lines+markers')
    return fig


# This function will create the graph for the data per Week. It will show
# in Red points those data points above EMA and in green those below. It takes two arguments. The dataset
# name and the filtered dataset. This function is for two datasets selected
def weekly_figure2_2dt_pg2(df1, df1name, df2, df2name):
    expo1name = df1name + " Exponential MA"
    expo2name = df2name + " Exponential MA"
    fig = go.Figure()
    # Add dataset one
    fig = fig.add_trace(go.Scatter(x=df1.Week, y=df1.Therms, line=dict(color='darkgray'), name=df1name,
                                   marker=dict(size=6, color=(df1.Therms >= df1.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df1.Week, y=df1.EMA, line=dict(color='lightseagreen'), name=expo1name))
    # Add dataset two
    fig = fig.add_trace(go.Scatter(x=df2.Week, y=df2.Therms, line=dict(color='bisque'), name=df2name,
                                   marker=dict(size=6, color=(df2.Therms >= df2.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df2.Week, y=df2.EMA, line=dict(color='darkorchid'), name=expo2name))
    fig.update_layout(showlegend=True, xaxis=dict(dtick=1), legend=dict(x=-.1, y=1.2, font=dict(size=12)),
                      title={
                          'text': "Gas Usage: Therms Consumed per Week",
                          'y': 0.93,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})
    fig.update_traces(mode='lines+markers')
    return fig


# Page 2: Monthly Analysis Figures ##############################################################################
# This function will create the graph for the data per Month. It will show
# in Red points those data points above EMA and in green those below. It takes two arguments. The dataset
# name and the filtered dataset. This function is for one dataset selected
def monthly_figure1_1dt_pg2(df1, df1name):
    expo1name = df1name + " Exponential MA"
    fig = go.Figure()
    fig = fig.add_trace(go.Scatter(x=df1.Month, y=df1.Therms, line=dict(color='darkgray'), name=df1name,
                                   marker=dict(size=6, color=(df1.Therms >= df1.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df1.Month, y=df1.EMA, line=dict(color='lightseagreen'), name=expo1name))
    fig.update_layout(showlegend=True, xaxis=dict(dtick=1), legend=dict(x=-.1, y=1.2, font=dict(size=12)),
                      title={
                          'text': "Gas Usage: Therms Consumed per Month",
                          'y': 0.93,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})
    fig.update_traces(mode='lines+markers')
    return fig


# This function will create the graph for the data per Month. It will show
# in Red points those data points above EMA and in green those below. It takes two arguments. The dataset
# name and the filtered dataset. This function is for two datasets selected
def monthly_figure2_2dt_pg2(df1, df1name, df2, df2name):
    expo1name = df1name + " Exponential MA"
    expo2name = df2name + " Exponential MA"
    fig = go.Figure()
    # Add dataset one
    fig = fig.add_trace(go.Scatter(x=df1.Month, y=df1.Therms, line=dict(color='darkgray'), name=df1name,
                                   marker=dict(size=6, color=(df1.Therms >= df1.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df1.Month, y=df1.EMA, line=dict(color='lightseagreen'), name=expo1name))
    # Add dataset two
    fig = fig.add_trace(go.Scatter(x=df2.Month, y=df2.Therms, line=dict(color='bisque'), name=df2name,
                                   marker=dict(size=6, color=(df2.Therms >= df2.EMA).astype('int'),
                                               colorscale=[[0, 'green'], [1, 'red']])))
    fig = fig.add_trace(go.Scatter(x=df2.Month, y=df2.EMA, line=dict(color='darkorchid'), name=expo2name))
    fig.update_layout(showlegend=True, xaxis=dict(dtick=1), legend=dict(x=-.1, y=1.2, font=dict(size=12)),
                      title={
                          'text': "Gas Usage: Therms consumed per Month",
                          'y': 0.93,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'})
    fig.update_traces(mode='lines+markers')
    return fig


#######################################################################################################################
#######################################################################################################################
# Page 3 functions
def page3_graph_1(df_1, df1name):
    # get a line graph
    fig = go.Figure()
    fig = fig.add_trace(go.Scatter(x=df_1.DateTime, y=df_1.Volume, mode='lines', name=df1name))
    fig.update_layout(
        title={
            'text': "Water Usage: Volume Per 5 Seconds",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig.update_layout(showlegend=True)
    return fig


def page3_graph_2(df_1, df1name, df_2, df2name):
    # get a line graph
    fig = go.Figure()
    fig = fig.add_trace(go.Scatter(x=df_1.DateTime, y=df_1.Volume, mode='lines', name=df1name))
    fig = fig.add_trace(go.Scatter(x=df_2.DateTime, y=df_2.Volume, mode='lines', name=df2name))
    fig.update_layout(
        title={
            'text': "Water Usage: Volume Per 5 Seconds",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig.update_layout(showlegend=True)
    return fig


def page3_graph_3(df_1, df1name, df_2, df2name, df_3, df3name):
    # get a line graph
    fig = go.Figure()
    fig = fig.add_trace(go.Scatter(x=df_1.DateTime, y=df_1.Volume, mode='lines', name=df1name))
    fig = fig.add_trace(go.Scatter(x=df_2.DateTime, y=df_2.Volume, mode='lines', name=df2name))
    fig = fig.add_trace(go.Scatter(x=df_3.DateTime, y=df_3.Volume, mode='lines', name=df3name))
    fig.update_layout(
        title={
            'text': "Water Usage: Volume Per 5 Seconds",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig.update_layout(showlegend=True)
    return fig


def filter_data_page3(df, startdate, enddate, slide1, slide2):
    df1 = pd.DataFrame(df[(df.DateTime >= startdate) & (df.DateTime <= enddate)])
    df1['Hour'] = df1.DateTime.dt.hour
    return df1[(df1.Hour >= slide1) & (df1.Hour <= slide2)]


#####################################################################################################################
# Page Layout functions
# Create function to output the heading. This will be use in every page
def Header(app):
    return html.Div([get_header(app), get_menu()])


def get_header(app):
    header = html.Div(
        [
            # row starts
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("vata-logo.png"),
                        className="logo",
                    ),
                    html.A(
                        html.Button("Learn More", id="learn-more-button"),
                        href="https://vataverks.com/wp/",
                    ),
                ],
                className="row",
            ),  # row ends
            # row 2 starts
            html.Div(
                [
                    html.Div(
                        [html.H3("Vata Verks Dashboard")],
                        className="twelve columns",
                    ),
                ],
                className="row",
                style={'textAlign': 'center'},
            ),  # row ends 
        ],
        className='row',
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Water Analysis",
                href="/dash-VataVerks-Dashboard/Water-Analysis",
                className="tab first",
            ),
            dcc.Link(
                "Gas Analysis",
                href="/dash-VataVerks-Dashboard/Gas-Analysis",
                className="tab",
            ),
            dcc.Link(
                "Aggregated:Water Data",
                href="/dash-VataVerks-Dashboard/aggregated-water-data",
                className="tab",
            ),
        ],
        className="row all-tabs",
        style={'textAlign': 'center', 'font-size': '16px', 'margin-left': '10px'}
    )
    return menu
