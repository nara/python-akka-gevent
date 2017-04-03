import gevent
from gevent.queue import Queue
from gevent import Greenlet
from actor import Actor
from worker import Worker
import traceback

class Manager(Actor):
    
    def __init__(self, boss, index):
        self.index = index
        self.boss = boss
        self.tasks = []

        self.workers = [Worker(self, i) for i in xrange(4)]
        for worker in self.workers:
            worker.start()

        Actor.__init__(self)

    def receive(self, message):
        if message['type'] == "worker.done":
            self.worker_done(message)
        else:
            self.process(message)
            
        gevent.sleep(0)

    def process(self, message):
        
        try:
            self.make_tasks_for_workers(message)
                
            for idx, worker in enumerate(self.workers):
                self.allocate_task(idx)
            
        except Exception as ex:
            print ex
            traceback.print_exc()
            self.boss.inbox.put({ 'type' : "manager.done", 'index': self.index, 'error' : ex.message, 'payload' : message['payload'] })

        return

    def worker_done(self, message):
        if message['error'] != "":
            print "error, re-adding"
            payload = message['payload']
            self.tasks.append(message['payload'])

        idx = message['index']
        assigned = self.allocate_task(idx)
        if not assigned:
            self.boss.inbox.put({ 'type' : "manager.done", 'index': self.index, 'error' : "", 'payload' : message['payload'] })
        
    def make_tasks_for_workers(self, message):
        #code to populate tasks for workers into self.tasks
        self.tasks = [{ 'payload' : { 'workertask' : i } } for i in xrange(1, 20)]
        return 

    def allocate_task(self, workerIndex):
        worker = self.workers[workerIndex]
        if(len(self.tasks) > 0):
            worker.inbox.put({ 'payload': self.tasks.pop(), 'type': "work" })
            return True

        return False
    