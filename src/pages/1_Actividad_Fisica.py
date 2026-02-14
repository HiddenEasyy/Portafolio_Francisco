# src/pages/1_Actividad_Fisica.py
"""
Formato para páginas independientes si decides usarlas.
Este archivo no se importa automáticamente por app.py (app.py usa sidebar navigation),
pero lo incluimos para mantener orden y poder convertir a multipage si quieres.
"""

def render(activity_df, user_id=None):
    from components.charts import plot_steps_time_series
    import streamlit as st
    st.header("Actividad física (página dedicada)")
    plot_steps_time_series(activity_df, user_id=user_id)
