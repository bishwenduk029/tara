FROM node:18.16 AS frontend_builder

WORKDIR /frontend

COPY ./frontend/ ./

RUN yarn build

# Stage 2: Final Image
FROM nvidia/cuda:11.7.1-runtime-ubuntu20.04

# Install NVIDIA Container Toolkit for GPU support
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=11.0"

# Install FFmpeg for video processing
RUN apt-get update && apt-get install -y ffmpeg

# Copy frontend build from the frontend_builder stage
COPY --from=frontend_builder /frontend/dist /app/frontend/dist

# Set the working directory for the Python application
WORKDIR /app

# Copy the backend Python requirements file
COPY ./backend/requirements.txt .

# Install Python dependencies
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# Copy the backend application code
COPY ./backend /app

# Environment variable for controlling the number of Uvicorn workers
ENV MAX_WORKERS=5

# Command to start the FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", ${MAX_WORKERS}]