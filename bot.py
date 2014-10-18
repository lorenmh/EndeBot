from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from translate import ende, deen
from wiki import wiki
from yt import yt
import re

class EndeBot(irc.IRCClient):
    nickname = "EndeBot"

    #re_yt = re.compile("[A-Za-z0-9\_\-]{11}")

    #this shit even necessary?
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        self.join(self.factory.channel)

    def get_message(self, user, msg):
        '''yt_search = re_yt.search(msg)
        
        if yt_search:
            return yt(yt_search.group())'''

        if msg.startswith(".ende"):
            query = msg.split(".ende")[1].strip()
            msg = "%s: %s" % (user, ende(query))
            return msg

        elif msg.startswith(".en"):
            query = msg.split(".en")[1].strip()
            msg = "%s: %s" % (user, deen(query))
            return msg

        elif msg.startswith(".deen"):
            query = msg.split(".deen")[1].strip()
            msg = "%s: %s" % (user, deen(query))
            return msg

        elif msg.startswith(".de"):
            query = msg.split(".de")[1].strip()
            msg = "%s: %s" % (user, ende(query))
            return msg

        elif msg.startswith(".w en"):
            query = msg.split(".w en")[1].strip()
            msg = "%s: %s" % (user, wiki(query, english=True))
            return msg

        elif msg.startswith(".w"):
            query = msg.split(".w")[1].strip()
            msg = "%s: %s" % (user, wiki(query))
            return msg

        elif msg.startswith(".help"):
          msg = "%s: Commands = [.ende / .de], [.deen / .en], [.w (de wikipedia)], [.w en (en wikipedia)], Repo = https://github.com/lorenmh/EndeBot" % user
          return msg

        elif msg.startswith(self.nickname + ':'):
            msg = "%s: ich bin EndeBot.  Message '.help' for command-list" % user
            return msg

        else:
            return None

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        msg = self.get_message(user, msg)
        if msg != None:
            if channel == self.nickname:
                self.msg(user, msg)
            else:
                self.msg(channel, msg)

    def irc_NICK(self, prefix, params):
        old_nick = prefix.split('!')[0]
        new_nick = params[0]

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
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

if __name__ == "__main__":
    f = EndeBotFactory('##deutsch')
    reactor.connectTCP("irc.freenode.net", 6667, f)
    reactor.run()
