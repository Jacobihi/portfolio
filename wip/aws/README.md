# Amazon Web Services (AWS)

I use AWS a bit more at work, so I'm mostly wanting to explore more options for exposure and experience.

In this repo I have done some basic EMR configuration and run spark based on some examples.

I chose EMR as an ambition for exposure into a variety of cloud-based distributed computing solutions.

As I went about learning and testing, I realized that the main application of AWS was to find somewhere to run spark on a large dataset. 

Therefore, I pivoted and focused my learning on running spark jobs on lambda.

# AWS Example

Following the tutorial from https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/launch-a-spark-job-in-a-transient-emr-cluster-using-a-lambda-function.html
but what I really need to do is follow the instructions on this one:
https://aws.amazon.com/blogs/big-data/run-and-debug-apache-spark-applications-on-aws-with-amazon-emr-on-amazon-eks/

# Iteration 1: Try it on ec2
ec2 is in the free tier but EMR is *not*. So I'm going to try that first. 

I followed [this helpful tutorial](https://plainenglish.io/blog/spark-on-aws-lambda-c65877c0ac96) for the docker configuration

And I followed the AWS docs on lambda to tdo the following:

1. Create an administrator user to do stuff as
2. Create an s3 bucket with keys `input` and `output`
3. Create a path called `job` 
4. I made my first lambda *role* in the console using the default lambda roles.
   3. See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html
   4. See https://docs.aws.amazon.com/lambda/latest/dg/images-test.html
5. Load the online retail data to `input`
6. Produce the aggregation by country + date in `output`
7. Trigger with upload to `job` to provide the event context 


See [make_pandas_layer](make_pandas_layer/README.md) for that project.

I'll be doing my EMR project in [emr_test](emr_test/README.md)


# Run Locally
1. Install the local runtime interface client https://docs.aws.amazon.com/lambda/latest/dg/python-image.html
2. follow commands in [run_docker_locally.sh](run_docker_locally.sh)

# Future consideration: Deploy using Sam
* [Install sam](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
* [Invoke locally](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-invoke.html)

# Notes
It was 1150 MB for that container, so I noped right out of that for long-term because I only get 500MB per months. 

When I do EMR I'll see if I can do a basic one when I get there.