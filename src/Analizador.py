"""
src/Analizador.py

Contiene el pipeline de preprocesamiento POO y la clase de análisis
exploratorio avanzado. Importable desde cualquier notebook del proyecto.

Uso
---
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
    from Analizador import (Transformador, ExcluirColumna, EliminarDuplicados,
                            ImputarMediana, NormalizarMinMax, Pipeline,
                            AnalizadorDiabetes)

"""

from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# CLASE BASE ABSTRACTA
class Transformador(ABC):
    """
    Contrato común para todas las transformaciones del pipeline.
    Define la interfaz que cada transformación concreta debe implementar.

    Principio: herencia + polimorfismo — la clase Pipeline puede
    tratar cualquier transformador de forma idéntica.
    """

    @abstractmethod
    def aplicar(self, df):
        """Aplica la transformación al DataFrame y retorna el resultado."""
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}()"


# RANSFORMACIONES CONCRETAS (herencia)
class ExcluirColumna(Transformador):
    """
    Excluye una columna del DataFrame.
    Uso: eliminar identificadores sin valor predictivo (PatientID).
    """

    def __init__(self, columna):
        self._columna = columna  # atributo encapsulado

    def aplicar(self, df):
        if self._columna not in df.columns:
            print(f"  [ExcluirColumna] '{self._columna}' no encontrada — omitida")
            return df
        resultado = df.drop(columns=[self._columna])
        print(f"  [ExcluirColumna] '{self._columna}' excluida ✓")
        return resultado


class EliminarDuplicados(Transformador):
    """
    Elimina filas duplicadas del DataFrame.
    """

    def aplicar(self, df):
        n_antes = len(df)
        resultado = df.drop_duplicates()
        n_eliminados = n_antes - len(resultado)
        print(f"  [EliminarDuplicados] {n_eliminados} duplicados eliminados ✓")
        return resultado


class ImputarMediana(Transformador):
    """
    Imputa valores nulos con la mediana de cada columna especificada.
    Se eligió mediana sobre media por su robustez ante outliers (UNAB, 2026b).
    """

    def __init__(self, columnas = None):
        # None = aplicar a todas las columnas numéricas excepto el target
        self._columnas = columnas

    def aplicar(self, df):
        cols = self._columnas if self._columnas else df.select_dtypes(include=[np.number]).columns.tolist()
        n_imputados = 0
        for col in cols:
            n_na = df[col].isnull().sum()
            if n_na > 0:
                mediana = df[col].median()
                df = df.copy()
                df[col] = df[col].fillna(mediana)
                n_imputados += n_na
        print(f"  [ImputarMediana] {n_imputados} valores imputados ✓")
        return df


class NormalizarMinMax(Transformador):
    """
    Normaliza columnas numéricas al rango [0, 1] con Min-Max.
    Fórmula: x_norm = (x - x_min) / (x_max - x_min)

    Se excluye la variable objetivo (Diabetic) por ser binaria categórica.
    """

    def __init__(self, excluir = None):
        self._excluir = excluir or []

    def aplicar(self, df):
        excluir_final = set(self._excluir + ['Diabetic'])
        cols_num = [c for c in df.select_dtypes(include=[np.number]).columns
                    if c not in excluir_final]
        resultado = df.copy()
        for col in cols_num:
            x_min, x_max = resultado[col].min(), resultado[col].max()
            rango = x_max - x_min
            if rango > 0:
                resultado[col] = (resultado[col] - x_min) / rango
        print(f"  [NormalizarMinMax] {len(cols_num)} columnas normalizadas ✓")
        return resultado


# PIPELINE: composición + polimorfismo
class Pipeline:
    """
    Orquesta una secuencia de transformaciones aplicando polimorfismo:
    ejecuta aplicar(df) sobre cada etapa sin saber cuál es.

    Principio de composición: 'tiene' etapas en lugar de 'ser' una.
    Principio de polimorfismo: trata todas las etapas igual a través
    del contrato definido en Transformador.

    Atributos
    ---------
    _etapas : list[Transformador] — Lista de transformaciones (encapsulada).
    """

    def __init__(self, etapas):
        # Validar que todas las etapas implementan el contrato
        for e in etapas:
            if not isinstance(e, Transformador):
                raise TypeError(f"{e} no es una instancia de Transformador")
        self._etapas = etapas  # atributo protegido

    def ejecutar(self, df):
        """Ejecuta las etapas en orden aplicando polimorfismo."""
        print(f"Pipeline iniciado — {len(self._etapas)} etapas\n")
        resultado = df.copy()
        for i, etapa in enumerate(self._etapas, 1):
            print(f"Etapa {i}/{len(self._etapas)}: {etapa}")
            resultado = etapa.aplicar(resultado)
        print(f"\nPipeline completado ✓  →  {resultado.shape[0]:,} × {resultado.shape[1]}")
        return resultado

    def listar_etapas(self):
        """Muestra las etapas configuradas."""
        for i, e in enumerate(self._etapas, 1):
            print(f"  {i}. {e}")


# ANALIZADOR DE DIABETES
class AnalizadorDiabetes:
    """
    Encapsula el análisis exploratorio avanzado del dataset de diabetes.
    Trabaja sobre el dataset ya procesado por el Pipeline.

    Principio de encapsulamiento:
    - _df y _resultados son atributos protegidos
    - Solo se exponen a través de métodos públicos

    Atributos
    ---------
    _df : Dataset procesado (protegido).
    _features : Variables predictoras.
    _target : Variable objetivo.
    _resultados : Cache de resultados calculados.
    """

    def __init__(self, df, features, target):
        self._df        = df.copy()       # estado encapsulado
        self._features  = features
        self._target    = target
        self._resultados = {}             # cache de resultados
        print(f"AnalizadorDiabetes inicializado ✓")
        print(f"  Filas    : {self._df.shape[0]:,}")
        print(f"  Features : {len(self._features)}")
        print(f"  Target   : '{self._target}'")

    def calcular_estadisticos_por_clase(self):
        """
        Calcula media, mediana y std por clase para cada feature.
        Complejidad: O(n·p) — itera sobre n filas por p features.
        """
        clases = sorted(self._df[self._target].unique())
        tabla  = []
        for feature in self._features:
            fila = {'Feature': feature}
            for clase in clases:
                vals     = self._df.loc[self._df[self._target] == clase, feature]
                etiqueta = 'No diabético' if clase == 0 else 'Diabético'
                fila[f'Media ({etiqueta})']   = round(vals.mean(), 4)
                fila[f'Mediana ({etiqueta})'] = round(vals.median(), 4)
                fila[f'Std ({etiqueta})']     = round(vals.std(), 4)
            fila['Δ Media (1-0)'] = round(
                abs(fila['Media (Diabético)'] - fila['Media (No diabético)']), 4
            )
            tabla.append(fila)
        resultado = pd.DataFrame(tabla).set_index('Feature')
        self._resultados['estadisticos_por_clase'] = resultado
        return resultado

    def detectar_outliers_iqr(self):
        """
        Detecta outliers con criterio IQR de Tukey.
        Complejidad: O(n·p) — una pasada por cada feature.
        """
        tabla = []
        for feature in self._features:
            vals    = self._df[feature]
            q1, q3  = vals.quantile(0.25), vals.quantile(0.75)
            iqr     = q3 - q1
            li, ls  = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            n_out   = int(((vals < li) | (vals > ls)).sum())
            tabla.append({
                'Feature': feature, 'Q1': round(q1, 4), 'Q3': round(q3, 4),
                'IQR': round(iqr, 4), 'Lím. Inf': round(li, 4),
                'Lím. Sup': round(ls, 4), 'N Outliers': n_out,
                '% Outliers': round(n_out / len(vals) * 100, 2),
            })
        resultado = pd.DataFrame(tabla).set_index('Feature')
        self._resultados['outliers_iqr'] = resultado
        return resultado

    def calcular_correlaciones(self):
        """
        Matriz de correlación de Pearson.
        Complejidad: O(n·p²) — p² pares de variables.
        """
        cols    = self._features + [self._target]
        matriz  = self._df[cols].corr(method='pearson').round(4)
        self._resultados['correlaciones'] = matriz
        return matriz

    def rankear_variables_recursivo(self):
        """Rankea features por correlación absoluta usando merge sort recursivo."""
        if 'correlaciones' not in self._resultados:
            self.calcular_correlaciones()
        corr        = self._resultados['correlaciones'][self._target]
        lista_pares = [(f, corr[f]) for f in self._features]
        lista_ord   = AnalizadorDiabetes._merge_sort_recursivo(lista_pares)
        resultado   = pd.DataFrame(lista_ord, columns=['Feature', 'Correlación'])
        resultado['|Correlación|'] = resultado['Correlación'].abs().round(4)
        resultado.index = range(1, len(resultado) + 1)
        resultado.index.name = 'Rank'
        self._resultados['ranking_variables'] = resultado
        return resultado

    def comparar_distribuciones_por_clase(self, n_top = 4):
        """Histogramas superpuestos por clase para los n features más correlacionados."""
        if 'ranking_variables' not in self._resultados:
            self.rankear_variables_recursivo()
        top  = self._resultados['ranking_variables']['Feature'].head(n_top).tolist()
        df0  = self._df[self._df[self._target] == 0]
        df1  = self._df[self._df[self._target] == 1]
        fig, axes = plt.subplots(1, n_top, figsize=(15, 4))
        for i, feature in enumerate(top):
            axes[i].hist(df0[feature], bins=30, alpha=0.6, color='steelblue', label='No diabético (0)', edgecolor='white')
            axes[i].hist(df1[feature], bins=30, alpha=0.6, color='coral', label='Diabético (1)', edgecolor='white')
            axes[i].set_title(feature, fontweight='bold', fontsize=10)
            axes[i].set_xlabel('Valor normalizado')
            axes[i].legend(fontsize=8)
            axes[i].grid(True, alpha=0.3)
        plt.suptitle('Distribución por clase — top 4 features más correlacionadas', fontsize=12, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def _merge_sort_recursivo(lista):
        """
        Ordena lista de (feature, correlación) por correlación absoluta descendente.
        Complejidad: O(p·log p)

        Caso base: lista de 0 o 1 elementos (ya ordenada).
        Caso recursivo: dividir, ordenar cada mitad y combinar.
        """
        # CASO BASE
        if len(lista) <= 1:
            return lista

        # CASO RECURSIVO: dividir y conquistar
        mid       = len(lista) // 2
        izquierda = AnalizadorDiabetes._merge_sort_recursivo(lista[:mid])
        derecha   = AnalizadorDiabetes._merge_sort_recursivo(lista[mid:])

        return AnalizadorDiabetes._merge(izquierda, derecha)

    @staticmethod
    def _merge(izq, der):
        """Combina dos sublistas ordenadas por correlación absoluta descendente."""
        resultado = []
        i = j = 0
        while i < len(izq) and j < len(der):
            if abs(izq[i][1]) >= abs(der[j][1]):
                resultado.append(izq[i]); i += 1
            else:
                resultado.append(der[j]); j += 1
        resultado.extend(izq[i:])
        resultado.extend(der[j:])
        return resultado