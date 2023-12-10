# Databricks notebook source
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, DoubleType, BooleanType, DateType

# COMMAND ----------

#changes o new branch
configs = {
"fs.azure.account.auth.type": "OAuth",
"fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
"fs.azure.account.oauth2.client.id": "----------------------------",# Add client ID
"fs.azure.account.oauth2.client.secret": '-------------------------------', # Add Secret Key
"fs.azure.account.oauth2.client.endpoint": "----------------------------------" # Add Tenant ID
}

dbutils.fs.mount(
source = "abfss://tokyoolympics@tokyoolympicsstrgacc.dfs.core.windows.net", # contrainer@storageacc
mount_point = "/mnt/tokyoolympic",
extra_configs = configs)

# COMMAND ----------

# MAGIC %fs
# MAGIC ls "/mnt/tokyoolympic"

# COMMAND ----------

# Reading the raw data from the source location i.e raw-data folder in ADLS for doing transformation on the raw data
athletes = spark.read.format("csv").option("header","true").option("inferSchema","true").load("/mnt/tokyoolympic/raw-data/athletes.csv")
coaches = spark.read.format("csv").option("header","true").option("inferSchema","true").load("/mnt/tokyoolympic/raw-data/coaches.csv")
entriesgender = spark.read.format("csv").option("header","true").option("inferSchema","true").load("/mnt/tokyoolympic/raw-data/entriesgender.csv")
medals = spark.read.format("csv").option("header","true").option("inferSchema","true").load("/mnt/tokyoolympic/raw-data/medal.csv")
teams = spark.read.format("csv").option("header","true").option("inferSchema","true").load("/mnt/tokyoolympic/raw-data/teams.csv")

# COMMAND ----------

athletes.show()

# COMMAND ----------

athletes.printSchema()

# COMMAND ----------

coaches.show()

# COMMAND ----------

coaches.printSchema()

# COMMAND ----------

entriesgender.show()

# COMMAND ----------

entriesgender.printSchema()

# COMMAND ----------

# Doing a transformation on entriesgender dataframe by changing the datastype to integer
entriesgender = entriesgender.withColumn("Female",col("Female").cast(IntegerType()))\
    .withColumn("Male",col("Male").cast(IntegerType()))\
    .withColumn("Total",col("Total").cast(IntegerType()))

# COMMAND ----------

entriesgender.printSchema()

# COMMAND ----------

medals.show()

# COMMAND ----------

medals.printSchema()

# COMMAND ----------

teams.show()

# COMMAND ----------

teams.printSchema()

# COMMAND ----------

# Find the top countries with the highest number of gold medals
top_gold_medal_countries = medals.orderBy("Gold", ascending=False).select("Team_Country","Gold").show()

# COMMAND ----------

# Calculate the average number of entries by gender for each discipline
average_entries_by_gender = entriesgender.withColumn(
    'Avg_Female', entriesgender['Female'] / entriesgender['Total']
).withColumn(
    'Avg_Male', entriesgender['Male'] / entriesgender['Total']
)
average_entries_by_gender.show()

# COMMAND ----------

# Writing or loading the transformed data into the target destination i.e transformed-data folder in ADLS

athletes.repartition(1).write.mode("overwrite").option("header",'true').csv("/mnt/tokyoolymic/transformed-data/athletes")
coaches.repartition(1).write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed-data/coaches")
entriesgender.repartition(1).write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed-data/entriesgender")
medals.repartition(1).write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed-data/medals")
teams.repartition(1).write.mode("overwrite").option("header","true").csv("/mnt/tokyoolymic/transformed-data/teams")


# COMMAND ----------


