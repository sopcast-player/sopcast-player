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

import socket

class pySocket:
	def __init__(self, host=None, port=None):
		self.host = host
		self.port = port
		
	def set_host(self, host):
		self.host = host
		
	def set_port(self, port):
		self.port = port
		
	def is_available(self, host=None, port=None):
		if host != None:
			self.host = host
			
		if port != None:
			self.port = port
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		return not self.sock.connect_ex((self.host, self.port)) == 0
