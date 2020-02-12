# Rest API Using Flask

### Instructions for running the App:

     pip install -r requirements.txt
     
     Create 'flask_rest_db' database in MySQL
     
     Run the below commands to create required tables:
     python migrate.py db init
     python migrate.py db migrate
     python migrate.py db upgrade
     python run.py