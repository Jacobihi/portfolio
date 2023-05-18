# I want to run an ssh command in a linux environment and then mount an external volume on run to save the package to.


FROM public.ecr.aws/lambda/python:3.9

RUN here=$(pwd)
RUN mkdir data
RUN mkdir docker-package
RUN pip install pandas -t docker-package
RUN cd $here
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
# RUN zip -r data/my-docker-zip.zip data/docker-package
CMD ["lambda_function.lambda_handler"]
