from django.db import models

STATE_CREATED = 1			# in this file?
STATE_ACCEPTED = 2
STATE_COMPLETED = 3

class User(models.Model):
   username = models.CharField(max_length = None, primary_key = True)
   password = models.CharField(max_length = None)
   email = models.EmailField(max_length = 254)
   description = models.CharField(max_length = None)
   # users.tasksCreated, users.tasksAccepted from Task ForeignKeys

   def __str__(self):
      return self.username

   def createTask(self, title, desc):
   	#

   def markTaskCompleted(self, taskID):
   	#

   def acceptTask(self, taskID):
   	#

   def postedTasks(self):
   	#

   def acceptedTasks(self):
   	#

   def setEmail(self, newEmail):
   	#

   def setPassword(self, newPass):
   	#

   def setDescription(self, newDesc):
   	#

def getUser(username):
	#

class Task(models.Model):
	id = models.AutoField(primary_key = True)				# don't specify this yourself (?)
   title = models.CharField(max_length = None)
   description = models.CharField(max_length = None)
   creator = models.ForeignKey(User, related_name = "tasksCreated", on_delete = models.CASCADE)
   acceptor = models.ForeignKey(User, related_name = "tasksAccepted", on_delete = models.PROTECT)
   timePosted = models.DateTimeField(auto_now_add = True)		# set the field to the time when it's created
   state = models.SmallIntegerField(default = STATE_CREATED)
   notify = models.BooleanField(default = False)		# 	iteration 1?

   def __str__(self):
      return self.title

   def markAccepted(self):
   	#

   def markCompleted(self):
   	#

   def setTitle(self, newTitle):
   	#

   def setDescription(self, newDesc):
   	#

   def notify(self):
   	#

def getTask(taskID):
	#
