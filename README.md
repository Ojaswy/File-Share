# File-Share
A File Sharing Django App

## Requirements
* Python
* Django, python_dotenv


## Installing
1) Install python for your platform
3) Clone the repo using ```git clone https://github.com/Ojaswy/File-Share.git```
2) Install python packages using ```pip install -r requirements.txt```
4) Make the database migrations
```shell
python manage.py makemigrations
python manage.py migrate
```
5) (Optional) Make superuser using
```shell
python manage.py createsuperuser
```
6) Rename .env.default to .env and populate the fields
7) Run ```python manage.py runserver``` to get your webserver working!
8) Browse to [127.0.0.1:8000](http://127.0.0.1:8000)
