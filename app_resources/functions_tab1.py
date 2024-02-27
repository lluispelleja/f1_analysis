from app_resources.user_options import driver_translate, driver_colors, TEAM_COLORS
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import fastf1.plotting
import streamlit as st
import altair as alt
import fastf1
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib as mpl
from matplotlib import colormaps

def race_position_all_drivers(session):
    fig = go.Figure()
    
    drivers_ls = session.drivers

    for drv in drivers_ls:
        drv_laps = session.laps.pick_driver(drv)

        abb = drv_laps['Driver'].iloc[0]
        abb_ = driver_translate[abb]
        color = driver_colors[abb_]

        fig.add_trace(go.Scatter(x=drv_laps['LapNumber'], y=drv_laps['Position'],
                                 mode='lines', name=abb, line=dict(color=color)))

    fig.update_layout(
        xaxis_title="Lap",
        yaxis_title="Position",
        yaxis=dict(autorange='reversed'),
        yaxis_tickvals=[1, 5, 10, 15, 20],
        yaxis_ticktext=[1, 5, 10, 15, 20],
        height=570,
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

def all_driver_LapTimes(race):
    driver_laps = race.laps.pick_quicklaps().reset_index()

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
    
def tyre_strategy_all_drivers(session):
    laps = session.laps

    stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
    stints = stints.groupby(["Driver", "Stint", "Compound"])
    stints = stints.count().reset_index()
    stints = stints.rename(columns={"LapNumber": "StintLength"})

    nn = []

    for i, row in stints.iterrows():
        nn.append(fastf1.plotting.COMPOUND_COLORS[row["Compound"]])
        
    stints["color"] = nn

    bars = alt.Chart(stints).mark_bar().encode(
        y=alt.Y('Driver:N', title='Driver'),
        x=alt.X('sum(StintLength):Q', title='Lap Number'),
        color=alt.Color('color:N', scale=None),
        order=alt.Order('Compound:N', sort='ascending')
    )

    st.altair_chart(bars, theme="streamlit", use_container_width=True)

def driver_times(race):
    # point_finishers = race.drivers[:10]
    driver_laps = race.laps.pick_drivers(race.drivers).pick_quicklaps()
    driver_laps = driver_laps.reset_index()
    driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()

    driver_colors_ = {abv: driver_colors[driver] for abv,
                    driver in driver_translate.items()}

    # Crear el gráfico de violín
    fig = px.violin(driver_laps, x='Driver', y="LapTime(s)", color="Driver", color_discrete_map=driver_colors_,)

    # Personalizar el diseño del gráfico
    fig.update_layout(
        xaxis_title="Lap Time (s)",
        yaxis_title="Driver",
        violinmode='overlay'
    )
    
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

def team_pace(race):
    laps = race.laps.pick_quicklaps()
    
    transformed_laps = laps.copy()
    transformed_laps.loc[:, "LapTime (s)"] = laps["LapTime"].dt.total_seconds()

    team_order = (
        transformed_laps[["Team", "LapTime (s)"]]
        .groupby("Team")
        .median()["LapTime (s)"]
        .sort_values()
        .index
    )

    team_palette = {team: TEAM_COLORS[team] for team in team_order}

    fig = px.box(transformed_laps, 
                x="Team", 
                y="LapTime (s)", 
                color="Team", 
                category_orders={"Team": team_order},
                color_discrete_map=team_palette)

    fig.update_layout(yaxis=dict(showgrid=False), margin=dict(t=0))

    fig.update_xaxes(title=None)

    fig.update_layout(height=500, width=800)
    
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

def gear_map(session):
    lap = session.laps.pick_fastest()
    tel = lap.get_telemetry()

    x = np.array(tel['X'].values)
    y = np.array(tel['Y'].values)

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    gear = tel['nGear'].to_numpy().astype(float)

    cmap = plt.cm.get_cmap('Paired')  # Use Paired colormap
    lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
    lc_comp.set_array(gear)
    lc_comp.set_linewidth(4)

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.add_collection(lc_comp)
    ax.axis('equal')
    ax.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

    cbar = plt.colorbar(mappable=lc_comp, label="Gear", boundaries=np.arange(1, 10))
    cbar.set_ticks(np.arange(1.5, 9.5))
    cbar.set_ticklabels(np.arange(1, 9))

    # Quitar el borde del gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Mostrar el gráfico en Matplotlib
    st.pyplot(fig)

def speed_map(session):
    colormap = mpl.cm.plasma
    lap = session.laps.pick_fastest()

    # Get telemetry data
    x = lap.telemetry['X']              # values for x-axis
    y = lap.telemetry['Y']              # values for y-axis
    color = lap.telemetry['Speed']      # value to base color gradient on

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # We create a plot with title and adjust some setting to make it look good.
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
    # fig.suptitle(f"{session.event['EventName']} {session.event.year} - Speed", size=24, y=0.97)

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')


    # After this, we plot the data itself.
    # Create background track line
    ax.plot(lap.telemetry['X'], lap.telemetry['Y'],
            color='black', linestyle='-', linewidth=16, zorder=0)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(color.min(), color.max())
    lc = LineCollection(segments, cmap=colormap, norm=norm,
                        linestyle='-', linewidth=5)

    # Set the values used for colormapping
    lc.set_array(color)

    # Merge all line segments together
    line = ax.add_collection(lc)


    # Finally, we create a color bar as a legend.
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap,
                                    orientation="horizontal")


    # Show the plot
    st.pyplot(fig)