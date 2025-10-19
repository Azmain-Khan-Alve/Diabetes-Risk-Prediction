# Step 1: Start with an official Python "base image"
# This gives us a clean Linux OS with Python 3.11 pre-installed.
FROM python:3.11-slim

# Step 2: Set a "working directory" inside the container
# This is where our app will live.
WORKDIR /app

# Step 3: Copy only the requirements file first and install dependencies
# This is a cool trick. Docker caches this step. If we don't change
# requirements.txt, it won't re-install everything, making builds faster.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy our application's source code and models into the container
# This copies the 'src' folder to '/app/src'
COPY ./src ./src
# This copies the 'models' folder to '/app/models'
COPY ./models ./models

# Step 5: Expose the port our app runs on
# This tells Docker that our application will be listening on port 5000.
EXPOSE 5000

# Step 6: Define the command to run the application
# This is the command that starts our Flask server.
CMD ["python", "src/app.py"]