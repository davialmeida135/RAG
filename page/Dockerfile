# Use an official Node.js runtime as a parent image
FROM node:14

# Set the working directory
WORKDIR /page

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Install http-server globally
RUN npm install -g http-server

# Expose the port the app runs on
EXPOSE 3000

# Start the application
CMD ["npm", "start"]