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

import pygtk
pygtk.require('2.0')
import gobject

import os
import os.path
import signal
import sys
import threading
import time

class Fork(gobject.GObject):
	__gproperties__ = {
		'command' : (gobject.TYPE_STRING,
			'command to fork',
			'command to fork when subclassing class Fork and launch function is called is called',
			'',
		 	gobject.PARAM_READWRITE),

		'args' : (gobject.TYPE_STRING,
			'arguments to command used during fork',
			'arguments to command used during fork, (commands are space seperated)',
			'',
		 	gobject.PARAM_READWRITE),
		 	     
		'pid' : (gobject.TYPE_INT,
			'resulting pid after fork',
			'The process id after fork is succesfully called',
			0,
			4194304,
			0,
		 	gobject.PARAM_READWRITE),
		 	     
	}
	
	__gsignals__ = {
		'pid-killed' : (gobject.SIGNAL_RUN_LAST,
			gobject.TYPE_NONE,
			()),
	}
	
	def __init__(self):
		gobject.GObject.__init__(self)
		self.set_property('command', '')
		self.set_property('args', '')
		self.set_property('pid', 0)
		self.worker_thread = ForkWorker(self)		
		
	def do_get_property(self, property):
		return getattr(self, property.name)
			
	def do_set_property(self, property, value):
		setattr(self, property.name, value)
			
	def launch(self):
		args = "%s %s" % (self.get_property('command'), self.get_property('args'))
		command_split = args.split(" ")
		pid = os.fork();
		if pid == -1: #fork error
			perror("fork")
			self.child_pid = None
		elif pid == 0: #execute in child
			stdout_file = sys.stdout.fileno()
			sys.stdout.close()
			os.close(stdout_file)
			stdin_file = sys.stdin.fileno()
			sys.stdin.close()
			os.close(stdin_file)
			stderr_file = sys.stderr.fileno()
			sys.stderr.close()
			os.close(stderr_file)
			os.execvp(command_split[0], command_split)
		else: #child's pid, main process execution
			self.set_property('pid', pid)
			
			if self.worker_thread:
				self.worker_thread.stop()
				self.worker_thread = None
			
			self.worker_thread = ForkWorker(self)
			self.worker_thread.start()

	def kill(self):
		if self.is_running() == True:
			try:
				os.kill(self.get_property('pid'), signal.SIGKILL)
				killedpid, stat = os.wait()
				self.set_property('pid', 0)
			except OSError:
				sys.stderr.write("Process %s does not exist\n" % self.pid)
	
	def is_running(self):
		if self.get_property('pid') != 0:
			return True
		else:
			return False
	
	def emit_closed(self):
		self.emit('pid-killed')

gobject.type_register(Fork)

class ForkWorker(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.closed = False
		self.loop = True
	
	def run(self):
		while self.loop:
			if self.parent.get_property('pid') != 0:
				try:
					ret = os.waitpid(self.parent.get_property('pid'), os.WNOHANG)
				except OSError:
					self.loop = False
			else:
				self.loop = False
			
			if not self.loop:
				self.parent.emit_closed()
				
			time.sleep(.1)
	
	def startup(self):
		self.loop = True
	
	def stop(self):
		self.loop = False

class ForkSOP(gobject.GObject):
	def __init__(self):
		gobject.GObject.__init__(self)
		self.f = Fork()
		self.exe_name = None
			
	def get_sp_sc_name(self):
		if self.exe_name == None:
			exe_names = ["sp-sc-auth", "sp-sc"]
		
			for name in exe_names:
				if any([os.path.exists(os.path.join(p, name)) for p in os.environ["PATH"].split(":")]):
					self.exe_name = name
					return self.exe_name
		
			if self.exe_name == None:
				raise Exception("ForkSOP", "Critical error, sp-sc-auth not found. Please install sp-auth!")
		else:
			return self.exe_name
		
	def fork_sop(self, sop_address, inbound_port, outbound_port):
		if self.f.get_property('command') == '':
			self.f.set_property('command', self.get_sp_sc_name())
		
		if sop_address == None or inbound_port == None or outbound_port == None:
			perror("invalid call to fork_sop")
		else:
			self.f.set_property('args', '%s %s %s' % (sop_address, inbound_port, outbound_port))
			self.f.launch()
			
	def kill_sop(self):
		self.f.kill()
	
	def is_running(self):
		return self.f.is_running()
		
gobject.type_register(ForkSOP)

class ForkExternalPlayer(gobject.GObject):
	__gsignals__ = {
		'killed' : (gobject.SIGNAL_RUN_LAST,
			gobject.TYPE_NONE,
			()),
	}
	
	def __init__(self):
		gobject.GObject.__init__(self)
		self.f = Fork()
		self.f.connect('pid-killed', self.killed_listener)
	
	def fork_player(self, command, url):
		self.f.set_property('command', command)
		self.f.set_property('args', url)
		self.f.launch()
	
	def kill(self):
		self.f.kill()
		
	def killed_listener(self, obj, data=None):
		self.emit('killed')
		
gobject.type_register(ForkExternalPlayer)
