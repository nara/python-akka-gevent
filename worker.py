import gevent
import gevent.monkey
from gevent.queue import Queue
from gevent import Greenlet
from actor import Actor
import traceback

class Worker(Actor):
    
    def __init__(self, boss, index):
        self.boss = boss
        self.index = index
        Actor.__init__(self)

    def receive(self, message):
        
        try:
            print 'worker doing the work... boss %d worker %d' %(self.boss.index, self.index)
            self.boss.inbox.put({ 'type' : "worker.done", 'index': self.index, 'error' : "", 'payload' : message['payload'] })
            
        except Exception as ex:
            print ex
            traceback.print_exc()
            self.boss.inbox.put({ 'type' : "worker.done", 'index': self.index, 'error' : ex.message, 'payload' : message['payload'] })
        
        gevent.sleep(0)