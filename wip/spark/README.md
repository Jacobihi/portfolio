# Intro
This project demonstrates my self-directed learnings with apache spark. 
I have done some deployment of this in the [aws](../aws/README.md) project on Lambda + attempted to learn to do it on EMR.

# Getting Started

I started with [this guide](https://www.datacamp.com/tutorial/pyspark-tutorial-getting-started-with-pyspark).

I had to download Java + Apache Spark and update my ~/.zshrc according to the suggestions.

# Setting up Python

```shell 
pyenv virtualenv 3.9.1 spark_demo
pyenv activate spark_demo
pip install --upgrade pip
pip install pyspark
```

Since I was running in pycharm console, I needed to edit my console environment variables to have the correct Java Home

I found this using ```java -XshowSettings:properties -version```

[//]: # (TODO: Create the same job with both Spark + DataFlow, execute with Beam; execute with Airflow; compare with https://docs.aws.amazon.com/glue/latest/dg/add-job.html.)
[//]: #  (https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/glue.html)

# Outline for a Spark Job 

* docs
* src
  * db
    * connectors
      * AbstractDBConnector
      * Postgres
      * BigQuery
      * Snowflake
    * schema
      * AbstractEntity
      * SourceEntity
      * TransformedEntity
  * config
    * session
    * source
    * destination
  * processor
    * job
    * pipeline
  * examples
    * Visualize Emissions from multiple countries + sectors
      * AWS EMR using Spark https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/launch-a-spark-job-in-a-transient-emr-cluster-using-a-lambda-function.html
        * Consider auto-scaling https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-automatic-scaling.html 
        * also use airflow: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html
        * https://hub.docker.com/r/gooddata/gooddata-cn-ce  
      * Consider this S3-> Redshift pipeline doc https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/build-an-etl-service-pipeline-to-load-data-incrementally-from-amazon-s3-to-amazon-redshift-using-aws-glue.html 
      * GCP Data flow using Apache Beam https://cloud.google.com/dataflow/docs/concepts/beam-programming-model
        * Deploy to looker
        * 
    * Apache Kafka streaming example source data https://github.com/viirya/eventsim
* tests

# Main Content to consider:

https://primap2.readthedocs.io/en/stable/readme.html

Which I came upon first from Google Dataset query https://datasetsearch.research.google.com/search?src=2&query=Food%20waste%20production%20worldwide%202019%2C%20by%20sector&docid=L2cvMTFyeW1kcWpqNw%3D%3D&filters=WyJbXCJmaWxlX2Zvcm1hdF9jbGFzc1wiLFtcIjFcIl1dIl0%3D&property=ZmlsZV9mb3JtYXRfY2xhc3M%3D
which took me to https://zenodo.org/record/7727475#.ZB9bfOzMJsA

Which I believe requires this citation:

[//]: # (TODO: How to site a dataset properly?)
[//]: # (TODO: Is there a dataset that requires less cognitive load to understand to work with for this demo?)

> Gütschow, J.; Jeffery, L.; Gieseke, R.; Gebel, R.; Stevens, D.; Krapp, M.; Rocha, M. (2016): The PRIMAP-hist national historical emissions time series, Earth Syst. Sci. Data, 8, 571-603, doi:10.5194/essd-8-571-2016
