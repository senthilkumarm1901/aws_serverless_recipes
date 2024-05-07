FROM public.ecr.aws/lambda/python:3.9

WORKDIR .

RUN yum update -y && yum install -y gcc-c++

RUN pip install --upgrade pip
RUN pip install "presidio_analyzer[transformers]"
RUN pip install presidio_anonymizer
RUN pip install urllib3==1.26.6 && python -m spacy download en_core_web_sm
RUN pip install sentencepiece protobuf

# Install huggingface-cli and download the model
# RUN yum install -y amazon-linux-extras && \
# amazon-linux-extras install epel -y && \
# yum-config-manager --enable epel && \
# yum install git-lfs -y

# RUN git clone https://huggingface.co/ab-ai/pii_model /var/task/

# check if the installed model is usable

RUN mkdir -p /tmp/model

# changing TRANSFORMERS_CACHE to HF_HOME
RUN python -c "import os; os.environ['HF_HOME'] = '/tmp/model' ; from transformers import AutoTokenizer, AutoModelForTokenClassification; \
tokenizer = AutoTokenizer.from_pretrained('ab-ai/pii_model').save_pretrained('/tmp/model'); \
ner_model = AutoModelForTokenClassification.from_pretrained('ab-ai/pii_model').save_pretrained('/tmp/model')"


RUN python -c "from transformers import AutoTokenizer, AutoModelForTokenClassification; \
tokenizer = AutoTokenizer.from_pretrained('ab-ai/pii_model',cache_dir='/tmp/model'); \
ner_model = AutoModelForTokenClassification.from_pretrained('ab-ai/pii_model',cache_dir='/tmp/model')"


COPY ./codes/*.py .

CMD [ "lambda_function.lambda_handler" ]

# how to build the docker
# sudo docker buildx build --build-arg HF_TOKEN=$HF_TOKEN --platform linux/arm64 -f Dockerfile . -t presidio_text_anonym_ab_pii:29Apr  


# how to create the docker container locally
# docker run --rm -ti --entrypoint /bin/bash --platform linux/arm64 presidio_text_anonym_ab_pii:29Apr  