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
import string
import time

class Listen:
	def __init__(self, host=None, port=None):
		self.sock = None
		self.host = host
		self.port = port
		self.connected = False
		
	def set_host(self, host):
		self.host = host
		
	def set_port(self, port):
		self.port = port
		
	def connect_to_server(self):
		if not self.connected:
			try:
				self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.sock.connect((self.host, self.port))
				self.connected = True
				return True
			except:
				return False
		else:
			return True
		
	def send_msg(self, msg):
		if self.connect_to_server() == True:
			sent = self.sock.send(msg)
			if sent == 0:
				raise RuntimeError, "socket connection broken"
			
	def receive_msg(self):
		BUFSIZE = 128
		msg = ''
		
		while string.count(msg, "\n") == 0:
			chunk = self.sock.recv(BUFSIZE)
				
			if chunk == '':
				raise RuntimeError, "socket connection broken"
			msg = msg + chunk
		
		self.sock.close()
		self.connected = False
			
		return msg
		
	def update_stats(self):
		try:
			self.send_msg("state\ns\n")
			self.send_msg("state\ns\n")
			stats = self.receive_msg()

			while len(stats.split(" ")) > 7:
				stats = stats.replace("  ", " ")

			stats = stats.split(" ")
			self.sock.close()

			return stats
		except:
			return None

