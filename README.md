# Django

# start/dev
$ docker-compose -f docker-compose.yml up

## Build project

```
docker-compose build
```

## Running for debug mode
```
docker-compose run --service web
```

## Start app
```
docker-compose run web python3 manage.py startapp <APPNAME>
```
