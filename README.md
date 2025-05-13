# nothiring!

# 📊 Proyecto de Mentoría con Nothiring — Importación y Procesamiento de Datos con Kedro

Este proyecto forma parte de una mentoría realizada en colaboración con la asociación **Nothiring**. Utiliza [Kedro](https://kedro.readthedocs.io/) para estructurar, importar y preparar datos de forma reproducible, profesional y escalable.

---

## 🧠 Objetivo del proyecto

- Guiar a personas en formación en el uso de herramientas profesionales de ciencia de datos
- Establecer una estructura robusta de trabajo basada en Kedro
- Importar un archivo `.csv` local de forma automatizada y documentada
- Dejar preparado un flujo de trabajo listo para escalar a análisis, modelado o visualización

---

## 🗂 Estructura del proyecto

```bash
nothiring/
├── .gitignore                   # Archivos a excluir del control de versiones
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias del proyecto
├── data/                        # Directorio de datos (excluido por Git)
│   ├── 01_raw/                  # Datos originales importados
│   ├── 02_intermediate/         # Datos transformados intermedios
│   ├── 03_primary/              # Datos preparados para modelado
│   ├── 04_feature/              # Datos con features extraídas
│   └── 05_model_input/          # Datos listos para modelar
├── conf/                        # Configuración de Kedro
│   ├── base/                    # Config común (datasets, parámetros)
│   │   ├── catalog.yml          # Registro de datasets
│   │   ├── parameters.yml       # Parámetros del pipeline
│   └── local/                   # Config local (opcional, excluida por Git)
├── logs/                        # Archivos de log (opcional)
├── src/                         # Código fuente del proyecto
│   └── nothiring/               # Paquete raíz del proyecto
│       ├── __init__.py
│       ├── pipelines/           # Pipelines Kedro
│       │   ├── import_data/     # Pipeline para importar CSV local
│       │   │   └── pipeline.py
│       │   └── utils/           # Funciones auxiliares (ej. mover archivos)
│       │       └── import_local.py
│       └── pipeline_registry.py # Registro de pipelines del proyecto
