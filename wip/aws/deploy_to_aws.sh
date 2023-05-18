
aws lambda create-function --region "${REGION}" --function-name test-spark \
    --package-type Image  \
    --code ImageUri="${REPO_URI}":"${IMAGE_TAG}"   \
    --role ${ROLE_ARN}
