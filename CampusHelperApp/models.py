from django.db import models
from django.core.exceptions import ValidationError

import random

STATE_CREATED = 1
STATE_ACCEPTED = 2
STATE_COMPLETED = 3

class User(models.Model):
   username = models.CharField(max_length = 100, primary_key = True)
   password = models.CharField(max_length = 100)
   email = models.EmailField(max_length = 254)
   description = models.CharField(max_length = 500)
   cookieID = models.BigIntegerField(default = random.randint(-(2 ** 63), (2 ** 63) - 1))
   # self.tasksCreated, self.tasksAccepted from Task ForeignKeys

   def __str__(self):
      return "user: " + self.username

   def markTaskCompleted(self, taskID):
   	getTask(taskID).markCompleted()

   def acceptTask(self, taskID):
   	getTask(taskID).markAccepted(self)

   def postedTasks(self):
   	return map(self.tasksCreated, lambda x: x.id)

   def acceptedTasks(self):
   	return map(self.tasksAccepted, lambda x: x.id)

   def setEmail(self, newEmail):
   	self.email = newEmail

   def setPassword(self, newPass):
   	self.password = newPass

   def setDescription(self, newDesc):
   	self.description = newDesc

class Task(models.Model):
   id = models.AutoField(primary_key = True)				# don't specify this yourself (?)
   title = models.CharField(max_length = 100)
   description = models.CharField(max_length = 500)
   creator = models.ForeignKey(User, related_name = "tasksCreated", on_delete = models.CASCADE)
   acceptor = models.ForeignKey(User, related_name = "tasksAccepted", on_delete = models.PROTECT, null = True, default = None)
   timePosted = models.DateTimeField(auto_now_add = True)		# set the field to the time when it's created
   state = models.SmallIntegerField(default = STATE_CREATED)
   notify = models.BooleanField(default = False)		# 	iteration 1?

   def __str__(self):
      return "task: " + self.title

   def markAccepted(self, acceptor):
   	if self.state == STATE_CREATED:
   		self.state = STATE_ACCEPTED
   		self.acceptor = acceptor
   	else:
   		raise ValidationError("wrong state to be marked as accepted")

   def markCompleted(self):
   	if self.state == STATE_ACCEPTED:
   		self.state = STATE_COMPLETED
   	else:
   		raise ValidationError("wrong state to be marked as completed")

   def setTitle(self, newTitle):
   	self.title = newTitle

   def setDescription(self, newDesc):
   	self.description = newDesc

   def notify(self):
   	self.notify = True

def newUser(username, password, email, desc):
   k = User(username = username, password = password, email = email, description = desc)
   k.save()
   return k

def getUser(username):
	return User.objects.get(username__exact = username)

def newTask(creator, title, desc):
	k = Task(creator = creator, title = title, description = desc)
	k.save()
	return k

def getTask(taskID):
	return Task.objects.get(id__exact = taskID)