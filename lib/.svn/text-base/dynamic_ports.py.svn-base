# Copyright (C) 2009-2011 Jason Scheunemann <jason.scheunemann@yahoo.com>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import random
import pySocket
import sys

class DynamicPorts:
	def __randomize(self):
		return random.randrange(3000, 65535, 1)
	
	def __check_available(self, port):
		s = pySocket.pySocket("127.0.0.1")
		s.set_port(port)
		return s.is_available()
	
	def __get_available_port(self):
		port = self.__randomize()
		while self.__check_available(port) == False:
			port = self.__randomize()
		
		return port
		
	def get_ports(self):
		inbound_port = self.__get_available_port()
		outbound_port = self.__get_available_port()
		
		return inbound_port, outbound_port
		
if __name__ == '__main__':
	dyn = DynamicPorts()
	inbound_port, outbound_port = dyn.get_ports()
	print "in: %d out: %d" % (inbound_port, outbound_port)
