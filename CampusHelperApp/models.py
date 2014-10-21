from django.db import models

STATE_CREATED = 1
STATE_ACCEPTED = 2
STATE_COMPLETED = 3

class User(models.Model):
   username = models.CharField(max_length = None, primary_key = True)
   password = models.CharField(max_length = None)
   email = models.EmailField(max_length = 254)
   description = models.CharField(max_length = None)
   # self.tasksCreated, self.tasksAccepted from Task ForeignKeys

   def __str__(self):
      return self.username

   def markTaskCompleted(self, taskID):
   	#

   def acceptTask(self, taskID):
   	#

   def postedTasks(self):
   	return self.tasksCreated

   def acceptedTasks(self):
   	return self.tasksAccepted

   def setEmail(self, newEmail):
   	self.email = newEmail

   def setPassword(self, newPass):
   	self.password = newPass

   def setDescription(self, newDesc):
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
   	self.state = STATE_ACCEPTED

   def markCompleted(self):
   	self.state = STATE_COMPLETED

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
