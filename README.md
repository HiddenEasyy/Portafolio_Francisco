# Dashboard de Salud y Bienestar (Fitbit)

Estructura y código para un dashboard interactivo construido con Streamlit.
Carga datos reales de Fitbit (`dailyActivity_merged.csv`, `sleepDay_merged.csv`, `weightLogInfo_merged.csv`)
ubicados en `/data/`.

## Ejecutar localmente

1. Crear y activar entorno:
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
