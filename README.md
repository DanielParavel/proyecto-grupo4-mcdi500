# Proyecto Grupo 4 — MCDIA500

## Predicción de Diabetes — Pima Indians Dataset

**Curso:** MCDIA500 — Programación para la Ciencia de Datos  
**Integrantes:** Daniel Hormazábal, Cristian Pasten, Enso Guidotti  
**Docente:** Omar Salinas Silva  

---

## Dataset

- **Nombre:** Pima Indians Diabetes Database (versión extendida)
- **Fuente:** Kaggle (Mathchi, 2023)
- **Registros:** 15.000 · **Variables:** 9 predictoras + 1 objetivo (Diabetic)
- **Datos crudos:** `data/raw/diabetes.csv`
- **Datos procesados:** `data/processed/diabetes_clean.csv`

---

## Descripción

Proyecto transversal de análisis predictivo sobre el dataset Pima Indians Diabetes
(Kaggle), orientado a clasificar pacientes con riesgo de diabetes tipo 2 mediante
variables clínicas estructuradas, aplicando el marco metodológico CRISP-DM en un
entorno de programación científica reproducible, colaborativo y trazable.

---

## Estructura del repositorio

```
proyecto-grupo4-mcdi500/
├── data/
│   ├── raw/              # diabetes.csv — datos originales sin modificar
│   └── processed/        # diabetes_clean.csv — generado por F2
├── docs/                 # documentación técnica y guías
├── notebooks/
│   ├── F1_Definicion.ipynb
│   ├── F2_Preprocesamiento.ipynb
│   ├── F3/
│   │    ├── F3_Modelado.ipynb 
│   │    └── README.md     # ejecución de la fase 3
│   └── F4/
│       └── F4_Visualizacion.ipynb 
├── src/              # scripts Python modulares
│   └── Analizador.py 
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Instalación del entorno

```bash
# Clonar el repositorio
git clone git@github.com:DanielParavel/proyecto-grupo4-mcdi500.git
cd proyecto-grupo4-mcdi500

# Crear entorno virtual
# macOS
python3.11 -m venv venv
source venv/bin/activate

# Windows (Git Bash)
py -3.11 -m venv venv
source venv/Scripts/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecución

### Fase 1 — Definición e inspección

```bash
jupyter notebook notebooks/F1_Definicion.ipynb
```

### Fase 2 — Preprocesamiento y transformación

```bash
jupyter notebook notebooks/F2_Preprocesamiento.ipynb
```

Al ejecutar F2 con **Kernel → Restart & Run All**, se genera automáticamente
`data/processed/diabetes_clean.csv` (15.000 filas × 9 columnas, normalizado).


---
### Fase 3 — Núcleo algorítmico, eficiencia e implementación orientada a objetos

```bash
jupyter notebook F3/F3_Modelado.ipynb
```
**Requisito previo:** F2 debe haberse ejecutado para disponer de 
`data/processed/diabetes_clean.csv`.

---
### Fase 4 — Visualizaciones analíticas y comunicación de resultados

```bash
jupyter notebook notebooks/F4/F4_Visualizacion.ipynb
```

Ejecutar con **Kernel → Restart & Run All**. El notebook carga los datos crudos
directamente desde `data/raw/diabetes.csv`, ejecuta el pipeline POO desde
`src/Analizador.py` y exporta automáticamente los tres gráficos analíticos a `docs/`.
No requiere ejecución previa de F2 o F3.

---
## Fases del proyecto

| Fase | Descripción | Notebook | Estado |
|------|-------------|----------|--------|
| F1 | Definición del problema y configuración del entorno | F1_Definicion.ipynb | ✓ Completada |
| F2 | Obtención, limpieza y transformación de datos | F2_Preprocesamiento.ipynb | ✓ Completada |
| F3 | Núcleo algorítmico, eficiencia e implementación POO | F3/F3_Modelado.ipynb | ✓ Completada |
| F4 | Visualizaciones analíticas y comunicación de resultados | F4/F4_Visualizacion.ipynb | ✓ Completada |
---


## Estrategia de ramas

| Rama | Propósito |
|------|-----------|
| main | Versión estable revisada por el equipo. Merge al cerrar cada fase |
| dev | Integración del equipo. Punto de convergencia antes de main |
| dev-daniel | Desarrollo activo de Daniel Hormazábal |
| dev-enso | Desarrollo activo de Enso Guidotti |
| dev-cristian | Desarrollo activo de Cristian Pasten |