from textblob import TextBlob


def calculate_growth_score(
    productivity,
    study_hours,
    sleep,
    energy,
    opportunities_got,
    opportunities_missed
):

    score = (
        productivity * 0.30 +
        study_hours * 0.20 +
        sleep * 0.10 +
        energy * 0.20 +
        opportunities_got * 10 -
        opportunities_missed * 5
    )

    return round(score, 2)


def analyze_sentiment(notes):

    analysis = TextBlob(notes)

    return analysis.sentiment.polarity