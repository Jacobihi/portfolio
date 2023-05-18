Work in Progress
========================

I am embarking on self-paced learning and demonstration exercises in the following technologies:

* Spark (for distributed ETL)
* GCP - Dataflow (for orchestration)
* GCP - BigQuery (for warehouse/massive distributed columnar data storage engine)
* AWS - Redshift (extending some professional experience to prove depth of knowledge for massive distributed columnar data storage engine)
* AWS - EMR (for variety of distributed massive parallel compute and variety of cloud workflows)

Why is there only work in progress?
------------------------------------------------

I'm in the middle of a life transition (moving from DC suburbs to rural Pennsylvania) and neither my schedule nor my internet are stable.
This makes this a particularly bad time to make meaningful progress on these projects, but I am going to hold myself accountable to growth
and technical experience using a variety of big data and cloud processing tools.


Some Ideas
------------

This is not commitment, just ideating some of my plans:

* Visualize Emissions from multiple countries + sectors
* AWS EMR using Spark https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/launch-a-spark-job-in-a-transient-emr-cluster-using-a-lambda-function.html
  * Consider auto-scaling https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-automatic-scaling.html
  * also use airflow: https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html
  * https://hub.docker.com/r/gooddata/gooddata-cn-ce
* Consider this S3-> Redshift pipeline doc https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/build-an-etl-service-pipeline-to-load-data-incrementally-from-amazon-s3-to-amazon-redshift-using-aws-glue.html
* GCP Data flow using Apache Beam https://cloud.google.com/dataflow/docs/concepts/beam-programming-model

  * Deploy to looker

* Apache Kafka streaming example source data https://github.com/viirya/eventsim

Possible Datasets
++++++++++++++++++

# Main Content to consider:

https://primap2.readthedocs.io/en/stable/readme.html

Which I came upon first from Google Dataset query https://datasetsearch.research.google.com/search?src=2&query=Food%20waste%20production%20worldwide%202019%2C%20by%20sector&docid=L2cvMTFyeW1kcWpqNw%3D%3D&filters=WyJbXCJmaWxlX2Zvcm1hdF9jbGFzc1wiLFtcIjFcIl1dIl0%3D&property=ZmlsZV9mb3JtYXRfY2xhc3M%3D
which took me to https://zenodo.org/record/7727475#.ZB9bfOzMJsA

Which I believe requires this citation:

[//]: # (TODO: How to site a dataset properly?)
[//]: # (TODO: Is there a dataset that requires less cognitive load to understand to work with for this demo?)

> Gütschow, J.; Jeffery, L.; Gieseke, R.; Gebel, R.; Stevens, D.; Krapp, M.; Rocha, M. (2016): The PRIMAP-hist national historical emissions time series, Earth Syst. Sci. Data, 8, 571-603, doi:10.5194/essd-8-571-2016
