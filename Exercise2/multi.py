from threading import Thread, Lock
lock = Lock()

def increase():
    global i
    global lock
    with lock:
    	for k in range(1000000):
        	i += 1


i = 0
p = Thread(target=increase)
p.start()

with lock:
	for k in range(1000001):
		i -= 1

p.join()

print "i =", i