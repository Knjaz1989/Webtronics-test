# webtronics-test
Welcom to the user posts API. 
First you need to sign up and then you can log in. 
You can create, change and delete posts. 
You can also rate posts, but not own. 
If there is "like" or "dislike" that you setted, you can't set another one.
But you can change you choice. If there is like and you want to set dislike, 
so dislike will be seetted and like will be deleted

Commands below you need to execute from project root directory
## Create database
```bash
alembic upgrade head
```

## Run server
```bash
./manager.py site run
```
