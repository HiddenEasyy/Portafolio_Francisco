# src/components/charts.py
import streamlit as st
import plotly.express as px
import pandas as pd

def plot_steps_time_series(activity_df, user_id=None):
    if activity_df.empty:
        if user_id:
            st.info(f"No hay datos de actividad para el usuario {user_id}.")
        else:
            st.info("No hay datos de actividad para graficar.")
        return
    
    if 'Date' not in activity_df.columns:
        st.error("Error: No se encontró la columna 'Date' en los datos de actividad.")
        return
        
    df = activity_df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    
    if user_id and 'Id' in df.columns:
        df = df[df['Id'] == str(user_id)]
        if df.empty:
            st.info(f"No se encontraron registros de actividad para el usuario {user_id}.")
            return
            
    if 'TotalSteps' not in df.columns:
        st.warning("La columna 'TotalSteps' no se encuentra en los datos. Verifica el formato del archivo.")
        return
        
    # Asegurarse de que hay datos válidos para graficar
    if df['TotalSteps'].isna().all():
        st.warning("No hay datos válidos de pasos para mostrar.")
        return
        
    fig = px.line(df, x='Date', y='TotalSteps', title='Pasos por día', markers=True)
    st.plotly_chart(fig, use_container_width=True)

def plot_sleep_bar(sleep_df, user_id=None):
    if sleep_df.empty:
        if user_id:
            st.info(f"No hay datos de sueño para el usuario {user_id}.")
        else:
            st.info("No hay datos de sueño para graficar.")
        return
        
    if 'Date' not in sleep_df.columns:
        st.error("Error: No se encontró la columna 'Date' en los datos de sueño.")
        return
        
    df = sleep_df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    
    if user_id and 'Id' in df.columns:
        df = df[df['Id'] == str(user_id)]
        if df.empty:
            st.info(f"No se encontraron registros de sueño para el usuario {user_id}.")
            return
            
    if 'TotalMinutesAsleep' not in df.columns:
        st.warning("La columna 'TotalMinutesAsleep' no se encuentra en los datos. Verifica el formato del archivo.")
        return
        
    # Asegurarse de que hay datos válidos para graficar
    if df['TotalMinutesAsleep'].isna().all():
        st.warning("No hay datos válidos de sueño para mostrar.")
        return
        
    df['HorasAsleep'] = df['TotalMinutesAsleep'] / 60
    fig = px.bar(df, x='Date', y='HorasAsleep', title='Horas de sueño por día')
    st.plotly_chart(fig, use_container_width=True)

def plot_scatter_activity_sleep(merged_df):
    if merged_df.empty:
        st.info("No hay datos combinados para correlaciones.")
        return
    # try to find columns for active minutes and sleep hours
    x_col = None
    for c in ['VeryActiveMinutes', 'FairlyActiveMinutes', 'totalMinutesAsleep', 'MinActive', 'MinutesActive']:
        if c in merged_df.columns:
            x_col = c
            break
    # better: compute approximate active minutes from VeryActive+Fairly if present
    if 'VeryActiveMinutes' in merged_df.columns and 'FairlyActiveMinutes' in merged_df.columns:
        merged_df['ActiveMinutes'] = merged_df['VeryActiveMinutes'].fillna(0) + merged_df['FairlyActiveMinutes'].fillna(0)
        x_col = 'ActiveMinutes'
    # sleep hours:
    if 'TotalMinutesAsleep' in merged_df.columns:
        merged_df['SleepHours'] = merged_df['TotalMinutesAsleep'] / 60
        y_col = 'SleepHours'
    elif 'HoursAsleep' in merged_df.columns:
        y_col = 'HoursAsleep'
    else:
        st.warning("No se encontró columna de sueño en el dataset combinado.")
        return

    if x_col is None:
        st.warning("No se encontró columna de actividad para correlación.")
        return

    fig = px.scatter(merged_df, x=x_col, y=y_col, trendline='ols', title=f'Relación: {x_col} vs {y_col}')
    st.plotly_chart(fig, use_container_width=True)
