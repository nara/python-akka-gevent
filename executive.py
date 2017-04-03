import gevent
import gevent.monkey
from actor import Actor
from manager import Manager
import re
import traceback

class Executive(Actor):
    
    def __init__(self):
        self.managers = [Manager(self, i) for i in xrange(5)]
        self.tasks = []
        self.no_more_pages = False

        for manager in self.managers:
            manager.start()

        Actor.__init__(self)

    def receive(self, message):
        if message['type'] == "manager.done":
            self.manager_done(message)
        else:
            self.process(message)
        gevent.sleep(0)

    def process(self, message):
        
        self.fetch_tasks()
        
        for idx, manager in enumerate(self.managers):
            self.allocate_task(idx)
        return

    def manager_done(self, message):
        
        if message['error'] != "":
            print "error, re-adding"
            payload = message['payload']
            self.tasks.append(message['payload'])
            
        idx = message['index']
        self.allocate_task(idx)
    
    def allocate_task(self, manager_index):
        manager = self.managers[manager_index]
        if(len(self.tasks) > 0):
            manager.inbox.put({ 'payload': self.tasks.pop(), 'type': "work" })
        else:
            self.fetch_tasks()
            if len(self.tasks) > 0:
                manager.inbox.put({ 'payload': self.tasks.pop(), 'type': "work" })
    
    def fetch_tasks(self):
        #code to populate tasks for managers self.tasks 
        self.tasks = [{ 'payload' : { 'managertask' : i } } for i in xrange(1, 20)]
        return
        

