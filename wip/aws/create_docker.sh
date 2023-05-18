# https://docs.aws.amazon.com/lambda/latest/dg/python-image.html
# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html
# https://docs.aws.amazon.com/lambda/latest/dg/images-test.html
# https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html
REPO_NAME=my-first-image
REGION=us-east-1

aws ecr create-repository --profile personal --repository-name "${REPO_NAME}" --region "${REGION}"
REPO_URI="${MY_AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}"
aws ecr get-login-password --profile personal --region us-east-1 | \
  docker login --username AWS --password-stdin "${REPO_URI}"
docker build  -t "${REPO_NAME}" .
IMAGE_TAG=latest
docker image tag "${REPO_NAME}":"${IMAGE_TAG}" "${REPO_URI}":"${IMAGE_TAG}"
docker image push "${REPO_URI}":"${IMAGE_TAG}"
