import pandas as pd
from multiprocessing import Pool

# Función modificada para evitar descargar el archivo en cada proceso
def calculate_age_sum(args):
    df, workclass = args
    filtered_df = df[df['workclass'] == workclass]
    age_sum = filtered_df['age'].sum()
    return workclass, age_sum

if __name__ == '__main__':
    # Descargar el CSV una sola vez
    df = pd.read_csv('https://raw.githubusercontent.com/guru99-edu/R-Programming/master/adult_data.csv')
    
    # Definir las clases de trabajo
    workclasses = ['Private', 'Local-gov', 'Self-emp-inc', 'Federal-gov']
    
    # Crear una lista de tuplas con el DataFrame y cada clase de trabajo
    tasks = [(df, workclass) for workclass in workclasses]
    
    # Usar multiprocessing para calcular la suma de edades en paralelo
    with Pool(processes=4) as pool:
        results = pool.map(calculate_age_sum, tasks)
    
    # Mostrar los resultados
    for result in results:
        print(f"Workclass: {result[0]}, Age Sum: {result[1]}")
