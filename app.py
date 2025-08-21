import streamlit as st
from datetime import datetime, timedelta

if "meet_name" not in st.session_state:
    st.session_state.meet_name = ""
if "meet_date" not in st.session_state:
    st.session_state.meet_date = None
if "days" not in st.session_state:
    st.session_state.days = {}
if "events" not in st.session_state:
    st.session_state.events = {}

st.title("🏊 Swimming Meet Scheduler")

st.header("Create a Swimming Meet")
st.session_state.meet_name = st.text_input("Meet Name", value=st.session_state.meet_name)
st.session_state.meet_date = st.date_input("Meet Start Date", value=datetime.today())

st.header("Add Days to the Meet")
new_day = st.date_input("Select a Day to Add", value=st.session_state.meet_date)
if st.button("Add Day"):
    day_str = new_day.strftime("%Y-%m-%d")
    if day_str not in st.session_state.days:
        st.session_state.days[day_str] = []
        st.success(f"Added Day: {day_str}")
    else:
        st.warning("Day already added.")

st.header("Add Events")
if st.session_state.days:
    selected_day = st.selectbox("Select Day", list(st.session_state.days.keys()))
    event_name = st.text_input("Event Name")
    num_heats = st.number_input("Number of Heats", min_value=1, value=1)
    heat_duration = st.number_input("Duration per Heat (minutes)", min_value=1, value=2)
    start_time_str = st.text_input("Start Time (HH:MM)", value="10:00")
    break_duration = st.number_input("Break Duration After Event (minutes)", min_value=0, value=0)

    if st.button("Add Event"):
        try:
            start_time = datetime.strptime(start_time_str, "%H:%M")
            event = {
                "name": event_name,
                "num_heats": num_heats,
                "heat_duration": heat_duration,
                "start_time": start_time,
                "break_duration": break_duration
            }
            st.session_state.days[selected_day].append(event)
            st.success(f"Added Event: {event_name} to {selected_day}")
        except ValueError:
            st.error("Invalid start time format. Use HH:MM.")

st.header("Meet Schedule")
for day, events in st.session_state.days.items():
    st.subheader(f"📅 {day}")
    current_time = None
    for idx, event in enumerate(events):
        if idx == 0:
            current_time = event["start_time"]
        else:
            current_time += timedelta(minutes=events[idx - 1]["num_heats"] * events[idx - 1]["heat_duration"] + events[idx - 1]["break_duration"])
            event["start_time"] = current_time

        st.markdown(f"**Event:** {event['name']}")
        for heat_num in range(event["num_heats"]):
            heat_time = event["start_time"] + timedelta(minutes=heat_num * event["heat_duration"])
            st.write(f"Heat {heat_num + 1}: {heat_time.strftime('%H:%M')}")
        if event["break_duration"] > 0:
            break_time = event["start_time"] + timedelta(minutes=event["num_heats"] * event["heat_duration"])
            st.write(f"Break: {event['break_duration']} minutes starting at {break_time.strftime('%H:%M')}")
