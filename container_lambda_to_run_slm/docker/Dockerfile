# Stage 1: Build environment using a Python base image
FROM python:3.12-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    cmake \
    zip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image using AWS Lambda Python image
FROM public.ecr.aws/lambda/python:3.12

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /var/lang/lib/python3.12/site-packages/

RUN mkdir -p ${LAMBDA_TASK_ROOT}/model
RUN pip install --no-cache-dir "huggingface_hub[cli]"
RUN huggingface-cli download microsoft/Phi-3-mini-4k-instruct-gguf Phi-3-mini-4k-instruct-q4.gguf --local-dir ${LAMBDA_TASK_ROOT}/model

COPY codes/lambda_function.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.handler" ]
