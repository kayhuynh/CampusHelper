from django.shortcuts import render
from django.http import HttpResponse

import json

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
	#

def mytasks(request):
	#
