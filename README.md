# Local Deployment

##### To start app on your machine run:  
`docker-compose up`

##### Collect static files:  
`docker exec -t secure_web_1 python manage.py collectstatic`

##### Run tests:  
`docker exec -t secure_web_1 python manage.py test`

# Demo

https://dry-scrubland-53938.herokuapp.com/

Sign in:  
https://dry-scrubland-53938.herokuapp.com/admin/

Important views:
* https://dry-scrubland-53938.herokuapp.com/protecor/create/ - create protected resource
* https://dry-scrubland-53938.herokuapp.com/api/v1/ - API
* https://dry-scrubland-53938.herokuapp.com/api/v1/resource/ - resources. You can go to "protected_url" and try POST
method with json body {"password": "<pass_from_previous_step>"}
* https://dry-scrubland-53938.herokuapp.com/api/v1/resource/stats/ - check stats