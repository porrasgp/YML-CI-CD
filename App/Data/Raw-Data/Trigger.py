from pyspark.sql import SparkSession
import requests

# Inicializar sesión de Spark
spark = SparkSession.builder.appName("AgeSumByWorkclass").getOrCreate()

# URL del archivo CSV
url = "https://raw.githubusercontent.com/guru99-edu/R-Programming/master/adult_data.csv"

# Descargar el archivo CSV y guardarlo localmente
response = requests.get(url)
with open("adult_data.csv", "wb") as file:
    file.write(response.content)

# Cargar el archivo CSV local como un DataFrame de Spark
df = spark.read.csv("adult_data.csv", header=True, inferSchema=True)

# Definir las clases de trabajo que deseas analizar
workclasses = ['Private', 'Local-gov', 'Self-emp-inc', 'Federal-gov']

# Crear una función para calcular la suma de edades por clase de trabajo
def calculate_age_sum(workclass):
    filtered_df = df.filter(df.workclass == workclass)
    age_sum = filtered_df.select(spark_sum("age")).collect()[0][0]
    return workclass, age_sum

# Ejecutar la función para cada clase de trabajo y mostrar resultados
results = [calculate_age_sum(workclass) for workclass in workclasses]
for result in results:
    print(f"Workclass: {result[0]}, Age Sum: {result[1]}")

# Cerrar la sesión de Spark
spark.stop()
