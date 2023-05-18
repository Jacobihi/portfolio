# Run AWS Lambda with Pandas

The purpose of this exercise was:

1. to test deployment of aws resources using the aws cli.
2. to get some more experience in the AWS console
3. to learn package deployment for a lambda with dependencies
   1. I gained some additional Docker experience (which I wound up using to produce my package, see [run_docker_locally.sh](run_docker_locally.sh)
   2. I tested out an ec2 to try to build the linux pandas

# What's It Do?

I wrote a generalized aggregator to take an input and use pandas to produce an aggregate output. 

While perhaps drab or dull, it allows me to understand how I might do ETL without thinking yet about the EMR configurations. 

It allowed me to test a trigger, which was helpful in understanding the actual use case of lambda. 

It takes a JSON job file as an event which it reads to get the input and output specification for this 
super simple transformation. 

I loaded [local_event.json](local_event.json) to my s3 bucket `job/` path to point to some sample data loaded in my input bucket with directive to write to the output bucket. 

[s3_event.json](s3_event.json) is the test data I used when testing an event input from an s3 put trigger.

)