import streamlit as st
import plotly.express as px
from datetime import date
from streamlit_option_menu import option_menu

st._config.set_option("theme.primaryColor", "#22c55e")
st._config.set_option("theme.font", "sans serif")

from yearly_report import generate_year_calendar, render_yearly_growth_graph
from database import create_table, insert_entry, fetch_entries
from analytics import calculate_growth_score, create_dataframe, generate_behavior_insights, detect_burnout_risk, predict_next_growth, get_low_days
from ml_model import analyze_sentiment, generate_ai_advice

st.set_page_config(page_title="Growth Tracker", layout="wide", initial_sidebar_state="expanded")
create_table()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; }

.stApp { background-color: #0a0a0f; color: #e2e8f0; }
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2d2d3d; border-radius: 3px; }

html, body { font-size: 18px !important; }
p, li, td, th { font-size: 18px !important; line-height: 1.7 !important; }
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span, .stSlider label, .stCheckbox label, .stSelectbox label, .stNumberInput label, .stTextArea label, .stDateInput label { font-size: 18px !important; font-weight: 600 !important; color: #94a3b8 !important; }
h1 { font-size: 56px !important; font-weight: 800 !important; }
h2 { font-size: 42px !important; font-weight: 700 !important; }
h3 { font-size: 32px !important; font-weight: 700 !important; }
h4 { font-size: 24px !important; font-weight: 600 !important; }
button p { font-size: 18px !important; font-weight: 600 !important; }
.stMarkdown p { font-size: 18px !important; }
.stSlider [data-testid="stTickBarMin"], .stSlider [data-testid="stTickBarMax"] { font-size: 13px !important; color: #475569 !important; }
.stSlider [data-testid="stThumbValue"] { font-size: 14px !important; font-weight: 700 !important; color: #22c55e !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0d0d1a 0%, #120d2e 40%, #0d1020 100%);
    border-right: 1px solid rgba(139,92,246,0.15);
}
section[data-testid="stSidebar"]::before {
    content: ''; position: fixed; top: 0; left: 0; width: 260px; height: 100%;
    background: radial-gradient(ellipse at 30% 20%, rgba(109,40,217,0.18) 0%, transparent 60%), radial-gradient(ellipse at 70% 80%, rgba(139,92,246,0.1) 0%, transparent 50%);
    pointer-events: none; z-index: 0;
}
section[data-testid="stSidebar"] * { color: #ffffff !important; }
section[data-testid="stSidebar"] .nav-link { border-radius: 10px !important; margin: 3px 8px !important; font-size: 20px !important; font-weight: 400 !important; transition: all 0.2s ease !important; border: 1px solid transparent !important; padding: 11px 14px !important; }
section[data-testid="stSidebar"] .nav-link:hover { background: rgba(139,92,246,0.12) !important; color: #c4b5fd !important; border-color: rgba(139,92,246,0.25) !important; transform: translateX(3px) !important; }
section[data-testid="stSidebar"] .nav-link-selected { background: rgba(139,92,246,0.18) !important; color: #c4b5fd !important; border-color: rgba(139,92,246,0.35) !important; font-weight: 700 !important; box-shadow: inset 0 0 20px rgba(139,92,246,0.08) !important; }
section[data-testid="stSidebar"] .nav-link-selected * { color: #c4b5fd !important; }

/* ── Hero ── */
.hero { padding: 48px 44px; border-radius: 20px; background: linear-gradient(135deg, #1a0533 0%, #0f0a2e 50%, #0a0f1e 100%); border: 1px solid #2d1b69; margin-bottom: 32px; position: relative; overflow: hidden; }
.hero::before { content: ''; position: absolute; top: -80px; right: -80px; width: 350px; height: 350px; background: radial-gradient(circle, rgba(139,92,246,0.18) 0%, transparent 70%); border-radius: 50%; }
.hero-label { font-size: 12px !important; font-weight: 600 !important; letter-spacing: 0.18em; text-transform: uppercase; color: #7c3aed !important; margin-bottom: 14px; }
.hero-title { font-size: 72px !important; font-weight: 900 !important; color: #f1f5f9 !important; line-height: 1.1; margin-bottom: 14px; letter-spacing: -0.03em; }
.hero-title span { color: #a78bfa !important; }
.hero-sub { font-size: 20px !important; color: #64748b !important; font-weight: 400 !important; line-height: 1.7; max-width: 600px; }

/* ── Stat Cards ── */
.stat-card { background: #111120; border: 1px solid #1e1e30; border-radius: 16px; padding: 26px; margin-bottom: 16px; transition: border-color 0.2s ease, transform 0.2s ease; }
.stat-card:hover { border-color: #3730a3; transform: translateY(-2px); }
.stat-label { font-size: 14px !important; font-weight: 600 !important; letter-spacing: 0.12em; text-transform: uppercase; color: #475569 !important; margin-bottom: 10px; }
.stat-value { font-size: 34px !important; font-weight: 800 !important; color: #f1f5f9 !important; letter-spacing: -0.03em; line-height: 1; }
.stat-accent { color: #a78bfa !important; }

/* ── Section Headers ── */
.section-title { font-size: 14px !important; font-weight: 700 !important; letter-spacing: 0.14em; text-transform: uppercase; color: #475569 !important; margin: 36px 0 18px 0; padding-bottom: 10px; border-bottom: 1px solid #1e1e30; }

/* ── Insight Cards ── */
.insight-card { background: #111120; border: 1px solid #1e1e30; border-radius: 12px; padding: 18px 22px; margin-bottom: 10px; font-size: 18px !important; color: #94a3b8 !important; line-height: 1.7; }

/* ── Low Day Cards ── */
.low-day-card { background: #110a0a; border: 1px solid #2d1515; border-left: 3px solid #ef4444; border-radius: 12px; padding: 20px 22px; margin-bottom: 12px; }
.low-day-date { font-size: 14px !important; font-weight: 600 !important; color: #f87171 !important; margin-bottom: 8px; }
.low-day-score { font-size: 28px !important; font-weight: 800 !important; color: #f1f5f9 !important; letter-spacing: -0.03em; }
.low-day-meta { font-size: 16px !important; color: #475569 !important; margin-top: 8px; }
.low-day-notes { font-size: 16px !important; color: #64748b !important; margin-top: 10px; font-style: italic; line-height: 1.6; }

/* ── Success ── */
div[data-testid="stAlert"] p { font-size: 18px !important; font-weight: 600 !important; }

/* ── Buttons ── */
.stButton > button { background: #7c3aed; color: white !important; border: none; border-radius: 10px; padding: 13px 28px; font-size: 18px !important; font-weight: 600 !important; transition: all 0.2s ease; width: 100%; }
.stButton > button:hover { background: #6d28d9; transform: translateY(-1px); }

/* ── Inputs ── */
.stTextInput input, .stNumberInput input, textarea, .stDateInput input { background: #111120 !important; color: #e2e8f0 !important; border: 1px solid #1e1e30 !important; border-radius: 10px !important; font-size: 18px !important; }
.stSelectbox > div > div { background: #111120 !important; border: 1px solid #1e1e30 !important; border-radius: 10px !important; color: #e2e8f0 !important; font-size: 18px !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 1px solid #1e1e30; }
.stTabs [data-baseweb="tab"] { font-size: 18px !important; font-weight: 600 !important; color: #475569 !important; padding: 12px 22px; }
.stTabs [aria-selected="true"] { color: #a78bfa !important; border-bottom: 2px solid #7c3aed !important; font-weight: 700 !important; }

/* ── Native metrics ── */
[data-testid="metric-container"] { background: #111120; border: 1px solid #1e1e30; border-radius: 14px; padding: 20px; }
[data-testid="metric-container"] label { color: #475569 !important; font-size: 15px !important; letter-spacing: 0.06em; font-weight: 600 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #f1f5f9 !important; font-size: 32px !important; font-weight: 800 !important; }

[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; border: 1px solid #1e1e30; }
#snowCanvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
</style>

<canvas id="snowCanvas"></canvas>
<script>
(function() {
    const canvas = document.getElementById('snowCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W = window.innerWidth, H = window.innerHeight;
    canvas.width = W; canvas.height = H;
    window.addEventListener('resize', () => { W = window.innerWidth; H = window.innerHeight; canvas.width = W; canvas.height = H; });
    const flakes = Array.from({length: 55}, () => ({ x: Math.random() * W, y: Math.random() * H, r: Math.random() * 1.5 + 0.5, speed: Math.random() * 0.5 + 0.15, wind: Math.random() * 0.3 - 0.15, opacity: Math.random() * 0.2 + 0.04 }));
    function draw() {
        ctx.clearRect(0, 0, W, H);
        flakes.forEach(f => {
            ctx.beginPath(); ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(167,139,250,${f.opacity})`; ctx.fill();
            f.y += f.speed; f.x += f.wind;
            if (f.y > H) { f.y = -f.r; f.x = Math.random() * W; }
            if (f.x > W) f.x = 0; if (f.x < 0) f.x = W;
        });
        requestAnimationFrame(draw);
    }
    draw();
})();
</script>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><div class="hero-label">Personal Analytics</div><div class="hero-title">Your Growth,<br><span>Tracked.</span></div><div class="hero-sub">Understand your patterns, catch burnout early, and celebrate the days you showed up.</div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<p style="font-size:20px;font-weight:500;letter-spacing:0.2em;text-transform:uppercase;color:#6d28d9;margin:8px 14px 20px 14px;display:block;">Growth Tracker</p>', unsafe_allow_html=True)
    menu = option_menu(
        menu_title=None,
        options=["Daily Entry", "Dashboard", "AI Insights", "Year Summary"],
        icons=["pencil", "bar-chart", "cpu", "calendar"],
        default_index=0,
        styles={
            "container": {"background-color": "transparent", "padding": "0"},
            "icon": {"color": "#7c3aed", "font-size": "18px"},
            "nav-link": {"font-size": "20px", "font-weight": "700", "color": "#ffffff", "padding": "11px 14px"},
            "nav-link-selected": {"font-weight": "700", "color": "#c4b5fd"},
        }
    )

rows = fetch_entries()
df = create_dataframe(rows)

if menu == "Daily Entry":
    st.markdown('<div class="section-title">Log your day</div>', unsafe_allow_html=True)
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
        notes = st.text_area("Personal Notes", placeholder="How did today feel?")
        golden_day = st.checkbox("Mark this as a Golden Day", value=False)
        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("Save Entry")
        if submit:
            growth_score = calculate_growth_score(mood, energy, productivity, sleep_hours, study_hours, int(workout), opportunities_gained, opportunities_missed)
            insert_entry((str(entry_date), mood, energy, productivity, sleep_hours, study_hours, int(workout), health_status, opportunities_gained, opportunities_missed, notes, int(golden_day), growth_score))
            st.success(f"Saved. Growth Score: {growth_score} / 10")

elif menu == "Dashboard":
    if df.empty:
        st.warning("No data yet. Start with a daily entry.")
    else:
        total_entries = len(df)
        coverage_percent = (total_entries / 365) * 100
        st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="stat-card"><div class="stat-label">Avg Growth Score</div><div class="stat-value stat-accent">{round(df["growth_score"].mean(),1)}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stat-card"><div class="stat-label">Days Tracked</div><div class="stat-value">{total_entries}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="stat-card"><div class="stat-label">Year Coverage</div><div class="stat-value">{coverage_percent:.0f}%</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="stat-card"><div class="stat-label">Avg Sleep</div><div class="stat-value">{round(df["sleep_hours"].mean(),1)}h</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Analytics</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["Charts", "Entries", "Analysis"])
        with tab1:
            for title, fig_obj in [
                ("Growth over time", px.line(df, x="date", y="growth_score", markers=True)),
                ("Mood distribution", px.histogram(df, x="mood", nbins=10)),
                ("Productivity vs Sleep", px.scatter(df, x="sleep_hours", y="productivity", size="growth_score", color="growth_score", hover_data=["date"], opacity=0.8)),
                ("Weekday performance", px.bar(df.groupby("weekday")["growth_score"].mean().reset_index(), x="weekday", y="growth_score")),
            ]:
                st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
                fig_obj.update_layout(template="plotly_dark", paper_bgcolor="#111120", plot_bgcolor="#111120", font=dict(color="#94a3b8", family="Inter", size=13), margin=dict(l=0, r=0, t=10, b=0))
                st.plotly_chart(fig_obj, use_container_width=True)
        with tab2:
            display_df = df[["date","mood","energy","productivity","sleep_hours","study_hours","growth_score","health_status"]].copy()
            display_df.columns = ["Date","Mood","Energy","Productivity","Sleep","Study","Score","Health"]
            st.dataframe(display_df.sort_values("Date", ascending=False), use_container_width=True, height=500)
        with tab3:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avg Productivity", round(df["productivity"].mean(), 2))
            with col2:
                st.metric("Avg Energy", round(df["energy"].mean(), 2))
            with col3:
                st.metric("Avg Mood", round(df["mood"].mean(), 2))
            st.markdown('<div class="section-title">Behaviour patterns</div>', unsafe_allow_html=True)
            st.info("Workout days vs non-workout, sleep impact, opportunity utilization — add more entries to unlock deeper patterns.")

elif menu == "AI Insights":
    if df.empty:
        st.warning("No data available.")
    else:
        with st.spinner("Analysing your patterns..."):
            latest_note = df.iloc[-1]["notes"]
            sentiment, polarity = analyze_sentiment(latest_note)
            burnout_risk = detect_burnout_risk(df)
            predicted_score = predict_next_growth(df)
        st.markdown('<div class="section-title">At a glance</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Sentiment", sentiment)
        col2.metric("Burnout Risk", burnout_risk)
        col3.metric("Predicted Score", predicted_score if predicted_score else "Need more data")
        st.markdown('<div class="section-title">Pattern insights</div>', unsafe_allow_html=True)
        for insight in generate_behavior_insights(df):
            st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Your low days</div>', unsafe_allow_html=True)
        low_days = get_low_days(df)
        if low_days.empty:
            st.success("No low days found. You have been doing great.")
        else:
            for _, row in low_days.iterrows():
                score = row["growth_score"]
                day_date = row["date"].date()
                notes = row["notes"] if row["notes"] else "No notes written."
                st.markdown(f'<div class="low-day-card"><div class="low-day-date">{day_date}</div><div class="low-day-score">{score}<span style="font-size:16px;font-weight:400;color:#475569;"> / 10</span></div><div class="low-day-meta">Mood {row["mood"]} / 10 &nbsp;·&nbsp; Energy {row["energy"]} / 10</div><div class="low-day-notes">{notes}</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)
        for advice in generate_ai_advice(sentiment, burnout_risk, predicted_score):
            st.info(advice)

elif menu == "Year Summary":
    st.markdown('<div class="section-title">2026 at a glance</div>', unsafe_allow_html=True)
    if df.empty:
        st.warning("No data available.")
    else:
        generate_year_calendar(df)
        st.markdown("---")
        render_yearly_growth_graph(df)