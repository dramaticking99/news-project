# 1. Use an official lightweight Node.js image as a base
FROM node:18-alpine

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy package.json and package-lock.json
COPY package*.json ./

# 4. Install application dependencies
RUN npm install

# 5. Copy the rest of your application's source code
COPY . .

# 6. Expose the port your app runs on
EXPOSE 5000

# 7. Define the command to run your app
CMD [ "npm", "run", "dev" ]