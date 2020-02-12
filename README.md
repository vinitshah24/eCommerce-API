# Rest API Using Flask

### Instructions for running the App:

     Install requirements for the project:
     pip install -r requirements.txt
     
     Execute the below command in MySQL:
     CREATE DATABASE flask_rest_db;
     
     Run the following commands to create required tables:
     python migrate.py db init
     python migrate.py db migrate
     python migrate.py db upgrade
     
     Run the application:
     python run.py
