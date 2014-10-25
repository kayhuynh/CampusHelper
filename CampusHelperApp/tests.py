from django.test import TestCase
from CampusHelperApp.models import User, Task, newUser, newTask, STATE_CREATED, STATE_ACCEPTED, STATE_COMPLETED
# Create your tests here.

class UserTestCase(TestCase):
    def setUp(self):
        newUser('Nick', 'nickrulez', 'nick@nick.com', 'This is Nick')
        newUser('Kevin', 'kevinrulez', 'kevin@kevin.com', 'This is KEvin')
        nick = User.objects.get(username = 'Nick')
        kevin = User.objects.get(username = 'Kevin')
        
        newTask(nick, 'Mow the lawn', 'With a pair of scissors')
        newTask(nick, 'Get armadillo poison', 'We have an infestation')
        newTask(kevin, 'Deliver pet armadillo', "They're so cute!")

    def test_has_password(self):
        """The user is created with a password"""
        nick = User.objects.get(username = 'Nick')
        self.assertEqual(nick.password, 'nickrulez')

    def test_mark_completed(self):
        nick = User.objects.get(username = 'Nick')
        kevin = User.objects.get(username = 'Kevin')
        mow = Task.objects.get(title = 'Mow the lawn')
        mow.markAccepted(kevin)
        nick.markTaskCompleted(mow.taskID)
        self.assertEqual(mow.state, STATE_ACCEPTED)

    def test_accept_task(self):
        nick = User.objects.get(username = 'Nick')
        deliver = Task.objects.get(title = 'Deliver pet armadillo')
        nick.acceptTask(deliver.taskID)
        deliver = Task.objects.get(title = 'Deliver pet armadillo')
        self.assertEqual(deliver.state, STATE_ACCEPTED)
        self.assertEqual(deliver.acceptor, nick)

    def test_posted_tasks(self):
        nick = User.objects.get(username = 'Nick')
        tasks = nick.postedTasks()
        self.assertEqual(len(tasks), 2)

    def test_accepted_tasks(self):
        kevin = User.objects.get(username = 'Kevin')
        mow = Task.objects.get(title = 'Mow the lawn')
        kevin.acceptTask(mow.taskID)
        tasks = kevin.acceptedTasks()
        self.assertEqual(len(tasks), 1)

    def test_set_email(self):
        kevin = User.objects.get(username = 'Kevin')
        kevin.setEmail('ta@cs169.gov')
        self.assertEqual(kevin.email, 'ta@cs169.gov')
    
    def test_set_password(self):
        kevin = User.objects.get(username = 'Kevin')
        kevin.setPassword('ta4lyfe')
        self.assertEqual(kevin.password, 'ta4lyfe')
    
    def test_set_description(self):
        kevin = User.objects.get(username = 'Kevin')
        kevin.setDescription('Best ta evar')
        self.assertEqual(kevin.description, 'Best ta evar')
    

class TaskTestCase(TestCase):
    def setUp(self):
        newUser('Nick', 'nickrulez', 'nick@nick.com', 'This is Nick')
        newUser('Kevin', 'kevinrulez', 'kevin@kevin.com', 'This is KEvin')
        nick = User.objects.get(username = 'Nick')
        kevin = User.objects.get(username = 'Kevin')
        
        newTask(nick, 'Mow the lawn', 'With a pair of scissors')
        newTask(nick, 'Get armadillo poison', 'We have an infestation')
        newTask(kevin, 'Deliver pet armadillo', "They're so cute!")

    def test_markAccepted(self):
        """Task should mark itself accepted"""
        lawn = Task.objects.get(title = 'Mow the lawn')
        kevin = User.objects.get(username = 'Kevin')
        lawn.markAccepted(kevin)
        self.assertEqual(lawn.state, STATE_ACCEPTED)
        self.assertEqual(lawn.acceptor, kevin)

    def test_markCompleted(self):
        poison = Task.objects.get(title = 'Get armadillo poison')
        kevin = User.objects.get(username = 'Kevin')
        poison.markAccepted(kevin)
        poison.markCompleted()
        self.assertEqual(poison.state, STATE_COMPLETED)
    
    def test_setTitle(self):
        lawn = Task.objects.get(title = 'Mow the lawn')
        lawn.setTitle('Cut my hair')
        self.assertEqual(lawn.title, 'Cut my hair')
    
    def test_setDescription(self):
        poison = Task.objects.get(title = 'Get armadillo poison')
        poison.setDescription('Well, they are kind of cute...')
        self.assertEqual(poison.description, 'Well, they are kind of cute...')

    def test_notify(self):
        deliver = Task.objects.get(title = "Deliver pet armadillo")
        deliver.notify()
        self.assertEqual(deliver.notify, True)
    
# Create your tests here.
