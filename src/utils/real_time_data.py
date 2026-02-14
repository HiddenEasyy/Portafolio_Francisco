import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_real_time_activity(base_data):
    """
    Genera datos de actividad en tiempo real basados en patrones históricos.
    """
    if base_data.empty:
        return pd.DataFrame()
    
    now = datetime.now()
    today = now.date()
    current_hour = now.hour
    
    # Crear nuevo registro para el día actual
    new_record = {
        'Id': base_data['Id'].iloc[-1] if 'Id' in base_data.columns else '1',
        'Date': pd.Timestamp(today),
        'TotalSteps': int(np.random.normal(
            base_data['TotalSteps'].mean(), 
            base_data['TotalSteps'].std() * 0.1
        ) * (current_hour / 24)),  # Escalar según la hora del día
        'Calories': int(np.random.normal(
            base_data['Calories'].mean(),
            base_data['Calories'].std() * 0.1
        ) * (current_hour / 24))
    }
    
    # Añadir columnas adicionales si existen en los datos base
    optional_columns = [
        'TotalDistance', 'VeryActiveMinutes', 'FairlyActiveMinutes',
        'LightlyActiveMinutes', 'SedentaryMinutes'
    ]
    
    for col in optional_columns:
        if col in base_data.columns:
            new_record[col] = float(np.random.normal(
                base_data[col].mean(),
                base_data[col].std() * 0.1
            ) * (current_hour / 24))
    
    return pd.DataFrame([new_record])

def generate_real_time_sleep(base_data):
    """
    Genera datos de sueño en tiempo real basados en patrones históricos.
    """
    if base_data.empty:
        return pd.DataFrame()
    
    now = datetime.now()
    today = now.date()
    
    # Solo generar datos de sueño si es después de las 8 AM
    if now.hour < 8:
        return pd.DataFrame()
    
    new_record = {
        'Id': base_data['Id'].iloc[-1] if 'Id' in base_data.columns else '1',
        'Date': pd.Timestamp(today),
        'TotalMinutesAsleep': int(np.random.normal(
            base_data['TotalMinutesAsleep'].mean(),
            base_data['TotalMinutesAsleep'].std() * 0.1
        )),
        'TotalTimeInBed': int(np.random.normal(
            base_data['TotalTimeInBed'].mean() if 'TotalTimeInBed' in base_data.columns else 480,
            30
        ))
    }
    
    return pd.DataFrame([new_record])

def generate_real_time_weight(base_data):
    """
    Genera datos de peso en tiempo real basados en patrones históricos.
    """
    if base_data.empty:
        return pd.DataFrame()
    
    now = datetime.now()
    today = now.date()
    
    # Generar dato de peso solo una vez al día
    if now.hour < 7:  # Simular medición matutina
        return pd.DataFrame()
    
    last_weight = base_data['WeightKg'].iloc[-1] if 'WeightKg' in base_data.columns else 70
    new_weight = float(np.random.normal(last_weight, 0.1))  # Pequeña variación
    
    new_record = {
        'Id': base_data['Id'].iloc[-1] if 'Id' in base_data.columns else '1',
        'Date': pd.Timestamp(today),
        'WeightKg': new_weight,
        'BMI': (new_weight / (1.7 ** 2))  # Asumiendo altura promedio de 1.7m
    }
    
    return pd.DataFrame([new_record])

def update_real_time_data(activity_df, sleep_df, weight_df):
    """
    Actualiza los DataFrames con datos simulados en tiempo real.
    """
    # Generar nuevos datos
    new_activity = generate_real_time_activity(activity_df)
    new_sleep = generate_real_time_sleep(sleep_df)
    new_weight = generate_real_time_weight(weight_df)
    
    # Actualizar DataFrames
    if not new_activity.empty:
        activity_df = pd.concat([activity_df, new_activity], ignore_index=True)
        activity_df = activity_df.drop_duplicates(subset=['Id', 'Date'], keep='last')
    
    if not new_sleep.empty:
        sleep_df = pd.concat([sleep_df, new_sleep], ignore_index=True)
        sleep_df = sleep_df.drop_duplicates(subset=['Id', 'Date'], keep='last')
    
    if not new_weight.empty:
        weight_df = pd.concat([weight_df, new_weight], ignore_index=True)
        weight_df = weight_df.drop_duplicates(subset=['Id', 'Date'], keep='last')
    
    return activity_df, sleep_df, weight_df