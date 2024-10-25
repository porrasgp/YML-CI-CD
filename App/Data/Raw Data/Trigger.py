from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum
from pyspark.sql import DataFrame

# Inicializar Spark
spark = SparkSession.builder.appName("AgeSumByWorkclass").getOrCreate()

# Cargar el archivo CSV como un DataFrame de Spark
df = spark.read.csv("https://raw.githubusercontent.com/guru99-edu/R-Programming/master/adult_data.csv", header=True, inferSchema=True)

# Definir las clases de trabajo que deseas analizar
workclasses = ['Private', 'Local-gov', 'Self-emp-inc', 'Federal-gov']

# Crear una lista para almacenar los resultados
results_list = []

# Calcular la suma de edades y almacenar los resultados en una lista
for workclass in workclasses:
    filtered_df = df.filter(df.workclass == workclass)
    age_sum = filtered_df.select(spark_sum("age")).collect()[0][0]
    results_list.append((workclass, age_sum))

# Convertir la lista de resultados en un DataFrame de Spark
results_df = spark.createDataFrame(results_list, ["workclass", "age_sum"])

# Guardar el DataFrame como un archivo Parquet (artifact)
results_df.write.mode("overwrite").parquet("App/Data/Raw Data")

# Cerrar sesión de Spark
spark.stop()
