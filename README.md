# Django rest image


Django rest image is api created to allow user to upload and list images.



## Features

- Upload images
- automatically creating thumbnails (size of thumbnails depends on user tier).
- Creating expiring links to images for users with specified tiers which allows to do it.




## Tech


- [django] 
- [django-rest-framework] 
- [postgresql]




## How to run

Inside the app folder run following command:

```sh
docker-compose  up
```
After run is recommended to run:

```sh
python3 manage.py createsuperuser
```
inside docker container and create user.

For locally runnings:
First u have to run postgre database with created rest_api database and then run following commands:

```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Description

Api is working on "api/v1/" url. Authentication is done using tokens  below I listed the adresses and functionality. 
For all requests exclude first we have to add Authorization header. There are three based tiers as it was described in task and one is extra for admin.
Staff users can create custom tiers.
| adres | description |
| ------ | ------ |
| token/login | Authorization adress - api returns auth token which is necessary to work with api |
| images | allowed method: get - we list our images|
| create | allowed method: post - we upload image - api create thumbnails and originl image if we have access to it  |
| explinks |allowed method: post -  we generate expiring link using link of image and time |






