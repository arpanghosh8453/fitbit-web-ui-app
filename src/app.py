# %%
import dash, requests
from dash import dcc
from dash import html, dash_table
from dash.dependencies import Output, State, Input
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import dash_dangerously_set_inner_html


# %%

app = dash.Dash(__name__)
app.title = "Fitbit Wellness Report"
server = app.server

app.layout = html.Div(children=[

    html.Div(id="input-area", className="hidden-print",
    style={
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center',
        'gap': '20px',
        'margin': 'auto',
        'flex-wrap': 'wrap',
        'margin-top': '30px'
    },children=[
        dcc.DatePickerRange(
        id='my-date-picker-range',
        display_format='MMMM DD, Y',
        minimum_nights=40,
        max_date_allowed=datetime.today().date() - timedelta(days=1),
        min_date_allowed=datetime.today().date() - timedelta(days=1000),
        end_date=datetime.today().date() - timedelta(days=1),
        start_date=datetime.today().date() - timedelta(days=365)
        ),
        dcc.Input(id='input-on-submit', value="", placeholder='API ACCESS TOKEN', type='text'),
        html.Button(id='submit-button', type='submit', children='Submit', n_clicks=0, className="button-primary"),
    ]),
    html.Div(id="instruction-area", className="hidden-print", style={'margin-top':'30px', 'margin-right':'auto', 'margin-left':'auto','text-align':'center'}, children=[
        html.P( "Allowed Date Range : Minimum 40 days — Maximum 365 days", style={'font-size':'17px', 'font-weight': 'bold', 'color':'#54565e'}),
        html.A("HOW TO GET ACCESS TOKEN?", href='https://github.com/arpanghosh8453/fitbit-web-ui-app/blob/main/help/GET_ACCESS_TOKEN.pdf', target="_blank", style={'text-decoration': 'none'})
        ]),
    html.Div(id='loading-div', style={'margin-top': '40px'}, children=[
    dcc.Loading(
            id="loading-progress",
            type="default",
            children=html.Div(id="loading-output-1")
        ),
    ]),

    html.Div(id='output_div', style={'max-width': '1400px', 'margin': 'auto'}, children=[

        html.Div(id='report-title-div', 
        style={
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center',
        'flex-direction': 'column',
        'margin-top': '20px'}, children=[
            html.H2(id="report-title", style={'font-weight': 'bold'}),
            html.H4(id="date-range-title", style={'font-weight': 'bold'}),
            html.P(id="generated-on-title", style={'font-weight': 'bold', 'font-size': '16'})
        ]),
        html.Div(style={"height": '40px'}),
        html.H4("Resting Heart Rate", style={'font-weight': 'bold'}),
        html.H6("Resting heart rate (RHR) is derived from a person's average sleeping heart rate. Fitbit tracks heart rate with photoplethysmography. This technique uses sensors and green light to detect blood volume when the heart beats. If a Fitbit device isn't worn during sleep, RHR is derived from daytime sedentary heart rate. According to the American Heart Association, a normal RHR is between 60-100 beats per minute (bpm), but this can vary based upon your age or fitness level."),
        dcc.Graph(
            id='graph_RHR',
            figure=px.line(),
            config= {'displaylogo': False}
        ),
        html.Div(id='RHR_table', style={'max-width': '1200px', 'margin': 'auto', 'font-weight': 'bold'}, children=[]),
        html.Div(style={"height": '40px'}),
        html.H4("Steps Count", style={'font-weight': 'bold'}),
        html.H6("Fitbit devices use an accelerometer to track steps. Some devices track active minutes, which includes activities over 3 metabolic equivalents (METs), such as brisk walking and cardio workouts."),
        dcc.Graph(
            id='graph_steps',
            figure=px.bar(),
            config= {'displaylogo': False}
        ),
        dcc.Graph(
            id='graph_steps_heatmap',
            figure=px.bar(),
            config= {'displaylogo': False}
        ),
        html.Div(id='steps_table', style={'max-width': '1200px', 'margin': 'auto', 'font-weight': 'bold'}, children=[]),
        html.Div(style={"height": '40px'}),
        html.H4("Activity", style={'font-weight': 'bold'}),
        html.H6("Heart Rate Zones (fat burn, cardio and peak) are based on a percentage of maximum heart rate. Maximum heart rate is calculated as 220 minus age. The Centers for Disease Control recommends that adults do at least 150-300 minutes of moderate-intensity aerobic activity each week or 75-150 minutes of vigorous-intensity aerobic activity each week."),
        dcc.Graph(
            id='graph_activity_minutes',
            figure=px.bar(),
            config= {'displaylogo': False}
        ),
        html.Div(id='fat_burn_table', style={'max-width': '1200px', 'margin': 'auto', 'font-weight': 'bold'}, children=[]),
        html.Div(id='cardio_table', style={'max-width': '1200px', 'margin': 'auto', 'font-weight': 'bold'}, children=[]),
        html.Div(id='peak_table', style={'max-width': '1200px', 'margin': 'auto', 'font-weight': 'bold'}, children=[]),
        html.Div(style={"height": '40px'}),
        html.H4("Weight Log", style={'font-weight': 'bold'}),
        html.H6("Fitbit connects with the Aria family of smart scales to track weight. Weight may also be self-reported using the Fitbit app. Studies suggest that regular weigh-ins may help people who want to lose weight."),
        dcc.Graph(
            id='graph_weight',
            figure=px.line(),
            config= {'displaylogo': False}
        ),
        html.Div(id='weight_table', style={'max-width': '1200px', 'margin': 'auto', 'font-weight': 'bold'}, children=[]),
        html.Div(style={"height": '40px'}),
        html.H4("SpO2", style={'font-weight': 'bold'}),
        html.H6("A pulse oximeter reading indicates what percentage of your blood is saturated, known as the SpO2 level. A typical, healthy reading is 95–100% . If your SpO2 level is less than 92%, a doctor may recommend you get an ABG. A pulse ox is the most common type of test because it's noninvasive and provides quick readings."),
        dcc.Graph(
            id='graph_spo2',
            figure=px.line(),
            config= {'displaylogo': False}
        ),
        html.Div(id='spo2_table', style={'max-width': '1200px', 'margin': 'auto', 'font-weight': 'bold'}, children=[]),
        html.Div(style={"height": '40px'}),
        html.H4("Sleep", style={'font-weight': 'bold'}),
        html.H6("Fitbit estimates sleep stages (awake, REM, light sleep and deep sleep) and sleep duration based on a person's movement and heart-rate patterns. The National Sleep Foundation recommends 7-9 hours of sleep per night for adults"),
        dcc.Graph(
            id='graph_sleep',
            figure=px.bar(),
            config= {'displaylogo': False}
        ),
        html.Div(id='sleep_table', style={'max-width': '1200px', 'margin': 'auto', 'font-weight': 'bold'}, children=[]),
        html.Div(style={"height": '40px'}),
        html.Div(className="hidden-print", style={'margin': 'auto', 'text-align': 'center'}, children=[
        dash_dangerously_set_inner_html.DangerouslySetInnerHTML( '''
        <form action="https://www.paypal.com/donate" method="post" target="_top">
<input type="hidden" name="hosted_button_id" value="X4CFTUDJ9ZXX2" />
<input type="image" src="https://pics.paypal.com/00/s/ZjQwZTU5NjktYzM2Ny00MTM3LTkzZWEtNDkwMjE2NGYzNDM4/file.PNG" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
<img alt="" border="0" src="https://www.paypal.com/en_CA/i/scr/pixel.gif" width="1" height="1" />
</form>
        ''')]),
        html.Div(style={"height": '25px'}),
    ]),
])

def format_minutes(minutes):
    return "%2dh %02dm" % (divmod(minutes, 60))

def calculate_table_data(df, measurement_name):
    df = df.sort_values(by='Date', ascending=False)
    result_data = {
        'Period' : ['30 days', '3 months', '6 months', '1 year'],
        'Average ' + measurement_name : [],
        'Max ' + measurement_name : [],
        'Min ' + measurement_name : []
    }
    last_date = df.head(1)['Date'].values[0]
    for period in [30, 90, 180, 365]:
        end_date = last_date
        start_date = end_date - pd.Timedelta(days=period)
        
        period_data = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        
        if len(period_data) >= period:

            max_hr = period_data[measurement_name].max()
            if measurement_name == "Steps Count":
                min_hr = period_data[period_data[measurement_name] != 0][measurement_name].min()
            else:
                min_hr = period_data[measurement_name].min()
            average_hr = round(period_data[measurement_name].mean(),2)
            
            if measurement_name == "Total Sleep Minutes":
                result_data['Average ' + measurement_name].append(format_minutes(average_hr))
                result_data['Max ' + measurement_name].append(format_minutes(max_hr))
                result_data['Min ' + measurement_name].append(format_minutes(min_hr))
            else:
                result_data['Average ' + measurement_name].append(average_hr)
                result_data['Max ' + measurement_name].append(max_hr)
                result_data['Min ' + measurement_name].append(min_hr)
        else:
            result_data['Average ' + measurement_name].append(pd.NA)
            result_data['Max ' + measurement_name].append(pd.NA)
            result_data['Min ' + measurement_name].append(pd.NA)
    
    return pd.DataFrame(result_data)

# Limits the date range to one year max
@app.callback(Output('my-date-picker-range', 'max_date_allowed'), Output('my-date-picker-range', 'end_date'),
             [Input('my-date-picker-range', 'start_date')])
def set_max_date_allowed(start_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    current_date = datetime.today().date() - timedelta(days=1)
    max_end_date = min((start + timedelta(days=365)).date(), current_date)
    return max_end_date, max_end_date

# Disables the button after click and starts calculations
@app.callback(Output('submit-button', 'disabled'), Output('my-date-picker-range', 'disabled'), Output('input-on-submit', 'disabled'), Input('submit-button', 'n_clicks'), prevent_initial_call=True)
def disable_button_and_calculate(n_clicks):
    return True, True, True

# fetch data and update graphs on click of submit
@app.callback(Output('report-title', 'children'), Output('date-range-title', 'children'), Output('generated-on-title', 'children'), Output('graph_RHR', 'figure'), Output('RHR_table', 'children'), Output('graph_steps', 'figure'), Output('graph_steps_heatmap', 'figure'), Output('steps_table', 'children'), Output('graph_activity_minutes', 'figure'), Output('fat_burn_table', 'children'), Output('cardio_table', 'children'), Output('peak_table', 'children'), Output('graph_weight', 'figure'), Output('weight_table', 'children'), Output('graph_spo2', 'figure'), Output('spo2_table', 'children'), Output('graph_sleep', 'figure'), Output('sleep_table', 'children'), Output("loading-output-1", "children"),
Input('submit-button', 'disabled'),
State('input-on-submit', 'value'), State('my-date-picker-range', 'start_date'), State('my-date-picker-range', 'end_date'),
prevent_initial_call=True)
def update_output(n_clicks, value, start_date, end_date):

    start_date = datetime.fromisoformat(start_date).strftime("%Y-%m-%d")
    end_date = datetime.fromisoformat(end_date).strftime("%Y-%m-%d")

    headers = {
        "Authorization": "Bearer " + value,
        "Accept": "application/json"
    }

    # Collecting data-----------------------------------------------------------------------------------------------------------------------
    
    user_profile = requests.get("https://api.fitbit.com/1/user/-/profile.json", headers=headers).json()
    response_heartrate = requests.get("https://api.fitbit.com/1/user/-/activities/heart/date/"+ start_date +"/"+ end_date +".json", headers=headers).json()
    response_steps = requests.get("https://api.fitbit.com/1/user/-/activities/steps/date/"+ start_date +"/"+ end_date +".json", headers=headers).json()
    response_weight = requests.get("https://api.fitbit.com/1/user/-/body/weight/date/"+ start_date +"/"+ end_date +".json", headers=headers).json()
    response_spo2 = requests.get("https://api.fitbit.com/1/user/-/spo2/date/"+ start_date +"/"+ end_date +".json", headers=headers).json()

    # Processing data-----------------------------------------------------------------------------------------------------------------------
    days_name_list = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday')
    report_title = "Wellness Report - " + user_profile["user"]["firstName"] + " " + user_profile["user"]["lastName"]
    report_dates_range = datetime.fromisoformat(start_date).strftime("%d %B, %Y") + " – " + datetime.fromisoformat(end_date).strftime("%d %B, %Y")
    generated_on_date = "Report Generated : " + datetime.today().date().strftime("%d %B, %Y")
    dates_list = []
    dates_str_list = []
    rhr_list = []
    steps_list = []
    weight_list = []
    spo2_list = []
    sleep_record_dict = {}
    deep_sleep_list, light_sleep_list, rem_sleep_list, awake_list, total_sleep_list = [],[],[],[],[]
    fat_burn_minutes_list, cardio_minutes_list, peak_minutes_list = [], [], []

    for entry in response_heartrate['activities-heart']:
        dates_str_list.append(entry['dateTime'])
        dates_list.append(datetime.strptime(entry['dateTime'], '%Y-%m-%d'))
        try:
            fat_burn_minutes_list.append(entry["value"]["heartRateZones"][1]["minutes"])
            cardio_minutes_list.append(entry["value"]["heartRateZones"][2]["minutes"])
            peak_minutes_list.append(entry["value"]["heartRateZones"][3]["minutes"])
        except KeyError as E:
            fat_burn_minutes_list.append(None)
            cardio_minutes_list.append(None)
            peak_minutes_list.append(None)
        if 'restingHeartRate' in entry['value']:
            rhr_list.append(entry['value']['restingHeartRate'])
        else:
            rhr_list.append(None)
    
    for entry in response_steps['activities-steps']:
        if int(entry['value']) == 0:
            steps_list.append(None)
        else:
            steps_list.append(int(entry['value']))

    for entry in response_weight["body-weight"]:
        weight_list.append(float(entry['value']))
    
    for entry in response_spo2:
        spo2_list += [None]*(dates_str_list.index(entry["dateTime"])-len(spo2_list))
        spo2_list.append(entry["value"]["avg"])
    spo2_list += [None]*(len(dates_str_list)-len(spo2_list))

    for i in range(0,len(dates_str_list),100):
        end_index = i+100
        if i+100 > len(dates_str_list):
            end_index = len(dates_str_list)
        temp_start_date = dates_str_list[i]
        temp_end_date = dates_str_list[end_index-1]

        response_sleep = requests.get("https://api.fitbit.com/1.2/user/-/sleep/date/"+ temp_start_date +"/"+ temp_end_date +".json", headers=headers).json()

        for sleep_record in response_sleep["sleep"][::-1]:
            if sleep_record['isMainSleep']:
                try:
                    sleep_record_dict[sleep_record['dateOfSleep']] = {'deep': sleep_record['levels']['summary']['deep']['minutes'],
                                                                    'light': sleep_record['levels']['summary']['light']['minutes'],
                                                                    'rem': sleep_record['levels']['summary']['rem']['minutes'],
                                                                    'wake': sleep_record['levels']['summary']['wake']['minutes'],
                                                                    'total_sleep': sleep_record["minutesAsleep"]}
                except KeyError as E:
                    pass

    for day in dates_str_list:
        if day in sleep_record_dict:
            deep_sleep_list.append(sleep_record_dict[day]['deep'])
            light_sleep_list.append(sleep_record_dict[day]['light'])
            rem_sleep_list.append(sleep_record_dict[day]['rem'])
            awake_list.append(sleep_record_dict[day]['wake'])
            total_sleep_list.append(sleep_record_dict[day]['total_sleep'])
        else:
            deep_sleep_list.append(None)
            light_sleep_list.append(None)
            rem_sleep_list.append(None)
            awake_list.append(None)
            total_sleep_list.append(None)

    df_merged = pd.DataFrame({
    "Date": dates_list,
    "Resting Heart Rate": rhr_list,
    "Steps Count": steps_list,
    "Fat Burn Minutes": fat_burn_minutes_list,
    "Cardio Minutes": cardio_minutes_list,
    "Peak Minutes": peak_minutes_list,
    "weight": weight_list,
    "SPO2": spo2_list,
    "Deep Sleep Minutes": deep_sleep_list,
    "Light Sleep Minutes": light_sleep_list,
    "REM Sleep Minutes": rem_sleep_list,
    "Awake Minutes": awake_list,
    "Total Sleep Minutes": total_sleep_list
    })
    
    df_merged["Total Active Minutes"] = df_merged["Fat Burn Minutes"] + df_merged["Cardio Minutes"] + df_merged["Peak Minutes"]
    rhr_avg = {'overall': round(df_merged["Resting Heart Rate"].mean(),1), '30d': round(df_merged["Resting Heart Rate"].tail(30).mean(),1)}
    steps_avg = {'overall': int(df_merged["Steps Count"].mean()), '30d': int(df_merged.sort_values(by='Date', ascending=False)["Steps Count"].head(31).mean())}
    weight_avg = {'overall': round(df_merged["weight"].mean(),1), '30d': round(df_merged["weight"].tail(30).mean(),1)}
    spo2_avg = {'overall': round(df_merged["SPO2"].mean(),1), '30d': round(df_merged["SPO2"].tail(30).mean(),1)}
    sleep_avg = {'overall': round(df_merged["Total Sleep Minutes"].mean(),1), '30d': round(df_merged["Total Sleep Minutes"].tail(30).mean(),1)}
    active_mins_avg = {'overall': round(df_merged["Total Active Minutes"].mean(),2), '30d': round(df_merged["Total Active Minutes"].tail(30).mean(),2)}
    weekly_steps_array = np.array([0]*days_name_list.index(datetime.fromisoformat(start_date).strftime('%A')) + df_merged["Steps Count"].to_list() + [0]*(6 - days_name_list.index(datetime.fromisoformat(end_date).strftime('%A'))))
    weekly_steps_array = np.transpose(weekly_steps_array.reshape((int(len(weekly_steps_array)/7), 7)))
    weekly_steps_array = pd.DataFrame(weekly_steps_array, index=days_name_list)

    # Plotting data-----------------------------------------------------------------------------------------------------------------------

    fig_rhr = px.line(df_merged, x="Date", y="Resting Heart Rate", line_shape="spline", color_discrete_sequence=["#d30f1c"], title=f"<b>Daily Resting Heart Rate<br><br><sup>Overall average : {rhr_avg['overall']} bpm | Last 30d average : {rhr_avg['30d']} bpm</sup></b><br><br><br>")
    fig_rhr.add_annotation(x=df_merged.iloc[df_merged["Resting Heart Rate"].idxmax()]["Date"], y=df_merged["Resting Heart Rate"].max(), text=str(df_merged["Resting Heart Rate"].max()), showarrow=False, arrowhead=0, bgcolor="#5f040a", opacity=0.80, yshift=15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_rhr.add_annotation(x=df_merged.iloc[df_merged["Resting Heart Rate"].idxmin()]["Date"], y=df_merged["Resting Heart Rate"].min(), text=str(df_merged["Resting Heart Rate"].min()), showarrow=False, arrowhead=0, bgcolor="#0b2d51", opacity=0.80, yshift=-15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_rhr.add_hline(y=df_merged["Resting Heart Rate"].mean(), line_dash="dot",annotation_text="Average : " + str(round(df_merged["Resting Heart Rate"].mean(), 1)) + " BPM", annotation_position="bottom right", annotation_bgcolor="#6b3908", annotation_opacity=0.6, annotation_borderpad=5, annotation_font=dict(family="Helvetica, monospace", size=14, color="#ffffff"))
    fig_rhr.add_hrect(y0=62, y1=68, fillcolor="green", opacity=0.15, line_width=0)
    rhr_summary_df = calculate_table_data(df_merged, "Resting Heart Rate")
    rhr_summary_table = dash_table.DataTable(rhr_summary_df.to_dict('records'), [{"name": i, "id": i} for i in rhr_summary_df.columns], style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}], style_header={'backgroundColor': '#5f040a','fontWeight': 'bold', 'color': 'white', 'fontSize': '14px'}, style_cell={'textAlign': 'center'})
    fig_steps = px.bar(df_merged, x="Date", y="Steps Count", color_discrete_sequence=["#2fb376"], title=f"<b>Daily Steps Count<br><br><sup>Overall average : {steps_avg['overall']} steps | Last 30d average : {steps_avg['30d']} steps</sup></b><br><br><br>")
    fig_steps.add_annotation(x=df_merged.iloc[df_merged["Steps Count"].idxmax()]["Date"], y=df_merged["Steps Count"].max(), text=str(df_merged["Steps Count"].max())+" steps", showarrow=False, arrowhead=0, bgcolor="#5f040a", opacity=0.80, yshift=15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_steps.add_annotation(x=df_merged.iloc[df_merged["Steps Count"].idxmin()]["Date"], y=df_merged["Steps Count"].min(), text=str(df_merged["Steps Count"].min())+" steps", showarrow=False, arrowhead=0, bgcolor="#0b2d51", opacity=0.80, yshift=-15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_steps.add_hline(y=df_merged["Steps Count"].mean(), line_dash="dot",annotation_text="Average : " + str(round(df_merged["Steps Count"].mean(), 1)) + " Steps", annotation_position="bottom right", annotation_bgcolor="#6b3908", annotation_opacity=0.8, annotation_borderpad=5, annotation_font=dict(family="Helvetica, monospace", size=14, color="#ffffff"))
    fig_steps_heatmap = px.imshow(weekly_steps_array, color_continuous_scale='YLGn', origin='lower', title="<b>Weekly Steps Heatmap</b>", labels={'x':"Week Number", 'y': "Day of the Week"}, height=350, aspect='equal')
    fig_steps_heatmap.update_traces(colorbar_orientation='h', selector=dict(type='heatmap'))
    steps_summary_df = calculate_table_data(df_merged, "Steps Count")
    steps_summary_table = dash_table.DataTable(steps_summary_df.to_dict('records'), [{"name": i, "id": i} for i in steps_summary_df.columns], style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}], style_header={'backgroundColor': '#072f1c','fontWeight': 'bold', 'color': 'white', 'fontSize': '14px'}, style_cell={'textAlign': 'center'})
    fig_activity_minutes = px.bar(df_merged, x="Date", y=["Fat Burn Minutes", "Cardio Minutes", "Peak Minutes"], title=f"<b>Activity Minutes<br><br><sup>Overall total active minutes average : {active_mins_avg['overall']} minutes | Last 30d total active minutes average : {active_mins_avg['30d']} minutes</sup></b><br><br><br>")
    fig_activity_minutes.update_layout(yaxis_title='Active Minutes', legend=dict(orientation="h",yanchor="bottom", y=1.02, xanchor="right", x=1, title_text=''))
    fat_burn_summary_df = calculate_table_data(df_merged, "Fat Burn Minutes")
    fat_burn_summary_table = dash_table.DataTable(fat_burn_summary_df.to_dict('records'), [{"name": i, "id": i} for i in fat_burn_summary_df.columns], style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}], style_header={'backgroundColor': '#636efa','fontWeight': 'bold', 'color': 'white', 'fontSize': '14px'}, style_cell={'textAlign': 'center'})
    cardio_summary_df = calculate_table_data(df_merged, "Cardio Minutes")
    cardio_summary_table = dash_table.DataTable(cardio_summary_df.to_dict('records'), [{"name": i, "id": i} for i in cardio_summary_df.columns], style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}], style_header={'backgroundColor': '#ef553b','fontWeight': 'bold', 'color': 'white', 'fontSize': '14px'}, style_cell={'textAlign': 'center'})
    peak_summary_df = calculate_table_data(df_merged, "Peak Minutes")
    peak_summary_table = dash_table.DataTable(peak_summary_df.to_dict('records'), [{"name": i, "id": i} for i in peak_summary_df.columns], style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}], style_header={'backgroundColor': '#00cc96','fontWeight': 'bold', 'color': 'white', 'fontSize': '14px'}, style_cell={'textAlign': 'center'})
    fig_weight = px.line(df_merged, x="Date", y="weight", line_shape="spline", color_discrete_sequence=["#6b3908"], title=f"<b>Weight<br><br><sup>Overall average : {weight_avg['overall']} Unit | Last 30d average : {weight_avg['30d']} Unit</sup></b><br><br><br>")
    fig_weight.add_annotation(x=df_merged.iloc[df_merged["weight"].idxmax()]["Date"], y=df_merged["weight"].max(), text=str(df_merged["weight"].max()), showarrow=False, arrowhead=0, bgcolor="#5f040a", opacity=0.80, yshift=15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_weight.add_annotation(x=df_merged.iloc[df_merged["weight"].idxmin()]["Date"], y=df_merged["weight"].min(), text=str(df_merged["weight"].min()), showarrow=False, arrowhead=0, bgcolor="#0b2d51", opacity=0.80, yshift=-15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_weight.add_hline(y=round(df_merged["weight"].mean(),1), line_dash="dot",annotation_text="Average : " + str(round(df_merged["weight"].mean(), 1)) + " Units", annotation_position="bottom right", annotation_bgcolor="#6b3908", annotation_opacity=0.6, annotation_borderpad=5, annotation_font=dict(family="Helvetica, monospace", size=14, color="#ffffff"))
    weight_summary_df = calculate_table_data(df_merged, "weight")
    weight_summary_table = dash_table.DataTable(weight_summary_df.to_dict('records'), [{"name": i, "id": i} for i in weight_summary_df.columns], style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}], style_header={'backgroundColor': '#4c3b7d','fontWeight': 'bold', 'color': 'white', 'fontSize': '14px'}, style_cell={'textAlign': 'center'})
    fig_spo2 = px.scatter(df_merged, x="Date", y="SPO2", color_discrete_sequence=["#983faa"], title=f"<b>SPO2 Percentage<br><br><sup>Overall average : {spo2_avg['overall']}% | Last 30d average : {spo2_avg['30d']}% </sup></b><br><br><br>", range_y=(90,100))
    fig_spo2.add_annotation(x=df_merged.iloc[df_merged["SPO2"].idxmax()]["Date"], y=df_merged["SPO2"].max(), text=str(df_merged["SPO2"].max())+"%", showarrow=False, arrowhead=0, bgcolor="#5f040a", opacity=0.80, yshift=15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_spo2.add_annotation(x=df_merged.iloc[df_merged["SPO2"].idxmin()]["Date"], y=df_merged["SPO2"].min(), text=str(df_merged["SPO2"].min())+"%", showarrow=False, arrowhead=0, bgcolor="#0b2d51", opacity=0.80, yshift=-15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_spo2.add_hline(y=df_merged["SPO2"].mean(), line_dash="dot",annotation_text="Average : " + str(round(df_merged["SPO2"].mean(), 1)) + "%", annotation_position="bottom right", annotation_bgcolor="#6b3908", annotation_opacity=0.6, annotation_borderpad=5, annotation_font=dict(family="Helvetica, monospace", size=14, color="#ffffff"))
    fig_spo2.update_traces(marker_size=6)
    spo2_summary_df = calculate_table_data(df_merged, "SPO2")
    spo2_summary_table = dash_table.DataTable(spo2_summary_df.to_dict('records'), [{"name": i, "id": i} for i in spo2_summary_df.columns], style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}], style_header={'backgroundColor': '#8d3a18','fontWeight': 'bold', 'color': 'white', 'fontSize': '14px'}, style_cell={'textAlign': 'center'})
    fig_sleep_minutes = px.bar(df_merged, x="Date", y=["Deep Sleep Minutes", "Light Sleep Minutes", "REM Sleep Minutes", "Awake Minutes"], title=f"<b>Sleep Stages<br><br><sup>Overall average : {format_minutes(int(sleep_avg['overall']))} | Last 30d average : {format_minutes(int(sleep_avg['30d']))}</sup></b><br><br>", color_discrete_map={"Deep Sleep Minutes": '#110d7f', "Light Sleep Minutes": '#8baff4', "REM Sleep Minutes": '#fabf76', "Awake Minutes": '#bd1120',})
    fig_sleep_minutes.update_layout(yaxis_title='Sleep Minutes', legend=dict(orientation="h",yanchor="bottom", y=1.02, xanchor="right", x=1, title_text=''))
    fig_sleep_minutes.add_annotation(x=df_merged.iloc[df_merged["Total Sleep Minutes"].idxmax()]["Date"], y=df_merged["Total Sleep Minutes"].max(), text=str(format_minutes(df_merged["Total Sleep Minutes"].max())), showarrow=False, arrowhead=0, bgcolor="#5f040a", opacity=0.80, yshift=15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_sleep_minutes.add_annotation(x=df_merged.iloc[df_merged["Total Sleep Minutes"].idxmin()]["Date"], y=df_merged["Total Sleep Minutes"].min(), text=str(format_minutes(df_merged["Total Sleep Minutes"].min())), showarrow=False, arrowhead=0, bgcolor="#0b2d51", opacity=0.80, yshift=-15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_sleep_minutes.add_hline(y=df_merged["Total Sleep Minutes"].mean(), line_dash="dot",annotation_text="Average : " + str(format_minutes(int(df_merged["Total Sleep Minutes"].mean()))), annotation_position="bottom right", annotation_bgcolor="#6b3908", annotation_opacity=0.6, annotation_borderpad=5, annotation_font=dict(family="Helvetica, monospace", size=14, color="#ffffff"))
    sleep_summary_df = calculate_table_data(df_merged, "Total Sleep Minutes")
    sleep_summary_table = dash_table.DataTable(sleep_summary_df.to_dict('records'), [{"name": i, "id": i} for i in sleep_summary_df.columns], style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}], style_header={'backgroundColor': '#636efa','fontWeight': 'bold', 'color': 'white', 'fontSize': '14px'}, style_cell={'textAlign': 'center'})
    
    return report_title, report_dates_range, generated_on_date, fig_rhr, rhr_summary_table, fig_steps, fig_steps_heatmap, steps_summary_table, fig_activity_minutes, fat_burn_summary_table, cardio_summary_table, peak_summary_table, fig_weight, weight_summary_table, fig_spo2, spo2_summary_table, fig_sleep_minutes, sleep_summary_table, ""

if __name__ == '__main__':
    app.run_server(debug=True)



# %%
