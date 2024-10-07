FROM ubuntu:latest
LABEL authors="reem"

RUN apt-get update

# Install nodejs and npm
RUN apt-get install -y nodejs npm

# Copy the code
COPY . /app

# Install node dependencies
WORKDIR /app
RUN npm install

# Run the app
CMD ["npm", "start"]
