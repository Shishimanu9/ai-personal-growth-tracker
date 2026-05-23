from textblob import TextBlob

def analyze_sentiment(note):
   if not note or note.strip() == "":
       return "Neutral", 0

   polarity = TextBlob(note).sentiment.polarity

   if polarity > 0.2:
       label = "Positive"
   elif polarity < -0.2:
       label = "Negative"
   else:
       label = "Neutral"

   return label, round(polarity, 2)


def generate_ai_advice(sentiment, burnout_risk, predicted_score):
   advice = []

   if sentiment == "Negative":
       advice.append("Your note sounds emotionally low. Try identifying the exact trigger behind today’s mood.")

   if burnout_risk == "High burnout risk":
       advice.append("You may be moving toward burnout. Reduce workload, improve sleep, and avoid overcommitting tomorrow.")

   if predicted_score is not None:
       if predicted_score >= 7:
           advice.append("Your next growth score prediction looks strong. Continue your current routine.")
       elif predicted_score < 5:
           advice.append("Your next growth score may drop. Focus on sleep, hydration, and one important task only.")

   if not advice:
       advice.append("Your current pattern looks stable. Keep logging consistently.")

   return advice
