# Databricks notebook source
# MAGIC %md
# MAGIC # Data Access

# COMMAND ----------

App_id="f4d3997b-e649-4743-9d9d-1d887c9f5a86"

Dir_id= "e7c0de5f-df02-44dc-97e5-40af1a4ab6cd"

Secret="hkP8Q~.mRJWI94-S0SJH55OdgwrMnuDts2_fOc6Z"


# COMMAND ----------


spark.conf.set("fs.azure.account.auth.type.nyctaxistoragepoc.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.nyctaxistoragepoc.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.nyctaxistoragepoc.dfs.core.windows.net", "f4d3997b-e649-4743-9d9d-1d887c9f5a86")
spark.conf.set("fs.azure.account.oauth2.client.secret.nyctaxistoragepoc.dfs.core.windows.net", "hkP8Q~.mRJWI94-S0SJH55OdgwrMnuDts2_fOc6Z")
spark.conf.set("fs.azure.account.oauth2.client.endpoint.nyctaxistoragepoc.dfs.core.windows.net", "https://login.microsoftonline.com/e7c0de5f-df02-44dc-97e5-40af1a4ab6cd/oauth2/token")

# COMMAND ----------

dbutils.fs.ls('abfss://bronze@nyctaxistoragepoc.dfs.core.windows.net/')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read the Connect

# COMMAND ----------

# MAGIC %md
# MAGIC ### Importing Libraries
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reading CSV
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ###TripType Data

# COMMAND ----------

df_trip_type = spark.read.format('csv')\
                    .option('header', 'true')\
                    .option('inferSchema', 'true')\
                    .load('abfss://bronze@nyctaxistoragepoc.dfs.core.windows.net/trip_type')


# COMMAND ----------

df_trip_type.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Trip Zone Data

# COMMAND ----------

df_zone = spark.read.format('csv')\
                    .option('header', 'true')\
                    .option('inferSchema', 'true')\
                    .load('abfss://bronze@nyctaxistoragepoc.dfs.core.windows.net/trip_zone')

# COMMAND ----------

df_zone.display()

# COMMAND ----------

df_trip = spark.read.format('parquet')\
                    .option('header', True)\
                    .schema(my_schema)\
                    .option('recursivefileLookup', True)\
                    .load('abfss://bronze@nyctaxistoragepoc.dfs.core.windows.net/trip_2023')

# COMMAND ----------

my_schema = '''
                VendorId BIGINT,
                lpep_pickup_datetime TIMESTAMP,
                Lpep_dropoff_datetime TIMESTAMP,
                store_and_fwd_flag STRING,
                RateCodeID BIGINT,
                PULocationID BIGINT,
                DOLocationID BIGINT,
                passenger_Count BIGINT,
                Trip_distance Double,
                Fare_amount DOUBLE,
                Extra DOUBLE,
                MTA_tax DOUBLE,
                Tip_amount DOUBLE,
                Tolls_amount DOUBLE,
                Ehail_fee DOUBLE,
                Improvement_surcharge DOUBLE,
                Total_amount DOUBLE,
                Payment_type BIGINT,
                Trip_type BIGINT,
                congestion_surcharge DOUBLE
            '''


# COMMAND ----------

df_trip.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Transformation

# COMMAND ----------

# MAGIC %md
# MAGIC **Taxi Trip Type**

# COMMAND ----------

df_trip_type.display()


# COMMAND ----------

df_trip_type = df_trip_type.withColumnRenamed("description", "trip_description")

# COMMAND ----------

# MAGIC %md
# MAGIC **Type of modes-- .mode('Append')\**
# MAGIC                  ** .mode('overwrite')\**
# MAGIC                  ** .mode('error')\**
# MAGIC                  ** .mode('ignore')\**
# MAGIC                  
# MAGIC                 

# COMMAND ----------

df_trip_type.write.format('parquet')\
                  .mode('Append')\
                  .option("path","abfss://silver@nyctaxistoragepoc.dfs.core.windows.net/taxi_data/trip_type")\
                  .save()

# COMMAND ----------

df_zone.display()

# COMMAND ----------

df_zone=df_zone.withColumn('zone1',split(col('zone'),'/')[0])\
                .withColumn('zone2',split(col('zone'),'/')[1])

# COMMAND ----------

df_zone.display()

# COMMAND ----------

df_zone.write.format('parquet')\
                  .mode('Append')\
                  .option("path","abfss://silver@nyctaxistoragepoc.dfs.core.windows.net/taxi_data/trip_zone")\
                  .save()

# COMMAND ----------

# MAGIC %md
# MAGIC **TRIP DATA**

# COMMAND ----------

df_trip.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Convert the Data ,Month & Year

# COMMAND ----------

df_trip = df_trip.withColumn('trip_date',to_date(col('lpep_pickup_datetime')))\
                  .withColumn('trip_year',year(col('lpep_pickup_datetime')))\
                  .withColumn('trip_month',month(col('lpep_pickup_datetime')))
df_trip.display()

# COMMAND ----------

df_trip = df_trip.select('VendorId','PULocationID','DOLocationID','fare_amount','total_amount')

# COMMAND ----------

df_trip.display()

# COMMAND ----------

df_trip.write.format('parquet')\
             .mode('append')\
             .option('path',"abfss://silver@nyctaxistoragepoc.dfs.core.windows.net/trip2023")\
             .save()   


# COMMAND ----------

# MAGIC %md
# MAGIC ## Analysis

# COMMAND ----------

display(df_trip)

# COMMAND ----------

