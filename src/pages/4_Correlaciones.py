# src/pages/4_Correlaciones.py
def render(activity_df, sleep_df, user_id=None):
    import streamlit as st
    from utils.data_loader import merge_activity_sleep
    from components.charts import plot_scatter_activity_sleep
    st.header("Correlaciones")
    merged = merge_activity_sleep(activity_df, sleep_df, id=user_id if user_id else None)
    plot_scatter_activity_sleep(merged)
    st.dataframe(merged.tail(50))
