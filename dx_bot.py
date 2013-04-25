#!/usr/bin/env python2.7

from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
import infix_interpreter


class IRCLogger(irc.IRCClient):
    #logfile = file('/tmp/hanirc.txt', 'a+')

    nickname = 'dice_bot'

    def signedOn(self):
        self.join('#13dx')
        
    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        print channel

    def privmsg(self, user, channel, message):
        message
        print "[got msg]%s" % message
        
        if message.startswith(":r"):            
            expr = message[2:]
            exp_res = infix_interpreter.solve_expr(expr)
            print "exp_res : " + exp_res
            self.msg(channel, exp_res)

        #self.logfile.write(" %s said %s \n" % ( user.split('!')[0], message ))
        #self.logfile.flush()

def main():
    f = protocol.ReconnectingClientFactory()
    f.protocol = IRCLogger
    reactor.connectTCP('apink.hanirc.org', 6667, f)
    reactor.run()

if __name__ == '__main__':
    main()
