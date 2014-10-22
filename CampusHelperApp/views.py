from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.template import RequestContext, loader
from CampusHelperApp import models
from CampusHelperApp.models import User
from CampusHelperApp.models import Task

#For now all POST method is implemented but still cookie has not been figured out. So please have a look. Please
#inspect line 4-6 imports because it might cause problems. Ensure the validation error is properly used and handled
#Call me 5104176797 if any question.

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
        	cookie = "asdfasdf"      #just to see if it works
        	#!!!!! we need a cookie there!!!!!!
        elif request.method == "GET":
          template = loader.get_template("index.html")
          context = RequestContext(request)
          return HttpResponse(template.render(context))
        return HttpResponse(json.dumps({"errcode": SUCCESS}), content_type = "application/json", status = 200)

    except (ValidationError):
    	return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)
      	#
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def login(request):
    try:
      if request.method == "GET":
        template = loader.get_template("login.html")
        context = RequestContext(request)
        return HttpResponse(template.render(context))
    except (ValidationError):
      return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)
        #
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def alltasks(request):
    try:
        if request.method == "GET" and "application/json" in request.META["CONTENT_TYPE"]:
          return HttpResponse("all tasks get request")
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

	#

def alltasksQuery(request, query):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
      	   pass
        elif request.method == "GET":
      	   return HttpResponse("alltasksquery get requests")
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

        	return HttpResponse(json.dumps({"errcode": SUCCESS}), content_type = "application/json", status = 200)

        elif request.method == "GET":
      	   return HttpResponse("get profile request")
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

    except (ValidationError):
    	return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)
	#
	#

def profileQuery(request, helper):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
          return HttpResponse("profile query post request")
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

        		return HttpResponse(json.dumps({"errcode": SUCCESS}), content_type = "application/json", status = 200)

        elif request.method == "GET":
          return HttpResponse("task Query get request")

    except (ValidationError):
    	return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)

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
        elif request.method == "GET":
            return HttpResponse("new task get request")
        return HttpResponse(json.dumps({"errcode": SUCCESS, taskID: newtask.id}), content_type = "application/json", status = 200)


    except (ValidationError):
    	return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)

      	#
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	#

def newuser(request):
  try:
    if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
      d = json.loads(bytes.decode(request.body))
      u = models.newUser(d["username"], d["password"], d["email"], d["description"])
      request.session["cookieID"] = u.cookieID
      return HttpResponse(json.dumps({"errcode" : SUCCESS}), content_type = "application/json")
    elif request.method == "GET":
      template = loader.get_template("signup.html")
      context = RequestContext(request)
      return HttpResponse(template.render(context))
  except (ValueError, KeyError):
      return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
  except ValidationError:
   	  return HttpResponse(json.dumps({"errcode" : FAILURE}), content_type = "application/json")

def mytasks(request):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
      	   return HttpResponse("mytasks post request")
        elif request.method == "GET":
      	   return HttpResponse("mytasks get request")
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	#
