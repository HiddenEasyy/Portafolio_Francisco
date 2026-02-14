# src/pages/2_Sueno.py
def render(sleep_df, user_id=None):
    import streamlit as st
    from components.charts import plot_sleep_bar
    st.header("Sueño (página dedicada)")
    plot_sleep_bar(sleep_df, user_id=user_id)
