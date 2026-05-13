# Dashboard de Salud y Bienestar (Fitbit)

Estructura y código para un dashboard interactivo construido con Streamlit.
Carga datos reales de Fitbit (`dailyActivity_merged.csv`, `sleepDay_merged.csv`, `weightLogInfo_merged.csv`)
ubicados en `/data/`.

## Requisitos para Docker
- Docker Desktop instalado
- Docker Compose incluido

## Levantar el proyecto con Docker

1. Clona el repositorio
2. Copia el archivo de variables de entorno:
  cp .env.example .env
3. Edita .env con tus valores
4. Levanta los contenedores:
  docker-compose up --build
5. Abre el navegador en: http://localhost:8501

## Detener el proyecto
docker-compose down

## Borrar datos de la base de datos (reset completo)
docker-compose down -v

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
