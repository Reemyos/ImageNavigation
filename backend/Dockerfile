FROM python:3.11-slim
LABEL authors="reem"

# Copy the code
WORKDIR /backend
COPY . /backend

# Install python dependencies
COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

# Set the environment variable
ENV PYTHONPATH="${PYTHONPATH}:/backend"

# Run the app
CMD ["uvicorn", "image_navigation:app", "--host", "0.0.0.0", "--port", "8000"]
