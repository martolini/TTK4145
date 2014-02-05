from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import json

class ElevatorServer(Protocol):

    def __init__(self, elevators):
        self.elevators = elevators
        self.state = "ELEVATOR"

    def connectionMade(self):
        print 'connection made by: ', self
        self.elevators.append(self)

    def connectionLost(self, reason):
        self.elevators.remove(self)
        print 'connection lost from: ', self

    def dataReceived(self, line):
        for elevator in self.elevators:
            if self != elevator:
                elevator.transport.write(line)


class ElevatorFactory(Factory):

    def __init__(self):
        self.elevators = [] # maps user names to Chat instances

    def buildProtocol(self, addr):
        return ElevatorServer(self.elevators)


reactor.listenTCP(8123, ElevatorFactory())
reactor.run()