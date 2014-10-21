from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ValidationError
<<<<<<< HEAD
from CampusHelperApp import models
from CampusHelperApp.models import User
from CampusHelperApp.models import Task

#For now all POST method is implemented but still cookie has not been figured out. So please have a look. Please
#inspect line 4-6 imports because it might cause problems. Ensure the validation error is properly used and handled
#Call me 5104176797 if any question.
=======

from CampusHelperApp import models
>>>>>>> 6b09a1f3f2a44a90c53dd65a339567511bda777d

import json

SUCCESS = 1
FAILURE = 2

USER_PASSWORD = 1
USER_EMAIL = 2
USER_DESCRIPTION = 3

TASK_TITLE = 1
TASK_DESCRIPTION = 2
TASK_STATE = 3

STATE_CREATED = 1
STATE_ACCEPTED = 2
STATE_COMPLETED = 3

def root(request):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
        	Requestheader = json.loads(request.body)
        	username = Requestheader("username")
        	password = Requestheader("password")
        	cookie
        	#!!!!! we need a cookie there!!!!!!

        else if request.method == "GET":

        return HttpResponse(json.dumps({errcode: SUCCESS, cookie: cookie}), content_type = "application/json", status = 200)

    except (ValidationError):
    	return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
      	#
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def alltasks(request):
    try:
        if request.method == "GET" and "application/json" in request.META["CONTENT_TYPE"]:

      	#
 
      	#
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

	#

def alltasksQuery(request, query):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
      	#
        else if request.method == "GET":
      	#
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	#

def profile(request):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
        	Requestheader = json.loads(request.body)
        	field = Requestheader("field")
        	newdata = Requestheader("newdata")
        	if field == USER_PASSWORD:
        		User.setPassword(newdata)

        	if field == USER_EMAIL:
        		User.setEmail(newdata)
        	
        	else:
        		User.setDescription(newdata)

        	return HttpResponse(json.dumps({errcode: SUCCESS}), content_type = "application/json", status = 200)

      	#
        else if request.method == "GET":
      	#
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

    except (ValidationError):
    	return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
	#
	#

def profileQuery(request, helper):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
        	
      	#
 
      	#
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	#

def taskQuery(request, taskID):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
        	Requestheader = json.loads(request.body)
        	field = Requestheader("field")
        	newdata = Requestheader("newdata")

        	if field == STATE:


        		if newdata == STATE_ACCEPTED:
        			cur_task = models.getTask(taskID)
        			cur_task.markAccepted()

        		else:
        			cur_task = models.getTask(taskID)
        			cur_task.markCompleted()

        		return HttpResponse(json.dumps({errcode: SUCCESS}), content_type = "application/json", status = 200)

        			


      	#
        else if request.method == "GET":

    except (ValidationError):
    	return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)

      	#
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	#

def newtask(request):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
        	Requestheader = json.loads(request.body)
        	title = Requestheader("title")
        	description = Requestheader("description")
        	creator

        	newtask = models.newTask(creator,title,description)

        else if request.method == "GET":

        return HttpResponse(json.dumps({errcode: SUCCESS, taskID: newtask.id}), content_type = "application/json", status = 200)


    except (ValidationError):
    	return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)

      	#
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	#

def newuser(request):
<<<<<<< HEAD
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
        	Requestheader = json.loads(request.body)
        	username = Requestheader("username")
        	password = Requestheader("password")
        	email = Requestheader("email")
        	description = Requestheader("description")

        	models.newUser(username,password,email,description)



      	#
        else if request.method == "GET":

        return HttpResponse(json.dumps({errcode: SUCCESS, taskID: newtask.id}), content_type = "application/json", status = 200)

    except (ValidationError):
    	return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
      	#
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	#
=======
   try:
      if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
         d = json.loads(bytes.decode(request.body))
         u = models.newUser(d["username"], d["password"], d["email"], d["description"])
         request.session["cookieID"] = u.cookieID
      	return HttpResponse(json.dumps({"errcode" : SUCCESS}), content_type = "application/json")
      else if request.method == "GET":
      	#
   except (ValueError, KeyError):
      return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
   except ValidationError:
   	return HttpResponse(json.dumps({"errcode" : FAILURE}), content_type = "application/json")
>>>>>>> 6b09a1f3f2a44a90c53dd65a339567511bda777d

def mytasks(request):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
      	#
        else if request.method == "GET":
      	#
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	#
