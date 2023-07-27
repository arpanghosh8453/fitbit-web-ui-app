# %%
import dash, requests, math
from dash import dcc
from dash import html
from dash.dependencies import Output, State, Input
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta


# %%

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[

    html.Div(style={
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
        minimum_nights=40,
        max_date_allowed=datetime.today().date() - timedelta(days=1),
        min_date_allowed=datetime.today().date() - timedelta(days=720),
        end_date=datetime.today().date() - timedelta(days=1),
        start_date=datetime.today().date() - timedelta(days=365)
        ),
        dcc.Input(id='input-on-submit', value="", placeholder='API ACCESS TOKEN', type='text'),
        html.Button(id='submit-button', type='submit', children='Submit', n_clicks=0, className="button-primary"),
    ]),

    html.Div(id='loading-div', style={'margin-top': '40px'}, children=[
    dcc.Loading(
            id="loading-progress",
            type="default",
            children=html.Div(id="loading-output-1")
        ),
    ]),

    html.Div(id='output_div', children=[

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

        dcc.Graph(
            id='graph_RHR',
            figure=px.line(),
            config= {'displaylogo': False}
        ),

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

        dcc.Graph(
            id='graph_activity_minutes',
            figure=px.bar(),
            config= {'displaylogo': False}
        ),

        dcc.Graph(
            id='graph_weight',
            figure=px.line(),
            config= {'displaylogo': False}
        ),

        dcc.Graph(
            id='graph_spo2',
            figure=px.line(),
            config= {'displaylogo': False}
        ),
    ]),
])

# Limits the date range to one year max
@app.callback(Output('my-date-picker-range', 'max_date_allowed'), Output('my-date-picker-range', 'end_date'),
             [Input('my-date-picker-range', 'start_date')])
def set_max_date_allowed(start_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    max_end_date = start + timedelta(days=365)
    return max_end_date, max_end_date

# Disables the button after click and starts calculations
@app.callback(Output('submit-button', 'disabled'), Output('my-date-picker-range', 'disabled'), Output('input-on-submit', 'disabled'), Input('submit-button', 'n_clicks'), prevent_initial_call=True)
def disable_button_and_calculate(n_clicks):
    return True, True, True

# fetch data and update graphs on click of submit
@app.callback(Output('report-title', 'children'), Output('date-range-title', 'children'), Output('generated-on-title', 'children'), Output('graph_RHR', 'figure'), Output('graph_steps', 'figure'), Output('graph_steps_heatmap', 'figure'), Output('graph_activity_minutes', 'figure'), Output('graph_weight', 'figure'), Output('graph_spo2', 'figure'), Output("loading-output-1", "children"),
Input('submit-button', 'disabled'),
State('input-on-submit', 'value'), State('my-date-picker-range', 'start_date'), State('my-date-picker-range', 'end_date'),
prevent_initial_call=True
)
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
    report_title = "Wellness report - " + user_profile["user"]["firstName"] + " " + user_profile["user"]["lastName"]
    report_dates_range = datetime.fromisoformat(start_date).strftime("%d %B, %Y") + " – " + datetime.fromisoformat(end_date).strftime("%d %B, %Y")
    generated_on_date = "Report Generated :" + datetime.today().date().strftime("%d %B, %Y")
    dates_list = []
    dates_str_list = []
    rhr_list = []
    steps_list = []
    weight_list = []
    spo2_list = []
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
        steps_list.append(int(entry['value']))

    for entry in response_weight["body-weight"]:
        weight_list.append(float(entry['value']))
    
    for entry in response_spo2:
        spo2_list += [None]*(dates_str_list.index(entry["dateTime"])-len(spo2_list))
        spo2_list.append(entry["value"]["avg"])
    spo2_list += [None]*(len(dates_str_list)-len(spo2_list))

    df_merged = pd.DataFrame({
    "Date": dates_list,
    "Resting Heart Rate": rhr_list,
    "Steps Count": steps_list,
    "Fat Burn Minutes": fat_burn_minutes_list,
    "Cardio Minutes": cardio_minutes_list,
    "Peak Minutes": peak_minutes_list,
    "weight": weight_list,
    "SPO2": spo2_list
    })

    non_zero_steps_df = df_merged[df_merged["Steps Count"] != 0]
    df_merged["Total Active Minutes"] = df_merged["Fat Burn Minutes"] + df_merged["Cardio Minutes"] + df_merged["Peak Minutes"]
    rhr_avg = {'overall': round(df_merged["Resting Heart Rate"].mean(),1), '30d': round(df_merged["Resting Heart Rate"].tail(30).mean(),1)}
    steps_avg = {'overall': round(non_zero_steps_df["Steps Count"].mean(),0), '30d': round(non_zero_steps_df["Steps Count"].tail(30).mean(),0)}
    weight_avg = {'overall': round(df_merged["weight"].mean(),1), '30d': round(df_merged["weight"].tail(30).mean(),1)}
    active_mins_avg = {'overall': round(df_merged["Total Active Minutes"].mean(),2), '30d': round(df_merged["Total Active Minutes"].tail(30).mean(),2)}
    weekly_steps_array = np.array([0]*days_name_list.index(datetime.fromisoformat(start_date).strftime('%A')) + df_merged["Steps Count"].to_list() + [0]*(6 - days_name_list.index(datetime.fromisoformat(end_date).strftime('%A'))))
    weekly_steps_array = np.transpose(weekly_steps_array.reshape((int(len(weekly_steps_array)/7), 7)))
    weekly_steps_array = pd.DataFrame(weekly_steps_array, index=days_name_list)
    # Plotting data-----------------------------------------------------------------------------------------------------------------------

    fig_rhr = px.line(df_merged, x="Date", y="Resting Heart Rate", line_shape="spline", color_discrete_sequence=["#d30f1c"], title=f"<b>Daily Resting Heart Rate<br><br><sup>Overall average : {rhr_avg['overall']} bpm | Last 30d average : {rhr_avg['30d']} bpm</sup></b><br><br><br>")
    fig_rhr.add_annotation(x=df_merged.iloc[df_merged["Resting Heart Rate"].idxmax()]["Date"], y=df_merged["Resting Heart Rate"].max(), text=str(df_merged["Resting Heart Rate"].max()), showarrow=False, arrowhead=0, bgcolor="#5f040a", opacity=0.80, yshift=15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_rhr.add_annotation(x=df_merged.iloc[df_merged["Resting Heart Rate"].idxmin()]["Date"], y=df_merged["Resting Heart Rate"].min(), text=str(df_merged["Resting Heart Rate"].min()), showarrow=False, arrowhead=0, bgcolor="#0b2d51", opacity=0.80, yshift=-15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_rhr.add_hline(y=df_merged["Resting Heart Rate"].mean(), line_dash="dot",annotation_text="Average : " + str(round(df_merged["Resting Heart Rate"].mean(), 1)), annotation_position="bottom right", annotation_bgcolor="#6b3908", annotation_opacity=0.6, annotation_borderpad=5, annotation_font=dict(family="Helvetica, monospace", size=14, color="#ffffff"))
    fig_rhr.add_hrect(y0=62, y1=68, fillcolor="green", opacity=0.15, line_width=0)
    fig_steps = px.bar(df_merged, x="Date", y="Steps Count", title=f"<b>Daily Steps Count<br><br><sup>Overall average : {steps_avg['overall']} steps | Last 30d average : {steps_avg['30d']} steps</sup></b><br><br><br>")
    fig_steps.add_annotation(x=df_merged.iloc[df_merged["Steps Count"].idxmax()]["Date"], y=df_merged["Steps Count"].max(), text=str(df_merged["Steps Count"].max())+" steps", showarrow=False, arrowhead=0, bgcolor="#5f040a", opacity=0.80, yshift=15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_steps.add_annotation(x=non_zero_steps_df.iloc[non_zero_steps_df["Steps Count"].idxmin()]["Date"], y=non_zero_steps_df["Steps Count"].min(), text=str(non_zero_steps_df["Steps Count"].min())+" steps", showarrow=False, arrowhead=0, bgcolor="#0b2d51", opacity=0.80, yshift=-15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_steps.add_hline(y=non_zero_steps_df["Steps Count"].mean(), line_dash="dot",annotation_text="Average : " + str(round(df_merged["Steps Count"].mean(), 1)), annotation_position="bottom right", annotation_bgcolor="#6b3908", annotation_opacity=0.8, annotation_borderpad=5, annotation_font=dict(family="Helvetica, monospace", size=14, color="#ffffff"))
    fig_steps_heatmap = px.imshow(weekly_steps_array, color_continuous_scale='YLGn', origin='lower', title="<b>Weekly Steps Heatmap</b>", labels={'x':"Week Number", 'y': "Day of the Week"}, height=350, aspect='equal')
    fig_steps_heatmap.update_traces(colorbar_orientation='h', selector=dict(type='heatmap'))
    fig_activity_minutes = px.bar(df_merged, x="Date", y=["Fat Burn Minutes", "Cardio Minutes", "Peak Minutes"], title=f"<b>Activity Minutes<br><br><sup>Overall average : {active_mins_avg['overall']} minutes | Last 30d average : {active_mins_avg['30d']} minutes</sup></b><br><br><br>")
    fig_activity_minutes.update_layout(yaxis_title='Active Minutes', legend=dict(orientation="h",yanchor="bottom", y=1.02, xanchor="right", x=1, title_text=''))
    fig_weight = px.line(df_merged, x="Date", y="weight", line_shape="spline", color_discrete_sequence=["#6b3908"], title=f"<b>Weight<br><br><sup>Overall average : {weight_avg['overall']} Unit | Last 30d average : {weight_avg['30d']} Unit</sup></b><br><br><br>")
    fig_weight.add_annotation(x=df_merged.iloc[df_merged["weight"].idxmax()]["Date"], y=df_merged["weight"].max(), text=str(df_merged["weight"].max()), showarrow=False, arrowhead=0, bgcolor="#5f040a", opacity=0.80, yshift=15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_weight.add_annotation(x=df_merged.iloc[df_merged["weight"].idxmin()]["Date"], y=df_merged["weight"].min(), text=str(df_merged["weight"].min()), showarrow=False, arrowhead=0, bgcolor="#0b2d51", opacity=0.80, yshift=-15, borderpad=5, font=dict(family="Helvetica, monospace", size=12, color="#ffffff"), )
    fig_weight.add_hline(y=round(df_merged["weight"].mean(),1), line_dash="dot",annotation_text="Average : " + str(round(df_merged["weight"].mean(), 1)), annotation_position="bottom right", annotation_bgcolor="#6b3908", annotation_opacity=0.6, annotation_borderpad=5, annotation_font=dict(family="Helvetica, monospace", size=14, color="#ffffff"))
    fig_spo2 = px.bar(df_merged, x="Date", y="SPO2", title="<b>SPO2 Percentage</b>", range_y=(80,100))

    
    return report_title, report_dates_range, generated_on_date, fig_rhr, fig_steps, fig_steps_heatmap, fig_activity_minutes, fig_weight, fig_spo2, ""

if __name__ == '__main__':
    app.run_server(debug=True)



# %%
