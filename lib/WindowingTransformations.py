# Copyright (C) 2011 Jason Scheunemann <jason.scheunemann@yahoo.com>.
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

class WindowingTransformations:
	def __init__(self, fs_widget, parent):
		self.parent = parent
		self.fs_widget = fs_widget
		self.hidden_widgets = []
		self.is_fw = False
		self.is_fs = False
	
	def fullscreen(self, fs=True):
		if not self.parent.config_manager.uses_new_bindings():
			if self.is_fw == False:
				self.hidden_widgets = []
				
		self.hide_stuff(self.fs_widget)
		
		if fs == True:
			self.fs_widget.get_toplevel().fullscreen()
			self.is_fs = True
		else:
			self.is_fw = True
		
		self.is_fs = True
		
	def hide_stuff(self, vis_widget):
		parent = vis_widget.get_parent()
		
		if parent is not parent.get_toplevel():
			for w in parent.get_children():
				if w is not vis_widget and w.get_property("visible"):
					self.hidden_widgets.append(w)
					w.hide()
			self.hide_stuff(parent)
		else:
			return
	
	def unfullscreen(self, fs=True):
		if self.is_fs:
			self.fs_widget.get_toplevel().unfullscreen()
			self.is_fs = False
		
		if not fs:
			self.is_fw = False
		
		if (fs and not self.is_fw) or not fs:	
			for w in self.hidden_widgets:
				w.show()
				self.hidden_widgets = []
			
	def fullwindow(self):
		w_width = self.fs_widget.get_toplevel().get_allocation()[2]
		w_height = self.fs_widget.get_toplevel().get_allocation()[3]
		self.prev_width = w_width - self.fs_widget.get_allocation()[2]
		self.prev_height = w_height - self.fs_widget.get_allocation()[3]
		self.fs_widget.get_toplevel().resize(self.fs_widget.get_allocation()[2], self.fs_widget.get_allocation()[3])
		self.fullscreen(fs=False)
		self.is_fw = True
		
	def unfullwindow(self):
		width = self.fs_widget.get_allocation()[2] + self.prev_width
		height = self.fs_widget.get_allocation()[3] + self.prev_height
		self.fs_widget.get_toplevel().resize(width, height)
		self.unfullscreen(fs=False)
		self.is_fw = False
		
