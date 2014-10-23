from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader, Context, Template

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError

from CampusHelperApp import models

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
			requestHeader = json.loads(request.body)
			username = requestHeader["username"]
			password = requestHeader["password"]
			u = models.getUser(username)
			if u.password != password:
				return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)
			request.session["cookieID"] = u.cookieID
			return HttpResponse(json.dumps({"errcode": SUCCESS}), content_type = "application/json", status = 200)
		elif request.method == "GET":
			template = loader.get_template("index.html")
			context = RequestContext(request)
			return HttpResponse(template.render(context))
		else:
			return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	except (ValidationError, ObjectDoesNotExist):
		return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)
	except (ValueError, KeyError):
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def login(request):
	if request.method == "GET":
		template = loader.get_template("login.html")
		context = RequestContext(request)
		return HttpResponse(template.render(context))
	else:
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

# Shows a list of all tasks globally 
def alltasks(request):
    if request.method == "GET":
        template = loader.get_template('alltasks.html')
        all_tasks = models.Task.objects.all()
        context = Context({"allTasks": all_tasks})
        return HttpResponse(template.render(context))
    else:
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
        """
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
            requestHeader = json.loads(request.body)
            field = requestHeader["field"]
            newdata = requestHeader["newdata"]
            cookieID = request.session["cookieID"]
            u = models.getUserByCookieID(cookieID)
            if field == USER_PASSWORD:
                u.setPassword(newdata)
            if field == USER_EMAIL:
                u.setEmail(newdata)
            elif field == USER_DESCRIPTION:
                u.setDescription(newdata)
        """
        if request.method == "GET":
            cookieID = request.session["cookieID"]
            u = models.getUserByCookieID(cookieID)
            template = loader.get_template("profile.html")
            context = Context({"user" : u.username})
            return HttpResponse(template.render(context))
        else:
            return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
    except ValidationError:
        return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

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
			field = requestHeader["field"]
			newdata = requestHeader["newdata"]
			cur_task = models.getTask(taskID)
			cookieID = request.session["cookieID"]
			u = models.getUserByCookieID(cookieID)
			if u.username != cur_task.creator:
				return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)
			if field == TASK_TITLE:
				cur_task.setTitle(newdata)
			elif field == TASK_DESCRIPTION:
				cur_task.setDescription(newdata)
			elif field == TASK_STATE:
				if newdata == STATE_ACCEPTED:
					cur_task.markAccepted(u)
				elif newdata == STATE_COMPLETED:
					cur_task.markCompleted()
				else:
					return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)
			else:
				return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)
			return HttpResponse(json.dumps({"errcode": SUCCESS}), content_type = "application/json", status = 200)
		elif request.method == "GET":
			return HttpResponse("task Query get request")
		else:
			return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	except (ValidationError):
		return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)
	except (ValueError, KeyError):
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def newtask(request):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
            requestHeader = json.loads(request.body)
            title = requestHeader["title"]
            description = requestHeader["description"]
            cookieID = request.session["cookieID"]
            u = models.getUserByCookieID(cookieID)
            creator = u.username
            task = models.newTask(u, title, description)
            return HttpResponse(json.dumps({"errcode": SUCCESS, "taskID": task.taskID}), content_type = "application/json", status = 200)
        elif request.method == "GET":
            return HttpResponse("new task get request")
        else:
            return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
    except (ValidationError):
        return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)
    except (ValueError, KeyError):
        return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def newuser(request):
	 try:
		  if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
				d = json.loads(bytes.decode(request.body))
				u = models.newUser(d["username"], d["password"], d["email"], d["description"])
				request.session["cookieID"] = u.cookieID
				return HttpResponse(json.dumps({"errcode": SUCCESS}), content_type = "application/json")
		  elif request.method == "GET":
				template = loader.get_template("signup.html")
				context = RequestContext(request)
				return HttpResponse(template.render(context))
		  else:
				return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	 except (ValidationError, IntegrityError):
		  return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json")
	 except (ValueError, KeyError):
		  return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def mytasks(request):
	try:
		if request.method == "GET":
			return HttpResponse("mytasks get request")
			u = models.getUserByCookieID(request.session["cookieID"])
		else:
			return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
	except ObjectDoesNotExist:
		return HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 200)
	except (ValueError, KeyError):
		return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)
