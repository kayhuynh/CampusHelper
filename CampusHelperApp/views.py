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
TASK_SUMMARY = 4
TASK_CATEGORY = 5
TASK_VALUE = 6

STATE_CREATED = 1
STATE_ACCEPTED = 2
STATE_COMPLETED = 3

# the request was in a correct format but it was bad for some reason - 403 "forbidden"
SOFTFAIL = HttpResponse(json.dumps({"errcode": FAILURE}), content_type = "application/json", status = 403)

# the request isn't even in a correct format - 400 "bad request"
HARDFAIL = HttpResponse(json.dumps({}), content_type = "application/json", status = 400)

def root(request):
    if request.method == "GET":
        template = loader.get_template("index.html")
        context = RequestContext(request)
        return HttpResponse(template.render(context))
    else:
        return HARDFAIL

def login(request):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
            requestHeader = json.loads(bytes.decode(request.body))
            username = requestHeader["username"]
            password = requestHeader["password"]
            u = models.getUser(username)
            if u.password != password:
                return SOFTFAIL
            request.session["cookieID"] = u.cookieID
            return HttpResponse(json.dumps({"errcode": SUCCESS}), content_type = "application/json")
        elif request.method == "GET":
            template = loader.get_template("login.html")
            context = RequestContext(request)
            return HttpResponse(template.render(context))
        else:
            return HARDFAIL
    except (ValidationError, ObjectDoesNotExist):
        return SOFTFAIL
    except (ValueError, KeyError):
        return HARDFAIL

def logout(request):
    request.session["cookieID"] = 0
    del request.session["cookieID"]
    return HttpResponse("logged out!")

# Shows a list of all tasks globally
def alltasks(request):
    try:
        if request.method == "GET":
            cookieID = request.session["cookieID"]
            user = models.getUserByCookieID(cookieID)
            template = loader.get_template("postBoard/alltasks.html")
            all_tasks = models.Task.objects.filter(state__exact = STATE_CREATED)
            if "showAccepted" in request.GET and request.GET["showAccepted"] == "true":
                all_tasks |= models.Task.objects.filter(state__exact = STATE_ACCEPTED)
            if "showCompleted" in request.GET and request.GET["showCompleted"] == "true":
                all_tasks |= models.Task.objects.filter(state__exact = STATE_COMPLETED)
            if "q" in request.GET:
                all_tasks = all_tasks.filter(title__contains = request.GET["q"])
            if "c" in request.GET:
                all_tasks = all_tasks.filter(category__exact = request.GET["c"])
            context = Context({"allTasks": all_tasks, "user": user.username})
            return HttpResponse(template.render(context))
        else:
            return HARDFAIL
    except (ValueError, KeyError):
        return HARDFAIL

def profile(request):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
            requestHeader = json.loads(bytes.decode(request.body))
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
            return HttpResponse(status = 200) #temporary addition by Nick to make test pass, previously no response returned
        #if request.method == "GET" and "q" in request.GET:
        if request.method == "GET":
            cookieID = request.session["cookieID"]
            u = models.getUserByCookieID(cookieID)
            template = loader.get_template("profile.html")
            context = Context({"user": u.username, "myCreatedTasks": u.tasksCreated.all(),
                "myAcceptedTasks": u.tasksAccepted.all()})
            return HttpResponse(template.render(context))
        else:
            return HARDFAIL
    except ValidationError:
        return SOFTFAIL
    except (ValueError, KeyError):
        return HARDFAIL

def task(request):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
            requestHeader = json.loads(bytes.decode(request.body))
            field = int(requestHeader["field"])
            newdata = requestHeader["newdata"]
            cur_task = models.getTask(request.GET["q"])
            cookieID = request.session["cookieID"]
            u = models.getUserByCookieID(cookieID)
            if u.username != cur_task.creator:
                if field == TASK_STATE:
                    if int(newdata) == STATE_ACCEPTED:
                        cur_task.markAccepted(u)
                    elif int(newdata) == STATE_COMPLETED:
                        cur_task.markCompleted()
                    else:
                        return SOFTFAIL
                else:
                    return SOFTFAIL
            elif field == TASK_TITLE:
                cur_task.setTitle(newdata)
            elif field == TASK_DESCRIPTION:
                cur_task.setDescription(newdata)
            elif field == TASK_SUMMARY:
                cur_task.setSummary(newdata)
            elif field == TASK_VALUE:
                cur_task.setValue(newdata)
            elif field == TASK_CATEGORY:
                cur_task.setCategory(newdata)
            else:
                return SOFTFAIL
            return HttpResponse(json.dumps({"errcode": SUCCESS}), content_type = "application/json")
        elif request.method == "GET":
            return HttpResponse("task get request")
        else:
            return HARDFAIL
    except (ValidationError):
        return SOFTFAIL
    except (ValueError, KeyError):
        return HARDFAIL

def newtask(request):
    try:
        if request.method == "POST" and "application/json" in request.META["CONTENT_TYPE"]:
            requestHeader = json.loads(bytes.decode(request.body))
            title = requestHeader["title"]
            description = requestHeader["description"]
            value = int(requestHeader["value"])
            summary = requestHeader["summary"]
            category = requestHeader["category"]
            cookieID = request.session["cookieID"]
            u = models.getUserByCookieID(cookieID)
            creator = u.username
            task = models.newTask(u, title, description, summary, value, category)
            return HttpResponse(json.dumps({"errcode": SUCCESS, "taskID": task.taskID}), content_type = "application/json")
        elif request.method == "GET":
            cookieID = request.session["cookieID"]
            u = models.getUserByCookieID(cookieID)
            template = loader.get_template("newtask.html")
            context = Context({"user": u.username})
            return HttpResponse(template.render(context))
        else:
            return HARDFAIL
    except (ValidationError):
        return SOFTFAIL
    except (ValueError, KeyError):
        return HARDFAIL

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
            return HARDFAIL
    except (ValidationError, IntegrityError):
        return SOFTFAIL
    except (ValueError, KeyError):
        return HARDFAIL

def mytasks(request):
    try:
        if request.method == "GET":
            u = models.getUserByCookieID(request.session["cookieID"])
            return HttpResponse("mytasks get request")
        else:
            return HARDFAIL
    except ObjectDoesNotExist:
        return SOFTFAIL
    except (ValueError, KeyError):
        return HARDFAIL
