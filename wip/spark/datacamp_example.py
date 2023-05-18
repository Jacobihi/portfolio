from pyspark.sql import SparkSession
import pyspark.sql.functions as ps_func


spark = (
    SparkSession.builder.appName("Datacamp Pyspark Tutorial")
    .config("spark.memory.offHeap.enabled", "true")
    .config("spark.memory.offHeap.size", "10g")
    .getOrCreate()
)

data_file = '/Users/jhickson/Downloads/Online Retail.csv'
df = spark.read.csv(data_file, header=True, escape="\"")
# exploration
df.show(5, 0)
df.count()
df.select('CustomerID').distinct().count()


df.groupBy('Country').agg(ps_func.countDistinct('CustomerID').alias('country_count')).orderBy(
    ps_func.desc('country_count')
).show()

"""
Per: https://spark.apache.org/docs/3.3.2/sql-migration-guide.html#query-engine 

> Parsing/formatting of timestamp/date strings. 
> This effects on CSV/JSON datasources and on the unix_timestamp, date_format, to_unix_timestamp, 
> from_unixtime, to_date, to_timestamp functions when patterns specified by users is used for parsing 
> and formatting. In Spark 3.0, we define our own pattern strings in Datetime Patterns for 
Formatting and Parsing, which is implemented via DateTimeFormatter under the hood. 
New implementation performs strict checking of its input. 
For example, the 2015-07-22 10:00:00 timestamp cannot be parse if pattern is yyyy-MM-dd because the 
parser does not consume whole input. Another example is the 31/01/2015 00:00 input cannot be parsed by the dd/MM/yyyy hh:mm pattern because hh supposes hours in the range 1-12. 
In Spark version 2.4 and below, java.text.SimpleDateFormat is used for timestamp/date string conversions, 
and the supported patterns are described in SimpleDateFormat. 
The old behavior can be restored by setting spark.sql.legacy.timeParserPolicy to LEGACY.


"""

"""
This is thus an incredibly useful reference: https://spark.apache.org/docs/3.3.2/sql-ref-datetime-pattern.html
"""
spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")  # BUT HOW DO I UNSET IT?
# of course, I opened this in Excel and I have some
# settings on my Mac that mean that my default date format is different.
# DataCamp used format 'yy/MM/dd HH:mm'
# My format is 'yyyy-mm-dd H:mm'
new_column = 'date'
source_column = "InvoiceDate"
date_format = 'yy/MM/dd HH:mm'  # data camp's, presumably the Windows Excel default.
date_format = 'yyyy-mm-dd H:mm'  # my system default
# https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.to_timestamp.html?highlight=to_timestamp#pyspark-sql-functions-to-timestamp
df = df.withColumn(new_column, ps_func.to_timestamp(source_column, date_format))
df.select(max(new_column)).show()

# SQL Syntax: https://spark.apache.org/docs/latest/sql-ref-syntax.html#dml-statements

as_sql = """
    SELECT customer_id, country, AVG(quantity) As average_quantity, MIN(date) AS earliest_date, 
    MAX(date) AS 
    latest_date
    FROM dataframe
    GROUP BY customer_id, country
    """

df.columns  # >> ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country', 'date']

"""
The below expression shows an example of doing a SQL statement type aggregation

"""
(
    df.groupBy("CustomerID", "Country")
    .agg(
            ps_func.avg("Quantity").alias("Average Quantity"),
            ps_func.max('date').alias("Latest Date"),
            ps_func.min('date').alias("Earliest Date"),
            ps_func.lit('Is Potato').alias("My alias")
    )
    .show()
)


# lit = ps_func.lit()
# One way to get a singleton, e.g., the earliest date
min_date = df.agg(ps_func.min('date').alias("x")).collect()[0]['x']


"""
Some additional learnings/gleanings from https://www.linkedin.com/pulse/end-pyspark-example-manoj-chandrashekar/
"""
# Create a queryable view!
df.createOrReplaceTempView("online_retail")
as_sql = """
    SELECT customer_id, country, AVG(quantity) As average_quantity, MIN(date) AS earliest_date, 
    MAX(date) AS 
    latest_date
    FROM dataframe
    GROUP BY customer_id, country
    """
