from app_resources.user_options import driver_translate, driver_colors
from timple.timedelta import strftimedelta
import plotly.graph_objs as go
from fastf1.core import Laps
import streamlit as st
import pandas as pd

def qualy_results(session):
    drivers = pd.unique(session.laps['Driver'])

    list_fastest_laps = list()
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)
    fastest_laps = Laps(list_fastest_laps) \
        .sort_values(by='LapTime') \
        .reset_index(drop=True)

    formated_t = []
    
    for i, row in fastest_laps.iterrows():
        total_seconds = row["LapTime"].total_seconds()

        # Calcular las horas, minutos y segundos
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = total_seconds % 60
        microseconds = row["LapTime"].microseconds

        # Formatear el tiempo en el formato deseado
        formatted_time = "{:02d}:{:02d}.{:02d}".format(minutes, int(seconds), int(microseconds / 10000))

        formated_t.append(formatted_time)

    fastest_laps["formated_lapTime"] = formated_t
    
    Q3 = []
    Q3_laps = []
    Q2 = []
    Q2_laps = []
    Q1 = []
    Q1_laps = []

    for i in range(0, 10):
        Q3.append(f"{fastest_laps['Driver'][i]} - {driver_translate[fastest_laps['Driver'][i]]}")
        Q3_laps.append(fastest_laps['formated_lapTime'][i])
        
    for i in range(10, 15):
        Q2.append(f"{fastest_laps['Driver'][i]} - {driver_translate[fastest_laps['Driver'][i]]}")
        Q2_laps.append(fastest_laps['formated_lapTime'][i])

    for i in range(15, 20):
        Q1.append(f"{fastest_laps['Driver'][i]} - {driver_translate[fastest_laps['Driver'][i]]}")
        Q1_laps.append(fastest_laps['formated_lapTime'][i])
        
    return Q3, Q3_laps, Q2, Q2_laps, Q1, Q1_laps

def qualy_result_graph(session):
    drivers = pd.unique(session.laps['Driver'])

    list_fastest_laps = list()

    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)
    fastest_laps = Laps(list_fastest_laps) \
        .sort_values(by='LapTime') \
        .reset_index(drop=True)

    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

    fastest_laps['LapTime_delta_seconds'] = fastest_laps['LapTimeDelta'].dt.total_seconds()
    fastest_laps['LapTime_delta_formatted'] = pd.to_datetime(fastest_laps['LapTime_delta_seconds'], unit='s').dt.strftime('%S.%f')

    fastest_laps = fastest_laps[fastest_laps["LapTime_delta_seconds"] < 6]
    driver_color = list()

    for index, lap in fastest_laps.iterlaps():
        driver = driver_translate[lap['Driver']]
        driver_color.append(driver_colors[driver])

    x_labels = []
    x_values = []
    start_time = fastest_laps['LapTime_delta_seconds'].min()
    end_time = fastest_laps['LapTime_delta_seconds'].max()
    current_time = start_time

    while current_time <= end_time:
        formatted_time = pd.to_datetime(current_time, unit='s').strftime('+%S.%f')
        formatted_time_truncated = formatted_time[:-3]
        x_values.append(current_time)
        x_labels.append(formatted_time_truncated)
        current_time += 0.5

    # Create bar trace
    bar_trace = go.Bar(
        y=fastest_laps.index,
        x=fastest_laps['LapTime_delta_seconds'],
        marker=dict(color=driver_color),
        orientation='h'
    )

    # Layout
    layout = go.Layout(
        yaxis=dict(
            tickvals=fastest_laps.index,
            ticktext=fastest_laps['Driver'],
            autorange='reversed'
        ),
        xaxis=dict(
            tickvals=x_values,
            ticktext=x_labels,
            showgrid=True,
            gridcolor='black',
            zeroline=False
        ),
        bargap=0.15,
        height=350,
        margin=dict(t=0)
    )

    # Create figure
    fig = go.Figure(data=[bar_trace], layout=layout)
    
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    
def qualy_lap_comp(session):
    drivers = pd.unique(session.laps['Driver'])

    d1 = session.laps.pick_driver(drivers[0]).pick_fastest()
    d2 = session.laps.pick_driver(drivers[1]).pick_fastest()
    d3 = session.laps.pick_driver(drivers[2]).pick_fastest()
    d4 = session.laps.pick_driver(drivers[3]).pick_fastest()
    d5 = session.laps.pick_driver(drivers[4]).pick_fastest()
    d6 = session.laps.pick_driver(drivers[5]).pick_fastest()
    d7 = session.laps.pick_driver(drivers[6]).pick_fastest()
    d8 = session.laps.pick_driver(drivers[7]).pick_fastest()
    d9 = session.laps.pick_driver(drivers[8]).pick_fastest()
    d10 = session.laps.pick_driver(drivers[9]).pick_fastest()

    t1 = d1.get_car_data().add_distance()
    t2 = d2.get_car_data().add_distance()
    t3 = d3.get_car_data().add_distance()
    t4 = d4.get_car_data().add_distance()
    t5 = d5.get_car_data().add_distance()
    t6 = d6.get_car_data().add_distance()
    t7 = d7.get_car_data().add_distance()
    t8 = d8.get_car_data().add_distance()
    t9 = d9.get_car_data().add_distance()
    t10 = d10.get_car_data().add_distance()

    trace_d1 = go.Scatter(x=t1['Distance'], y=t1['Speed'], mode='lines', name=drivers[0], line=dict(color=driver_colors[driver_translate[drivers[0]]]))
    trace_d2 = go.Scatter(x=t2['Distance'], y=t2['Speed'], mode='lines', name=drivers[1], line=dict(color=driver_colors[driver_translate[drivers[1]]]))
    trace_d3 = go.Scatter(x=t3['Distance'], y=t3['Speed'], mode='lines', name=drivers[2], line=dict(color=driver_colors[driver_translate[drivers[2]]]))
    trace_d4 = go.Scatter(x=t4['Distance'], y=t4['Speed'], mode='lines', name=drivers[3], line=dict(color=driver_colors[driver_translate[drivers[3]]]))
    trace_d5 = go.Scatter(x=t5['Distance'], y=t5['Speed'], mode='lines', name=drivers[4], line=dict(color=driver_colors[driver_translate[drivers[4]]]))
    trace_d6 = go.Scatter(x=t6['Distance'], y=t6['Speed'], mode='lines', name=drivers[5], line=dict(color=driver_colors[driver_translate[drivers[5]]]))
    trace_d7 = go.Scatter(x=t7['Distance'], y=t7['Speed'], mode='lines', name=drivers[6], line=dict(color=driver_colors[driver_translate[drivers[6]]]))
    trace_d8 = go.Scatter(x=t8['Distance'], y=t8['Speed'], mode='lines', name=drivers[7], line=dict(color=driver_colors[driver_translate[drivers[7]]]))
    trace_d9 = go.Scatter(x=t9['Distance'], y=t9['Speed'], mode='lines', name=drivers[8], line=dict(color=driver_colors[driver_translate[drivers[8]]]))
    trace_d10 = go.Scatter(x=t10['Distance'], y=t10['Speed'], mode='lines', name=drivers[9], line=dict(color=driver_colors[driver_translate[drivers[9]]]))

    layout = go.Layout(
        xaxis=dict(title='Distance in m'),
        yaxis=dict(title='Speed in km/h'),
        legend=dict(x=1.1, y=1),
        margin=dict(t=0),
        height=400
    )

    data = [trace_d1, trace_d2, trace_d3, trace_d4, trace_d5, trace_d6, trace_d7, trace_d8, trace_d9, trace_d10]

    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    
    trace_d1_t = go.Scatter(x=t1['Distance'], y=t1['Throttle'], mode='lines', name=drivers[0], line=dict(color=driver_colors[driver_translate[drivers[0]]]))
    trace_d2_t = go.Scatter(x=t2['Distance'], y=t2['Throttle'], mode='lines', name=drivers[1], line=dict(color=driver_colors[driver_translate[drivers[1]]]))
    trace_d3_t = go.Scatter(x=t3['Distance'], y=t3['Throttle'], mode='lines', name=drivers[2], line=dict(color=driver_colors[driver_translate[drivers[2]]]))
    trace_d4_t = go.Scatter(x=t4['Distance'], y=t4['Throttle'], mode='lines', name=drivers[3], line=dict(color=driver_colors[driver_translate[drivers[3]]]))
    trace_d5_t = go.Scatter(x=t5['Distance'], y=t5['Throttle'], mode='lines', name=drivers[4], line=dict(color=driver_colors[driver_translate[drivers[4]]]))
    trace_d6_t = go.Scatter(x=t6['Distance'], y=t6['Throttle'], mode='lines', name=drivers[5], line=dict(color=driver_colors[driver_translate[drivers[5]]]))
    trace_d7_t = go.Scatter(x=t7['Distance'], y=t7['Throttle'], mode='lines', name=drivers[6], line=dict(color=driver_colors[driver_translate[drivers[6]]]))
    trace_d8_t = go.Scatter(x=t8['Distance'], y=t8['Throttle'], mode='lines', name=drivers[7], line=dict(color=driver_colors[driver_translate[drivers[7]]]))
    trace_d9_t = go.Scatter(x=t9['Distance'], y=t9['Throttle'], mode='lines', name=drivers[8], line=dict(color=driver_colors[driver_translate[drivers[8]]]))
    trace_d10_t = go.Scatter(x=t10['Distance'], y=t10['Throttle'], mode='lines', name=drivers[9], line=dict(color=driver_colors[driver_translate[drivers[9]]]))

    layout = go.Layout(
        xaxis=dict(title='Distance in m'),
        yaxis=dict(title='Throttle preassure (%)'),
        legend=dict(x=1.1, y=1),
        margin=dict(t=0),
        height=200
    )

    data_t = [trace_d1_t, trace_d2_t, trace_d3_t, trace_d4_t, trace_d5_t, trace_d6_t, trace_d7_t, trace_d8_t, trace_d9_t, trace_d10_t]

    fig2 = go.Figure(data=data_t, layout=layout)
    st.plotly_chart(fig2, theme='streamlit', use_container_width=True)
    
    trace_d1_b = go.Scatter(x=t1['Distance'], y=t1['Brake'], mode='lines', name=drivers[0], line=dict(color=driver_colors[driver_translate[drivers[0]]]))
    trace_d2_b = go.Scatter(x=t2['Distance'], y=t2['Brake'], mode='lines', name=drivers[1], line=dict(color=driver_colors[driver_translate[drivers[1]]]))
    trace_d3_b = go.Scatter(x=t3['Distance'], y=t3['Brake'], mode='lines', name=drivers[2], line=dict(color=driver_colors[driver_translate[drivers[2]]]))
    trace_d4_b = go.Scatter(x=t4['Distance'], y=t4['Brake'], mode='lines', name=drivers[3], line=dict(color=driver_colors[driver_translate[drivers[3]]]))
    trace_d5_b = go.Scatter(x=t5['Distance'], y=t5['Brake'], mode='lines', name=drivers[4], line=dict(color=driver_colors[driver_translate[drivers[4]]]))
    trace_d6_b = go.Scatter(x=t6['Distance'], y=t6['Brake'], mode='lines', name=drivers[5], line=dict(color=driver_colors[driver_translate[drivers[5]]]))
    trace_d7_b = go.Scatter(x=t7['Distance'], y=t7['Brake'], mode='lines', name=drivers[6], line=dict(color=driver_colors[driver_translate[drivers[6]]]))
    trace_d8_b = go.Scatter(x=t8['Distance'], y=t8['Brake'], mode='lines', name=drivers[7], line=dict(color=driver_colors[driver_translate[drivers[7]]]))
    trace_d9_b = go.Scatter(x=t9['Distance'], y=t9['Brake'], mode='lines', name=drivers[8], line=dict(color=driver_colors[driver_translate[drivers[8]]]))
    trace_d10_b = go.Scatter(x=t10['Distance'], y=t10['Brake'], mode='lines', name=drivers[9], line=dict(color=driver_colors[driver_translate[drivers[9]]]))
    
    layout = go.Layout(
        xaxis=dict(title='Distance in m'),
        yaxis=dict(title='Brake preassure (%)'),
        legend=dict(x=1.1, y=1),
        margin=dict(t=0),
        height=200
    )

    data_b = [trace_d1_b, trace_d2_b, trace_d3_b, trace_d4_b, trace_d5_b, trace_d6_b, trace_d7_b, trace_d8_b, trace_d9_b, trace_d10_b]
    fig3 = go.Figure(data=data_b, layout=layout)
    st.plotly_chart(fig3, theme='streamlit', use_container_width=True)
    
    trace_d1_rp = go.Scatter(x=t1['Distance'], y=t1['RPM'], mode='lines', name=drivers[0], line=dict(color=driver_colors[driver_translate[drivers[0]]]))
    trace_d2_rp = go.Scatter(x=t2['Distance'], y=t2['RPM'], mode='lines', name=drivers[1], line=dict(color=driver_colors[driver_translate[drivers[1]]]))
    trace_d3_rp = go.Scatter(x=t3['Distance'], y=t3['RPM'], mode='lines', name=drivers[2], line=dict(color=driver_colors[driver_translate[drivers[2]]]))
    trace_d4_rp = go.Scatter(x=t4['Distance'], y=t4['RPM'], mode='lines', name=drivers[3], line=dict(color=driver_colors[driver_translate[drivers[3]]]))
    trace_d5_rp = go.Scatter(x=t5['Distance'], y=t5['RPM'], mode='lines', name=drivers[4], line=dict(color=driver_colors[driver_translate[drivers[4]]]))
    trace_d6_rp = go.Scatter(x=t6['Distance'], y=t6['RPM'], mode='lines', name=drivers[5], line=dict(color=driver_colors[driver_translate[drivers[5]]]))
    trace_d7_rp = go.Scatter(x=t7['Distance'], y=t7['RPM'], mode='lines', name=drivers[6], line=dict(color=driver_colors[driver_translate[drivers[6]]]))
    trace_d8_rp = go.Scatter(x=t8['Distance'], y=t8['RPM'], mode='lines', name=drivers[7], line=dict(color=driver_colors[driver_translate[drivers[7]]]))
    trace_d9_rp = go.Scatter(x=t9['Distance'], y=t9['RPM'], mode='lines', name=drivers[8], line=dict(color=driver_colors[driver_translate[drivers[8]]]))
    trace_d10_rp = go.Scatter(x=t10['Distance'], y=t10['RPM'], mode='lines', name=drivers[9], line=dict(color=driver_colors[driver_translate[drivers[9]]]))
    
    layout = go.Layout(
        xaxis=dict(title='Distance in m'),
        yaxis=dict(title='RPM'),
        legend=dict(x=1.1, y=1),
        margin=dict(t=0),
        height=200
    )
    
    data_rp = [trace_d1_rp, trace_d2_rp, trace_d3_rp, trace_d4_rp, trace_d5_rp, trace_d6_rp, trace_d7_rp, trace_d8_rp, trace_d9_rp, trace_d10_rp]
    fig4 = go.Figure(data=data_rp, layout=layout)
    st.plotly_chart(fig4, theme='streamlit', use_container_width=True)