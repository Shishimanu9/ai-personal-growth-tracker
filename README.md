# AI Personal Growth Tracker 2026

## Overview

AI Personal Growth Tracker 2026 is a personal analytics and self-improvement application built using Python and Streamlit.

The application allows users to:
- Track daily emotional and productivity patterns
- Analyze growth trends
- Monitor health and energy
- Measure opportunity utilization
- Generate AI-powered behavioral insights using sentiment analysis

The system stores structured daily life data and transforms it into meaningful visual analytics and summaries.

---

# Purpose of the Project

This project was created to combine:
- Personal growth tracking
- AI-based emotional analysis
- Productivity analytics
- Behavioral pattern recognition

The goal is to help users better understand:
- Their emotional trends
- Productivity consistency
- Health impact on growth
- Opportunity utilization
- Long-term self-improvement patterns

---

# Tech Stack

## Frontend
- Python
- Streamlit

## Backend / Logic
- Python

## Database
- SQLite

## Data Processing
- Pandas
- NumPy

## Visualization
- Plotly Express

## AI / NLP
- TextBlob
- NLTK

---

# Main Features

## 1. Daily Entry System

Users can log:
- Mood
- Energy
- Productivity
- Sleep
- Study hours
- Workout status
- Health status
- Opportunities gained
- Opportunities missed
- Personal notes

The application calculates a custom Growth Score based on user activity.

---

## 2. Dashboard Analytics

Displays:
- Growth progression graph
- Mood distribution chart
- Average productivity
- Average energy
- Average growth score

---

## 3. AI Behavioral Analysis

Uses sentiment analysis on notes written by the user.

Features:
- Emotional trend detection
- Positive vs bad day comparison
- AI-generated behavioral insights
- Best growth day detection

---

## 4. Year Summary

Provides:
- Opportunity utilization percentage
- Total growth score
- Sick day count
- Best performing month
- Overall yearly life summary

---

# Project Architecture

## File Structure

```text
personal-growth-ai/
│
├── app.py
├── database.py
├── ml_model.py
├── analytics.py
├── growth_tracker.db
├── requirements.txt
├── README.md
└── .gitignore
