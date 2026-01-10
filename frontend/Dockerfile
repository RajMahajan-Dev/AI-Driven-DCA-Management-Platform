# Use Node 18 alpine
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json ./

# Clean install dependencies
RUN rm -rf node_modules package-lock.json && \
    npm install --legacy-peer-deps

# Copy application code
COPY . .

# Set environment variable to bind to all interfaces
ENV HOST=0.0.0.0

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "start"]
