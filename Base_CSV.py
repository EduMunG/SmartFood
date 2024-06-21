# import pandas as pd

# # Leer el archivo CSV
# df = pd.read_csv('data_base.csv')



import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('data_base_1.csv')

# Filtrar los registros donde el grupo no es 1.0, 2.0, 11.0, 23.0, 15.0, o 24.0
df_filtrado = df[(df['group'] != 1.0) & (df['group'] != 2.0) & (df['group'] != 11.0) & 
                 (df['group'] != 23.0) & (df['group'] != 15.0) & (df['group'] != 24.0)]

# Reiniciar el índice del DataFrame filtrado para que vaya de 1 a N
df_filtrado.reset_index(drop=True, inplace=True)
df_filtrado.index = df_filtrado.index + 1

# Guardar el nuevo archivo CSV sin los registros con los grupos especificados y con el índice actualizado
df_filtrado.to_csv('data_filtrado.csv', index_label='index')
