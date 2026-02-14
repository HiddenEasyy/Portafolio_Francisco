# src/pages/3_Peso.py
def render(weight_df, user_id=None):
    import streamlit as st
    import plotly.express as px
    st.header("Peso (página dedicada)")
    if weight_df.empty:
        st.info("No hay registros de peso.")
        return
    df = weight_df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    if 'WeightKg' in df.columns:
        st.plotly_chart(px.line(df, x='Date', y='WeightKg', title='Peso (kg)'), use_container_width=True)
    if 'BMI' in df.columns:
        st.plotly_chart(px.line(df, x='Date', y='BMI', title='IMC'), use_container_width=True)
