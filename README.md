# webtronics-test
Welcom to the user posts API. 
First you need to sign up and then you can log in. 
You can create, change and delete posts. 
You can also rate posts, but not own. 
If there is "like" or "dislike" that you setted, you can't set another one.
But you can change you choice. If there is like and you want to set dislike, 
so dislike will be seetted and like will be deleted

Commands below you need to execute from project root directory
## Run docker compose
if using version 1
```bash
docker-compose up -d
```
if using version 2
```bash
docker compose up -d
```

## Create database
get into "site" container and execute
```bash
docker exec -it site sh
```
and create database
```bash
alembic upgrade head
```
then create admin
```bash
./manager.py admin create-admin
```
run tests
```bash
pytest tests
```
