import pandas as pd
import numpy as np
from tkinter import Tk
from tkinter import filedialog
import os
import argparse

# VER SI ESTOY O NO EN MODO VERBOSE
# Crear el parser de argumentos
parser = argparse.ArgumentParser(description="Programa con modo verbose")
# Añadir el argumento 'verbose' como una opción booleana
parser.add_argument('--verbose', action='store_true', help="Activar modo verbose")
# Parsear los argumentos
args = parser.parse_args()
# Verificar si el modo verbose está activado
verbose = args.verbose

# Función para seleccionar el archivo y verificar el formato
def seleccionar_archivo(numero_documento):
    # Ocultar la ventana principal de Tkinter
    root = Tk()
    root.withdraw()

    # Abrir el cuadro de diálogo para seleccionar un archivo
    archivo_seleccionado = filedialog.askopenfilename(
        title="Seleccionar archivo " + str(numero_documento),
        filetypes=[("Archivos Excel", "*.xls *.xlsx")]
    )

    # Verificar si el archivo es xls o xlsx
    if archivo_seleccionado and archivo_seleccionado.endswith(('.xls', '.xlsx')):
        return archivo_seleccionado
    else:
        print("El archivo seleccionado no es válido. Debe ser un archivo .xls o .xlsx.")
        return None
    
# Función para listar las columnas y pedir al usuario que seleccione cuál usar
def seleccionar_columnas(dataframe, alias_archivo, nombres_opcionales):
    print(f"\nColumnas disponibles en {alias_archivo}:")
    columnas = dataframe.columns.tolist()
    for idx, col in enumerate(columnas, start=1):
        print(f"{idx}. {col}")
    
    # Función para obtener una entrada válida del usuario
    def obtener_columna(prompt):
        while True:
            try:
                seleccion = int(input(prompt))
                if 1 <= seleccion <= len(columnas):
                    return columnas[seleccion - 1]
                else:
                    print(f"Por favor, selecciona un número entre 1 y {len(columnas)}.")
            except ValueError:
                print("Entrada inválida. Debe ser un número.")

    # Preguntar al usuario qué columna utilizar para cada campo obligatorio
    cod_col = obtener_columna("Selecciona la columna para 'Cod': ")
    nom_col = obtener_columna("Selecciona la columna para 'Nom': ")

    # Lista para guardar los nombres y columnas opcionales seleccionadas
    columnas_opcionales_seleccionadas = {}

    # Si se indicó seleccionar columnas opcionales
    opc = len(nombres_opcionales)
    contador_opcionales = 3  # Empezamos desde Campo3
    contador_nombres_opcionales = 0
    while opc > 0:
        # Preguntar cuál es la columna en el archivo para la columna opcional
        col_opcional = obtener_columna(f"Selecciona la columna para '{nombres_opcionales[contador_nombres_opcionales]}': ")

        # Agregar la columna opcional seleccionada
        nombre_campo = f'Campo{contador_opcionales}'
        columnas_opcionales_seleccionadas[nombre_campo] = col_opcional

        # Incrementar el contador para el siguiente nombre de campo
        contador_opcionales += 1
        # Incrementar el contador para el siguiente nombre opcional
        contador_nombres_opcionales += 1
        # Decrementar el contador de columnas opcionales restantes
        opc -= 1

    # Crear una lista con todas las columnas seleccionadas (obligatorias y opcionales)
    columnas_finales = [cod_col, nom_col] + list(columnas_opcionales_seleccionadas.values())
    
    # Crear un diccionario para el renombrado final de las columnas
    columnas_renombradas = {
        cod_col: 'Cod',
        nom_col: 'Nom'
    }
    # Añadir las opcionales renombradas, por ejemplo: "Cat" -> "Campo3"
    for campo, col_opcional in columnas_opcionales_seleccionadas.items():
        columnas_renombradas[col_opcional] = campo

    # Renombrar las columnas seleccionadas (y retorno tambien la lista de nombres opcionales para futuro uso)
    return dataframe[columnas_finales].rename(columns=columnas_renombradas)

# Seleccionar y cargar los archivos
titulo_documento_1 = seleccionar_archivo(1)
titulo_documento_2 = seleccionar_archivo(2)

# Verificar si se seleccionaron archivos válidos
if titulo_documento_1 and titulo_documento_2:
    # Pedir al usuario un alias para los archivos seleccionados
    alias_documento_1 = input(f"Ingresa un alias para el archivo '{titulo_documento_1}': ")
    alias_documento_2 = input(f"Ingresa un alias para el archivo '{titulo_documento_2}': ")

    # Cargar los archivos
    documento_1 = pd.read_excel(titulo_documento_1, dtype=str)
    documento_2 = pd.read_excel(titulo_documento_2, dtype=str)
    print("Archivos cargados exitosamente.")
    
    # Loop para confirmar selección de columnas
    confirmacion = 'no'
    while confirmacion == 'no':
        # Consultar si desea seleccionar columnas opcionales
        opcionales = int(input("¿Deseas seleccionar columnas opcionales? Indicar cantidad (0 si no deseas seleccionar ninguna): "))
        while opcionales > 1:
            opcionales = int(input("Indique un número menor a 2. Por el momento solo se permite una columna opcional (0 si no deseas seleccionar ninguna): "))
        
        # Guardar los nombres para las columnas opcionales
        nombres_opcionales = []
        for i in range(opcionales):  # Iterar opcionales veces
            nombre_opcional = input(f"Ingresa el nombre para la columna opcional {i+1}: ")
            nombres_opcionales.append(nombre_opcional)


        # Permitir al usuario seleccionar las columnas para cada archivo (y recupero los nombres opcionales proporcionados por el mismo)
        documento_1 = seleccionar_columnas(documento_1, alias_documento_1, nombres_opcionales)
        documento_2 = seleccionar_columnas(documento_2, alias_documento_2, nombres_opcionales)

        print("\nDocumentos finales con las columnas seleccionadas:")
        print(f"{alias_documento_1}:\n", documento_1.head())
        print("\n")	# Salto de línea
        print(f"{alias_documento_2}:\n", documento_2.head())
        print("\n")	# Salto de línea

        confirmacion = input("¿Estás satisfecho con la selección de columnas? (si/no): ").lower()
        print("\n")	# Salto de línea
    print("Selección de columnas confirmada. Procesando archivos...")
    print("\n")	# Salto de línea
else:
    print("No se pudo cargar uno o más archivos.")
    print("\n")	# Salto de línea

#######################################################
# DATAFRAMES PARA PRUEBAS
# data1 = {
#     'Cod': ['A', 'A', 'A', 'B', 'B', 'I', ''],
#     'Nom': ['A', 'B', '', 'B', 'A', '', 'C'],
#     'Campo3': ['1', '', '1', '2', '1', '2', '2'],
# }
# documento_1 = pd.DataFrame(data1)

# data2 = {
#     'Cod': ['A', 'B', 'I', '', 'C', 'A', 'A', 'T', 'B', '', 'A'],
#     'Nom': ['', 'B', '', 'C', 'A', 'B', 'A', 'D', 'D', 'D', ''],
#     'Campo3': ['1', '1', '1', '', '2', '', '1', '1', '1', '2', '2'],
# }
# documento_2 = pd.DataFrame(data2)
#######################################################

# Cantidad de filas por archivo antes de simplificar
print("LEYENDO DATOS...")
print("Cantidad original de filas/elementos del documento 1 ->", documento_1.shape[0])
print("Cantidad original de filas/elementos del documento 2 ->",documento_2.shape[0])
print("\n")	# Salto de línea

def process_missing_fields(df, num_missing_fields, num_fields):   
    # Paso 1: Filtrar filas con un número específico de campos faltantes

    # Inicializar la lista con las columnas obligatorias
    columnas_seleccionadas = ['Nom', 'Cod']

    # Verificar si hay columnas opcionales y agregarlas dinámicamente
    for i in range(3, 3 + opcionales):  # Comienza en Campo3, luego Campo4, etc.
        columnas_seleccionadas.append(f'Campo{i}')

    # `df[columnas_seleccionadas]` selecciona las columnas relevantes
    # `replace('', np.nan)` convierte valores vacíos en NaN para un tratamiento uniforme
    df_replace = df[columnas_seleccionadas].replace('', np.nan)

    # `isna().sum(axis=1)` cuenta el número de valores NaN en cada fila
    # `== num_missing_fields` selecciona las filas que tienen exactamente `num_missing_fields` campos faltantes
    df_missing = df_replace[df_replace.isna().sum(axis=1) == num_missing_fields]

    # Si num_missing_fields es igual a num_fields (es decir, todas las columnas están vacías), elimino todas las filas vacías
    if num_missing_fields == num_fields:
        df = df.drop(df_missing.index)
        return df
    # Si el numero de filas de df_missing es 0 retorno df tal y cómo está (abortar función)
    if df_missing.shape[0] == 0:
        return df
    
    # Paso 2: Mantener las filas que no tienen el número de campos faltantes especificado
    df_remaining = df[~df.index.isin(df_missing.index)]

    # Función auxiliar para encontrar una fila más completa en `df_complete` que coincida con los campos no faltantes de `row`
    def find_complete_row(row, df_complete, non_nan_columns):
        # Comparar cada fila en `df_complete` con la fila `row`
        condition = (df_complete[non_nan_columns] == row[non_nan_columns]).all(axis=1)
        matches = df_complete[condition]
        
        if not matches.empty:
            return matches.iloc[0]  # Retornar la primera coincidencia completa
        return None  # Retornar None si no se encuentra una coincidencia

    # Paso 3: Procesar cada fila con campos faltantes
    rows_to_remove = []  # Lista para almacenar índices de filas a eliminar
    for idx, row in df_missing.iterrows():
        # Buscar una fila más completa en `df_remaining`
        non_nan_columns = [col for col in row.index if pd.notna(row[col]) and row[col] != ''] # Lista de columnas no vacías
        complete_row = find_complete_row(row, df_remaining, non_nan_columns)
        
        # Si encontré una fila más completa que coincide con los campos no faltantes de `row`, elimino `row` (se absorbe)
        if complete_row is not None:
            rows_to_remove.append(idx)
    
    # Eliminar las filas del DataFrame original
    df_cleaned = df.drop(index=rows_to_remove)
    return df_cleaned

# Simplificar los archivos, eliminando filas redundantes
def simplify_df(df):
    # Eliminar filas duplicadas
    df = df.drop_duplicates()

    # Iterar desde la cantidad total de campos faltantes hasta 1 para ir absorviendo filas incompletas
    num_fields = 2 + opcionales # 2 campos obligatorios + cantidad de campos opcionales

    for num_missing in range(num_fields, 0, -1):
        df = process_missing_fields(df, num_missing, num_fields)
    
    return df


print("SIMPLIFICANDO...")
documento_1 = simplify_df(documento_1)
documento_2 = simplify_df(documento_2)

# Crear las rutas para los archivos simplificados dentro de la carpeta de salida
# Crear el nombre de la carpeta con los alias
carpeta_salida = f"Resultados/{alias_documento_1}-{alias_documento_2}"

# Verificar si la carpeta existe, si no, crearla
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

# Guardar las tablas simplificadas en nuevos archivos y contar las filas
ruta_documento1_simpl = os.path.join(carpeta_salida, os.path.splitext(os.path.basename(titulo_documento_1))[0] + ' Simplificado.xlsx')
ruta_documento2_simpl = os.path.join(carpeta_salida, os.path.splitext(os.path.basename(titulo_documento_2))[0] + ' Simplificado.xlsx')

cant_documento1 = documento_1.shape[0]
cant_documento2 = documento_2.shape[0]

documento_1.to_excel(ruta_documento1_simpl, index=False)
documento_2.to_excel(ruta_documento2_simpl, index=False)

# Imprimir la cantidad de filas y la ruta de guardado para cada archivo
print(f"Nueva cantidad de filas/elementos del documento 1 -> {cant_documento1} (Disponible en: {ruta_documento1_simpl})")
print(f"Nueva cantidad de filas/elementos del documento 2 -> {cant_documento2} (Disponible en: {ruta_documento2_simpl})")

# Definición de nombres a usar en el DataFrame final
titulo_cod_documento_1 = f'Cod_{alias_documento_1}'
titulo_nom_documento_1 = f'Nom_{alias_documento_1}'
titulos_opcionales_doc1 = [f'{nombre}_{alias_documento_1}' for nombre in nombres_opcionales]

titulo_cod_documento_2 = f'Cod_{alias_documento_2}'
titulo_nom_documento_2 = f'Nom_{alias_documento_2}'
titulos_opcionales_doc2 = [f'{nombre}_{alias_documento_2}' for nombre in nombres_opcionales]

# Chequeo de consistencia
def mover_datos_doc2(result, match_idx):
    # Crear la estructura básica de la nueva fila con las columnas 'Cod' y 'Nom'
    new_row = {
        'Cod': result.loc[match_idx, titulo_cod_documento_2],
        'Nom': result.loc[match_idx, titulo_nom_documento_2],
    }
    # Si hay columnas opcionales, agregarlas dinámicamente
    for i in range(opcionales):  # 'opcionales' indica la cantidad de columnas opcionales y el rango va de 0 a 'opcionales' - 1
        new_row[f'Campo{i + 3}'] = result.loc[match_idx, titulos_opcionales_doc2[i]]

    # Intento reubicar los datos REDATAM de la fila match_idx a una nueva fila usando concurrencia
    result = procesar_fila(new_row, result)
    if verbose:
        print("Fila movida")
    return result

def actualizar_fila_coincidente(result, match_idx, row):
    result.loc[match_idx, titulo_cod_documento_2] = row['Cod']
    result.loc[match_idx, titulo_nom_documento_2] = row['Nom']
    # Si hay columnas opcionales, las actualizo dinámicamente
    for i in range(opcionales):  # 'opcionales' indica la cantidad de columnas opcionales y el rango va de 0 a 'opcionales' - 1
        result.loc[match_idx, titulos_opcionales_doc2[i]] = row[f'Campo{i + 3}']

    if verbose:
        print("Fila actualizada:")
        print(result.loc[match_idx])

def nueva_fila(result, row):
    # Agregego los campos obligatorios de documento_1
    new_row = {
        titulo_cod_documento_1: '',
        titulo_nom_documento_1: '',
    }

    # Inserto las columnas opcionales de documento_1 si existen
    for i in range(opcionales):
        new_row[titulos_opcionales_doc1[i]] = ''

    # Inserto los campos obligatorios de documento_2
    new_row[titulo_cod_documento_2] = row['Cod']
    new_row[titulo_nom_documento_2] = row['Nom']

    # Inserto las columnas opcionales de documento_2 si existen
    for i in range(opcionales):  # 'opcionales' indica la cantidad de columnas opcionales y el rango va de 0 a 'opcionales' - 1
        new_row[titulos_opcionales_doc2[i]] = row[f'Campo{i + 3}']
    
    result = pd.concat([result, pd.DataFrame([new_row])], ignore_index=True)
    return result

def procesar_fila(row, result):
    if verbose:
        print("\n")	# Salto de línea
        print("Fila a procesar: ")
        print(row)

    # Coincidencia por Cod y Nom
    Cod_match = result[titulo_cod_documento_1] == row['Cod']
    Nom_match = result[titulo_nom_documento_1] == row['Nom']
    Cod_Nom_match = Cod_match & Nom_match

    ## Defino la lista de columnas del documento 2 a evaluar a continuación
    columnas_a_evaluar = [titulo_cod_documento_2, titulo_nom_documento_2]
    for i in range(opcionales): # Agrego las columnas opcionales si existen
        columnas_a_evaluar.append(titulos_opcionales_doc2[i])

    if Cod_Nom_match.any():
        if verbose:
            print("Coincide Cod y Nom con:")
            print(result[Cod_Nom_match])

        # Coincide tanto Cod como Nom
        match_idx = result[Cod_Nom_match].index[0]
        
        # Si ya tiene datos en las columnas del documento 2, moverlos a una nueva fila
        if (~(result.loc[match_idx, columnas_a_evaluar].isna()) & 
        ~(result.loc[match_idx, columnas_a_evaluar] == '')).any():
            if verbose: print("El match ya tiene datos en las columnas del documento 2. Moviendolos a nueva fila...")
            result = mover_datos_doc2(result, match_idx)

        # Actualizar la fila existente con los datos de row
        if verbose: print("Actualizando fila existente...")
        actualizar_fila_coincidente(result, match_idx, row)

    elif Cod_match.any():
        if verbose:
            print("Coincide solo Cod")
            print(result[Cod_match])

        # Coincide solo Cod
        matches = result[Cod_match]
        actualizado = False

        for match_idx in matches.index:
            if verbose: print("Probando con fila: " + str(match_idx)) 
            # 1. Si las columnas del documento 2 del match están vacías, actualizo la fila con mis datos
            if (result.loc[match_idx, columnas_a_evaluar].isna() | 
            (result.loc[match_idx, columnas_a_evaluar] == '')).all(): 
                if verbose: print("Columnas del documento 2 del match vacías. Actualizando fila existente con mis datos...")
                actualizar_fila_coincidente(result, match_idx, row)
                actualizado = True # Marcar como actualizado
                break
        # Si no pude actualizar ningún match pruebo las siguientes opciones
        if not actualizado:
            if verbose: print("No habia filas con columnas del documento 2 del match vacías. Probando otras opciones...")
            for match_idx in matches.index:
                if verbose: print("Probando con fila: " + str(match_idx))    
                # 2. Si en el match hay datos obligatorios del documento 2 (Nom o Categoría) y Cod_documento2 no coincide con el mío (el correcto), muevo los datos del documento 2 del match a una nueva fila y actualizo el match
                if ((result.loc[match_idx, titulo_nom_documento_2] != '' and not pd.isna(result.loc[match_idx, titulo_nom_documento_2])) or \
                (result.loc[match_idx, titulos_opcionales_doc2[0]] != '' and not pd.isna(result.loc[match_idx, titulos_opcionales_doc2[0]]))) and \
                result.loc[match_idx, titulo_cod_documento_2] != row['Cod']:
                    if verbose: print("Cod_documento2 del match no coincide con el mío (el correcto) y hay otros datos del documento 2. Moviendo datos del documento 2 del match a nueva fila...")
                    result = mover_datos_doc2(result, match_idx)

                    # Actualizar la fila existente con los datos de row
                    if verbose: print("Actualizando fila existente con mis datos...")
                    actualizar_fila_coincidente(result, match_idx, row)
                    actualizado = True # Marcar como actualizado
                    break

            # Si no pude actualizar ningún match pruebo las siguientes opciones
            if not actualizado:
                if verbose: print("No habia filas con Cod_documento2 incorrecto. Probando otras opciones...")
                for match_idx in matches.index: 
                    if verbose: print("Probando con fila: " + str(match_idx))       
                    # 3. Si los Cod coinciden
                    if result.loc[match_idx, titulo_cod_documento_2] == row['Cod']:
                        # Caso 1: Si yo tengo Nom y Categoría del documento 2 y a match le falta alguna de ellas
                        if (row['Nom'] != '' and not pd.isna(row['Nom'])) and \
                        (row['Campo3'] != '' and not pd.isna(row['Campo3'])) and \
                        (pd.isna(result.loc[match_idx, titulo_nom_documento_2]) or result.loc[match_idx, titulo_nom_documento_2] == '' or
                        pd.isna(result.loc[match_idx, titulos_opcionales_doc2[0]]) or result.loc[match_idx, titulos_opcionales_doc2[0]] == ''):
                            if verbose: print("Cod_documento2 del match coincide con el mío (el correcto) y match tiene incompletos Nom o Categoría, yo tengo ambos (más completo). Me quedo con la fila. Moviendo datos del documento 2 del match a nueva fila...")
                            result = mover_datos_doc2(result, match_idx)

                            # Actualizar la fila existente con los datos de row
                            if verbose: print("Actualizando fila existente con mis datos...")
                            actualizar_fila_coincidente(result, match_idx, row)
                            actualizado = True  # Marcar como actualizado
                            break
                        
                if not actualizado:
                    if verbose: print("No había filas con Cod_documento2 correcto pero incompletas en Nom y Categoría. Probando el siguiente caso...")
                    for match_idx in matches.index: 
                        if verbose: print("Probando con fila: " + str(match_idx))
                        # 3. Si los Cod coinciden
                        if result.loc[match_idx, titulo_cod_documento_2] == row['Cod']:  
                            # Caso 2: Si yo tengo solo Nom_documento2 y match no tiene Nom_documento2
                            if (row['Nom'] != '' and not pd.isna(row['Nom'])) and \
                            (pd.isna(result.loc[match_idx, titulo_nom_documento_2]) or result.loc[match_idx, titulo_nom_documento_2] == ''):
                                print("Cod_documento2 del match coincide coincide con el mío (el correcto) y match no tiene Nom_documento2, yo si (más completo). Me quedo con la fila. Moviendo datos del documento 2 del match a nueva fila...")
                                result = mover_datos_doc2(result, match_idx)

                                # Actualizar la fila existente con los datos de row
                                if verbose: print("Actualizando fila existente con mis datos...")
                                actualizar_fila_coincidente(result, match_idx, row)
                                actualizado = True  # Marcar como actualizado
                                break

                if not actualizado:
                    if verbose: print("No había filas con Cod_REDATAM correcto pero sin Nom. Probando el siguiente caso...")
                    for match_idx in matches.index: 
                        if verbose: print("Probando con fila: " + str(match_idx))
                        # 3. Si los Cod coinciden
                        if result.loc[match_idx, titulo_cod_documento_2] == row['Cod']:
                            # Caso 3: Si yo tengo solo Categoría_documento2 y match no tiene ni Nom ni Categoría_documento2
                            if (row['Campo3'] != '' and not pd.isna(row['Campo3'])) and \
                            (pd.isna(result.loc[match_idx, titulo_nom_documento_2]) or result.loc[match_idx, titulo_nom_documento_2] == '') and \
                            (pd.isna(result.loc[match_idx, titulos_opcionales_doc2[0]]) or result.loc[match_idx, titulos_opcionales_doc2[0]] == ''):
                                if verbose: print("Cod_documento2 del match coincide coincide con el mío (el correcto) y match no tiene ni Nom ni Categoría del documento 2, yo tengo al menos categoría (más completo). Me quedo con la fila. Moviendo datos del documento 2 del match a nueva fila...")
                                result = mover_datos_doc2(result, match_idx)

                                # Actualizar la fila existente con los datos de row
                                if verbose: print("Actualizando fila existente con mis datos...")
                                actualizar_fila_coincidente(result, match_idx, row)
                                actualizado = True  # Marcar como actualizado
                                break

                # Caso 4: Si ninguno de los matches me permitió tomar la fila, creo una nueva fila para mis datos
                if not actualizado:
                    if verbose: print("Ninguna fila coincidió lo suficiente. Creando nueva fila para mis datos...")
                    result = nueva_fila(result, row)


    elif Nom_match.any():
        if verbose:
            print("Coincide solo Nom")
            print(result[Nom_match])

        # Coincide solo Nom
        matches = result[Nom_match]
        actualizado = False
        if verbose: print("Matches encontrados:", matches.index)
        for match_idx in matches.index:
            if verbose: print("Probando con fila: " + str(match_idx))
            # Si las columnas del documento 2 del match están vacías, actualizo la fila con mis datos
            if (result.loc[match_idx, columnas_a_evaluar].isna() | (result.loc[match_idx, columnas_a_evaluar] == '')).all(): 
                if verbose: print("El match no tiene datos del documento 2. Actualizando fila existente...")
                actualizar_fila_coincidente(result, match_idx, row)
                actualizado = True # Marcar como actualizado
                break
        # Si no pude actualizar ningún match, crear una nueva fila
        if not actualizado:
                if verbose: print("El match ya tiene datos del documento 2. Creando nueva fila para mis datos...")
                result = nueva_fila(result, row)

    else:
        # No hay coincidencias, agregar una nueva fila
        # Categoría puede repetirse por lo que me da igual si coincide solo categoría, no implica nada, se hace una nueva fila y punto
        if verbose:
            print("No hay coincidencias")
            print("Creando nueva fila para mis datos...")
        result = nueva_fila(result, row)

    return result

print("\n")	# Salto de línea
print("CHEQUEANDO CONSISTENCIA...")
print("Filas a procesar:", cant_documento1 + cant_documento2)
# Inicializar el DataFrame de resultado
result = documento_1.copy()
result.columns = [titulo_cod_documento_1, titulo_nom_documento_1, titulos_opcionales_doc1[0]]
result[titulo_cod_documento_2] = ''
result[titulo_nom_documento_2] = ''
result[titulos_opcionales_doc2[0]] = ''
for idx, row in documento_2.iterrows():
    result = procesar_fila(row, result)

# Resultados
# Completar los valores faltantes con '' para que no haya NaN
result.fillna({titulo_cod_documento_1:''}, inplace=True)
result.fillna({titulo_cod_documento_2:''}, inplace=True)
result.fillna({titulo_nom_documento_1:''}, inplace=True)
result.fillna({titulo_nom_documento_2:''}, inplace=True)
result.fillna({titulos_opcionales_doc1[0]:''}, inplace=True)
result.fillna({titulos_opcionales_doc2[0]:''}, inplace=True)

def verificar_consistencia(row):
    # Verifico los campos obligatorios primero
    if (row[titulo_cod_documento_1] != row[titulo_cod_documento_2]) or (row[titulo_nom_documento_1] != row[titulo_nom_documento_2]):
        return 'No'
    
    # Comparo los campos opcionales dinámicamente
    for i in range(opcionales):
        if row[titulos_opcionales_doc1[i]] != row[titulos_opcionales_doc2[i]]:
            return 'No'
    
    # Si todos los campos coinciden
    return 'Sí'

# Aplico la función para chequear consistencia de las filas
result['Consistencia'] = result.apply(verificar_consistencia, axis=1)
filas_finales = result.shape[0]
total_consistentes = result[result['Consistencia'] == 'Sí'].shape[0]
porcentaje_consistencia = (total_consistentes / filas_finales) * 100
print("\n")	# Salto de línea
print(f"Filas resultantes: {filas_finales}")

# Guardo el resultado
print("\n")	# Salto de línea
ruta_resultado = os.path.join(carpeta_salida, 'Chequeo de consistencia.xlsx')
result.to_excel(f'{ruta_resultado}', index=False)
print(f"Filas consistentes: {total_consistentes} ({porcentaje_consistencia:.2f}%) -> Resultado disponible en: {ruta_resultado}")
print("\n")	# Salto de línea