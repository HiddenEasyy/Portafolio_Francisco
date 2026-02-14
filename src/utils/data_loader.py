# src/utils/data_loader.py
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from .data_simulator import UserHealthSimulator

# Simuladores predefinidos para usuarios
SIMULATED_USERS = {
    '1': {'name': 'Ana García', 'activity_level': 'alto', 'seed': 42},
    '2': {'name': 'Juan Pérez', 'activity_level': 'medio', 'seed': 43},
    '3': {'name': 'María López', 'activity_level': 'bajo', 'seed': 44}
}

def _safe_read_csv(path, parse_dates=None):
    try:
        if not path.exists():
            st.warning(f"Archivo no encontrado: {path}")
            return pd.DataFrame()
        df = pd.read_csv(path, parse_dates=parse_dates, low_memory=False)
        # Validar que el DataFrame no esté vacío
        if df.empty:
            st.warning(f"El archivo {path} está vacío")
        return df
    except Exception as e:
        st.error(f"Error al leer {path}: {str(e)}")
        return pd.DataFrame()

def _ensure_datetime(df, col_candidates, new_name="Date"):
    """
    Tries to find a date column from candidates and normalize to 'Date'.
    """
    for c in col_candidates:
        if c in df.columns:
            df[new_name] = pd.to_datetime(df[c], errors='coerce')
            return df
    # fallback: try any datetime-like column
    for c in df.columns:
        if 'date' in c.lower() or 'time' in c.lower():
            try:
                df[new_name] = pd.to_datetime(df[c], errors='coerce')
                return df
            except Exception:
                continue
    # if none found, create empty Date
    df[new_name] = pd.NaT
    return df

def _standardize_id(df):
    if df.empty:
        return df
    if 'Id' in df.columns:
        df['Id'] = df['Id'].astype(str)
    elif 'id' in df.columns:
        df['Id'] = df['id'].astype(str)
    return df

def load_data():
    """
    Carga datos simulados para todos los usuarios predefinidos.
    """
    if 'simulators' not in st.session_state:
        st.session_state.simulators = {
            user_id: UserHealthSimulator(
                user_id,
                start_date=datetime.now() - timedelta(days=30),
                seed=user_info['seed']
            )
            for user_id, user_info in SIMULATED_USERS.items()
        }
        
    # Generar o actualizar datos
    all_activity = []
    all_sleep = []
    all_weight = []
    
    for user_id, simulator in st.session_state.simulators.items():
        # Obtener datos históricos si no existen
        if f'historical_data_{user_id}' not in st.session_state:
            st.session_state[f'historical_data_{user_id}'] = simulator.generate_historical_data()
            
        # Obtener actualización en tiempo real
        realtime_data = simulator.generate_realtime_update()
        
        # Combinar datos históricos con tiempo real
        for data_type in ['activity', 'sleep', 'weight']:
            historical = st.session_state[f'historical_data_{user_id}'][data_type]
            realtime = realtime_data[data_type]
            
            if not realtime.empty:
                # Actualizar o agregar datos en tiempo real
                combined = pd.concat([historical, realtime]).drop_duplicates(subset=['Id', 'Date'], keep='last')
                st.session_state[f'historical_data_{user_id}'][data_type] = combined
            else:
                combined = historical
                
            if data_type == 'activity':
                all_activity.append(combined)
            elif data_type == 'sleep':
                all_sleep.append(combined)
            else:
                all_weight.append(combined)

    # Combinar todos los datos de usuarios
    activity = pd.concat(all_activity, ignore_index=True) if all_activity else pd.DataFrame()
    sleep = pd.concat(all_sleep, ignore_index=True) if all_sleep else pd.DataFrame()
    weight = pd.concat(all_weight, ignore_index=True) if all_weight else pd.DataFrame()
    
    # Asegurar que todas las fechas sean pandas Timestamp y ordenar
    for df in [activity, sleep, weight]:
        if not df.empty and 'Date' in df.columns:
            # Convertir fechas a pandas Timestamp
            df['Date'] = pd.to_datetime(df['Date'])
            # Ordenar por fecha
            df.sort_values('Date', inplace=True, ignore_index=True)
            
    return activity, sleep, weight

def get_user_ids(activity_df, sleep_df, weight_df):
    """
    Obtiene los IDs de usuario que tienen datos en al menos uno de los DataFrames.
    También valida que los IDs sean consistentes entre los diferentes conjuntos de datos.
    """
    ids_by_source = {
        'actividad': set(activity_df['Id'].dropna().astype(str).unique()) if not activity_df.empty and 'Id' in activity_df.columns else set(),
        'sueño': set(sleep_df['Id'].dropna().astype(str).unique()) if not sleep_df.empty and 'Id' in sleep_df.columns else set(),
        'peso': set(weight_df['Id'].dropna().astype(str).unique()) if not weight_df.empty and 'Id' in weight_df.columns else set()
    }
    
    # Obtener todos los IDs únicos
    all_ids = set().union(*ids_by_source.values())
    
    # Validar y mostrar información sobre la disponibilidad de datos
    if not all_ids:
        st.warning("No se encontraron IDs de usuario en ninguno de los conjuntos de datos.")
        return []
    
    # Crear un resumen de disponibilidad de datos por ID
    id_summary = {}
    for id_str in sorted(all_ids):
        sources = []
        if id_str in ids_by_source['actividad']:
            sources.append('actividad')
        if id_str in ids_by_source['sueño']:
            sources.append('sueño')
        if id_str in ids_by_source['peso']:
            sources.append('peso')
        id_summary[id_str] = sources
    
    # Mostrar resumen en la interfaz
    with st.expander("Ver disponibilidad de datos por usuario"):
        for id_str, sources in id_summary.items():
            st.text(f"Usuario {id_str}: datos de {', '.join(sources)}")
    
    return sorted(list(all_ids))

def merge_activity_sleep(activity_df, sleep_df, id=None):
    """
    Merge activity and sleep on Id and Date (Date alignment by day).
    Returns merged dataframe.
    """
    try:
        a = activity_df.copy() if activity_df is not None else pd.DataFrame()
        s = sleep_df.copy() if sleep_df is not None else pd.DataFrame()
        
        if a.empty and s.empty:
            return pd.DataFrame()
            
        # Asegurar que las fechas sean pandas Timestamp
        for df in [a, s]:
            if not df.empty and 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date']).dt.normalize()

        if id:
            if 'Id' in a.columns:
                a = a[a['Id'] == str(id)]
            if 'Id' in s.columns:
                s = s[s['Id'] == str(id)]
                
    except Exception as e:
        st.error(f"Error al procesar los datos: {str(e)}")
        return pd.DataFrame()

    # merge by Date and Id if present
    if 'Id' in a.columns and 'Id' in s.columns:
        merged = pd.merge(a, s, on=['Id','Date'], how='outer', suffixes=('_act','_sleep'))
    else:
        merged = pd.merge(a, s, on='Date', how='outer', suffixes=('_act','_sleep'))

    # Sort and return
    merged = merged.sort_values('Date').reset_index(drop=True)
    return merged
