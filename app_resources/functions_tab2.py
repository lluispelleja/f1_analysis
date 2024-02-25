from app_resources.user_options import driver_translate
import plotly.graph_objects as go
import plotly.express as px
from fastf1 import utils
import fastf1.plotting
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import fastf1

def race_position(driver_ls, session, d1, d2):
    fig = go.Figure()

    for drv in driver_ls:
        drv_laps = session.laps.pick_driver(drv)

        abb = drv_laps['Driver'].iloc[0]
        color = fastf1.plotting.driver_color(abb)

        fig.add_trace(go.Scatter(x=drv_laps['LapNumber'], y=drv_laps['Position'],
                                mode='lines', name=abb, line=dict(color=color)))

    fig.update_layout(
        xaxis_title="Lap",
        yaxis_title="Position",
        yaxis=dict(autorange='reversed'),
        yaxis_tickvals=[1, 5, 10, 15, 20],
        yaxis_ticktext=[1, 5, 10, 15, 20],
        height=350,
        margin=dict(t=0)
    )

    fig.update_layout(
        legend=dict(
            x=1,
            y=1.02,
            traceorder="normal",
            bgcolor="rgba(255, 255, 255, 0)",
            bordercolor="rgba(255, 255, 255, 0)"
        )
    )

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    
def driver_LapTimes(race, d1, d2):
    driver_laps_1 = race.laps.pick_driver(d1).pick_quicklaps().reset_index()
    driver_laps_2 = race.laps.pick_driver(d2).pick_quicklaps().reset_index()

    driver_laps = pd.concat([driver_laps_1, driver_laps_2])

    new = []

    for i, row in driver_laps.iterrows():
        nn = driver_translate[row["Driver"]]
        new.append(nn)

    driver_laps["Driver"] = new
    
    driver_laps['LapTime_seconds'] = driver_laps['LapTime'].dt.total_seconds()
    driver_laps['LapTime_formatted'] = pd.to_datetime(driver_laps['LapTime_seconds'], unit='s').dt.strftime('%M:%S.%f')

    fig = px.scatter(driver_laps,
                    x="LapNumber",
                    y="LapTime_seconds",
                    color="Driver",
                    color_discrete_map=fastf1.plotting.DRIVER_COLORS,
                    labels={"LapNumber": "Lap Number", "LapTime_seconds": "Lap Time"},
                    hover_data={"LapTime_formatted": True},
                    height=425)

    max_time = int(np.ceil(driver_laps['LapTime_seconds'].max()))
    tickvals = list(range(0, max_time + 1))
    ticktext = [pd.to_datetime(sec, unit='s').strftime('%M:%S') for sec in tickvals]
    fig.update_yaxes(tickvals=tickvals, ticktext=ticktext)

    fig.update_layout(xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
                    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'), margin=dict(t=0))

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    
def delta_race(session, d1, d2):
    driver1 = session.laps.pick_driver(d1).pick_quicklaps().reset_index()
    driver2 = session.laps.pick_driver(d2).pick_quicklaps().reset_index()

    delta_time, ref_tel, compare_tel = utils.delta_time(driver1, driver2)

    # Create trace
    trace = go.Scatter(x=ref_tel['Distance'], y=delta_time, mode='lines', line=dict(dash='dash'))

    # Create layout
    layout = go.Layout(
        xaxis=dict(title='Distance'),
        yaxis=dict(title=f'<-- {d1} ahead | {d2} ahead -->'),
        height=300,
        margin=dict(t=0)
    )

    # Create figure
    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    
def tyre_strategy(session, d1, d2):
    laps = session.laps

    stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
    stints = stints.groupby(["Driver", "Stint", "Compound"])
    stints = stints.count().reset_index()
    stints = stints.rename(columns={"LapNumber": "StintLength"})

    total_stints = pd.concat([stints[stints["Driver"] == d1], stints[stints["Driver"] == d2]])
    nn = []

    for i, row in total_stints.iterrows():
        nn.append(fastf1.plotting.COMPOUND_COLORS[row["Compound"]])
        
    total_stints["color"] = nn

    bars = alt.Chart(total_stints).mark_bar().encode(
        y=alt.Y('Driver:N', title='Driver'),
        x=alt.X('sum(StintLength):Q', title='Lap Number'),
        color=alt.Color('color:N', scale=None),
        order=alt.Order('Compound:N', sort='ascending')
    )

    st.altair_chart(bars, theme="streamlit", use_container_width=True)
    
def speed(session, d1, d2):
    d1_laps = session.laps.pick_driver(d1).pick_fastest()
    d2_laps = session.laps.pick_driver(d2).pick_fastest()

    d1_tel = d1_laps.get_car_data().add_distance()
    d2_tel = d2_laps.get_car_data().add_distance()

    rbr_color = fastf1.plotting.team_color(d1_laps["Team"])
    mer_color = fastf1.plotting.team_color(d2_laps["Team"])

    trace_ver = go.Scatter(x=d1_tel['Distance'], y=d1_tel['Speed'], mode='lines', name=d1, line=dict(color=rbr_color))
    trace_ham = go.Scatter(x=d2_tel['Distance'], y=d2_tel['Speed'], mode='lines', name=d2, line=dict(color=mer_color))

    layout = go.Layout(
        xaxis=dict(title='Distance in m'),
        yaxis=dict(title='Speed in km/h'),
        legend=dict(x=0, y=1),
        margin=dict(t=0)
    )

    data = [trace_ver, trace_ham]

    fig = go.Figure(data=data, layout=layout)
    
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    
def delta_times(session, d1, d2):
    driver1 = session.laps.pick_driver(d1).pick_fastest()
    driver2 = session.laps.pick_driver(d2).pick_fastest()

    delta_time, ref_tel, compare_tel = utils.delta_time(driver1, driver2)

    # Create trace
    trace = go.Scatter(x=ref_tel['Distance'], y=delta_time, mode='lines', line=dict(dash='dash'))

    # Create layout
    layout = go.Layout(
        xaxis=dict(title='Distance'),
        yaxis=dict(title=f'<-- {d1} ahead | {d2} ahead -->'),
        height=300,
        margin=dict(t=0)
    )

    # Create figure
    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)