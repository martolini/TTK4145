from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
from sys import stdout
import json
from random import randint

host, port = '78.91.30.144', 8123

class Elevator(Protocol):
    def dataReceived(self, data):
        if data.strip() == 'givenumber':
            self.transport.write(str(randint(1,10)))
    	print data,

class EchoClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return Elevator()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason


reactor.connectTCP(host, port, EchoClientFactory())
reactor.run()