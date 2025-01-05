# Databricks notebook source
# MAGIC %md
# MAGIC ## Data Access

# COMMAND ----------


spark.conf.set("fs.azure.account.auth.type.nyctaxistoragepoc.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.nyctaxistoragepoc.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.nyctaxistoragepoc.dfs.core.windows.net", "f4d3997b-e649-4743-9d9d-1d887c9f5a86")
spark.conf.set("fs.azure.account.oauth2.client.secret.nyctaxistoragepoc.dfs.core.windows.net", "hkP8Q~.mRJWI94-S0SJH55OdgwrMnuDts2_fOc6Z")
spark.conf.set("fs.azure.account.oauth2.client.endpoint.nyctaxistoragepoc.dfs.core.windows.net", "https://login.microsoftonline.com/e7c0de5f-df02-44dc-97e5-40af1a4ab6cd/oauth2/token")

# COMMAND ----------

# MAGIC %md
# MAGIC #Database Creation

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP DATABASE IF EXISTS gold;
# MAGIC CREATE DATABASE gold;

# COMMAND ----------

# MAGIC %md
# MAGIC #Data Reading Writing & Creating Delta Table

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# MAGIC %md
# MAGIC **DATA ZONE**

# COMMAND ----------

silver = "abfss://silver@nyctaxistoragepoc.dfs.core.windows.net"
gold =  'abfss://gold@nyctaxistoragepoc.dfs.core.windows.net'

# COMMAND ----------

dbutils.fs.ls(f'{silver}')

# COMMAND ----------

dbutils.fs.ls('abfss://gold@nyctaxistoragepoc.dfs.core.windows.net')

# COMMAND ----------

df_zone=spark.read.format('parquet')\
                  .option('header','true')\
                  .option('inferSchema','true')\
                  .load('abfss://silver@nyctaxistoragepoc.dfs.core.windows.net/taxi_data/trip_zone')

# COMMAND ----------


df_zone.write.format('delta')\
            .mode('append')\
            .save('abfss://gold@nyctaxistoragepoc.dfs.core.windows.net/trip_zone')


# COMMAND ----------

# Write data to Delta table
df_zone.write.format('delta')\
            .mode('append')\
            .saveAsTable('gold.trip_zone')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from gold.trip_zone

# COMMAND ----------

# MAGIC %md
# MAGIC **Trip Type**

# COMMAND ----------

df_type=spark.read.format('parquet')\
                  .option('header','true')\
                  .option('inferSchema','true')\
                  .load('abfss://silver@nyctaxistoragepoc.dfs.core.windows.net/taxi_data/trip_type')

# COMMAND ----------

df_type.write.format('delta')\
            .mode('append')\
            .save('abfss://gold@nyctaxistoragepoc.dfs.core.windows.net/trip_type')



# COMMAND ----------

# Write data to Delta table
df_type.write.format('delta')\
            .mode('append')\
            .saveAsTable('gold.trip_type')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from gold.trip_type

# COMMAND ----------

# MAGIC %md
# MAGIC **Trip Data**
# MAGIC

# COMMAND ----------

df_trip=spark.read.format('parquet')\
                  .option('header','true')\
                  .option('inferSchema','true')\
                  .load('abfss://silver@nyctaxistoragepoc.dfs.core.windows.net/trip2023')

# COMMAND ----------


df_trip.write.format('delta')\
            .mode('append')\
            .save('abfss://gold@nyctaxistoragepoc.dfs.core.windows.net/trip_data')

# COMMAND ----------

# Write data to Delta table
df_trip.write.format('delta')\
            .mode('append')\
            .saveAsTable('gold.trip_data')

# COMMAND ----------

df_trip.display()

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from gold.trip_data