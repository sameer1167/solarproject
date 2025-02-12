# Use official Python image
FROM  python:3.13.2

#make a folder in container as it is my working directory
WORKDIR /SolarApp

#copying requrments.txt
COPY requirments.txt .

#install depandencies
# •	pip install -r requirements.txt → Installs all required Python packages.
# •	–no-cache-dir → Prevents unnecessary caching to keep the container lightweight.
RUN pip install --no-cache-dir -r requirments.txt

#copy the rest to working directory that is SolarApp
COPY . .

# Expose port 8000 (default Django port)
EXPOSE 8000

# Run migrations and start Django server
# CMD → Defines the default command that runs when the container starts.
# •	sh -c → Runs a shell command.
# •	python manage.py migrate → Applies database migrations.
# •	&& → Runs the next command only if migrations succeed.
# •	python manage.py runserver 0.0.0.0:8000 → Starts the Django server and listens on all network interfaces (0.0.0.0), allowing external access.
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]