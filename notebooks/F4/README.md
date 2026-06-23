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
│   ├── F3/
│   │   ├── F3_Modelado.ipynb
│   │   └── README.md     #ejecución de la fase 3
│   └── F4/
│       ├── F4_Modelado.ipynb
│       └── README.md     #ejecución de la fase 4
├── src/                   # módulo reutilizable (Analizador.py)
├── docs/                  # documentación técnica y guías
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
### Fase 4 — Análisis, reproducibilidad y comunicación de resultados

## Módulo reutilizable (`src/Analizador.py`)

F4 reutiliza sin modificaciones las clases ya implementadas en F3, evidenciando
la reproducibilidad del módulo entre fases:

| Clase | Tipo | Responsabilidad |
|-------|------|-----------------|
| `Transformador` | ABC | Contrato común: define `aplicar(df)` |
| `ExcluirColumna` | Subclase | Elimina columnas sin valor predictivo |
| `EliminarDuplicados` | Subclase | Garantiza integridad del dataset |
| `ImputarMediana` | Subclase | Imputa NaN con mediana (robusta a outliers) |
| `NormalizarMinMax` | Subclase | Escala features al rango [0, 1] |
| `Pipeline` | Composición | Orquesta etapas con polimorfismo |
| `AnalizadorDiabetes` | Encapsulamiento | Análisis exploratorio con caché interno |

```bash
jupyter notebook F4/F4_Modelado.ipynb
```
**Requisito previo:** F3 debe haberse ejecutado (o `src/Analizador.py` debe estar
disponible) para disponer de las clases del pipeline y de `data/processed/diabetes_clean.csv`.

El notebook implementa:

- **Integración F1-F4** — reconstruye el flujo completo desde la carga del dataset
  RAW hasta las conclusiones finales, reutilizando el pipeline POO y la clase
  `AnalizadorDiabetes` sin modificaciones respecto a F3.
- **Storytelling en tres actos** — visualizaciones analíticas estructuradas como
  narrativa de datos:
  - **Acto 1 (Contexto):** distribución de la variable objetivo (balance 67/33).
  - **Acto 2 (Conflicto):** Pregnancies como variable más discriminativa por
    diferencia de medias entre clases.
  - **Acto 3 (Resolución):** mapa de correlaciones de Pearson con la variable
    objetivo (heatmap + barras con umbrales de Cohen, 1988).
- **Metodología y trazabilidad** — tabla comparativa de herramientas y mejoras
  aplicadas en cada fase (F1 → F4).
- **Reflexión crítica** — discusión sobre limitaciones de la correlación lineal
  de Pearson (caso PlasmaGlucose) y sobre la interpretabilidad clínica tras la
  normalización Min-Max.
- **Conclusiones** — síntesis de hallazgos principales, eficiencia algorítmica
  (merge sort recursivo O(p·log p); vectorización con speedup de uno a dos
  órdenes de magnitud frente al bucle iterativo, variable según ejecución) y
  modularidad del proyecto.

---

## Estrategia de ramas

| Rama | Propósito |
|------|-----------|
| main | Versión estable revisada por el equipo. Merge al cerrar cada fase |
| dev | Integración del equipo. Punto de convergencia antes de main |
| dev-daniel | Desarrollo activo de Daniel Hormazábal |
| dev-enso | Desarrollo activo de Enso Guidotti |
| dev-cristian | Desarrollo activo de Cristian Pasten |
