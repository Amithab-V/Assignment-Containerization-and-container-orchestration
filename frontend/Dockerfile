# Use official Node.js Alpine image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies separately to leverage Docker cache
COPY helloService/package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# Start the application
CMD ["npm", "run", "dev"]