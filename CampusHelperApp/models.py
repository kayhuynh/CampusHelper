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
    verifyCode = models.CharField(max_length = 5, blank = True, null = True)
    cookieID = models.BigIntegerField(unique = True)

    def __str__(self):
        return self.username

    def markTaskCompleted(self, taskID):
        getTask(taskID).markCompleted(self)

    def acceptTask(self, taskID):
        getTask(taskID).markAccepted(self)

    def unreadMessages(self):
        return filter(lambda x: not x.read, self.messagesReceived.all())

    def readMessages(self):
        return filter(lambda x: x.read, self.messagesReceived.all())

    def postedTasks(self):
        return map(lambda x: x.taskID, self.tasksCreated.all())

    def acceptedTasks(self):
        return map(lambda x: x.taskID, self.tasksAccepted.all())

    def completedTasks(self):
        return map(lambda x: x.taskID, filter(lambda x: x.state == STATE_COMPLETED, self.tasksAccepted.all()))

    def score(self):
        scoredTasks = map(lambda x: x.value, \
            filter(lambda x: x.state == STATE_COMPLETED and x.value != None, \
                self.tasksAccepted.all()))
        if len(scoredTasks) == 0:
            return None
        else:
            return sum(scoredTasks) / (0.0 + len(scoredTasks))

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

    def checkCode(self, verifyCode):
        if verifyCode == self.verifyCode:
            self.verifyCode = None
            self.full_clean()
            self.save()
            return True
        else:
            return False

    def verified(self):
        return self.verifyCode == None

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
    value = models.PositiveSmallIntegerField(blank = True, null = True, default = None)
    category = models.TextField(max_length = None)

    def __str__(self):
        return self.title

    def unmarkAccepted(self, acceptor):
        if self.state == STATE_ACCEPTED and acceptor == self.acceptor:
            self.state = STATE_CREATED
            self.acceptor = None
            self.full_clean()
            self.save()
        else:
            raise ValidationError("state or acceptor not right")

    def markAccepted(self, acceptor):
        if self.state == STATE_CREATED and acceptor != self.creator:
            self.state = STATE_ACCEPTED
            self.acceptor = acceptor
            self.full_clean()
            self.save()
        else:
            raise ValidationError("state or acceptor not right")

    def markCompleted(self, creator):
        if self.state == STATE_ACCEPTED and creator == self.creator:
            self.state = STATE_COMPLETED
            self.full_clean()
            self.save()
        else:
            raise ValidationError("state or creator not right")

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

    def setValue(self, newValue, creator):
        if self.state == STATE_COMPLETED and self.value == None and newValue <= 5 and creator == self.creator:
            self.value = newValue
            self.full_clean()
            self.save()
        else:
            raise ValidationError("value or creator not right")

    def setCategory(self, newCategory):
        self.category = newCategory
        self.full_clean()
        self.save()

    def notify(self):
        self.notify = True
        self.full_clean()
        self.save()

class Message(models.Model):
    messageID = models.AutoField(primary_key = True)
    contents = models.TextField(max_length = None)
    task = models.ForeignKey(Task, related_name = "messages", on_delete = models.CASCADE)
    sender = models.ForeignKey(User, related_name = "messagesSent", on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, related_name = "messagesReceived", on_delete = models.CASCADE)
    timeSent = models.DateTimeField(auto_now_add = True)
    read = models.BooleanField(default = False)

    def __str__(self):
        return self.contents

    def markRead(self, receiver):
        if not self.read and receiver == self.receiver:
            self.read = True
            self.full_clean()
            self.save()
        else:
            raise ValidationError("readness or receiver not right")

def newUser(username, password, email, desc, verifyCode):
    cookieID = random.randint(-(2 ** 63), (2 ** 63) - 1)
    k = User(username = username, password = password, email = email, description = desc, cookieID = cookieID, verifyCode = verifyCode)
    k.full_clean()
    k.save()
    return k

def getUser(username):
    return User.objects.get(username__exact = username)

def getUserByCookieID(cookieID):
    return User.objects.get(cookieID__exact = cookieID)

def newTask(creator, title, desc, summary, category):
    k = Task(creator = creator, title = title, description = desc, summary = summary, category = category)
    k.full_clean()
    k.save()
    return k

def getTask(taskID):
    return Task.objects.get(taskID__exact = taskID)

def newMessage(sender, receiver, task, contents):
    k = Message(sender = sender, receiver = receiver, task = task, contents = contents)
    k.full_clean()
    k.save()
    return k

def getMessage(messageID):
    return Message.objects.get(messageID__exact = messageID)
