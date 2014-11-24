from django.test import TestCase
from django.test import Client
from CampusHelperApp.models import User, Task, Message, newUser, newTask, newMessage, STATE_CREATED, STATE_ACCEPTED, STATE_COMPLETED

import json

class UserTestCase(TestCase):
    def setUp(self):
        newUser('Nick', 'nickrulez', 'nick@nick.com', 'This is Nick', None)
        newUser('Kevin', 'kevinrulez', 'kevin@kevin.com', 'This is Kevin', None)
        self.nick = User.objects.get(username = 'Nick')
        kevin = User.objects.get(username = 'Kevin')

        newTask(self.nick, 'Mow the lawn', 'With a pair of scissors', "summ", 1)
        newTask(self.nick, 'Get armadillo poison', 'We have an infestation', "summ", 1)
        newTask(kevin, 'Deliver pet armadillo', "They're so cute!", "summ", 1)

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

    def test_checkCode(self):
        self.nick.verifyCode = 1
        self.assertTrue(self.nick.checkCode(1))
        self.assertFalse(self.nick.checkCode(1))


class TaskTestCase(TestCase):
    def setUp(self):
        self.nick = newUser('Nick', 'nickrulez', 'nick@nick.com', 'This is Nick', None)
        self.kevin = newUser('Kevin', 'kevinrulez', 'kevin@kevin.com', 'This is KEvin', None)

        self.mow = newTask(self.nick, 'Mow the lawn', 'With a pair of scissors', "summ", 1)
        self.poison = newTask(self.nick, 'Get armadillo poison', 'We have an infestation', "summ", 1)
        self.pet = newTask(self.kevin, 'Deliver pet armadillo', "They're so cute!", "summ", 1)

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
        poison.markCompleted(self.nick)
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

    def test_unmarkAccepted(self):
        self.mow.markAccepted(self.kevin)
        self.assertEqual(self.mow.state, STATE_ACCEPTED)
        self.mow.unmarkAccepted(self.kevin)
        self.assertEqual(self.mow.state, STATE_CREATED)

    def test_setSummary(self):
        self.mow.setSummary('With hedge trimmers')
        self.assertEqual(self.mow.summary, 'With hedge trimmers')
    
    def test_setValue(self):
        self.mow.markAccepted(self.kevin)
        self.mow.markCompleted(self.nick)
        self.mow.setValue(4, self.nick)
        self.assertEqual(self.mow.value, 4)

    def test_setCategory(self):
        self.pet.setCategory("Delivery")
        self.assertEqual(self.pet.category, "Delivery")

class MessageTestCase(TestCase):
    def setUp(self):
        self.nick = newUser('Nick', 'nickrulez', 'nick@nick.com', 'This is Nick', None)
        self.kevin = newUser('Kevin', 'kevinrulez', 'kevin@kevin.com', 'This is Kevin', None)
        self.poison = newTask(self.nick, 'Get armadillo poison', 'We have an infestation', "summ", 1)
        self.message = newMessage(self.kevin, self.nick, self.poison, "Don't do that, I like armadillos :(")

    def test_markRead(self):
        self.message.markRead(self.nick)
        self.assertTrue(self.message.read)
        

class FunctionalTestCase(TestCase):

    def setUp(self):
        self.nick = newUser('Nick', 'nickrulez', 'nick@nick.com', 'This is Nick', None)
        self.kevin = newUser('Kevin', 'kevinrulez', 'kevin@kevin.com', 'This is Kevin', None)
        self.water = newTask(self.nick, 'Water plants', 'With water', "summ", 1)
        self.message = newMessage(self.kevin, self.nick, self.water, "I'll do it")

    def test_login_get(self):
        c = Client()
        response = c.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Login' in response.content and 'Dedicated' not in response.content)

    def test_root_get(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Dedicated' in response.content)

    def test_login_post_correct(self):
        c = Client()
        nick = User.objects.get(username = 'Nick')
        response = c.post('/login', json.dumps({"username": nick.username, "password": nick.password, "cookieID": nick.cookieID}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"verified": 1, "errcode": 1}')

    def test_login_post_incorrect(self):
        c = Client()
        nick = User.objects.get(username = 'Nick')
        response = c.post('/login', json.dumps({"username": nick.username, "password": 'Nickdroolz', "cookieID": nick.cookieID}), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, '{"errcode": 2}')

    def test_alltasks(self):
        c = Client()
        nick = User.objects.get(username = 'Nick')
        c.post('/login', json.dumps({"username": nick.username, "password": nick.password}), content_type="application/json")
        response = c.get('/alltasks')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Water' in response.content)

    def test_new_task_post(self):
        c = Client()
        nick = User.objects.get(username = 'Nick')
        c.post('/login', json.dumps({"username": nick.username, "password": nick.password}), content_type="application/json")
        response = c.post('/newtask', json.dumps({"title": "Do my homework", "description": "I'm really stupid and can't on my own", "value": "1", "summary": "I'll pay anything!", "category": "Academic Tutoring"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('taskID' in response.content)

    def test_new_task_get(self):
        c = Client()
        nick = User.objects.get(username = 'Nick')
        c.post('/login', json.dumps({"username": nick.username, "password": nick.password}), content_type="application/json")
        response = c.post('/newtask', json.dumps({"title": "Do my homework", "description": "I'm really stupid and can't on my own", "value": "1", "summary": "I'll pay anything!", "category": "Academic Tutoring"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        self.assertTrue("cookieID" in c.session)
        c.get('/logout')
        self.assertTrue("cookieID" not in c.session)

    def test_mytasks(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        response = c.get('/mytasks')
        self.assertEqual(response.status_code, 200)

    def test_profile_get(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        response = c.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Nick' in response.content)

    def test_profile_post(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        response = c.post('/profile', json.dumps({"field": 1, "newdata": "ilovenick"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_newtask_get(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        response = c.get('/newtask')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Post a New Task" in response.content)

    def test_newuser_post(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        response = c.post('/newuser', json.dumps({"username": "Lorde", "password": "I am Lorde", "email": "Lorde@berkeley.edu", "description": "Lorde Lorde Lorde"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('{"errcode": 1}' in response.content)

    def test_newuser_get(self):
        c = Client()
        response = c.get('/newuser')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Sign Up" in response.content)

    def test_task_get(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        response = c.get('/task?q='+str(self.water.taskID))
        self.assertEqual(response.status_code, 200)
    
    def test_newmessage_post(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        response = c.post('/newmessage', json.dumps({"receiver": self.kevin.username, "task": self.water.taskID, "contents": 'k'}), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_mymessages_get(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        response = c.get('/mymessages')
        self.assertEqual(response.status_code, 200)
    
    def test_mymessages_post(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        response = c.post('/mymessages?q='+str(self.message.messageID))
        self.assertEqual(response.status_code, 200)

    def test_verifyemail_get(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        response = c.get('/verifyemail')
        self.assertEqual(response.status_code, 200)

    def test_verifyemail_post_softfail(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        response = c.post('/verifyemail', json.dumps({"verifcode": 1}), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_task_invalid_state(self):
        c = Client()
        c.post('/login', json.dumps({"username": self.nick.username, "password": self.nick.password}), content_type="application/json")
        response = c.post('/task?q='+str(self.water.taskID), json.dumps({"field": 3, "newdata": STATE_CREATED}), content_type="application/json")
        self.assertEqual(response.status_code, 403)
                          
