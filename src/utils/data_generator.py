from dataclasses import dataclass
from datetime import datetime, time, timedelta
import numpy as np
import pandas as pd

@dataclass
class UserProfile:
    id: str
    name: str
    age: int
    height: float  # en cm
    base_weight: float  # en kg
    activity_level: str
    sleep_schedule: tuple[time, time]  # (hora dormir, hora despertar)
    step_goal: int

class HealthDataGenerator:
    def __init__(self):
        # Perfiles de usuario predefinidos
        self.users = {
            "1": UserProfile(
                id="1",
                name="Ana García",
                age=28,
                height=165,
                base_weight=62.5,
                activity_level="alto",
                sleep_schedule=(time(23, 0), time(6, 30)),
                step_goal=12000
            ),
            "2": UserProfile(
                id="2",
                name="Juan Pérez",
                age=35,
                height=178,
                base_weight=75.0,
                activity_level="medio",
                sleep_schedule=(time(23, 30), time(7, 0)),
                step_goal=10000
            ),
            "3": UserProfile(
                id="3",
                name="María López",
                age=42,
                height=170,
                base_weight=68.0,
                activity_level="bajo",
                sleep_schedule=(time(22, 30), time(6, 0)),
                step_goal=8000
            )
        }

    def _generate_daily_steps(self, user: UserProfile, date: datetime, current_hour: int = None) -> dict:
        """Genera datos de actividad física diaria"""
        is_weekend = date.weekday() >= 5
        base_multiplier = {
            "alto": 1.2,
            "medio": 1.0,
            "bajo": 0.8
        }[user.activity_level]

        # Factor de actividad base según el día
        if is_weekend:
            base_steps = user.step_goal * 0.8  # Menos activo en fines de semana
        else:
            base_steps = user.step_goal

        # Variación diaria natural
        daily_variation = np.random.normal(1, 0.2)
        total_steps = int(base_steps * daily_variation * base_multiplier)

        # Si se proporciona la hora actual, ajustar los pasos
        if current_hour is not None:
            # Distribución de actividad durante el día
            hour_weights = np.array([
                0.01, 0.01, 0.01, 0.01, 0.01, 0.02,  # 0-5 AM
                0.05, 0.08, 0.10, 0.08, 0.07, 0.08,  # 6-11 AM
                0.07, 0.08, 0.07, 0.06, 0.05, 0.07,  # 12-5 PM
                0.06, 0.05, 0.02, 0.01, 0.01, 0.01   # 6-11 PM
            ])
            cumulative_weight = np.sum(hour_weights[:current_hour + 1])
            total_steps = int(total_steps * cumulative_weight)

        # Calcular calorías y minutos activos
        calories = int(total_steps * 0.05)  # Aproximación simple de calorías
        active_minutes = {
            "VeryActiveMinutes": int(total_steps * 0.0015),
            "FairlyActiveMinutes": int(total_steps * 0.002),
            "LightlyActiveMinutes": int(total_steps * 0.004),
            "SedentaryMinutes": max(0, 1440 - int(total_steps * 0.0075))
        }

        return {
            "Date": date,
            "TotalSteps": total_steps,
            "Calories": calories,
            **active_minutes
        }

    def _generate_sleep_data(self, user: UserProfile, date: datetime) -> dict:
        """Genera datos de sueño realistas"""
        sleep_start, sleep_end = user.sleep_schedule
        
        # Variación en el tiempo de sueño
        is_weekend = date.weekday() >= 5
        base_sleep_hours = 8 if is_weekend else 7
        sleep_variation = np.random.normal(0, 0.5)
        actual_sleep_hours = max(4, min(10, base_sleep_hours + sleep_variation))
        
        # Tiempo en cama (algo más que el tiempo dormido)
        time_in_bed = actual_sleep_hours + np.random.uniform(0.1, 0.3)
        
        return {
            "Date": date,
            "TotalMinutesAsleep": int(actual_sleep_hours * 60),
            "TotalTimeInBed": int(time_in_bed * 60)
        }

    def _generate_weight_data(self, user: UserProfile, date: datetime) -> dict:
        """Genera datos de peso con variaciones realistas"""
        days_since_start = (date - datetime.now().replace(day=1)).days
        
        # Tendencia sutil de peso (±1kg por mes)
        trend = (days_since_start / 30) * np.random.choice([-1, 1]) * 0.1
        
        # Variación diaria normal
        daily_variation = np.random.normal(0, 0.2)
        
        # Peso final
        weight = user.base_weight + trend + daily_variation
        
        # Calcular IMC
        height_m = user.height / 100
        bmi = weight / (height_m * height_m)
        
        return {
            "Date": date,
            "WeightKg": round(weight, 2),
            "BMI": round(bmi, 2)
        }

    def generate_historical_data(self, days: int = 90) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Genera datos históricos para todos los usuarios"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')

        activity_data = []
        sleep_data = []
        weight_data = []

        for user_id, user in self.users.items():
            for date in dates:
                # Datos de actividad (diario)
                activity = self._generate_daily_steps(user, date)
                activity["Id"] = user_id
                activity_data.append(activity)

                # Datos de sueño (diario)
                sleep = self._generate_sleep_data(user, date)
                sleep["Id"] = user_id
                sleep_data.append(sleep)

                # Datos de peso (cada 3 días)
                if date.day % 3 == 0:
                    weight = self._generate_weight_data(user, date)
                    weight["Id"] = user_id
                    weight_data.append(weight)

        return (
            pd.DataFrame(activity_data),
            pd.DataFrame(sleep_data),
            pd.DataFrame(weight_data)
        )

    def generate_realtime_update(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Genera datos en tiempo real para todos los usuarios"""
        now = datetime.now()
        current_hour = now.hour

        activity_data = []
        sleep_data = []
        weight_data = []

        for user_id, user in self.users.items():
            # Datos de actividad
            activity = self._generate_daily_steps(user, now, current_hour)
            activity["Id"] = user_id
            activity_data.append(activity)

            # Datos de sueño (solo si es después de despertar)
            if now.time() > user.sleep_schedule[1]:
                sleep = self._generate_sleep_data(user, now)
                sleep["Id"] = user_id
                sleep_data.append(sleep)

            # Datos de peso (solo una vez al día, en la mañana)
            if now.hour in [6, 7, 8]:
                weight = self._generate_weight_data(user, now)
                weight["Id"] = user_id
                weight_data.append(weight)

        return (
            pd.DataFrame(activity_data),
            pd.DataFrame(sleep_data),
            pd.DataFrame(weight_data)
        )

    def get_user_info(self, user_id: str) -> dict:
        """Obtiene información del usuario"""
        user = self.users.get(user_id)
        if not user:
            return None
        
        return {
            "name": user.name,
            "age": user.age,
            "height": user.height,
            "activity_level": user.activity_level,
            "step_goal": user.step_goal
        }