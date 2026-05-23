import pandas as pd
import numpy as np

def calculate_growth_score(mood, energy, productivity, sleep, study, workout, gained, missed):

    sleep_score = min(float(sleep) / 8, 1) * 10
    study_score = min(float(study) / 6, 1) * 10
    workout_score = 10 if workout == 1 else 0

    opportunity_score = 0
    total_opp = int(gained) + int(missed)
    if total_opp > 0:
        opportunity_score = (int(gained) / total_opp) * 10

    score = (
        productivity * 0.30 +
        energy * 0.25 +
        mood * 0.20 +
        sleep_score * 0.10 +
        study_score * 0.05 +
        workout_score * 0.05 +
        opportunity_score * 0.05
    )

    return round(score, 2)


def create_dataframe(rows):
    # ✅ golden_day column added — must match DB column order
    columns = [
        "id", "date", "mood", "energy", "productivity", "sleep_hours",
        "study_hours", "workout", "health_status", "opportunities_gained",
        "opportunities_missed", "notes", "golden_day", "growth_score"
    ]

    df = pd.DataFrame(rows, columns=columns)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.month_name()
        df["weekday"] = df["date"].dt.day_name()
        df["golden_day"] = df["golden_day"].fillna(0).astype(int)

    return df


def generate_behavior_insights(df):
    insights = []

    if df.empty or len(df) < 3:
        return ["Add at least 3 entries to generate proper AI insights."]

    avg_growth = df["growth_score"].mean()
    avg_sleep = df["sleep_hours"].mean()
    avg_productivity = df["productivity"].mean()

    best_day = df.loc[df["growth_score"].idxmax()]
    insights.append(f"Your average growth score is {avg_growth:.2f}/10.")
    insights.append(f"Your best growth day was {best_day['date'].date()} with score {best_day['growth_score']}/10.")

    if avg_sleep < 6:
        insights.append("Your average sleep is low. This may be affecting your energy and productivity.")

    if avg_productivity >= 7:
        insights.append("Your productivity level is strong and consistent.")
    else:
        insights.append("Your productivity needs improvement. Try tracking what causes low-focus days.")

    workout_days = df[df["workout"] == 1]
    non_workout_days = df[df["workout"] == 0]

    if not workout_days.empty and not non_workout_days.empty:
        workout_avg = workout_days["growth_score"].mean()
        non_workout_avg = non_workout_days["growth_score"].mean()
        if workout_avg > non_workout_avg:
            diff = workout_avg - non_workout_avg
            insights.append(f"Workout days improve your growth score by around {diff:.2f} points.")

    if df["sleep_hours"].corr(df["productivity"]) > 0.3:
        insights.append("Your sleep has a positive impact on productivity.")

    missed_total = df["opportunities_missed"].sum()
    gained_total = df["opportunities_gained"].sum()
    if gained_total + missed_total > 0:
        utilization = gained_total / (gained_total + missed_total) * 100
        insights.append(f"Your opportunity utilization is {utilization:.1f}%.")

    return insights


def detect_burnout_risk(df):
    if df.empty or len(df) < 5:
        return "Not enough data"

    recent = df.tail(5)
    low_energy = recent["energy"].mean() < 5
    low_mood = recent["mood"].mean() < 5
    low_sleep = recent["sleep_hours"].mean() < 6
    low_productivity = recent["productivity"].mean() < 5

    risk_score = sum([low_energy, low_mood, low_sleep, low_productivity])

    if risk_score >= 3:
        return "High burnout risk"
    elif risk_score == 2:
        return "Medium burnout risk"
    else:
        return "Low burnout risk"


def predict_next_growth(df):
    if df.empty or len(df) < 7:
        return None

    df = df.copy()
    df["day_number"] = range(1, len(df) + 1)

    from sklearn.linear_model import LinearRegression
    X = df[["day_number"]]
    y = df["growth_score"]

    model = LinearRegression()
    model.fit(X, y)

    prediction = model.predict([[len(df) + 1]])[0]
    return round(float(prediction), 2)

# ─────────────────────────────────────────────
# LOW DAYS DETECTION
# ─────────────────────────────────────────────

def get_low_days(df):

    if df is None or df.empty:
        return pd.DataFrame()

    low = df[
        df["growth_score"] < 4
    ].copy()

    low = low.sort_values(
        by="date",
        ascending=False
    )

    return low