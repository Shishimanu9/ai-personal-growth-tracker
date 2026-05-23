import streamlit as st
import calendar
import plotly.express as px
from datetime import date
from streamlit.components.v1 import html as st_html


def get_score_color(score):
    if score < 2:
        return "#FFB6C1"   # Very Bad Day — Baby Pink
    elif score < 4:
        return "#3B82F6"   # Low Day — Steel Blue
    elif score < 7:
        return "#8B7CF6"   # Average Day — Periwinkle Purple
    else:
        return "#2EE59D"   # Good Day — Spring Green


def generate_year_calendar(df):

    today = date.today()
    current_year = today.year

    score_map = {}
    golden_map = {}

    if df is not None and not df.empty:
        for _, row in df.iterrows():
            clean_date = str(row["date"]).split(" ")[0]
            score_map[clean_date] = row["growth_score"]
            if "golden_day" in df.columns:
                golden_map[clean_date] = int(row["golden_day"])

    # Build day cells HTML
    months_html = ""
    weekday_labels = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

    for month_num in range(1, 13):
        month_name = calendar.month_name[month_num]
        cal_obj = calendar.Calendar(firstweekday=6)
        days = list(cal_obj.itermonthdays(current_year, month_num))

        weekdays_html = "".join(f'<div class="weekday">{wd}</div>' for wd in weekday_labels)

        cells_html = ""
        for day in days:
            if day == 0:
                cells_html += '<div class="day empty"></div>'
            else:
                day_str = f"{current_year}-{month_num:02d}-{day:02d}"
                color = "#2d3f55"
                text_color = "#4a6080"

                if day_str in score_map:
                    if golden_map.get(day_str) == 1:
                        color = "#FFCC33"
                    else:
                        color = get_score_color(score_map[day_str])
                    text_color = "#ffffff"

                today_class = " today" if (today.month == month_num and today.day == day) else ""
                cells_html += f'<div class="day{today_class}" style="background:{color};color:{text_color};">{day}</div>'

        months_html += f'''
        <div class="month-card">
            <div class="month-name">{month_name}</div>
            <div class="weekday-grid">{weekdays_html}</div>
            <div class="calendar-grid">{cells_html}</div>
        </div>'''

    # Full self-contained HTML document — fixes iframe CSS isolation issue
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #0f172a; font-family: 'Segoe UI', sans-serif; padding: 20px; }}
  .planner-title {{ font-size: 28px; font-weight: 800; color: white; text-align: center; margin-bottom: 20px; }}
  .legend {{ display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; margin-bottom: 24px; }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; color: white; font-size: 12px; font-weight: 600; }}
  .legend-dot {{ width: 14px; height: 14px; border-radius: 4px; display: inline-block; flex-shrink: 0; }}
  .months-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
  .month-card {{ background: #1e293b; border-radius: 14px; padding: 14px; }}
  .month-name {{ color: white; font-size: 15px; font-weight: 800; text-align: center; margin-bottom: 8px; }}
  .weekday-grid {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px; margin-bottom: 4px; }}
  .weekday {{ color: #64748b; text-align: center; font-size: 9px; font-weight: 700; padding: 2px 0; }}
  .calendar-grid {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px; }}
  .day {{ aspect-ratio: 1; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; }}
  .empty {{ background: transparent !important; }}
  .today {{ outline: 2px solid white; outline-offset: 1px; }}
  @media(max-width: 700px) {{ .months-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
</style>
</head>
<body>
  <div class="planner-title">📅 {current_year} — Your Growth Journey</div>
  <div class="legend">
    <div class="legend-item"><span class="legend-dot" style="background:#2d3f55;"></span>No Entry</div>
    <div class="legend-item"><span class="legend-dot" style="background:#FFB6C1;"></span>Very Bad Day</div>
    <div class="legend-item"><span class="legend-dot" style="background:#3B82F6;"></span>Low Day</div>
    <div class="legend-item"><span class="legend-dot" style="background:#8B7CF6;"></span>Average Day</div>
    <div class="legend-item"><span class="legend-dot" style="background:#2EE59D;"></span>Good Day</div>
    <div class="legend-item"><span class="legend-dot" style="background:#FFCC33;"></span>Golden Memory</div>
  </div>
  <div class="months-grid">{months_html}</div>
</body>
</html>"""

    st_html(full_html, height=2300, scrolling=True)


def render_yearly_growth_graph(df):
    if df is None or df.empty:
        st.info("No data yet. Add daily entries to see your growth graph.")
        return

    st.subheader("📈 Growth Score Over the Year")
    fig = px.line(df, x="date", y="growth_score", markers=True, line_shape="spline", color_discrete_sequence=["#7c6fff"])
    fig.update_layout(
        plot_bgcolor="#1e293b",
        paper_bgcolor="#1e293b",
        font_color="white",
        xaxis=dict(gridcolor="#334155"),
        yaxis=dict(gridcolor="#334155", range=[0, 10])
    )
    st.plotly_chart(fig, use_container_width=True)