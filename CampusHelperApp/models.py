from django.db import models
from django.core.exceptions import ValidationError

import random

STATE_CREATED = 1
STATE_ACCEPTED = 2
STATE_COMPLETED = 3

class User(models.Model):
    username = models.TextField(max_length = None, primary_key = True)
    password = models.TextField(max_length = None)
    email = models.EmailField(max_length = 254)
    description = models.TextField(max_length = None)
    cookieID = models.BigIntegerField(unique = True)
    # self.tasksCreated, self.tasksAccepted from Task ForeignKeys

    def __str__(self):
        return "user: " + self.username

    def markTaskCompleted(self, taskID):
        getTask(taskID).markCompleted()

    def acceptTask(self, taskID):
        getTask(taskID).markAccepted(self)

    def postedTasks(self):
        return map(lambda x: x.taskID, self.tasksCreated.all())

    def acceptedTasks(self):
        return map(lambda x: x.taskID, self.tasksAccepted.all())

    def setEmail(self, newEmail):
        self.email = newEmail
        self.save()

    def setPassword(self, newPass):
        self.password = newPass
        self.save()

    def setDescription(self, newDesc):
        self.description = newDesc
        self.save()

class Task(models.Model):
    taskID = models.AutoField(primary_key = True)               # don't specify this yourself (?)
    title = models.TextField(max_length = None)
    description = models.TextField(max_length = None)
    creator = models.ForeignKey(User, related_name = "tasksCreated", on_delete = models.CASCADE)
    acceptor = models.ForeignKey(User, related_name = "tasksAccepted", on_delete = models.PROTECT, null = True, default = None)
    timePosted = models.DateTimeField(auto_now_add = True)      # set the field to the time when it's created
    state = models.SmallIntegerField(default = STATE_CREATED)
    notify = models.BooleanField(default = False)       #   iteration 1?

    def __str__(self):
        return "task: " + self.title

    def markAccepted(self, acceptor):
        if self.state == STATE_CREATED:
            self.state = STATE_ACCEPTED
            self.acceptor = acceptor
            self.save()
        else:
            raise ValidationError("wrong state to be marked as accepted")

    def markCompleted(self):
        if self.state == STATE_ACCEPTED:
            self.state = STATE_COMPLETED
            self.save()
        else:
            raise ValidationError("wrong state to be marked as completed")

    def setTitle(self, newTitle):
        self.title = newTitle
        self.save()

    def setDescription(self, newDesc):
        self.description = newDesc
        self.save()

    def notify(self):
        self.notify = True
        self.save()

def newUser(username, password, email, desc):
    cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
    k = User(username = username, password = password, email = email, description = desc, cookieID = cookieID)
    k.save()
    return k

def getUser(username):
    return User.objects.get(username__exact = username)

def getUserByCookieID(cookieID):
    return User.objects.get(cookieID__exact = cookieID)

def newTask(creator, title, desc):
    k = Task(creator = creator, title = title, description = desc)
    k.save()
    return k

def getTask(taskID):
    return Task.objects.get(taskID__exact = taskID)
