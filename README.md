# Rest API Using Flask

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Setting up virualenv and installing requirements

Create virtual environment for the application:<br />
```
virtualenv app
```
 
Source scripts to activate the virtualenv:<br />
```
source Scripts/activate
```
 
Install requirements for the project:<br />
```
pip install -r requirements.txt
```

### Setting database in MySQL:
```
CREATE DATABASE flask_rest_db;
```

### Creating required tables:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
``` 
### Runing the application:
```
python run.py
```
