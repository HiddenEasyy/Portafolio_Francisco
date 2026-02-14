import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class UserHealthSimulator:
    def __init__(self, user_id, start_date=None, seed=None):
        """
        Inicializa un simulador de datos de salud para un usuario específico.
        """
        self.user_id = str(user_id)
        if seed is not None:
            np.random.seed(seed)
            
        # Establecer fecha de inicio (30 días atrás por defecto)
        self.start_date = start_date or (datetime.now() - timedelta(days=30))
        
        # Características base del usuario (aleatorias pero consistentes)
        self.base_stats = {
            'weight': np.random.normal(75, 5),  # peso en kg
            'height': np.random.normal(170, 10),  # altura en cm
            'activity_level': np.random.choice(['bajo', 'medio', 'alto']),
            'sleep_pattern': np.random.choice(['regular', 'irregular']),
            'step_goal': np.random.randint(8000, 12000)
        }

    def _generate_daily_steps(self, date, hour_now=None):
        """Genera pasos diarios basados en patrones realistas"""
        is_weekend = date.weekday() >= 5
        base_steps = self.base_stats['step_goal'] * (0.8 if is_weekend else 1.0)
        
        # Variación diaria
        daily_variation = np.random.normal(1, 0.2)
        total_steps = int(base_steps * daily_variation)
        
        # Si es el día actual, ajustar según la hora
        if hour_now is not None:
            return int(total_steps * (hour_now / 24))
        return total_steps

    def _generate_sleep_data(self, date):
        """Genera datos de sueño realistas"""
        is_weekend = date.weekday() >= 5
        base_sleep = 8 if is_weekend else 7  # más sueño en fines de semana
        
        if self.base_stats['sleep_pattern'] == 'irregular':
            variation = np.random.normal(0, 1)
        else:
            variation = np.random.normal(0, 0.5)
            
        sleep_hours = max(4, min(12, base_sleep + variation))
        return {
            'TotalMinutesAsleep': int(sleep_hours * 60),
            'TotalTimeInBed': int(sleep_hours * 60 + np.random.randint(10, 30))
        }

    def _generate_weight_data(self, date):
        """Genera datos de peso con variaciones realistas"""
        days_passed = (date - self.start_date).days
        trend = days_passed * 0.01 * np.random.choice([-1, 1])  # tendencia sutil
        daily_variation = np.random.normal(0, 0.2)
        weight = self.base_stats['weight'] + trend + daily_variation
        height_m = self.base_stats['height'] / 100
        bmi = weight / (height_m * height_m)
        
        return {
            'WeightKg': round(weight, 2),
            'BMI': round(bmi, 2)
        }

    def generate_historical_data(self):
        """Genera datos históricos desde la fecha de inicio hasta ahora"""
        now = datetime.now()
        dates = pd.date_range(start=self.start_date, end=now, freq='D')
        
        # Generar datos de actividad
        activity_data = []
        sleep_data = []
        weight_data = []
        
        for date in dates:
            # Actividad
            steps = self._generate_daily_steps(date)
            activity_data.append({
                'Id': self.user_id,
                'Date': date,
                'TotalSteps': steps,
                'Calories': int(steps * 0.05),
                'VeryActiveMinutes': int(steps * 0.0002 * np.random.normal(1, 0.2)),
                'FairlyActiveMinutes': int(steps * 0.0003 * np.random.normal(1, 0.2)),
                'LightlyActiveMinutes': int(steps * 0.001 * np.random.normal(1, 0.2))
            })
            
            # Sueño
            sleep = self._generate_sleep_data(date)
            sleep_data.append({
                'Id': self.user_id,
                'Date': date,
                **sleep
            })
            
            # Peso (no diario, cada 3 días)
            if date.day % 3 == 0:
                weight = self._generate_weight_data(date)
                weight_data.append({
                    'Id': self.user_id,
                    'Date': date,
                    **weight
                })
        
        return {
            'activity': pd.DataFrame(activity_data),
            'sleep': pd.DataFrame(sleep_data),
            'weight': pd.DataFrame(weight_data)
        }

    def generate_realtime_update(self):
        """Genera datos en tiempo real para el momento actual"""
        now = datetime.now()
        
        # Actividad actual (basada en la hora del día)
        activity_data = {
            'Id': self.user_id,
            'Date': pd.Timestamp(now.date()),
            'TotalSteps': self._generate_daily_steps(now.date(), now.hour),
            'Calories': 0,  # se calculará después
            'VeryActiveMinutes': 0,
            'FairlyActiveMinutes': 0,
            'LightlyActiveMinutes': 0
        }
        
        # Calcular calorías y minutos activos proporcionales a los pasos
        activity_data['Calories'] = int(activity_data['TotalSteps'] * 0.05)
        activity_data['VeryActiveMinutes'] = int(activity_data['TotalSteps'] * 0.0002 * now.hour/24)
        activity_data['FairlyActiveMinutes'] = int(activity_data['TotalSteps'] * 0.0003 * now.hour/24)
        activity_data['LightlyActiveMinutes'] = int(activity_data['TotalSteps'] * 0.001 * now.hour/24)
        
        # Sueño (solo si es después de despertar)
        sleep_data = None
        if now.hour >= 7:
            sleep = self._generate_sleep_data(now.date())
            sleep_data = {
                'Id': self.user_id,
                'Date': pd.Timestamp(now.date()),
                **sleep
            }
        
        # Peso (solo una vez al día, en la mañana)
        weight_data = None
        if now.hour >= 6 and now.hour <= 9:
            weight = self._generate_weight_data(now.date())
            weight_data = {
                'Id': self.user_id,
                'Date': pd.Timestamp(now.date()),
                **weight
            }
            
        return {
            'activity': pd.DataFrame([activity_data]),
            'sleep': pd.DataFrame([sleep_data]) if sleep_data else pd.DataFrame(),
            'weight': pd.DataFrame([weight_data]) if weight_data else pd.DataFrame()
        }