# Use a robust and commonly available tag for the Python 3.11 Lambda base image
FROM public.ecr.aws/lambda/python:3.11

# Set working directory inside the container
WORKDIR /var/task

# Install Python packages.
# For large scientific libraries like PyTorch and NumPy, it's best to rely on pre-built wheels.
# We will use versions that are known to have good manylinux wheel support for Python 3.11.

# 1. Install PyTorch CPU wheel (direct URL, verify this specific URL if it breaks again)
# The version 2.3.0 is a good starting point for Py3.11.
RUN pip install "https://download.pytorch.org/whl/cpu/torch-2.3.0%2Bcpu-cp311-cp311-linux_x86_64.whl" \
    --target /var/task \
    --no-cache-dir

# 2. Install numpy, transformers, and boto3
# Use a version of numpy that's known to have reliable manylinux wheels for py3.11.
# Pinning transformers to a version compatible with our chosen torch.
# Allow pip to find the best binary for numpy and transformers' sub-dependencies.
RUN pip install \
    numpy==1.24.4 \
    transformers==4.30.2 \
    boto3 \
    --target /var/task \
    --no-cache-dir

# Copy your Lambda handler code into the container
COPY inference_handler.py .

# --- Copy the pre-downloaded model weights ---
RUN mkdir -p /opt/ml_model/
COPY ./local_distilbert_model/ /opt/ml_model/

# Set the default command for the container
CMD ["inference_handler.lambda_handler"]