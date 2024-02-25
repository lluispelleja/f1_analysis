import streamlit as st
from app_resources.user_options import years, drivers_2022, drivers_2023, races_2022, races_2023
from app_resources.functions_tab1 import race_position_all_drivers, tyre_strategy_all_drivers, team_pace, gear_map, speed_map, driver_times, all_driver_LapTimes
from app_resources.functions_tab2 import race_position, driver_LapTimes, tyre_strategy, speed, delta_times, delta_race
from app_resources.functions_tab3 import qualy_results, qualy_result_graph, qualy_lap_comp
import fastf1.plotting

st.set_page_config(layout="wide") 
st.title("F1 ANALYSIS HUB")
tab0, tab1, tab2, tab3 = st.tabs(["Home", "Race Overview", "Driver comparison in race", "Qualifying Overview"])

with tab0:
    st.subheader("Welcome to F1 Analysisi hub")
    st.write("Here you will find all the insights of every Formula 1 race. This application has been built for the Formula 1 fans to access to the information about the competition and for who want to go one step further and watch the sport from a more detailed view.")
    st.write("")
    st.markdown(f'<p style="font-size: 20px;font-weight: bold;margin-bottom: 0px;">How the application works?</p>', unsafe_allow_html=True)
    st.write("The application has three tabs located at the top of the screen, each tab has its use case and its purpose:")
    
    col1, col2 = st.columns([0.02, 1.98])
    
    with col2:
        st.write('- **Race Overview**: In this tab you can select any race of the years 2022 and 2023 to have an overview of what happened in it, when you choose the race it will start loading the data and show you different graphs that you can interact with, such as driver positions, driver lap times and car telemetries. In each graph there is an explanation of how to make a good use of it and all its features. ')
        st.info('The first time a session is uploaded it may take a few minutes as there is a lot of data, you can see the upload status on the top right hand side of the screen.', icon="ℹ️")
        
        st.write('- **Driver comparison in race**: In this tab you can choose any race from the years 2022 and 2023, in which choosing two drivers who participated that year in the championship to make a comparison between them. The graphs to be displayed are such as driver positions, driver lap times and car telemetries. In this case it will display different graphics to the first tab adding the comparison of their best lap and the time difference in the race.')
        st.info('On charts where a legend is available you can filter by double-clicking on the first pilot and single-clicking on the following ones, to reset the filter double-click on the legend again.', icon="💡")
        
        st.write("- **Qualifying Overview**: In this tab you can choose the Qualy of any Grand Prix held in the years 2022 and 2023, by doing so the application will load different graphs to be able to analyse the performance of each driver in the session and their best lap times. These graphs will be the ranking of the drivers in each session, the comparison of the drivers' laps and much more.")
        st.info('In this tab you can compare between several drivers using the legends of the graphs as filters.', icon="💡")

with tab1:
    col1, col2, col23, col3 = st.columns([1,1,2,0.1])

    with col1:
        year = st.selectbox('Select the year:', years, key=1)
    
    with col2:
        if year == 2022:
            races = st.selectbox("Select the race:", races_2022)
            races_years = races_2022
        elif year == 2023:
            races = st.selectbox("Select the race:", races_2023)
            races_years = races_2023
    
    if year != "Select Year" and races != "Select a GP":
        with col23:
            st.info('The first time a session is uploaded it may take a few minutes as there is a lot of data, you can see the upload status on the top right hand side of the screen.', icon="ℹ️")
        
        race = fastf1.get_session(year, races_years[races], "R")
        race.load()
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">Position evolution in the {race.event.year} {race.event["EventName"]}</p>', unsafe_allow_html=True)
        st.write("This graph shows the position of all drivers during the whole race, by double clicking on the legend you can isolate the driver and by clicking on another one you can compare only those two drivers, to reset the legend double-click on any name.")
        race_position_all_drivers(race)
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">Laptimes in the {race.event.year} {race.event["EventName"]}</p>', unsafe_allow_html=True)
        st.write("This graph shows the laptimes of all drivers during the whole race, by double clicking on the legend you can isolate the driver and by clicking on another one you can compare only those two drivers, to reset the legend double-click on any name.")
        all_driver_LapTimes(race)
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">Tyre strategy in the {race.event.year} {race.event["EventName"]}</p>', unsafe_allow_html=True)
        st.write("In this graph you can see the tyre strategy used by each driver differentiating the compounds by their original colours.")
        tyre_strategy_all_drivers(race)
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">Drivers lap time distribution in the {race.event.year} {race.event["EventName"]}</p>', unsafe_allow_html=True)
        st.write("In this graph we can see the distribution of lap times of all the drivers who ran in the race, seeing how consistent they were during the race, by their original coloursby double clicking on the legend you can isolate the driver and by clicking on another one you can compare only those two drivers, to reset the legend double-click on any name.")
        driver_times(race)
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">Team pace comparison in the {race.event.year} {race.event["EventName"]}</p>', unsafe_allow_html=True)
        st.write("In this graph you can see which team was more consistent during the race, you can also see the average lap time and the distribution of the laps knowing more or less what pace their two drivers were on during the race, by double clicking on the legend you can isolate the team and by clicking on another one you can compare only those two teams, to reset the legend double-click on any name.")
        team_pace(race)
        
        col_1, col_2 = st.columns(2)
        
        with col_1:
            st.markdown(f'<p style="text-align: center; font-size: 16px;font-weight: bold; margin-bottom: 0px;">{race.event["EventName"]} {race.event.year} - Gear</p>', unsafe_allow_html=True)
            st.write("In this graph you can see which gear is used in each part of the circuit in order to see the characteristics of the circuit.")
            gear_map(race)
        
        with col_2:
            st.markdown(f'<p style="text-align: center; font-size: 16px;font-weight: bold; margin-bottom: 0px;">{race.event["EventName"]} {race.event.year} - Speed</p>', unsafe_allow_html=True)
            st.write("In this graph you will find the speed in each part of the circuit, in order to see its fast and slow areas, knowing which type of car can win in each sector.")
            speed_map(race)
            
with tab2:
    col1, col2, col23, col3 = st.columns(4)

    with col1:
        year = st.selectbox('Select the year:', years, key=2)

    with col2:
        if year == 2022:
            drivers_1 = st.selectbox("Select the 1st driver:", drivers_2022, key=22345678)
        elif year == 2023:
            drivers_1 = st.selectbox("Select the 1st driver:", drivers_2023, key=22345678)

    with col23:
        if year == 2022 and drivers_1 != "Select a driver":
            drivers_2 = st.selectbox("Select the 2nd driver", drivers_2022, key=33456789)
        elif year == 2023 and drivers_1 != "Select a driver":
            drivers_2 = st.selectbox("Select the 2nd driver", drivers_2023, key=33456789)

    with col3:
        if year == 2022 and drivers_1 != "Select a driver" and drivers_2 != "Select a driver":
            races = st.selectbox("Select the race:", races_2022, key=34567890)
            races_years = races_2022
        elif year == 2023 and drivers_1 != "Select a driver" and drivers_2 != "Select a driver":
            races = st.selectbox("Select the race:", races_2023, key=34567890)
            races_years = races_2023
            
    if year != "Select Year" and drivers_1 != "Select a driver" and drivers_2 != "Select a driver" and races != "Select a GP":
        st.info('The first time a session is uploaded it may take a few minutes as there is a lot of data, you can see the upload status on the top right hand side of the screen.', icon="ℹ️")
        
        session = fastf1.get_session(year, races_years[races], "R")
        session.load()
        driver_ls = [drivers_1, drivers_2]
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">{drivers_1} vs {drivers_2} position evolution in the {session.event.year} {session.event["EventName"]}</p>', unsafe_allow_html=True)
        st.write("This graph shows the position of the drivers during the whole race.")
        race_position(driver_ls, session, drivers_1, drivers_2)
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">{drivers_1} vs {drivers_2} Laptimes in the {session.event.year} {session.event["EventName"]}</p>', unsafe_allow_html=True)
        st.write("This graph shows the drivers' lap times during the whole race.")
        driver_LapTimes(session, drivers_1, drivers_2)
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">Delta Time vs. Distance on the race</p>', unsafe_allow_html=True)
        st.write(f"This graph shows the drivers' gap between them during the whole race, if the delta is greater than 0 it means that {drivers_2} is ahead and if the delta is lower than 0 it means that {drivers_1} is ahead.")
        delta_race(session, drivers_1, drivers_2)
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">{drivers_1} vs {drivers_2} Tyre strategy in the {session.event.year} {session.event["EventName"]}</p>', unsafe_allow_html=True)
        st.write("This graph shows the drivers' tyre strategies during the whole race.")
        tyre_strategy(session, drivers_1, drivers_2)
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">Fastest Lap Comparison {session.event["EventName"]} {session.event.year}</p>', unsafe_allow_html=True)
        st.write("This graph shows the drivers' speed in their fastest lap on the race.")
        speed(session, drivers_1, drivers_2)
        
        st.markdown('<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">Delta Time vs. Distance on the best lap</p>', unsafe_allow_html=True)
        st.write("This graph shows the drivers' delta difference between them on its fastest lap during the race.")
        delta_times(session, drivers_1, drivers_2)
        
with tab3:
    col1, col2, col23, col3 = st.columns([1,1,2,0.1])

    with col1:
        year = st.selectbox('Select the year:', years, key=165464)
    
    with col2:
        if year == 2022:
            races = st.selectbox("Select the race:", races_2022, key=45678)
            races_years = races_2022
        elif year == 2023:
            races = st.selectbox("Select the race:", races_2023, key=456123)
            races_years = races_2023
    
    if year != "Select Year" and races != "Select a GP":
        with col23:
            st.info('The first time a session is uploaded it may take a few minutes as there is a lot of data, you can see the upload status on the top right hand side of the screen.', icon="ℹ️")
        
        qualy = fastf1.get_session(year, races_years[races], "Q")
        qualy.load(telemetry=True)
        
        Q3, Q3_laps, Q2, Q2_laps, Q1, Q1_laps = qualy_results(qualy)
        
        st.write("")
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">{qualy.event["EventName"]} {qualy.event.year} Qualifying results</p>', unsafe_allow_html=True)
        st.write("In this part you can find the Qualy result divided in 3 parts, you will also find the best lap times of each driver.")
        
        co1, co2, co3 = st.columns(3)
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with co1:
            st.markdown(f'<p style="font-size: 20px;font-weight: bold; margin-top: 10px; margin-bottom: 5px; text-align: center">Q3 results</p>', unsafe_allow_html=True)
            
        with co2:
            st.markdown(f'<p style="font-size: 20px;font-weight: bold; margin-top: 10px; margin-bottom: 5px; text-align: center">Eliminated from Q2</p>', unsafe_allow_html=True)
        
        with co3:
            st.markdown(f'<p style="font-size: 20px;font-weight: bold; margin-top: 10px; margin-bottom: 5px; text-align: center">Eliminated from Q1</p>', unsafe_allow_html=True)
        
        with c1:
            for i in range(0, len(Q3)):
                st.success(f"{i + 1} - {Q3[i]}")
         
        with c2:
            for i in range(0, len(Q3)):
                st.success(Q3_laps[i])
        
        with c3:
            for i in range(0, len(Q2)):
                st.warning(f"{i + 11} - {Q2[i]}")
         
        with c4:
            for i in range(0, len(Q2)):
                st.warning(Q2_laps[i])
                
        with c5:
            for i in range(0, len(Q1)):
                st.error(f"{i + 16} - {Q1[i]}")
         
        with c6:
            for i in range(0, len(Q1)):
                st.error(Q1_laps[i])
        
        st.write("")
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">{qualy.event["EventName"]} {qualy.event.year} Qualifying drivers gap to Fastest Lap: {Q3_laps[0]} - ({Q3[0][:3]})</p>', unsafe_allow_html=True)
        st.write("In this graph you will find the time difference between the drivers and the pole position expressed in seconds, the drivers are sorted in order of classification. If the time difference to pole exceeds 6 seconds, it will not be displayed on the chart.")
        qualy_result_graph(qualy)
        
        st.markdown(f'<p style="font-size: 16px;font-weight: bold; margin-bottom: 0px;">{qualy.event["EventName"]} {qualy.event.year} best lap of top 10 drivers comparison</p>', unsafe_allow_html=True)
        st.write("In this graph you can see the best Q3 lap times of the drivers who made it through. To see it better, you can filter by driver by double clicking on the legend and then clicking on the driver you want to compare it with. It works the same for all charts.")
        qualy_lap_comp(qualy)
