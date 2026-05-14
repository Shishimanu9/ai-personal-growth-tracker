import pandas as pd
import plotly.express as px


def create_dataframe(rows):

    columns = [
        "id",
        "date",
        "mood",
        "energy",
        "productivity",
        "sleep",
        "study_hours",
        "workout",
        "health",
        "opportunities_got",
        "opportunities_missed",
        "notes",
        "growth_score"
    ]

    df = pd.DataFrame(rows, columns=columns)

    return df


def growth_chart(df):

    fig = px.line(
        df,
        x="date",
        y="growth_score",
        title="Growth Progress 2026"
    )

    return fig


def mood_chart(df):

    mood_counts = df["mood"].value_counts().reset_index()

    mood_counts.columns = ["mood", "count"]

    fig = px.pie(
        mood_counts,
        names="mood",
        values="count",
        title="Mood Distribution"
    )

    return fig