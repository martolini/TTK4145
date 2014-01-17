from threading import Thread

def increase():
    global i
    for k in range(1000000):
        i += 1

i = 0
p = Thread(target=increase)
p.start()

for k in range(1000000):
	i -= 1

p.join()

print "i =", i