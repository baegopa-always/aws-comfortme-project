# aws 에서 제공하는 lambda base image (python)
FROM amazon/aws-lambda-python:3.8

# optional : ensure that pip is up to data
RUN /var/lang/bin/python3.8 -m pip install --upgrade pip

#pre-trained model copy
COPY korean_bert_model /var/task/korean_bert_model

#lambda function copy
COPY lambda_function.py /var/task/

#requirements copy
COPY requirements.txt /var/task/

# install packages
RUN pip install -r /var/task/requirements.txt

# lambda_function.handler 실행
CMD ["lambda_function.handler"]