# src/components/kpi_cards.py
import streamlit as st
import numpy as np

def show_kpi_cards(activity_df, sleep_df, weight_df, user_id=None):
    """
    Muestra 4 KPI cards: pasos promedio, min activos promedio, horas de sueño promedio, peso actual/promedio.
    """
    # Defensive defaults
    pasos = int(activity_df["TotalSteps"].mean()) if (not activity_df.empty and "TotalSteps" in activity_df.columns) else 0
    # active minutes: try common columns
    active_cols = [c for c in activity_df.columns if 'Active' in c and 'Minutes' in c]
    if not active_cols and 'VeryActiveMinutes' in activity_df.columns:
        vigorous = activity_df.get('VeryActiveMinutes', 0).fillna(0)
        fairly = activity_df.get('FairlyActiveMinutes', 0).fillna(0)
        active_minutes_avg = int((vigorous + fairly).mean())
    elif active_cols:
        active_minutes_avg = int(activity_df[active_cols[0]].mean())
    else:
        active_minutes_avg = 0

    # Sleep: hours average
    if (not sleep_df.empty) and 'TotalMinutesAsleep' in sleep_df.columns:
        sleep_hours_avg = round(float(sleep_df['TotalMinutesAsleep'].mean() / 60), 1)
    else:
        sleep_hours_avg = 0.0

    # Weight: latest if exists else average
    weight_val = None
    if not weight_df.empty:
        if 'WeightKg' in weight_df.columns:
            # get latest non-null weight
            w = weight_df['WeightKg'].dropna()
            if not w.empty:
                weight_val = round(float(w.iloc[-1]), 1)
            else:
                weight_val = round(float(weight_df['WeightKg'].mean()), 1)
    if weight_val is None:
        weight_val_display = "N/A"
    else:
        weight_val_display = f"{weight_val} kg"

    # Layout
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pasos (promedio)", f"{pasos:,}")
    c2.metric("Minutos activos (prom.)", f"{active_minutes_avg}")
    c3.metric("Horas de sueño (prom.)", f"{sleep_hours_avg}")
    c4.metric("Peso (último / prom.)", weight_val_display)
