import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def format_metric(value: float, suffix: str = "") -> str:
    """Formatea valores métricos para mostrar"""
    if isinstance(value, (int, float)):
        if value >= 1000:
            return f"{value:,.0f}{suffix}"
        elif value >= 100:
            return f"{value:.1f}{suffix}"
        else:
            return f"{value:.2f}{suffix}"
    return f"{value}{suffix}"

def plot_activity_metrics(df: pd.DataFrame, user_id: str = None):
    """Gráfica de métricas de actividad"""
    if df.empty:
        st.info("No hay datos de actividad disponibles.")
        return

    # Filtrar por usuario si se especifica
    if user_id:
        df = df[df['Id'] == user_id]

    # Crear gráfica de pasos
    fig_steps = px.line(
        df, 
        x='Date', 
        y='TotalSteps',
        title='Pasos Diarios',
        labels={'TotalSteps': 'Pasos', 'Date': 'Fecha'},
        markers=True
    )
    st.plotly_chart(fig_steps, use_container_width=True)

    # Gráfica de tendencia semanal de pasos promedio
    if len(df) >= 7:
        df_semanal = df.copy()
        df_semanal['Semana'] = df_semanal['Date'].dt.to_period('W').apply(lambda r: r.start_time)
        pasos_semanal = df_semanal.groupby('Semana')['TotalSteps'].mean().reset_index()
        fig_week = px.bar(
            pasos_semanal,
            x='Semana',
            y='TotalSteps',
            title='Promedio Semanal de Pasos',
            labels={'TotalSteps': 'Pasos promedio', 'Semana': 'Semana'}
        )
        st.plotly_chart(fig_week, use_container_width=True)

        # Gráfica de tendencia semanal de calorías quemadas promedio
        calorias_semanal = df_semanal.groupby('Semana')['Calories'].mean().reset_index()
        fig_cal = px.bar(
            calorias_semanal,
            x='Semana',
            y='Calories',
            title='Promedio Semanal de Calorías Quemadas',
            labels={'Calories': 'Calorías promedio', 'Semana': 'Semana'}
        )
        st.plotly_chart(fig_cal, use_container_width=True)

    # Mostrar distribución de actividad del último día
    latest_data = df.iloc[-1]
    total_minutes = sum([
        latest_data['VeryActiveMinutes'],
        latest_data['FairlyActiveMinutes'],
        latest_data['LightlyActiveMinutes'],
        latest_data['SedentaryMinutes']
    ])

    activity_dist = pd.DataFrame([{
        'Tipo': 'Muy Activo',
        'Minutos': latest_data['VeryActiveMinutes'],
        'Porcentaje': (latest_data['VeryActiveMinutes'] / total_minutes) * 100
    }, {
        'Tipo': 'Bastante Activo',
        'Minutos': latest_data['FairlyActiveMinutes'],
        'Porcentaje': (latest_data['FairlyActiveMinutes'] / total_minutes) * 100
    }, {
        'Tipo': 'Poco Activo',
        'Minutos': latest_data['LightlyActiveMinutes'],
        'Porcentaje': (latest_data['LightlyActiveMinutes'] / total_minutes) * 100
    }, {
        'Tipo': 'Sedentario',
        'Minutos': latest_data['SedentaryMinutes'],
        'Porcentaje': (latest_data['SedentaryMinutes'] / total_minutes) * 100
    }])

    fig_dist = px.pie(
        activity_dist,
        values='Minutos',
        names='Tipo',
        title='Distribución de Actividad (Último día)',
        hole=0.3
    )
    st.plotly_chart(fig_dist, use_container_width=True)

def plot_sleep_metrics(df: pd.DataFrame, user_id: str = None):
    """Gráfica de métricas de sueño"""
    if df.empty:
        st.info("No hay datos de sueño disponibles.")
        return

    # Filtrar por usuario si se especifica
    if user_id:
        df = df[df['Id'] == user_id]

    # Convertir minutos a horas (evitar SettingWithCopyWarning)
    df = df.copy()
    df.loc[:, 'HorasDeSueño'] = df['TotalMinutesAsleep'] / 60
    df.loc[:, 'HorasEnCama'] = df['TotalTimeInBed'] / 60

    # Gráfica mejorada: barras apiladas y diferencia visible
    import plotly.graph_objects as go
    df['Diferencia'] = df['HorasEnCama'] - df['HorasDeSueño']
    fig_sleep = go.Figure()
    fig_sleep.add_trace(go.Bar(
        x=df['Date'],
        y=df['HorasDeSueño'],
        name='Horas de Sueño',
        marker_color='rgba(60, 179, 113, 0.85)'
    ))
    fig_sleep.add_trace(go.Bar(
        x=df['Date'],
        y=df['Diferencia'],
        name='Diferencia (En cama sin dormir)',
        marker_color='rgba(255, 140, 0, 0.7)'
    ))
    fig_sleep.update_layout(
        barmode='stack',
        title='Horas de Sueño vs. Tiempo en Cama',
        xaxis_title='Fecha',
        yaxis_title='Horas',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    # Anotación de diferencia promedio
    diff = df['Diferencia'].mean()
    fig_sleep.add_annotation(
        text=f"Promedio sin dormir: {diff:.2f} h",
        xref="paper", yref="paper",
        x=0.99, y=0.99, showarrow=False,
        font=dict(size=13, color="#333"),
        bgcolor="#f0f8ff", bordercolor="#20B2AA", borderwidth=1
    )
    st.plotly_chart(fig_sleep, use_container_width=True)

    # Gráfica de tendencia semanal de horas de sueño promedio
    if len(df) >= 7:
        df_semanal = df.copy()
        df_semanal['Semana'] = df_semanal['Date'].dt.to_period('W').apply(lambda r: r.start_time)
        sueno_semanal = df_semanal.groupby('Semana')['HorasDeSueño'].mean().reset_index()
        fig_week = px.bar(
            sueno_semanal,
            x='Semana',
            y='HorasDeSueño',
            title='Promedio Semanal de Horas de Sueño',
            labels={'HorasDeSueño': 'Horas promedio', 'Semana': 'Semana'}
        )
        st.plotly_chart(fig_week, use_container_width=True)

    # Calcular eficiencia del sueño
    df.loc[:, 'EficienciaSueño'] = (df['TotalMinutesAsleep'] / df['TotalTimeInBed']) * 100
    
    # Gráfica de eficiencia del sueño
    fig_efficiency = px.line(
        df,
        x='Date',
        y='EficienciaSueño',
        title='Eficiencia del Sueño (%)',
        labels={
            'Date': 'Fecha',
            'EficienciaSueño': 'Eficiencia (%)'
        },
        markers=True
    )
    st.plotly_chart(fig_efficiency, use_container_width=True)

def plot_weight_metrics(df: pd.DataFrame, user_id: str = None):
    """Gráfica de métricas de peso"""
    if df.empty:
        st.info("No hay datos de peso disponibles.")
        return

    # Filtrar por usuario si se especifica
    if user_id:
        df = df[df['Id'] == user_id]

    # Gráfica de peso
    fig_weight = px.line(
        df,
        x='Date',
        y='WeightKg',
        title='Evolución del Peso',
        labels={
            'Date': 'Fecha',
            'WeightKg': 'Peso (kg)'
        },
        markers=True
    )
    st.plotly_chart(fig_weight, use_container_width=True)

    # Gráfica de tendencia semanal de peso promedio
    if len(df) >= 7:
        df_semanal = df.copy()
        df_semanal['Semana'] = df_semanal['Date'].dt.to_period('W').apply(lambda r: r.start_time)
        peso_semanal = df_semanal.groupby('Semana')['WeightKg'].mean().reset_index()
        fig_week = px.bar(
            peso_semanal,
            x='Semana',
            y='WeightKg',
            title='Promedio Semanal de Peso',
            labels={'WeightKg': 'Peso promedio (kg)', 'Semana': 'Semana'}
        )
        st.plotly_chart(fig_week, use_container_width=True)

    # Gráfica de IMC
    fig_bmi = px.line(
        df,
        x='Date',
        y='BMI',
        title='Evolución del IMC',
        labels={
            'Date': 'Fecha',
            'BMI': 'IMC'
        },
        markers=True
    )
    # Añadir línea de IMC ideal (peso ideal)
    altura_cm = None
    sexo = 'male'
    if user_id is not None:
        try:
            user_info = st.session_state.data_generator.get_user_info(user_id)
            altura_cm = user_info.get('height', None)
            sexo = user_info.get('gender', 'male')
        except Exception:
            pass
    # Añadir rangos de IMC (una sola vez)
    fig_bmi.add_hline(y=18.5, line_dash="dash", line_color="red", annotation_text="Bajo peso")
    fig_bmi.add_hline(y=25, line_dash="dash", line_color="blue", annotation_text="Sobrepeso")
    fig_bmi.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Obesidad")
    st.plotly_chart(fig_bmi, use_container_width=True)

def plot_correlations(activity_df: pd.DataFrame, sleep_df: pd.DataFrame, user_id: str = None):
    """Gráfica de correlaciones entre actividad y sueño"""
    if activity_df.empty or sleep_df.empty:
        st.info("No hay suficientes datos para mostrar correlaciones.")
        return

    # Filtrar por usuario si se especifica
    if user_id:
        activity_df = activity_df[activity_df['Id'] == user_id]
        sleep_df = sleep_df[sleep_df['Id'] == user_id]

    # Combinar datos de actividad y sueño
    merged_df = pd.merge(
        activity_df,
        sleep_df,
        on=['Id', 'Date'],
        how='inner'
    )

    if merged_df.empty:
        st.info("No hay datos coincidentes para mostrar correlaciones.")
        return

    # Convertir minutos de sueño a horas (evitar SettingWithCopyWarning)
    merged_df = merged_df.copy()
    merged_df.loc[:, 'HorasSueño'] = merged_df['TotalMinutesAsleep'] / 60

    # Gráfica de correlación Pasos vs Sueño
    fig_corr = px.scatter(
        merged_df,
        x='TotalSteps',
        y='HorasSueño',
        title='Correlación entre Pasos Diarios y Horas de Sueño',
        labels={
            'TotalSteps': 'Pasos Diarios',
            'HorasSueño': 'Horas de Sueño'
        },
        trendline="ols"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # Gráfica de correlación Calorías vs Sueño
    fig_cal_corr = px.scatter(
        merged_df,
        x='Calories',
        y='HorasSueño',
        title='Correlación entre Calorías Quemadas y Horas de Sueño',
        labels={
            'Calories': 'Calorías',
            'HorasSueño': 'Horas de Sueño'
        },
        trendline="ols"
    )
    st.plotly_chart(fig_cal_corr, use_container_width=True)