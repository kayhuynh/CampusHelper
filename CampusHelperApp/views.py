from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ValidationError

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
      	#
      else if request.method == "GET":
      	#
   except (ValueError, KeyError):
      return HttpResponse(json.dumps({}), content_type = "application/json", status = 500)

def alltasks(request):
	#

def alltasksQuery(request, query):
	#

def profile(request):
	#

def profileQuery(request, helper):
	#

def taskQuery(request, taskID):
	#

def newtask(request):
	#

def newuser(request):
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

def mytasks(request):
	#
