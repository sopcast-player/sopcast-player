#! /usr/bin/python
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

"""VLC Widget classes.

This module provides two helper classes, to ease the embedding of a
VLC component inside a pygtk application.

VLCWidget is a simple VLC widget.

DecoratedVLCWidget provides simple player controls.

$Id$
"""

import gtk
import sys
import vlc

from WindowingTransformations import WindowingTransformations

from gettext import gettext as _

class VLCWidget(gtk.DrawingArea):
	"""Simple VLC widget.

	Its player can be controlled through the 'player' attribute, which
	is a vlc.MediaPlayer() instance.
	"""
	def __init__(self, container, parent):
		gtk.DrawingArea.__init__(self)
		self.parent_cls = parent
		self.container = container
		
		instance=vlc.Instance()
		self.player=instance.media_player_new()
		
		self.vlc_event_manager = self.player.event_manager()
		self.vlc_event_manager.event_attach(vlc.EventType.MediaPlayerPositionChanged,self.pos_callback, self.player)
		
		def handle_embed(*args):
			if sys.platform == 'win32':
				self.player.set_hwnd(self.window.handle)
			else:
				self.player.set_xwindow(self.window.xid)
			return True
			
		self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
		self.connect("button_press_event", self.on_mouse_button_clicked)				
			
		self.connect("map", handle_embed)
		
		self.wt = WindowingTransformations(self.container, self.parent_cls)

		self.container.get_toplevel().add_events(gtk.gdk.KEY_PRESS_MASK)
		self.container.get_toplevel().connect("key-press-event", self.on_key_press)
		
		self.set_size_request(320, 200)		
		self.modify_bg(gtk.STATE_NORMAL, self.get_colormap().alloc_color("black"))		
		self.container.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
		self.is_fs = False
		self.is_fw = False
	
	def pos_callback(self, event, player):
		if player.get_time() / 1000 / 3600 / 24 > 0:
			print "%s day(s) %s:%s:%s/%s:%s:%s" % (player.get_time() / 1000 / 3600 / 24,
				self.format_time_part(player.get_time() / 1000 / 3600 % 24, True),
				self.format_time_part(player.get_time() / 1000 / 60 % 60),
				self.format_time_part(player.get_time() / 1000 % 60),
				self.format_time_part(player.get_length() / 1000 / 3600, True),
				self.format_time_part(player.get_length() / 1000 / 60 % 60),
				self.format_time_part(player.get_length() / 1000 % 60))
		else:
			print "%s:%s:%s/%s:%s:%s" % (self.format_time_part(player.get_time() / 1000 / 3600, True),
				self.format_time_part(player.get_time() / 1000 / 60 % 60),
				self.format_time_part(player.get_time() / 1000 % 60),
				self.format_time_part(player.get_length() / 1000 / 3600, True),
				self.format_time_part(player.get_length() / 1000 / 60 % 60),
				self.format_time_part(player.get_length() / 1000 % 60))
        	#print('%s to %.2f%% (%.2f%%)' % (event.type, event.u.new_position * 100, player.get_position() * 100))

	def format_time_part(self, part, hour=False):
		if hour == False:
			if part < 10:
				return "0%s" % (part)
			else:
				return part
		else:
			if part < 1:
				return "0"
			else:
				return part
		
		

	def on_key_press(self, widget, event, data=None):
		if event.keyval == gtk.keysyms.Escape:
			if self.is_fs:
				self.toggle_fullscreen()
		elif gtk.gdk.keyval_name(event.keyval) in ["f", "F"]:
			if self.is_playing():
				self.toggle_fullscreen()
		elif gtk.gdk.keyval_name(event.keyval) in ["h", "H"]:
			if not self.is_fs:
				self.toggle_fullwindow()
		return False
		
	def on_mouse_button_clicked(self, widget, event):
		if event.type == gtk.gdk._2BUTTON_PRESS:
			if self.is_playing():
				self.toggle_fullscreen()
		else:
			return True
			
	def toggle_fullscreen(self):
		if self.is_fs:
			self.unfullscreen()
		else:
			self.fullscreen()

	def toggle_fullwindow(self):
		if self.is_fw:
			self.unfullwindow()
		else:
			self.fullwindow()

	def set_media_url(self, url):
		self.player.set_mrl(url)
		
	def play_media(self):
		self.player.play()
		if len(self.container.get_children()) == 0:
			self.container.add(self)
		
		self.show()

	def is_playing(self):
		return self.player.is_playing()
		
	def media_loaded(self):
		return self.is_playing()
		
	def resume_media(self):
		self.player.resume()
		
	def stop_media(self):
		self.player.stop()
		
	def pause_media(self):
		self.player.pause()
		
	def exit_media(self):
		exit = True
		
	def display_text(self, text):
		self.player.display_text("%s" % text, 0, 5000)
		
	def is_fullscreen(self):
		return self.is_fs
		
	def fullscreen(self):
		self.wt.fullscreen()
		self.is_fs = True
	
	def unfullscreen(self):
		self.wt.unfullscreen()
		self.is_fs = False
		
	def fullwindow(self):
		self.wt.fullwindow()
		self.is_fw = True
	
	def unfullwindow(self):
		self.wt.unfullwindow()
		self.is_fw = False
	
	def set_volume(self, level):
		self.player.audio_set_volume(level)
		
	def screenshot(self):
		return self.player.snapshot(0)

