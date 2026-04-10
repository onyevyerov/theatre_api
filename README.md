# Theatre API
API for a theater service that allows people to browse available performances and buy tickets without leaving home.
# Installing using GitHub
Install PostgreSQL and create db
````
git clone https://github.com/onyevyerov/theatre_api.git
cd theatre_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db username>
set DB_PASSWORD=<your db user password>
set SECRET_KEY=<your secret key>
python manage.py migrate
python manage.py runserver
````
# Run with docker
Docker should be installed
```bash
docker-compose build
docker-compose up
```
## Getting access
- create user via /api/user/register/
- get access token via /api/user/login/
## Features
- JWT authenticated
- Admin panel /admin/
- Documentation is located at /api/swagger/
- Managing orders and tickets
- Creating plays with genres, actors
- Creating theatre halls
- Adding performances
- Filtering plays and performances