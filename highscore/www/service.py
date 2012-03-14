# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from twisted.application import strports, service
from twisted.web import server, static
from highscore.www import resource

class WWWService(service.MultiService):

    def __init__(self, highscore, config):
        service.MultiService.__init__(self)
        self.setName('highscore.www')
        self.highscore = highscore
        self.config = config

        self.port = config.get('port', 8080)
        self.port_service = None
        self.site = None
        self.site_public_html = None

        root = static.Data('placeholder', 'text/plain')
        root.putChild('', resource.HighscoresResource(self.highscore))
        root.putChild('user', resource.UsersPointsResource(self.highscore))

        self.site = server.Site(root)

        port = "tcp:%d" % self.port if type(self.port) == int else self.port
        self.port_service = strports.service(port, self.site)
        self.port_service.setServiceParent(self)