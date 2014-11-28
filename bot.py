from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from translate import ende, deen
from wiki import wiki
from yt import yt
import re, time

def time_str():
  return time.strftime("[%H:%M:%S|%d/%m/%y]") 

def log(text):
  print time_str(), text

class EndeBot(irc.IRCClient):
    #re_yt = re.compile("[A-Za-z0-9\_\-]{11}")
    nickname = "EndeBot"

    #this shit even necessary?
    def connectionMade(self):
        log('CONNECTED')
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        log('CONNECTION LOST')
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        log('SIGNED ON')
        self.join(self.factory.channel)
   
    def joined(self, channel):
        log('JOINED %s' % channel)

    def left(self, channel):
        log('LEFT %s' % channel)

    def kickedFrom(self, channel):
        log('KICKED FROM %s BY %s:%s' % (channel, kicker, message))

    def get_message(self, user, msg):
        if msg.startswith(".ende"):
            log("%s:%s" % (user,msg))
            query = msg.split(".ende")[1].strip()
            if len(query) > 0:
                msg = "%s: %s" % (user, ende(query))
                return msg
            return None

        elif msg.startswith(".en"):
            log("%s:%s" % (user,msg))
            query = msg.split(".en")[1].strip()
            if len(query) > 0:
                msg = "%s: %s" % (user, deen(query))
                return msg
            return None

        elif msg.startswith(".deen"):
            log("%s:%s" % (user,msg))
            query = msg.split(".deen")[1].strip()
            if len(query) > 0:
                msg = "%s: %s" % (user, deen(query))
                return msg
            return None

        elif msg.startswith(".de"):
            log("%s:%s" % (user,msg))
            query = msg.split(".de")[1].strip()
            if len(query) > 0:
                msg = "%s: %s" % (user, ende(query))
                return msg
            return None

        elif msg.startswith(".w en"):
            log("%s:%s" % (user,msg))
            query = msg.split(".w en")[1].strip()
            if len(query) > 0:
                msg = "%s: %s" % (user, wiki(query, english=True))
                return msg
            return None

        elif msg.startswith(".w"):
            log("%s:%s" % (user,msg))
            query = msg.split(".w")[1].strip()
            if len(query) > 0:
                msg = "%s: %s" % (user, wiki(query))
                return msg
            return None

        elif msg.startswith(".help"):
            log("%s:%s" % (user,msg))
            msg = "%s: Commands = [.ende / .de], [.deen / .en], [.w (de wikipedia)], [.w en (en wikipedia)], Repo = https://github.com/lorenmh/EndeBot" % user
            return msg

        elif msg.startswith(self.nickname + ':'):
            log("%s:%s" % (user,msg))
            msg = "%s: ich bin EndeBot.  Message '.help' for command-list" % user
            return msg
        
        re_yt = re.compile("(^|\s+|\/|=)(?P<id>[A-Za-z0-9\_\-]{11})($|\s+|\/\?\&)")
        yt_search = re_yt.search(msg)
        if yt_search:
             info = yt(yt_search.group('id'))
             if info:
                  log("%s:%s" % (user, msg))
                  return info
        
        return None

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        msg = self.get_message(user, msg)

        if msg != None:
            if channel == self.nickname:
                log("BOT_PRIVATE:%s" % msg)
                self.msg(user, msg)
            else:
                log("BOT:%s" % msg)
                self.msg(channel, msg)

    def alterCollidedNick(self, nickname):
        return nickname + "_"

class EndeBotFactory(protocol.ClientFactory):
    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        p = EndeBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        log("CLIENT CONNECTION LOST: %s" % reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        log("CLIENT CONNECTION FAILED: %s" % reason)
        reactor.stop()

if __name__ == "__main__":
    f = EndeBotFactory('#deutsch')
    #f = EndeBotFactory('#mytest')
    reactor.connectTCP("irc.freenode.net", 6667, f)
    reactor.run()
