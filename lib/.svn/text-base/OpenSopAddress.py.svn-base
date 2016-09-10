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

import sys
import os
import gtk
import locale
import gettext

cur_locale = locale.setlocale(locale.LC_ALL, "")

gtk.glade.bindtextdomain("sopcast-player")
gtk.glade.textdomain("sopcast-player")

gettext.bindtextdomain("sopcast-player")
gettext.textdomain("sopcast-player")

lang = gettext.translation("sopcast-player", languages=[cur_locale], fallback=True)
lang.install('sopcast-player')

class OpenSopAddress(object):
	def __init__(self, parent):
		self.window = None
		self.parent = parent
		
	def main(self):
		gladefile = "%s/%s" % (os.path.realpath(os.path.dirname(sys.argv[0])), "../ui/OpenSopAddress.glade")
			
		self.glade_window = gtk.glade.XML(gladefile, "window")
		self.window = self.glade_window.get_widget("window")
		self.window.set_modal(True)
		self.window.set_transient_for(self.parent.window)
		self.window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
		
		dic = { "on_window_destroy" : gtk.main_quit,
			"on_cancel_clicked" : self.on_cancel_clicked,
			"on_done_clicked" : self.on_done_clicked }
			
		self.glade_window.signal_autoconnect(dic)
		
		gtk.main()
		
	def on_cancel_clicked(self, src, data=None):
		self.window.destroy()
		
	def on_done_clicked(self, src, data=None):
		if self.sop_address.get_text()[:len("sop://".lower())] != "sop://".lower():
			self.sop_address.get_text()
		else:		
			self.window.destroy()
		
	def __getattribute__(self, key):
		value = None
		try:
			value = object.__getattribute__(self, key)
		except AttributeError:
			glade_window = object.__getattribute__(self, 'glade_window')
			value = glade_window.get_widget(key)	

		return value
