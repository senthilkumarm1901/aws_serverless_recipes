# Stage 1: Build environment using a Python base image
FROM python:3.12 as builder

# Install build tools
RUN apt-get update && apt-get install -y gcc g++ cmake zip

# Copy requirements.txt and install packages with appropriate CMAKE_ARGS
COPY requirements.txt .
RUN CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install --upgrade pip && pip install -r requirements.txt

# Stage 2: Final image using AWS Lambda Python image
FROM public.ecr.aws/lambda/python:3.12

# Install huggingface-cli and download the model
# the original phi2 model - TheBloke/phi-2-GGUF phi-2.Q4_K_M.gguf

# RUN pip install huggingface-hub && \
#     mkdir model && \
#     huggingface-cli download microsoft/Phi-3-mini-4k-instruct-q4.gguf --local-dir ./model --local-dir-use-symlinks False

RUN pip install huggingface-hub && mkdir -p model 

# downloaded manually from https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/tree/main
COPY ./Phi-3-mini-4k-instruct-q4.gguf model/

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /var/lang/lib/python3.12/site-packages/

# Copy lambda function code
RUN echo "changed some code in function"
COPY codes/lambda_function.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.handler" ]

# sudo docker buildx build --platform linux/arm64 -f Dockerfile . -t llm_on_lambda:24apr2024

# to start the container locally
# docker run --rm -ti --platform linux/arm64 -p 9000:8080 llm_on_lambda:24apr2024

# to invoke the lambda locally
# curl "http://localhost:9000/2015-03-31/functions/function/invocations" \
#      -d '{ "body": "{ \"prompt\": \"Generate a good name for a bakery.\" }" }' > output.json


# curl -X PUT -d @example_prompt_input.json "http://localhost:9000/2015-03-31/functions/function/invocations"

# to experiment locally in docker
# docker run --rm -ti --entrypoint /bin/bash --platform linux/arm64 llm_on_lambda:24apr2024  