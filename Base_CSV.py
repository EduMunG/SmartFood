# import pandas as pd

# # Leer el archivo CSV
# df = pd.read_csv('data_base.csv')



import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('data_base.csv', index_col='index')

# Verificar si el índice 4 existe en el DataFrame
if 4 in df.index:
    # Eliminar el registro con index = 4
    df.drop(index=4, inplace=True)

# Reiniciar el índice del DataFrame para que vaya de 1 a N
df.reset_index(drop=True, inplace=True)
df.index = df.index + 1

# Guardar el nuevo archivo CSV sin el registro con index = 4 y con el índice actualizado
df.to_csv('data_filtrado.csv', index_label='index')
