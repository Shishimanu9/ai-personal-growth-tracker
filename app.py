import streamlit as st
import plotly.express as px
from datetime import date

from yearly_report import (
    generate_year_calendar,
    render_yearly_growth_graph
)

from database import (
    create_table,
    insert_entry,
    fetch_entries
)

from analytics import (
    calculate_growth_score,
    create_dataframe,
    generate_behavior_insights,
    detect_burnout_risk,
    predict_next_growth,
    get_low_days          # ← add this line
)

from ml_model import (
    analyze_sentiment,
    generate_ai_advice
)


# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Personal Growth Tracker 2026",
    layout="wide"
)

create_table()


# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.metric-card {
    padding: 20px;
    border-radius: 18px;
    background: linear-gradient(135deg, #1e293b, #334155);
    color: white;
    text-align: center;
}

.big-title {
    font-size: 38px;
    font-weight: 800;
}

.insight-box {
    padding: 18px;
    border-radius: 14px;
    background-color: #1e293b;
    color: white;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────

st.markdown(
    "<div class='big-title'>AI Personal Growth Tracker 2026</div>",
    unsafe_allow_html=True
)

st.write(
    "Track mood, productivity, health, opportunities, and AI-based behavior patterns."
)


# ─────────────────────────────────────────────────────────────
# SIDEBAR MENU
# ─────────────────────────────────────────────────────────────

menu = st.sidebar.radio(
    "Navigation",
    [
        "Daily Entry",
        "Dashboard",
        "AI Insights",
        "Year Summary"
    ]
)


# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────

rows = fetch_entries()
df = create_dataframe(rows)


# ─────────────────────────────────────────────────────────────
# DAILY ENTRY PAGE
# ─────────────────────────────────────────────────────────────

if menu == "Daily Entry":

    st.header("Daily Entry")

    with st.form("entry_form"):

        entry_date = st.date_input(
            "Date",
            date.today()
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            mood = st.slider(
                "Mood",
                1,
                10,
                5
            )

            energy = st.slider(
                "Energy",
                1,
                10,
                5
            )

            productivity = st.slider(
                "Productivity",
                1,
                10,
                5
            )

        with col2:

            sleep_hours = st.number_input(
                "Sleep Hours",
                0.0,
                14.0,
                7.0
            )

            study_hours = st.number_input(
                "Study / Work Hours",
                0.0,
                16.0,
                4.0
            )

            workout = st.checkbox(
                "Workout Done?"
            )

        with col3:

            health_status = st.selectbox(
                "Health Status",
                [
                    "Healthy",
                    "Sick",
                    "Tired",
                    "Stressed"
                ]
            )

            opportunities_gained = st.number_input(
                "Opportunities Gained",
                0,
                20,
                0
            )

            opportunities_missed = st.number_input(
                "Opportunities Missed",
                0,
                20,
                0
            )

        notes = st.text_area(
            "Personal Notes"
        )
        golden_day = st.checkbox(
             " Mark this as a Golden Day", value=False)

        submit = st.form_submit_button(
            "Save Entry"
        )

        if submit:

            growth_score = calculate_growth_score(
                mood,
                energy,
                productivity,
                sleep_hours,
                study_hours,
                int(workout),
                opportunities_gained,
                opportunities_missed
            )

            insert_entry((
                str(entry_date),
                mood,
                energy,
                productivity,
                sleep_hours,
                study_hours,
                int(workout),
                health_status,
                opportunities_gained,
                opportunities_missed,
                notes,
                int(golden_day),
                growth_score
            ))

            st.success(
                f"Entry saved. Growth Score: {growth_score}/10"
            )


# ─────────────────────────────────────────────────────────────
# DASHBOARD PAGE
# ─────────────────────────────────────────────────────────────

elif menu == "Dashboard":

    st.header("Dashboard Analytics")

    if df.empty:

        st.warning(
            "No data found. Add daily entries first."
        )

    else:

        total_entries = len(df)

        coverage_percent = (
            total_entries / 365
        ) * 100

        # TOP METRICS

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Avg Growth Score",
            round(
                df["growth_score"].mean(),
                2
            )
        )

        col2.metric(
            "Days Tracked",
            total_entries
        )

        col3.metric(
            "Year Coverage",
            f"{coverage_percent:.1f}%"
        )

        st.markdown("")

        # SECONDARY METRICS

        col4, col5, col6 = st.columns(3)

        col4.metric(
            "Avg Productivity",
            round(
                df["productivity"].mean(),
                2
            )
        )

        col5.metric(
            "Avg Energy",
            round(
                df["energy"].mean(),
                2
            )
        )

        col6.metric(
            "Avg Sleep",
            round(
                df["sleep_hours"].mean(),
                2
            )
        )

        # GROWTH GRAPH

        st.subheader(
            "Growth Progression"
        )

        fig = px.line(
            df,
            x="date",
            y="growth_score",
            markers=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # DAILY ENTRIES TABLE

        st.subheader(
            "📋 Daily Entries Log"
        )

        display_df = df[[
            "date",
            "mood",
            "energy",
            "productivity",
            "sleep_hours",
            "study_hours",
            "growth_score",
            "health_status"
        ]].copy()

        display_df.columns = [
            "Date",
            "Mood",
            "Energy",
            "Productivity",
            "Sleep",
            "Study",
            "Growth Score",
            "Health"
        ]

        display_df = display_df.sort_values(
            by="Date",
            ascending=False
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            height=500
        )

        # MOOD DISTRIBUTION

        st.subheader(
            "Mood Distribution"
        )

        fig2 = px.histogram(
            df,
            x="mood",
            nbins=10
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # PRODUCTIVITY VS SLEEP

        st.subheader(
            "Productivity vs Sleep"
        )

        fig3 = px.scatter(
            df,
            x="sleep_hours",
            y="productivity",
            size="growth_score",
            color="growth_score",
            hover_data=["date"]
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # WEEKDAY PERFORMANCE

        st.subheader(
            "Weekday Performance"
        )

        weekday_avg = (
            df.groupby("weekday")["growth_score"]
            .mean()
            .reset_index()
        )

        fig4 = px.bar(
            weekday_avg,
            x="weekday",
            y="growth_score"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )


# ─────────────────────────────────────────────────────────────
# AI INSIGHTS PAGE
# ─────────────────────────────────────────────────────────────

# This is just the AI Insights section — paste this into your app.py
# replacing the existing "elif menu == AI Insights" block

elif menu == "AI Insights":

    st.header("AI Behavioral Insights")

    if df.empty:
        st.warning("No data available.")

    else:
        latest_note = df.iloc[-1]["notes"]
        sentiment, polarity = analyze_sentiment(latest_note)
        burnout_risk = detect_burnout_risk(df)
        predicted_score = predict_next_growth(df)

        col1, col2, col3 = st.columns(3)
        col1.metric("Latest Note Sentiment", sentiment)
        col2.metric("Burnout Risk", burnout_risk)
        col3.metric("Predicted Next Growth", predicted_score if predicted_score else "Need more data")

        # ── Pattern Insights ──────────────────────────────────
        st.subheader("🧠 AI Pattern Insights")
        insights = generate_behavior_insights(df)
        for insight in insights:
            st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)

        # ── Low Days — the days you were struggling ───────────
        st.subheader("🔴 Your Low Days — When You Were Struggling")

        low_days = get_low_days(df)

        if low_days.empty:
            st.success("No low days found. You've been doing great!")
        else:
            st.markdown(
                f"<div class='insight-box'>You had <b>{len(low_days)}</b> low day(s) this year "
                f"(growth score below 4). Here's what those days looked like:</div>",
                unsafe_allow_html=True
            )

            for _, row in low_days.iterrows():
                score = row["growth_score"]
                day_date = row["date"].date()
                mood = row["mood"]
                energy = row["energy"]
                notes = row["notes"] if row["notes"] else "No notes written."

                # Color the card by how bad the day was
                if score < 2:
                    border_color = "#FF3333"
                    label = "Very Hard Day"
                else:
                    border_color = "#FF6B6B"
                    label = "Low Day"

                st.markdown(f"""
                <div style="
                    background:#1e293b;
                    border-left: 4px solid {border_color};
                    border-radius: 12px;
                    padding: 16px 20px;
                    margin-bottom: 12px;
                    color: white;
                ">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-size:16px; font-weight:800;">📅 {day_date}</span>
                        <span style="background:{border_color}; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:700;">{label} — Score: {score}/10</span>
                    </div>
                    <div style="display:flex; gap:20px; font-size:13px; color:#94a3b8; margin-bottom:8px;">
                        <span>😐 Mood: <b style="color:white;">{mood}/10</b></span>
                        <span>⚡ Energy: <b style="color:white;">{energy}/10</b></span>
                    </div>
                    <div style="font-size:13px; color:#cbd5e1; font-style:italic;">"{notes}"</div>
                </div>
                """, unsafe_allow_html=True)

            # What caused the low days — quick pattern
            avg_mood_low = low_days["mood"].mean()
            avg_energy_low = low_days["energy"].mean()
            avg_sleep_low = low_days["sleep_hours"].mean()

            st.markdown(f"""
            <div class='insight-box'>
                <b>Pattern on your low days:</b><br>
                Average Mood: {avg_mood_low:.1f}/10 &nbsp;|&nbsp;
                Average Energy: {avg_energy_low:.1f}/10 &nbsp;|&nbsp;
                Average Sleep: {avg_sleep_low:.1f} hrs
            </div>
            """, unsafe_allow_html=True)

        # ── AI Recommendations ────────────────────────────────
        st.subheader("💡 AI Recommendations")
        advice_list = generate_ai_advice(sentiment, burnout_risk, predicted_score)
        for advice in advice_list:
            st.info(advice)


# ─────────────────────────────────────────────────────────────
# YEAR SUMMARY PAGE
# ─────────────────────────────────────────────────────────────

elif menu == "Year Summary":

    st.header(
        "Your Yearly Growth Journey"
    )

    if df.empty:

        st.warning(
            "No data available."
        )

    else:

        generate_year_calendar(df)

        st.markdown("---")

        render_yearly_growth_graph(df)