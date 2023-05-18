# https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
# After much trial and error, I FINALLY figured out how to make things work.

# Step 1.
# create the docker image that python runs on local.
# Alternatively, you *could* do this on ec2 and grant role to lambda layers + s3
#   Refer to https://repost.aws/knowledge-center/lambda-import-module-error-python

here=$(pwd)
cd $here/examples/aws/make_pandas_layer
docker build -t imitate:latest .

# Because I used AWS's python image,
#   From `Test an image with RIE included in the image` at https://docs.aws.amazon.com/lambda/latest/dg/images-test.html I can run the emulator.
#   the -v option mounts the downloads directory on my host machine to the docker's /data directory, which I made in the dockerfile
docker run -d -v ~/Downloads:/data  imitate:latest
# The container ID is printed to console
  docker ps # or use this to get ID
CONTAINER_ID=#set here
docker exec -it $CONTAINER_ID sh
# Then run
mkdir data/my-docker-package
cd data/my-docker-package
mkdir python

pip install \
  --target python \
  --upgrade \
  pandas

exit
docker cp $CONTAINER_ID:/var/task/data/my-docker-package ~/Downloads/
# Now the image-generated linux-architecture pandas files are in ~/Downloads/my-docker-package/python
cd ~/Downloads/my-docker-package/python
zip ~/Downloads/layer.zip .
# This produces the valid and final zip file to upload
aws s3 cp  ~/Downloads/layer.zip  s3://$BUCKET/deployment.zip

# Could run
zip_path=~/Downloads/layer.zip
aws lambda publish-layer-version \
  --layer-name pandas-layer \
  --zip-file fileb://${zip_path} \
  --compatible-runtimes python3.9 \
  --region us-east-1

# see https://docs.aws.amazon.com/cli/latest/reference/lambda/publish-layer-version.html
# OR --content S3Bucket=$BUCKET,S3Key=deployment.zip\