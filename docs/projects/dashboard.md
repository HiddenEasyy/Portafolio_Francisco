# Dashboard de Salud y Bienestar (Fitbit)

Resumen
--

Proyecto para visualizar datos personales de Fitbit mediante un dashboard interactivo (Streamlit). Incluye análisis de actividad física, sueño y peso.

Estructura (en este repositorio)
--

- `src/` — Código principal del dashboard.
- `data/` — CSV con datos: `dailyActivity_merged.csv`, `sleepDay_merged.csv`, `weightLogInfo_merged.csv`.
- `notebooks/` — Exploración y análisis previos.
- `assets/` — Iconos y gráficos.

Cómo ejecutar localmente
--

1. Crear y activar entorno (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Ejecutar el dashboard (ejemplo con Streamlit):

```powershell
streamlit run src/app.py
```

Capturas
--

Incluye las imágenes en el repositorio (`assets/`) que pueden mostrarse aquí o en `projects/Dashboard_Salud/screenshots/`.

Notas
--

Si quieres que reestructure el repositorio para mover este proyecto a `projects/Dashboard_Salud/` lo puedo hacer (esto cambiará rutas relativas). De momento mantengo la estructura actual y documento cómo ejecutarlo.
