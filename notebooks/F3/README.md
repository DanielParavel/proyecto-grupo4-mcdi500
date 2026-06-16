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
├── notebooks/
│   ├── F1_Definicion.ipynb
│   ├── F2_Preprocesamiento.ipynb
│   └── F3/
│       ├── F3_Modelado.ipynb 
│       └── README.md     #ejecución de la fase 3
├── docs/                 # documentación técnica y guías
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
# macOS / Linux
python3.11 -m venv venv
source venv/bin/activate

# Windows (Git Bash)
py -3.11 -m venv venv
source venv/Scripts/activate

# Instalar dependencias
pip install -r requirements.txt
```

---
### Fase 3 — Núcleo algorítmico, eficiencia e implementación orientada a objetos

```bash
jupyter notebook F3/F3_Modelado.ipynb
```
**Requisito previo:** F2 debe haberse ejecutado para disponer de 
`data/processed/diabetes_clean.csv`.

El notebook implementa:

- **Pipeline POO** — jerarquía `Transformador` (ABC) con 4 subclases concretas
  (`ExcluirColumna`, `EliminarDuplicados`, `ImputarMediana`, `NormalizarMinMax`)
  y clase `Pipeline` con composición y polimorfismo.
- **Validación técnica** — 5 pruebas formales con `assert`/`try-except` cubriendo
  casos normal, límite y excepción.
- **Clase `AnalizadorDiabetes`** — estadísticos por clase, outliers IQR,
  correlaciones Pearson y ranking de variables.
- **Merge sort recursivo** — `_merge_sort_recursivo()` y `_merge()` como
  `@staticmethod` dentro de `AnalizadorDiabetes`. Complejidad O(p·log p).
- **Mediciones con `timeit`** — escalamiento sobre 5 tamaños (1k → 15k filas)
  y comparación iterativo vs. vectorizado (~41× speedup).
- **Complejidad espacial** — medición con `tracemalloc`.

---

## Estrategia de ramas

| Rama | Propósito |
|------|-----------|
| main | Versión estable revisada por el equipo. Merge al cerrar cada fase |
| dev | Integración del equipo. Punto de convergencia antes de main |
| dev-daniel | Desarrollo activo de Daniel Hormazábal |
| dev-enso | Desarrollo activo de Enso Guidotti |
| dev-cristian | Cristián esta utilizando git de manera local por problemas con GITHUB |