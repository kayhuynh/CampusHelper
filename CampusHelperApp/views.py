from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError
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
<<<<<<< HEAD
   try:
      if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
        	requestHeader = json.loads(request.body)
        	username = requestHeader("username")
        	password = requestHeader("password")
        	u = models.getUser(username)
        	if u.password != password:
        		return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
         request.session["cookieID"] = u.cookieID
        	return HttpResponse(json.dumps({errcode: SUCCESS}), content_type = "application/json", status = 200)
      elif request.method == "GET":
          template = loader.get_template("index.html")
          context = RequestContext(request)
          return HttpResponse(template.render(context))
      	#
      else:
      	return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
   except (ValidationError, ObjectDoesNotExist):
    	return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
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

def alltasksQuery(request, query):
   try:
      if request.method == "GET":
      	return HttpResponse("alltasksquery get requests")
      else:
      	return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
   except (ValueError, KeyError):
      return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def profile(request):
   try:
      if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
        	requestHeader = json.loads(request.body)
        	field = requestHeader("field")
        	newdata = requestHeader("newdata")
        	cookieID = request.session["cookieID"]
        	u = models.getUserByCookieID(cookieID)
        	if field == USER_PASSWORD:
        		u.setPassword(newdata)
        	if field == USER_EMAIL:
        		u.setEmail(newdata)
        	elif field == USER_DESCRIPTION:
        		u.setDescription(newdata)
        	else:
        		User.setDescription(newdata)

        	return HttpResponse(json.dumps({"errcode": SUCCESS}), content_type = "application/json", status = 200)

        elif request.method == "GET":
      	   return HttpResponse("get profile request")
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

    except (ValidationError):
    	return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)

def profileQuery(request, helper):
   try:
      if request.method == "GET":
        	return HttpResponse("profile query get request")
      else:
      	return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
   except (ValueError, KeyError):
      return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def taskQuery(request, taskID):
   try:
      if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
        	requestHeader = json.loads(request.body)
        	field = requestHeader("field")
        	newdata = requestHeader("newdata")
        	cur_task = models.getTask(taskID)
        	cookieID = request.session["cookieID"]
        	u = models.getUserByCookieID(cookieID)
        	if u.username != cur_task.creator:
        		return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
        	if field == TASK_TITLE:
        		cur_task.setTitle(newdata)
        	elif field == TASK_DESCRIPTION:
        		cur_task.setDescription(newdata)
        	elif field == TASK_STATE:
        		if newdata == STATE_ACCEPTED:
        			cur_task.markAccepted()
        		elif newdata == STATE_COMPLETED:
        			cur_task.markCompleted()
        		return HttpResponse(json.dumps({"errcode": SUCCESS}), content_type = "application/json", status = 200)

        elif request.method == "GET":
          return HttpResponse("task Query get request")

    except (ValidationError):
    	return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)

    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	#

def mytasks(request):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
      	   return HttpResponse("mytasks post request")
        elif request.method == "GET":
      	   return HttpResponse("mytasks get request")
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
    else:
        return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
     		else:
     			return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
     		return HttpResponse(json.dumps({errcode: SUCCESS}), content_type = "application/json", status = 200)
      elif request.method == "GET":
      	#
      else:
      	return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
   except (ValidationError):
    	return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
   except (ValueError, KeyError):
      return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
=======
	try:
		if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
			requestHeader = json.loads(request.body)
			username = requestHeader("username")
			password = requestHeader("password")
			u = models.getUser(username)
			if u.password != password:
				return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
			request.session["cookieID"] = u.cookieID
			return HttpResponse(json.dumps({errcode: SUCCESS}), content_type = "application/json", status = 200)
		elif request.method == "GET":
			#
		else:
			return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	except (ValidationError, ObjectDoesNotExist):
		return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
	except (ValueError, KeyError):
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def alltasks(request):
	try:
		if request.method == "GET":
			#
		else:
			return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	except (ValueError, KeyError):
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def alltasksQuery(request, query):
	try:
		if request.method == "GET":
			#
		else:
			return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	except (ValueError, KeyError):
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def profile(request):
	try:
		if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
			requestHeader = json.loads(request.body)
			field = requestHeader("field")
			newdata = requestHeader("newdata")
			cookieID = request.session["cookieID"]
			u = models.getUserByCookieID(cookieID)
			if field == USER_PASSWORD:
				u.setPassword(newdata)
			if field == USER_EMAIL:
				u.setEmail(newdata)
			elif field == USER_DESCRIPTION:
				u.setDescription(newdata)
			else:
				return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
			return HttpResponse(json.dumps({errcode: SUCCESS}), content_type = "application/json", status = 200)
		elif request.method == "GET":
			#
		else:
			return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	except ValidationError:
		return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
	except (ValueError, KeyError):
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def profileQuery(request, helper):
	try:
		if request.method == "GET":
			#
		else:
			return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	except (ValueError, KeyError):
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def taskQuery(request, taskID):
	try:
		if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
			requestHeader = json.loads(request.body)
			field = requestHeader("field")
			newdata = requestHeader("newdata")
			cur_task = models.getTask(taskID)
			cookieID = request.session["cookieID"]
			u = models.getUserByCookieID(cookieID)
			if u.username != cur_task.creator:
				return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
			if field == TASK_TITLE:
				cur_task.setTitle(newdata)
			elif field == TASK_DESCRIPTION:
				cur_task.setDescription(newdata)
			elif field == TASK_STATE:
				if newdata == STATE_ACCEPTED:
					cur_task.markAccepted()
				elif newdata == STATE_COMPLETED:
					cur_task.markCompleted()
				else:
					return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
			else:
				return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
			return HttpResponse(json.dumps({errcode: SUCCESS}), content_type = "application/json", status = 200)
		elif request.method == "GET":
			#
		else:
			return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	except (ValidationError):
		return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
	except (ValueError, KeyError):
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
>>>>>>> 1ca8e657e608940b7fd949c595e5f4dbcd002779

def newtask(request):
	try:
		if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
			requestHeader = json.loads(request.body)
			title = requestHeader("title")
			description = requestHeader("description")
			cookieID = request.session["cookieID"]
			u = models.getUserByCookieID(cookieID)
			creator = u.username
			task = models.newTask(creator, title, description)
			return HttpResponse(json.dumps({errcode: SUCCESS, taskID: task.taskID}), content_type = "application/json", status = 200)
		elif request.method == "GET":
			#
		else:
			return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	except (ValidationError):
		return HttpResponse(json.dumps({errcode: FAILURE}), content_type = "application/json", status = 200)
	except (ValueError, KeyError):
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def newuser(request):
	try:
		if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
			d = json.loads(bytes.decode(request.body))
			u = models.newUser(d["username"], d["password"], d["email"], d["description"])
			request.session["cookieID"] = u.cookieID
			return HttpResponse(json.dumps({"errcode" : SUCCESS}), content_type = "application/json")
		elif request.method == "GET":
			#
		else:
			return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	except (ValidationError, IntegrityError):
		return HttpResponse(json.dumps({"errcode" : FAILURE}), content_type = "application/json")
	except (ValueError, KeyError):
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def mytasks(request):
	try:
		if request.method == "GET":
			#
		else:
			return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	except (ValueError, KeyError):
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
