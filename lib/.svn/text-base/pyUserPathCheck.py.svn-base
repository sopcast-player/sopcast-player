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

class UserPathCheck:
	def __init__(self, file_name):
		self.file_name = file_name
	
	def __get_user_path_array(self):
		return os.environ['PATH'].split(':')
	
	def file_exists(self):
		file_exists = False
		for path in self.__get_user_path_array():
			if os.path.isfile(os.path.join(path, self.file_name)):
				file_exists = True
				break
		return file_exists
			
