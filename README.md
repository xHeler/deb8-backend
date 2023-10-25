# Deb8 - Backend

## Requirements
- Python version 3.10.12
- Docker newest version + compose plugin

## Instalation

```shell
python3 -m venv .venv

# windows
.venv/Scripts/activate
# linux
source .venv/bin/activate

pip3 install -r requirements.txt
```

## Running project
```shell
docker compose up -d --build
```

## Database migration (First run only!)
```shell
docker compose exec web python manage.py migrate
```

## Using Swagger

You must login ang get token from endpoint `http://localhost:8000/api/auth/login/`

Also you need to add this token into `Authorize` field in swagger on endpoint `http://localhost:8000/swagger/"` with key word. 

Example: ```key a2de1cc7ca27c8e5a699d41d6d08739ea68e285f```
