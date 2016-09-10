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

import os
import socket
import sys
import urllib

class FileDownload:

	def __init__(self, url = None, file=None, report_handler=None):
		self.url = url
		self.file = file
		self.report_handler = report_handler

	def download_file(self, url=None, file=None, report_handler=None):
		if url != None:
			self.url = url
			
		if file != None:
			self.file = file
			
		if report_handler != None:
			self.report_handler = None
			
		if self.url == None or self.file == None:
			raise Exception, "url and file are required arguments"


		old_socket_timeout = socket.getdefaulttimeout()
		socket.setdefaulttimeout(10)
		
		try:
			urllib.urlretrieve(url, file, report_handler)
			urllib.urlcleanup()
		except IOError, e:
			raise e
		
		file = None
		
		socket.setdefaulttimeout(old_socket_timeout)
		
	def destroy(self):
		self = None

