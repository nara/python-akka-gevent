import gevent
from executive import Executive 
import gevent.monkey

gevent.monkey.patch_all()

executive = Executive()
executive.start()
executive.inbox.put({ 'type': 'work', 'payload': { 'plan' : "lets get it done" } })
gevent.joinall([executive]) 