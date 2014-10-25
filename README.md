CampusHelper
============

To run the project:
first clone a copy from git repo
then call ./manage.py migrate
then call ./manage.py runserver to run it locally.

To test the project:
run test from coverage: coverage run --source="." manage.py test CampusHelperApp

-----
In order to push to github:
	git push origin <branch>

***
In order to push to Heroku:
	git push heroku <branch>

*** 
In order to simulate Heroku locally: RUN
	foreman start
in the same directory as the Procfile
