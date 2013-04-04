#!/usr/bin/env python2.7

from twisted.internet import reactor, protocol
from twisted.words.protocols import irc

class IRCLogger(irc.IRCClient):
    logfile = file('/tmp/hanirc.txt', 'a+')

    nick = 'davey_jones_logger'

    def signedOn(self):
        self.join('#dx')

    def privmsg(self, user, channel, message):
        print "Got msg %s " % message
        self.logfile.write(" %s said %s \n" % ( user.split('!')[0], message ))
        self.logfile.flush()

def main():
    f = protocol.ReconnectingClientFactory()
    f.protocol = IRCLogger
    reactor.connectTCP('irc.hanirc.org', 6667, f)
    reactor.run()

if __name__ == '__main__':
    main()
