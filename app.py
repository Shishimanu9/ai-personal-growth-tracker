import streamlit as st
import plotly.express as px
from datetime import date
from streamlit_option_menu import option_menu

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
    get_low_days
)

from ml_model import (
    analyze_sentiment,
    generate_ai_advice
)

st.set_page_config(
    page_title="AI Personal Growth Tracker 2026",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_table()

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
    color: white;
}
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f12 0%, #14532d 60%, #052e16 100%);
    border-right: 1px solid rgba(74,222,128,0.2);
    box-shadow: 4px 0 24px rgba(0,0,0,0.5);
}
section[data-testid="stSidebar"] * { color: #dcfce7 !important; }
section[data-testid="stSidebar"] h2 { color: #4ade80 !important; text-shadow: 0 0 12px rgba(74,222,128,0.5); }
section[data-testid="stSidebar"] .nav-link {
    border-radius: 12px !important;
    margin: 4px 8px !important;
    transition: all 0.25s ease !important;
    border: 1px solid transparent !important;
}
section[data-testid="stSidebar"] .nav-link:hover {
    background: rgba(74,222,128,0.15) !important;
    border: 1px solid rgba(74,222,128,0.35) !important;
    transform: translateX(5px) !important;
    box-shadow: 0 4px 14px rgba(74,222,128,0.25) !important;
}
section[data-testid="stSidebar"] .nav-link-selected {
    background: linear-gradient(90deg, rgba(74,222,128,0.3), rgba(34,197,94,0.15)) !important;
    border: 1px solid rgba(74,222,128,0.5) !important;
    box-shadow: 0 4px 18px rgba(74,222,128,0.3) !important;
}

/* ── Titles ── */
.big-title { font-size: 48px; font-weight: 900; color: #c4b5fd; margin-bottom: 10px; }

/* ── Hero ── */
.hero-section {
    padding: 35px; border-radius: 24px;
    background: linear-gradient(135deg, #312e81, #581c87);
    color: white; margin-bottom: 25px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* ── Metric Cards ── */
.metric-card {
    background: rgba(255,255,255,0.05); backdrop-filter: blur(12px);
    padding: 25px; border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center; box-shadow: 0 8px 30px rgba(0,0,0,0.25); margin-bottom: 20px;
}
.metric-card h3 { color: #cbd5e1; font-size: 16px; margin-bottom: 8px; }
.metric-card h1 { color: white; font-size: 38px; font-weight: 800; }

/* ── Insight Box ── */
.insight-box {
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
    padding: 18px; border-radius: 18px; margin-bottom: 14px; color: white;
}

/* ── Buttons ── */
.stButton>button {
    width: 100%; background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white; border-radius: 14px; border: none; padding: 14px;
    font-size: 16px; font-weight: 700;
}

/* ── Inputs ── */
.stTextInput input, .stNumberInput input, textarea, .stDateInput input {
    background-color: #1e293b !important; color: white !important; border-radius: 12px !important;
}
[data-testid="stDataFrame"] { border-radius: 18px; overflow: hidden; }
.stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; }
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
    padding: 15px; border-radius: 18px;
}

/* ── Snowfall canvas ── */
#snowCanvas {
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none; z-index: 0;
}
</style>

<!-- Snowfall animation -->
<canvas id="snowCanvas"></canvas>
<script>
(function() {
    const canvas = document.getElementById('snowCanvas');
    const ctx = canvas.getContext('2d');
    let W = window.innerWidth, H = window.innerHeight;
    canvas.width = W; canvas.height = H;
    window.addEventListener('resize', () => {
        W = window.innerWidth; H = window.innerHeight;
        canvas.width = W; canvas.height = H;
    });
    const flakes = Array.from({length: 80}, () => ({
        x: Math.random() * W,
        y: Math.random() * H,
        r: Math.random() * 3 + 1,
        speed: Math.random() * 0.8 + 0.3,
        wind: Math.random() * 0.4 - 0.2,
        opacity: Math.random() * 0.5 + 0.1
    }));
    function draw() {
        ctx.clearRect(0, 0, W, H);
        flakes.forEach(f => {
            ctx.beginPath();
            ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255,255,255,${f.opacity})`;
            ctx.fill();
            f.y += f.speed;
            f.x += f.wind;
            if (f.y > H) { f.y = -f.r; f.x = Math.random() * W; }
            if (f.x > W) f.x = 0;
            if (f.x < 0) f.x = W;
        });
        requestAnimationFrame(draw);
    }
    draw();
})();
</script>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-section"><div class="big-title">AI Personal Growth Tracker 2026</div><p style="font-size:18px;color:#e2e8f0;margin-top:10px;line-height:1.7;">Track mood, productivity, health, opportunities, and AI-powered behavioral growth patterns.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🧠 Navigation")
    menu = option_menu(
        menu_title=None,
        options=["Daily Entry", "Dashboard", "AI Insights", "Year Summary"],
        icons=["pencil-fill", "bar-chart-fill", "robot", "calendar-check-fill"],
        default_index=0,
        styles={
            "container": {"background-color": "transparent"},
            "icon": {"color": "#4ade80", "font-size": "16px"},
            "nav-link": {"color": "#dcfce7", "font-size": "15px", "font-weight": "600"},
            "nav-link-selected": {"color": "white", "font-weight": "800"},
        }
    )

rows = fetch_entries()
df = create_dataframe(rows)

# ─────────────────────────────────────────────────────────────
# DAILY ENTRY
# ─────────────────────────────────────────────────────────────

if menu == "Daily Entry":
    st.subheader("📝 Daily Entry")
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("entry_form"):
        entry_date = st.date_input("Date", date.today())
        col1, col2, col3 = st.columns(3)
        with col1:
            mood = st.slider("Mood", 1, 10, 5)
            energy = st.slider("Energy", 1, 10, 5)
            productivity = st.slider("Productivity", 1, 10, 5)
        with col2:
            sleep_hours = st.number_input("Sleep Hours", 0.0, 14.0, 7.0)
            study_hours = st.number_input("Study / Work Hours", 0.0, 16.0, 4.0)
            workout = st.checkbox("Workout Done?")
        with col3:
            health_status = st.selectbox("Health Status", ["Healthy", "Sick", "Tired", "Stressed"])
            opportunities_gained = st.number_input("Opportunities Gained", 0, 20, 0)
            opportunities_missed = st.number_input("Opportunities Missed", 0, 20, 0)
        notes = st.text_area("Personal Notes")
        golden_day = st.checkbox("✨ Mark this as a Golden Day", value=False)
        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("🚀 Save Entry")
        if submit:
            growth_score = calculate_growth_score(
                mood, energy, productivity, sleep_hours, study_hours,
                int(workout), opportunities_gained, opportunities_missed
            )
            insert_entry((
                str(entry_date), mood, energy, productivity, sleep_hours,
                study_hours, int(workout), health_status,
                opportunities_gained, opportunities_missed,
                notes, int(golden_day), growth_score
            ))
            st.success(f"✅ Entry saved successfully. Growth Score: {growth_score}/10")

# ─────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────

elif menu == "Dashboard":
    st.subheader("📊 Dashboard Analytics")
    st.markdown("<br>", unsafe_allow_html=True)
    if df.empty:
        st.warning("No data found. Add daily entries first.")
    else:
        total_entries = len(df)
        coverage_percent = (total_entries / 365) * 100
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><h3>Avg Growth Score</h3><h1>{round(df["growth_score"].mean(),2)}</h1></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><h3>Days Tracked</h3><h1>{total_entries}</h1></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><h3>Year Coverage</h3><h1>{coverage_percent:.1f}%</h1></div>', unsafe_allow_html=True)
        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric("🔥 Avg Productivity", round(df["productivity"].mean(), 2))
        with col5:
            st.metric("⚡ Avg Energy", round(df["energy"].mean(), 2))
        with col6:
            st.metric("😴 Avg Sleep", round(df["sleep_hours"].mean(), 2))
        st.markdown("<br>", unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["📈 Graphs", "📋 Entries", "🧠 Analysis"])
        with tab1:
            for title, fig_obj in [
                ("📈 Growth Progression", px.line(df, x="date", y="growth_score", markers=True)),
                ("😐 Mood Distribution", px.histogram(df, x="mood", nbins=10)),
                ("🔥 Productivity vs Sleep", px.scatter(df, x="sleep_hours", y="productivity", size="growth_score", color="growth_score", hover_data=["date"], opacity=0.7)),
                ("📅 Weekday Performance", px.bar(df.groupby("weekday")["growth_score"].mean().reset_index(), x="weekday", y="growth_score")),
            ]:
                st.subheader(title)
                fig_obj.update_layout(template="plotly_dark", paper_bgcolor="#111827", plot_bgcolor="#111827", font=dict(color="white"))
                st.plotly_chart(fig_obj, use_container_width=True)
        with tab2:
            st.subheader("📋 Daily Entries Log")
            display_df = df[["date","mood","energy","productivity","sleep_hours","study_hours","growth_score","health_status"]].copy()
            display_df.columns = ["Date","Mood","Energy","Productivity","Sleep","Study","Growth Score","Health"]
            st.dataframe(display_df.sort_values("Date", ascending=False), use_container_width=True, height=500)
        with tab3:
            st.info("Your analytics and growth patterns are improving over time.")

# ─────────────────────────────────────────────────────────────
# AI INSIGHTS
# ─────────────────────────────────────────────────────────────

elif menu == "AI Insights":
    st.subheader("🧠 AI Behavioral Insights")
    if df.empty:
        st.warning("No data available.")
    else:
        with st.spinner("Generating AI insights..."):
            latest_note = df.iloc[-1]["notes"]
            sentiment, polarity = analyze_sentiment(latest_note)
            burnout_risk = detect_burnout_risk(df)
            predicted_score = predict_next_growth(df)
        col1, col2, col3 = st.columns(3)
        col1.metric("😊 Latest Note Sentiment", sentiment)
        col2.metric("⚠️ Burnout Risk", burnout_risk)
        col3.metric("📈 Predicted Next Growth", predicted_score if predicted_score else "Need more data")
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🧠 AI Pattern Insights")
        for insight in generate_behavior_insights(df):
            st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)
        st.subheader("🔴 Your Low Days")
        low_days = get_low_days(df)
        if low_days.empty:
            st.success("No low days found.")
        else:
            for _, row in low_days.iterrows():
                score = row["growth_score"]
                day_date = row["date"].date()
                mood = row["mood"]
                energy = row["energy"]
                notes = row["notes"] if row["notes"] else "No notes written."
                st.markdown(f'<div style="background:#1e293b;border-left:4px solid #ff4d6d;border-radius:18px;padding:18px;margin-bottom:14px;color:white;"><h4>📅 {day_date}</h4><p>Growth Score: <b>{score}/10</b></p><p>Mood: {mood}/10 | Energy: {energy}/10</p><p>"{notes}"</p></div>', unsafe_allow_html=True)
        st.subheader("💡 AI Recommendations")
        for advice in generate_ai_advice(sentiment, burnout_risk, predicted_score):
            st.info(advice)

# ─────────────────────────────────────────────────────────────
# YEAR SUMMARY
# ─────────────────────────────────────────────────────────────

elif menu == "Year Summary":
    st.subheader("📅 Your Yearly Growth Journey")
    if df.empty:
        st.warning("No data available.")
    else:
        generate_year_calendar(df)
        st.markdown("---")
        render_yearly_growth_graph(df)