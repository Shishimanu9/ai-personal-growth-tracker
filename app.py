import streamlit as st
import pandas as pd
from datetime import date

from database import create_table
from database import insert_entry
from database import get_all_entries

from ml_model import calculate_growth_score
from ml_model import analyze_sentiment

from analytics import create_dataframe
from analytics import growth_chart
from analytics import mood_chart

# Create database table
create_table()

# Streamlit Config
st.set_page_config(
    page_title="AI Personal Growth Tracker",
    layout="wide"
)

st.title("AI Personal Growth Tracker 2026")

# Sidebar Navigation
menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Daily Entry",
        "Dashboard",
        "AI Analysis",
        "Year Summary"
    ]
)

# =========================
# DAILY ENTRY
# =========================

if menu == "Daily Entry":

    st.header("Daily Life Entry")

    entry_date = st.date_input("Date", date.today())

    mood = st.selectbox(
        "Mood",
        ["Positive", "Neutral", "Bad"]
    )

    energy = st.slider("Energy Level", 1, 10)

    productivity = st.slider("Productivity", 1, 10)

    sleep = st.slider("Sleep Hours", 0.0, 12.0, 6.0)

    study_hours = st.slider("Study Hours", 0.0, 15.0, 2.0)

    workout = st.selectbox(
        "Workout Done",
        ["Yes", "No"]
    )

    health = st.selectbox(
        "Health Status",
        ["Healthy", "Sick"]
    )

    opportunities_got = st.number_input(
        "Opportunities Got",
        min_value=0,
        max_value=100,
        value=0
    )

    opportunities_missed = st.number_input(
        "Opportunities Missed",
        min_value=0,
        max_value=100,
        value=0
    )

    notes = st.text_area("Notes")

    if st.button("Save Entry"):

        growth_score = calculate_growth_score(
            productivity,
            study_hours,
            sleep,
            energy,
            opportunities_got,
            opportunities_missed
        )

        data = (
            str(entry_date),
            mood,
            energy,
            productivity,
            sleep,
            study_hours,
            workout,
            health,
            opportunities_got,
            opportunities_missed,
            notes,
            growth_score
        )

        insert_entry(data)

        st.success("Entry Saved Successfully")

        st.metric("Growth Score", growth_score)

# =========================
# DASHBOARD
# =========================

elif menu == "Dashboard":

    st.header("Growth Dashboard")

    rows = get_all_entries()

    if len(rows) == 0:
        st.warning("No data available")

    else:

        df = create_dataframe(rows)

        st.dataframe(df)

        st.plotly_chart(growth_chart(df))

        st.plotly_chart(mood_chart(df))

        st.subheader("Statistics")

        avg_growth = df["growth_score"].mean()
        avg_productivity = df["productivity"].mean()
        avg_energy = df["energy"].mean()

        col1, col2, col3 = st.columns(3)

        col1.metric("Average Growth", round(avg_growth, 2))
        col2.metric("Average Productivity", round(avg_productivity, 2))
        col3.metric("Average Energy", round(avg_energy, 2))

# =========================
# AI ANALYSIS
# =========================

elif menu == "AI Analysis":

    st.header("AI Behavioral Analysis")

    rows = get_all_entries()

    if len(rows) == 0:
        st.warning("No data available")

    else:

        df = create_dataframe(rows)

        sentiments = []

        for note in df["notes"]:
            sentiments.append(analyze_sentiment(str(note)))

        df["sentiment"] = sentiments

        avg_sentiment = df["sentiment"].mean()

        st.subheader("Sentiment Score")

        st.metric("Average Sentiment", round(avg_sentiment, 2))

        positive_days = len(df[df["mood"] == "Positive"])
        bad_days = len(df[df["mood"] == "Bad"])

        st.subheader("AI Insights")

        if avg_sentiment > 0:
            st.success("Overall emotional state remained positive")
        else:
            st.error("Negative emotional trend detected")

        if positive_days > bad_days:
            st.success("You had more positive days than bad days")
        else:
            st.warning("Bad days exceeded positive days")

        best_day = df.loc[df["growth_score"].idxmax()]

        st.subheader("Best Growth Day")

        st.write(best_day)

# =========================
# YEAR SUMMARY
# =========================

elif menu == "Year Summary":

    st.header("2026 Year Summary")

    rows = get_all_entries()

    if len(rows) == 0:
        st.warning("No data available")

    else:

        df = create_dataframe(rows)

        total_opportunities = df["opportunities_got"].sum()
        total_missed = df["opportunities_missed"].sum()

        utilization = 0

        if total_opportunities + total_missed > 0:

            utilization = (
                total_opportunities /
                (total_opportunities + total_missed)
            ) * 100

        st.subheader("Opportunity Analysis")

        st.metric(
            "Opportunity Utilization %",
            round(utilization, 2)
        )

        sick_days = len(df[df["health"] == "Sick"])

        st.metric("Sick Days", sick_days)

        total_growth = df["growth_score"].sum()

        st.metric("Total Growth Score", round(total_growth, 2))

        best_month = df.groupby(
            pd.to_datetime(df["date"]).dt.month
        )["growth_score"].mean().idxmax()

        st.metric("Best Month", best_month)

        st.subheader("Life Summary")

        st.write(
            f"You captured {len(df)} days of your 2026 journey."
        )

        st.write(
            f"You utilized {round(utilization, 2)}% of your opportunities."
        )

        st.write(
            "This AI tracker monitored emotional, productivity, health, and growth patterns throughout the year."
        )