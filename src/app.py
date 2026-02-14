# src/app.py
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from utils.data_generator import HealthDataGenerator
from utils.visualizations import (
    format_metric,
    plot_activity_metrics,
    plot_sleep_metrics,
    plot_weight_metrics,
    plot_correlations
)

st.set_page_config(
    page_title="Dashboard de Salud",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Función para calcular el tiempo hasta la próxima actualización
def get_time_until_next_update():
    if 'last_update' not in st.session_state:
        return 0
    elapsed = (datetime.now() - st.session_state.last_update).total_seconds()
    return max(0, 60 - int(elapsed))

# Inicializar el estado de la sesión
if 'data_generator' not in st.session_state:
    st.session_state.data_generator = HealthDataGenerator()
    st.session_state.last_update = datetime.now()
    # Generar datos históricos iniciales
    activity_df, sleep_df, weight_df = st.session_state.data_generator.generate_historical_data()
    st.session_state.historical_data = {
        'activity': activity_df,
        'sleep': sleep_df,
        'weight': weight_df
    }

# Función para actualizar datos
def update_data():
    if 'historical_data' not in st.session_state:
        activity_df, sleep_df, weight_df = st.session_state.data_generator.generate_historical_data()
        st.session_state.historical_data = {
            'activity': activity_df,
            'sleep': sleep_df,
            'weight': weight_df
        }
        return

    # Actualizar con datos en tiempo real
    real_time_activity, real_time_sleep, real_time_weight = st.session_state.data_generator.generate_realtime_update()
    
    # Combinar datos históricos con tiempo real
    for df_name, real_time_df in [
        ('activity', real_time_activity),
        ('sleep', real_time_sleep),
        ('weight', real_time_weight)
    ]:
        if not real_time_df.empty:
            historical = st.session_state.historical_data[df_name].copy()
            # Actualizar o agregar nuevos datos
            combined = pd.concat([historical, real_time_df])
            combined = combined.drop_duplicates(subset=['Id', 'Date'], keep='last')
            combined = combined.sort_values('Date')
            st.session_state.historical_data[df_name] = combined

    st.session_state.last_update = datetime.now()


# Actualizar datos solo si ha pasado 1 minuto
import time as _time
if 'historical_data' not in st.session_state or (datetime.now() - st.session_state.last_update).total_seconds() >= 60:
    update_data()

# Refrescar la interfaz cada segundo para el contador
segundos = get_time_until_next_update()
st.session_state['segundos_restantes'] = segundos
if segundos > 0:
    _time.sleep(1)
    if hasattr(st, "experimental_rerun") and callable(st.experimental_rerun):
        st.experimental_rerun()

# Barra lateral
with st.sidebar:
    col_logo, col_spacer, col_logo2 = st.columns([1,2,1])
    with col_logo2:
        st.write("")
    with col_spacer:
        st.image("assets/logo.png", width=90)
    with col_logo:
        st.write("")
    st.markdown("<h2 style='text-align:center; color:#2E8B57; margin-bottom:0;'>Dashboard Salud</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray; margin-top:0;'>Bienvenido/a, cuida tu bienestar cada día</p>", unsafe_allow_html=True)
    st.divider()
    
    # Mostrar hora de última actualización y tiempo hasta la próxima
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"**Última actualización:** {st.session_state.last_update.strftime('%H:%M:%S')}")
    with col2:
        segundos = st.session_state.get('segundos_restantes', get_time_until_next_update())
        st.write(f"Próxima: {segundos}s")
    
    # Botón de actualización manual
    if st.button("🔄 Actualizar datos"):
        update_data()
    
    st.divider()
    
    # Selector de usuario
    users = st.session_state.data_generator.users
    user_options = [f"{user.name} ({uid})" for uid, user in users.items()]
    selected_option = st.selectbox("👤 Seleccionar Usuario", options=user_options)
    # Obtener ID del usuario seleccionado
    selected_user = selected_option.split("(")[-1].strip(")")
    
    st.divider()
    
    # Navegación
    section = st.radio("📊 Sección", ["Resumen", "Actividad", "Sueño", "Peso", "Correlaciones", "Datos"])

# Obtener datos actuales
current_data = st.session_state.historical_data
activity_df = current_data['activity']
sleep_df = current_data['sleep']
weight_df = current_data['weight']


# Mostrar información del usuario seleccionado y peso ideal
def calcular_peso_ideal(altura_cm, sexo):
    # Fórmula de Devine para adultos
    if sexo.lower() == 'male' or sexo.lower() == 'hombre':
        return 50 + 0.9 * (altura_cm - 152)
    else:
        return 45.5 + 0.9 * (altura_cm - 152)

if selected_user:
    user_info = st.session_state.data_generator.get_user_info(selected_user)
    peso_ideal = calcular_peso_ideal(user_info['height'], user_info.get('gender', 'male'))
    st.markdown(f"""
    <div style='background: #f0f8ff; border-radius: 16px; box-shadow: 0 2px 8px #0001; padding: 1.2rem 1rem 0.5rem 1rem; margin-bottom: 1.2rem;'>
        <h3 style='text-align:center; color:#2E8B57; margin-bottom:0.5rem;'>👤 {user_info['name']}</h3>
        <div style='display: flex; justify-content: space-around; flex-wrap: wrap;'>
            <div style='text-align:center; margin: 0.5rem;'>
                <span style='font-size:1.1rem; color:#555;'>Edad</span><br>
                <span style='font-weight:bold; font-size:1.3rem;'>{user_info['age']} años</span>
            </div>
            <div style='text-align:center; margin: 0.5rem;'>
                <span style='font-size:1.1rem; color:#555;'>Altura</span><br>
                <span style='font-weight:bold; font-size:1.3rem;'>{user_info['height']} cm</span>
            </div>
            <div style='text-align:center; margin: 0.5rem;'>
                <span style='font-size:1.1rem; color:#555;'>Nivel de Actividad</span><br>
                <span style='font-weight:bold; font-size:1.3rem;'>{user_info['activity_level'].title()}</span>
            </div>
            <div style='text-align:center; margin: 0.5rem;'>
                <span style='font-size:1.1rem; color:#555;'>Meta de Pasos</span><br>
                <span style='font-weight:bold; font-size:1.3rem;'>{format_metric(user_info['step_goal'])}</span>
            </div>
            <div style='text-align:center; margin: 0.5rem;'>
                <span style='font-size:1.1rem; color:#555;'>Peso Ideal</span><br>
                <span style='font-weight:bold; font-size:1.3rem;'>{peso_ideal:.1f} kg</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)



# Contenido principal según la sección seleccionada (solo usuario individual)
if section == "Resumen":
    st.markdown("""
    <h3 style='color:#2E8B57;'>🏃‍♂️ Resumen general</h3>
    <ul>
    <li><b>Pasos:</b> Caminar al menos 7,000-10,000 pasos al día ayuda a mantener un estilo de vida activo.</li>
    <li><b>Calorías:</b> Las calorías quemadas dependen de la actividad física y el metabolismo. Mantenerse activo ayuda a controlar el peso.</li>
    <li><b>Sueño:</b> Se recomienda dormir entre 7 y 9 horas diarias para una buena salud física y mental.</li>
    <li><b>Peso Actual:</b> El peso es solo una referencia, lo importante es mantener hábitos saludables.</li>
    </ul>
    """, unsafe_allow_html=True)
    activity_view = activity_df[activity_df['Id'] == selected_user]
    sleep_view = sleep_df[sleep_df['Id'] == selected_user]
    weight_view = weight_df[weight_df['Id'] == selected_user]
    # Métricas principales resaltadas
    st.markdown("""
    <div style='display: flex; justify-content: space-around; flex-wrap: wrap; margin-bottom: 1.2rem;'>
        <div style='background: #e6f7e6; border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem; min-width: 160px; text-align:center; box-shadow: 0 1px 4px #0001;'>
            <span style='color:#2E8B57; font-size:1.1rem;'>Pasos Hoy</span><br>
            <span style='font-weight:bold; font-size:1.5rem;'>{pasos}</span>
        </div>
        <div style='background: #e6f0fa; border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem; min-width: 160px; text-align:center; box-shadow: 0 1px 4px #0001;'>
            <span style='color:#4682B4; font-size:1.1rem;'>Calorías quemadas hoy</span><br>
            <span style='font-weight:bold; font-size:1.5rem;'>{calorias}</span>
        </div>
        <div style='background: #f3e6fa; border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem; min-width: 160px; text-align:center; box-shadow: 0 1px 4px #0001;'>
            <span style='color:#6A5ACD; font-size:1.1rem;'>Horas de Sueño</span><br>
            <span style='font-weight:bold; font-size:1.5rem;'>{sueno}</span>
        </div>
        <div style='background: #fff4e6; border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem; min-width: 160px; text-align:center; box-shadow: 0 1px 4px #0001;'>
            <span style='color:#FF8C00; font-size:1.1rem;'>Peso Actual</span><br>
            <span style='font-weight:bold; font-size:1.5rem;'>{peso}</span>
        </div>
    </div>
    """.format(
        pasos=format_metric(activity_view.iloc[-1]['TotalSteps']) if not activity_view.empty else "-",
        calorias=format_metric(activity_view.iloc[-1]['Calories'], " kcal") if not activity_view.empty else "-",
        sueno=format_metric(sleep_view.iloc[-1]['TotalMinutesAsleep'] / 60, "h") if not sleep_view.empty else "-",
        peso=format_metric(weight_view.iloc[-1]['WeightKg'], " kg") if not weight_view.empty else "-"
    ), unsafe_allow_html=True)
    # Gráficas resumidas
    col1, col2 = st.columns(2)
    with col1:
        plot_activity_metrics(activity_view)
    with col2:
        plot_sleep_metrics(sleep_view)
elif section == "Actividad":
    st.markdown("""
    <h3 style='color:#4682B4;'>🚶‍♀️ Actividad Física</h3>
    <ul>
    <li>Caminar, correr o moverse ayuda a mantener un peso saludable y mejora el ánimo.</li>
    <li>Se recomienda al menos 150 minutos de actividad moderada a la semana.</li>
    <li>¡Cada paso cuenta para tu bienestar!</li>
    </ul>
    """, unsafe_allow_html=True)
    df_view = activity_df[activity_df['Id'] == selected_user]
    plot_activity_metrics(df_view)
elif section == "Sueño":
    st.markdown("""
    <h3 style='color:#6A5ACD;'>😴 Sueño</h3>
    <ul>
    <li>Dormir bien es fundamental para la salud física y mental.</li>
    <li>Se recomienda dormir entre 7 y 9 horas por noche para adultos.</li>
    <li>La eficiencia del sueño mide qué porcentaje del tiempo en cama realmente duermes.</li>
    </ul>
    """, unsafe_allow_html=True)
    df_view = sleep_df[sleep_df['Id'] == selected_user]
    plot_sleep_metrics(df_view)
elif section == "Peso":
    st.markdown("""
    <h3 style='color:#FF8C00;'>⚖️ Evolución del Peso y del IMC</h3>
    <ul>
    <li><b>Peso Ideal:</b> Es un valor estimado según tu altura y sexo. No es un objetivo estricto, sino una referencia saludable.</li>
    <li><b>IMC (Índice de Masa Corporal):</b> Es una medida que relaciona tu peso y altura. Un IMC entre 18.5 y 24.9 se considera saludable. Consulta a un profesional para una valoración personalizada.</li>
    </ul>
    """, unsafe_allow_html=True)
    df_view = weight_df[weight_df['Id'] == selected_user]
    plot_weight_metrics(df_view)
    # Mostrar peso ideal y diferencia
    if selected_user:
        user_info = st.session_state.data_generator.get_user_info(selected_user)
        peso_ideal = calcular_peso_ideal(user_info['height'], user_info.get('gender', 'male'))
        if not df_view.empty:
            peso_actual = df_view.iloc[-1]['WeightKg']
            diferencia = peso_actual - peso_ideal
            if abs(diferencia) < 1:
                mensaje = f"¡Felicidades! Estás en tu peso ideal. ¡Sigue así! 🏆"
            elif diferencia > 0:
                mensaje = f"Te faltan {abs(diferencia):.1f} kg para alcanzar tu peso ideal. ¡Tú puedes lograrlo! 💪"
            else:
                mensaje = f"Estás {abs(diferencia):.1f} kg por debajo de tu peso ideal. ¡Sigue cuidando tu salud! 🌟"
            st.info(f"**Peso ideal:** {peso_ideal:.1f} kg\n\n**Peso actual:** {peso_actual:.1f} kg\n\n{mensaje}")

elif section == "Correlaciones":
    st.markdown("""
    <h3 style='color:#20B2AA;'>🔗 Correlaciones</h3>
    <ul>
    <li>Esta sección muestra si existe relación entre tu actividad física y tu sueño.</li>
    <li>La línea azul es una tendencia: si sube, más actividad se asocia a más horas de sueño; si baja, a menos horas.</li>
    <li>El coeficiente <b>r</b> indica la fuerza de la relación: cerca de 0 = sin relación, cerca de 1 o -1 = relación fuerte.</li>
    </ul>
    """, unsafe_allow_html=True)
    act_view = activity_df[activity_df['Id'] == selected_user]
    slp_view = sleep_df[sleep_df['Id'] == selected_user]
    # Calcular correlaciones
    import numpy as np
    merged = act_view.merge(slp_view, on=["Id", "Date"], suffixes=("_act", "_slp"))
    r_pasos = np.nan
    r_cal = np.nan
    interpretacion_pasos = ""
    interpretacion_cal = ""
    if not merged.empty:
        if merged["TotalSteps"].std() > 0 and (merged["TotalMinutesAsleep"].std() > 0):
            r_pasos = merged["TotalSteps"].corr(merged["TotalMinutesAsleep"])
        if merged["Calories"].std() > 0 and (merged["TotalMinutesAsleep"].std() > 0):
            r_cal = merged["Calories"].corr(merged["TotalMinutesAsleep"])
        def interpreta(r):
            if np.isnan(r):
                return "No hay datos suficientes."
            if abs(r) < 0.2:
                return "No hay relación significativa."
            elif abs(r) < 0.5:
                return "Relación débil."
            elif abs(r) < 0.7:
                return "Relación moderada."
            else:
                return "Relación fuerte."
        interpretacion_pasos = interpreta(r_pasos)
        interpretacion_cal = interpreta(r_cal)
    plot_correlations(act_view, slp_view)
    st.markdown(f"""
    <div style='background:#f0f8ff; border-radius:12px; padding:1rem; margin-top:1rem;'>
    <b>Correlación Pasos vs Sueño:</b> r = {r_pasos:.2f} <br><i>{interpretacion_pasos}</i><br><br>
    <b>Correlación Calorías vs Sueño:</b> r = {r_cal:.2f} <br><i>{interpretacion_cal}</i>
    </div>
    """, unsafe_allow_html=True)

elif section == "Datos":
    st.markdown("""
    <h3 style='color:#008080;'>📋 Tabla de Datos Generados</h3>
    <p>Aquí puedes ver los datos simulados de actividad, sueño y peso para el usuario seleccionado.</p>
    """, unsafe_allow_html=True)
    st.subheader("Actividad Física")
    st.markdown("""
    **Columnas:**
    - `Date`: Fecha del registro
    - `TotalSteps`: Pasos totales en el día
    - `Calories`: Calorías quemadas
    - `VeryActiveMinutes`: Minutos de actividad muy intensa
    - `FairlyActiveMinutes`: Minutos de actividad moderada
    - `LightlyActiveMinutes`: Minutos de actividad ligera
    - `SedentaryMinutes`: Minutos sedentarios
    """)
    st.dataframe(activity_df[activity_df['Id'] == selected_user].sort_values('Date', ascending=False).reset_index(drop=True))
    st.subheader("Sueño")
    st.markdown("""
    **Columnas:**
    - `Date`: Fecha del registro
    - `TotalMinutesAsleep`: Minutos totales dormidos
    - `TotalTimeInBed`: Minutos totales en cama
    """)
    st.dataframe(sleep_df[sleep_df['Id'] == selected_user].sort_values('Date', ascending=False).reset_index(drop=True))
    st.subheader("Peso")
    st.markdown("""
    **Columnas:**
    - `Date`: Fecha del registro
    - `WeightKg`: Peso en kilogramos
    - `BMI`: Índice de Masa Corporal
    """)
    st.dataframe(weight_df[weight_df['Id'] == selected_user].sort_values('Date', ascending=False).reset_index(drop=True))





