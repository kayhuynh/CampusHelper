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
    # self.tasksCreated.all(), self.tasksAccepted.all() from Task ForeignKeys

    def __str__(self):
        return self.username

    def markTaskCompleted(self, taskID):
        getTask(taskID).markCompleted()

    def acceptTask(self, taskID):
        getTask(taskID).markAccepted(self)

    def postedTasks(self):
        return map(lambda x: x.taskID, self.tasksCreated.all())

    def acceptedTasks(self):
        return map(lambda x: x.taskID, self.tasksAccepted.all())

    def completedTasks(self):
        return map(lambda x: x.taskID, filter(lambda x: x.state == STATE_COMPLETED, self.tasksAccepted.all()))

    def score(self):
        return sum(map(lambda x: x.value, filter(lambda x: x.state == STATE_COMPLETED, self.tasksAccepted.all())))

    def setEmail(self, newEmail):
        self.email = newEmail
        self.full_clean()
        self.save()

    def setPassword(self, newPass):
        self.password = newPass
        self.full_clean()
        self.save()

    def setDescription(self, newDesc):
        self.description = newDesc
        self.full_clean()
        self.save()

class Task(models.Model):
    taskID = models.AutoField(primary_key = True)
    title = models.TextField(max_length = None)
    description = models.TextField(max_length = None)
    creator = models.ForeignKey(User, related_name = "tasksCreated", on_delete = models.CASCADE)
    acceptor = models.ForeignKey(User, related_name = "tasksAccepted", on_delete = models.PROTECT, blank = True, null = True, default = None)
    timePosted = models.DateTimeField(auto_now_add = True)
    state = models.SmallIntegerField(default = STATE_CREATED)
    notify = models.BooleanField(default = False)
    summary = models.TextField(max_length = None)
    value = models.PositiveSmallIntegerField()
    category = models.TextField(max_length = None)

    def __str__(self):
        return self.title

    def markAccepted(self, acceptor):
        if self.state == STATE_CREATED:
            self.state = STATE_ACCEPTED
            self.acceptor = acceptor
            self.full_clean()
            self.save()
        else:
            raise ValidationError("wrong state to be marked as accepted")

    def markCompleted(self):
        if self.state == STATE_ACCEPTED:
            self.state = STATE_COMPLETED
            self.full_clean()
            self.save()
        else:
            raise ValidationError("wrong state to be marked as completed")

    def setTitle(self, newTitle):
        self.title = newTitle
        self.full_clean()
        self.save()

    def setSummary(self, newSummary):
        self.summary = newSummary;
        sef.full_clean()
        self.save()

    def setDescription(self, newDesc):
        self.description = newDesc
        self.full_clean()
        self.save()

    def setSummary(self, newSummary):
        self.summary = newSummary
        self.full_clean()
        self.save()

    def setValue(self, newValue):
        self.value = newValue
        self.full_clean()
        self.save()

    def setCategory(self, newCategory):
        self.category = newCategory
        self.full_clean()
        self.save()

    def notify(self):
        self.notify = True
        self.full_clean()
        self.save()

def newUser(username, password, email, desc):
    cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
    k = User(username = username, password = password, email = email, description = desc, cookieID = cookieID)
    k.full_clean()
    k.save()
    return k

def getUser(username):
    return User.objects.get(username__exact = username)

def getUserByCookieID(cookieID):
    return User.objects.get(cookieID__exact = cookieID)

def newTask(creator, title, desc, summary, value, category):
    k = Task(creator = creator, title = title, description = desc, summary = summary, value = value, category = category)
    k.full_clean()
    k.save()
    return k

def getTask(taskID):
    return Task.objects.get(taskID__exact = taskID)
