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


# Begining 2011 review of code, started 30 April 2011

import gettext
import gobject
import gtk
import gtk.glade
import locale
import math
import sys
import os

from DatabaseOperations import DatabaseOperations
from dynamic_ports import DynamicPorts
from fork import ForkSOP
from listen import Listen
import pySocket
from pySopCastConfigurationManager import pySopCastConfigurationManager
from VLCWidget import VLCWidget
from OptionsDialog import OptionsDialog
from WindowingTransformations import WindowingTransformations
from SopcastPlayerWorkerThread import UpdateUIThread
from ChannelGuideWorkerThread import UpdateChannelGuideThread
from OpenSopAddress import OpenSopAddress

cur_locale = locale.setlocale(locale.LC_ALL, "")

gtk.glade.bindtextdomain("sopcast-player")
gtk.glade.textdomain("sopcast-player")

gettext.bindtextdomain("sopcast-player")
gettext.textdomain("sopcast-player")

lang = gettext.translation("sopcast-player", languages=[cur_locale], fallback=True)
lang.install('sopcast-player')

def is_chinese():
	return not cur_locale[:len("zh".lower())] != "zh".lower()

class pySopCast(object):
	def __init__(self, channel_url=None, inbound_port=None, outbound_port=None):
		gtk.gdk.threads_init()
		#*****************Sopcast specific code*******************
		self.vlc= None
		self.ui_worker = None
		self.channel_url = channel_url
		self.static_ports = False
		self.inbound_port = inbound_port
		self.outbound_port = outbound_port
		self.sop_stats = None
		#used by external player
		self.outbound_media_url = None
		self.channel_guide_language = None
		self.sopcast_client_installed = True
		self.channel_guide_worker = None
		self.channel_guide_url = None		
		self.external_player_command = None
		self.fullwindow = False
		try:
			self.fork_sop = ForkSOP()
		except:
			self.sopcast_client_installed = False				
		#************************End******************************
		
		self.status_bar_text = None
		self.db_operations = DatabaseOperations()		
		self.treeview_selection = None
		self.window_title = "SopCast Player"
		self.config_manager = None
		
				
	def main(self, sop_address=None, sop_address_name=None):
		gladefile = "%s/%s" % (os.path.realpath(os.path.dirname(sys.argv[0])), "../ui/pySopCast.glade")
			
		self.glade_window = gtk.glade.XML(gladefile, "window", "sopcast-player")
		self.window = self.glade_window.get_widget("window")
		
		glade_context_menu = gtk.glade.XML(gladefile, "context_menu", "sopcast-player")
		self.context_menu = glade_context_menu.get_widget("context_menu")
		
		glade_bookmarks_context_menu = gtk.glade.XML(gladefile, "bookmarks_context_menu", "sopcast-player")
		self.bookmarks_context_menu = glade_bookmarks_context_menu.get_widget("bookmarks_context_menu")
		

		
		window_signals = { "on_mainWindow_destroy" : self.on_exit,
			"on_play_button_clicked" : self.on_play_button_clicked,
			"on_menu_quit_activate" : self.on_menu_quit_activate,
			"on_menu_fullscreen_activate" : self.on_fullscreen_activate,
			"on_menu_add_bookmark_activate" : self.on_add_bookmark,
			"on_stop_clicked" : self.on_stop_clicked,
			"on_volume_adjust_bounds" : self.on_volume_adjust_bounds,
			"on_menu_about_activate" : self.on_menu_about_activate,
			"on_open_sop_address_activate" : self.on_open_sop_address_activate,
			"on_show_url_activate" : self.on_show_url_activate,
			"on_refresh_channel_guide_clicked" : self.on_refresh_channel_guide_clicked,
			"on_menu_screenshot_activate" : self.on_menu_screenshot_activate,
			"on_menu_preferences_activate" : self.on_menu_preferences_activate,
			"on_menu_stay_on_top_toggled" : self.on_menu_stay_on_top_toggled,
			"on_menu_show_controls_toggled" : self.on_menu_show_controls_toggled,
			"on_window_key_press_event" : self.on_window_key_press_event,
			"on_channel_treeview_button_press_event" : self.on_channel_treeview_button_press_event }
			
		self.glade_window.signal_autoconnect(window_signals)
		
		context_menu_signals = { "on_context_menu_play_activate" : self.on_context_menu_play_activate,
					 "on_context_menu_properties_activate" : self.on_context_menu_properties_activate }
		glade_context_menu.signal_autoconnect(context_menu_signals)
		
		bookmarks_context_menu_signals = { "on_bookmarks_context_delete_activate" : self.on_bookmarks_context_delete_activate, }
		glade_bookmarks_context_menu.signal_autoconnect(bookmarks_context_menu_signals)
		
		#*****************Sopcast specific code*******************
		self.config_manager = pySopCastConfigurationManager()
		self.vlc = VLCWidget(self.eb, self)
		self.player_volume = self.config_manager.player_volume()
		self.volume.set_value(self.player_volume)
		self.ui_worker = UpdateUIThread(self, self.config_manager.channel_timeout())
		self.ui_worker.start()			
		self.channel_guide_url = self.config_manager.channel_guide_url()
		self.channel_guide_hpane.set_position(self.config_manager.channel_guide_pane_position())		
		self.channel_guide_language = self.config_manager.channel_guide_language()		
		
		if self.config_manager.use_external_player() == True:
			self.set_media_player_visible(False)
			self.external_player_command = self.config_manager.external_player_command()
			show_channel_guide_pane = True	
		
		#these four lines don't belong with sc code but must be before populate_channel_treeview
		self.channel_treeview_model = gtk.TreeStore(int, str, str, str, str, str, int, int, int, str)
		self.treeview_selection = self.channel_treeview.get_selection()
		self.treeview_selection_changed_handler = self.treeview_selection.connect("changed", self.on_selection_changed)
		self.channel_treeview.connect("row_activated", self.on_channel_treeview_row_activated)			
				
		chinese = self.channel_guide_language == _("Chinese")
		self.populate_channel_treeview(chinese)		
		
		if sop_address != None:
			if sop_address[:len("sop://".lower())] == "sop://".lower():
				self.play_channel(sop_address, sop_address_name)
		#************************End******************************		
		
		self.window.set_default_size(self.config_manager.player_width(), self.config_manager.player_height())
		self.display_pane.set_position(self.config_manager.display_pane_position())
		show_channel_guide_pane = self.config_manager.show_channel_guide()		
		self.window.set_keep_above(self.config_manager.stay_on_top())		
		self.menu_stay_on_top.set_active(self.config_manager.stay_on_top())
		self.populate_bookmarks()

		column = gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=1)
		self.channel_treeview.append_column(column)
		
		if show_channel_guide_pane == False:
			self.channel_guide_pane.hide()
		
		self.wt = WindowingTransformations(self.eb, self)
		self.show_channel_guide.set_active(show_channel_guide_pane)
		self.show_channel_guide.connect("toggled", self.on_show_channel_guide_toggled)
	
		if self.channel_url != None:
			self.play_channel()
		
		self.window.show()
			
		gtk.main()
		
		if self.fork_sop != None:
			self.fork_sop.kill_sop()
			
	def on_mouse_button_clicked(self, widget, event):
		if event.type == gtk.gdk._2BUTTON_PRESS:
			if self.is_playing():
				self.toggle_fullscreen()
		else:
			return True
			
	def toggle_fullscreen(self):
		if not self.fullscreen:
			if self.vlc.media_loaded():
				self.vlc.fullscreen()
				#self.vlc.display_text("         %s" % "Press Esc to exit fullscreen")
				self.fullscreen = not self.fullscreen
		else:
			self.vlc.unfullscreen()
			self.fullscreen = not self.fullscreen
	
	#code for context menu
	def on_context_menu_play_activate(self, src, data=None):
		self.play_channel(self.channel_treeview_model[self.channel_treeview.get_cursor()[0]][9])
	
	def on_context_menu_properties_activate(self, src, data=None):
		path, column = self.channel_treeview.get_cursor()
		
		gladefile = "%s/%s" % (os.path.realpath(os.path.dirname(sys.argv[0])), "../ui/ChannelProperties.glade")
			
		tree = gtk.glade.XML(gladefile, "window")
		
		dialog = tree.get_widget("window")
		dialog.set_title("%s - %s" % (_("Properties"), "SopCast Player"))
		dialog.set_transient_for(self.window)
		
		label_name = tree.get_widget("label_name")
		label_classification = tree.get_widget("label_classification")
		label_stream_type = tree.get_widget("label_stream_type")
		label_bitrate = tree.get_widget("label_bitrate")
		label_qc = tree.get_widget("label_qc")
		label_qs = tree.get_widget("label_qs")
		label_description = tree.get_widget("label_description")
		
		label_group = [label_name, label_classification, label_stream_type, label_bitrate, label_qc, label_qs, label_description]
		labels = ["%s: %s" % (_("Name"), self.html_escape(self.channel_treeview_model[path][1])), "%s: %s" % (_("Classification"), self.html_escape(self.channel_treeview_model[path][4])), "%s: %s" % (_("Stream Format"), self.html_escape(self.channel_treeview_model[path][5].upper())), "%s %d kb/s" % (_("Bitrate:"), self.channel_treeview_model[path][6]), "%s: %d" % (_("QC"), self.channel_treeview_model[path][7]), "%s: %d" % (_("QS"), self.channel_treeview_model[path][8]), "%s: %s" % (_("Description"), self.html_escape(self.channel_treeview_model[path][2]))]
		self.set_label_group(label_group, labels)
		
		dialog.run()
		
		dialog.destroy()
	#end
	
	def on_fullscreen_activate(self, src, data=None):
		self.vlc.toggle_fullscreen()
		
	def __getattribute__(self, key):
		value = None
		try:
			value = object.__getattribute__(self, key)
		except AttributeError:
			glade_window = object.__getattribute__(self, 'glade_window')
			value = glade_window.get_widget(key)	

		return value
	
	def get_ports(self):
		inbound_port = None
		outbound_port = None
		exit = False
		
		if self.config_manager.use_static_ports() == True:
			inbound_port = self.config_manager.inbound_static_port()
			outbound_port = self.config_manager.outbound_static_port()
			self.static_ports = True
			s = pySocket.pySocket()
			if not s.is_available(self.config_manager.server(), inbound_port) or not s.is_available(self.config_manager.server(), outbound_port):

				dialog = gtk.Dialog(_("Static Ports Unavailable"),
					self.window,
					gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
					(gtk.STOCK_NO, gtk.RESPONSE_REJECT,
					gtk.STOCK_YES, gtk.RESPONSE_ACCEPT))
			
				hbox = gtk.HBox()
		
			
				label = gtk.Label(_("Static ports unavailable, do you wish to continue using dynamic ports?"))
				hbox.pack_start(label)
				hbox.set_size_request(-1, 50)
				hbox.show_all()
				dialog.set_default_response(gtk.RESPONSE_ACCEPT)
				dialog.vbox.pack_start(hbox)
		
				if dialog.run() == gtk.RESPONSE_REJECT:
					exit = True
				
				dialog.destroy()

				dyn = DynamicPorts()
				inbound_port, outbound_port = dyn.get_ports()
				self.static_ports = False
		else:
			dyn = DynamicPorts()
			inbound_port, outbound_port = dyn.get_ports()
		
		if exit == True:
			inbound_port = None
			outbound_port = None
			
		return inbound_port, outbound_port
	
	
	###################################
	def on_bookmarks_button_pressed(self, src, event, bookmark):
		if event.button == 3:
			self.selected_bookmark = bookmark
			self.bookmarks_context_menu.popup(None, None, None, event.button, event.time)
		
	def on_bookmarks_context_delete_activate(self, src, data=None):
		self.db_operations.delete_bookmark(self.selected_bookmark[0])
		self.bookmarks_menu.popdown()
		self.main_menu.cancel()
		self.populate_bookmarks()
		
	def populate_bookmarks(self):
		self.clear_bookmarks()
		for bookmark in self.db_operations.retrieve_bookmarks():
			menu_item = gtk.MenuItem(bookmark[1])
			menu_item.connect("activate", self.on_menu_bookmark_channel_activate, bookmark)
			menu_item.connect("button_press_event", self.on_bookmarks_button_pressed, bookmark)
			self.menu_bookmarks.get_submenu().append(menu_item)
			self.menu_bookmarks.get_submenu().show_all()
	
	def populate_channel_treeview(self, chinese=False):
		self.channel_treeview.set_model()
		self.channel_treeview_model.clear()
		if chinese == False:
			channel_groups = self.db_operations.retrieve_channel_groups()
		else:
			channel_groups = self.db_operations.retrieve_channel_groups_cn()
		
		for channel_group in channel_groups:
			channel_group_iter = self.channel_treeview_model.append(None, self.prepare_row_for_channel_treeview_model(channel_group))
			
			if chinese == False:
				channels = self.db_operations.retrieve_channels_by_channel_group_id(channel_group[0])
			else:
				channels = self.db_operations.retrieve_channels_by_channel_group_id_cn(channel_group[0])
		
			for channel in channels:
				self.channel_treeview_model.append(channel_group_iter, self.prepare_row_for_channel_treeview_model(channel))
		
		self.channel_treeview.set_model(self.channel_treeview_model)

	def set_media_player_visible(self, visible):
		if visible == True:
			if self.show_channel_guide.get_active() == False:
				self.channel_guide_pane.hide()
					
			self.menu_view.show()
			self.media_box.show()
			self.channel_properties_pane.hide()
		else:
			self.menu_view.hide()
			self.media_box.hide()
			self.channel_properties_pane.show()
			
			if self.channel_guide_pane.get_property("visible") == False:
				self.channel_guide_pane.show()
	
	def prepare_row_for_channel_treeview_model(self, row):
		if len(row) == 10:
			return row
		else:
			return [row[0], row[1], row[2], None, None, None, 0, 0, 0, None]
			
	def clear_bookmarks(self):
		menu_items = self.menu_bookmarks.get_submenu().get_children()
		
		if len(menu_items) > 2:
			i = 2
			while i < len(menu_items):
				self.menu_bookmarks.get_submenu().remove(menu_items[i])
				i += 1
	
	def on_menu_quit_activate(self, src, data=None):
		self.window.destroy()
		
	def on_menu_bookmark_channel_activate(self, src, channel_info):
		self.play_channel(channel_info[2])
		
	def on_add_bookmark(self, src, data=None):
		dialog = gtk.Dialog(_("Channel Bookmark"),
			self.window,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
			gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			
		hbox = gtk.HBox()
			
		label = gtk.Label("%s %s" % (_("Name"), ": "))
		entry = gtk.Entry()
		
		entry.connect("activate", lambda a: dialog.response(gtk.RESPONSE_ACCEPT))
		
		if self.selection != None:
			if len(entry.get_text()) > 0:
				entry.set_text(self.selection[1])
		
		if self.selection:
			entry.set_text(self.selection[1])
		
		hbox.pack_start(label)
		hbox.pack_start(entry)
		hbox.set_size_request(-1, 50)
		hbox.show_all()
		dialog.set_default_response(gtk.RESPONSE_ACCEPT)
		dialog.vbox.pack_start(hbox)
		
		if dialog.run() == gtk.RESPONSE_ACCEPT:
			if len(entry.get_text()) > 0:
				self.add_bookmark(unicode(entry.get_text()), self.url)
			
		dialog.destroy()
		
	def on_stop_clicked(self, src, data=None):
		self.menu_fullscreen.set_sensitive(False)
		self.vlc.stop_media()
		
		self.ui_worker.shutdown()
		if self.fork_sop.is_running() == True:
			self.fork_sop.kill_sop()
		
		self.update_statusbar("")
		self.window.set_title(self.window_title)
		
	def on_volume_adjust_bounds(self, src, data=None):
		self.player_volume = int(src.get_value())
		self.vlc.set_volume(self.player_volume)
	
	def on_menu_about_activate(self, src, data=None):
		gladefile = "%s/%s" % (os.path.realpath(os.path.dirname(sys.argv[0])), "../ui/About.glade")
		about_file = gtk.glade.XML(gladefile, "about")
		about = about_file.get_widget("about")
		about.set_transient_for(self.window)
		about.run()
		about.destroy()
	
	def on_open_sop_address_activate(self, src, data=None):
		dialog = gtk.Dialog(_("Open Sop Address"),
			self.window,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
			gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			
		hbox = gtk.HBox()
			
		label = gtk.Label("%s %s" % (_("Enter Sop Address"), ": "))
		entry = gtk.Entry()
		
		clipboard = gtk.clipboard_get().wait_for_text()
		
		if clipboard and clipboard[0:6].lower() == "sop://":
			entry.set_text(clipboard)
		
		############# Code contribution by Benjamin Kluglein ####################
		entry.connect("activate", lambda a: dialog.response(gtk.RESPONSE_ACCEPT))
		#########################################################################
		
		hbox.pack_start(label)
		hbox.pack_start(entry)
		hbox.set_size_request(-1, 50)
		hbox.show_all()
		dialog.set_default_response(gtk.RESPONSE_ACCEPT)
		dialog.vbox.pack_start(hbox)
		
		if dialog.run() == gtk.RESPONSE_ACCEPT:
			if len(entry.get_text()) > 0:
				self.play_channel(entry.get_text())
			
		dialog.destroy()
		
		
	def on_show_url_activate(self, src, data=None):
		dialog = gtk.Dialog(_("URL"),
			self.window,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			
		hbox = gtk.HBox()
		entry = gtk.Entry(30)
		
		clipboard = gtk.clipboard_get().wait_for_text()
		
		entry.set_text(self.channel_url)
		entry.set_editable(False)
		if len(entry.get_text()) > 0:
			entry.select_region(0, len(entry.get_text()))
		
		############# Code contribution by Benjamin Kluglein ####################
		entry.connect("activate", lambda a: dialog.response(gtk.RESPONSE_ACCEPT))
		#########################################################################
		
		hbox.pack_start(entry)
		hbox.set_size_request(250, 50)
		hbox.show_all()
		dialog.set_default_response(gtk.RESPONSE_ACCEPT)
		dialog.vbox.pack_start(hbox)
		dialog.run()
		dialog.destroy()
	
	def on_show_channel_guide_toggled(self, src, data=None):
		window_width = self.window.get_size()[0]
		window_height = self.window.get_size()[1]
		handle_width = self.display_pane.style_get_property("handle-size")
		
		if src.get_active() == True:
			self.window.resize(window_width + self.config_manager.channel_guide_width(), window_height)
			self.channel_guide_pane.show()
			
		else:
			pane2_width = self.display_pane.get_child2().get_allocation()[2]
			self.config_manager.channel_guide_width(pane2_width + handle_width)
			
			self.channel_guide_pane.hide()
			self.window.resize(self.display_pane.get_child1().get_allocation()[2], window_height)
	
	def on_channel_treeview_row_activated(self, treeview, path, view_column, data=None):
		if self.channel_treeview_model.iter_has_child(treeview.get_model().get_iter(path)) == True:
			if self.channel_treeview.row_expanded(path) == False:
				self.channel_treeview.expand_row(path, False)
			else:
				self.channel_treeview.collapse_row(path)
		else:
			self.play_channel(self.selection[9], self.selection[1])
			
	def set_label_group(self, label_group, labels=None):
		i = 0
		if labels != None:
			while i < len(label_group):
				label_group[i].set_label(labels[i])
				i += 1
		else:
			while i < len(label_group):
				label_group[i].set_label("")
				i += 1

	def on_selection_changed(self, src, data=None):
		model, s_iter = src.get_selected()

		if s_iter:
			row = model.get_path(s_iter)
			self.selection = self.channel_treeview_model[row]
	
			if self.channel_treeview_model.iter_has_child(s_iter) == False:
				label_group = [self.label_name, self.label_channel_group, self.label_classification, self.label_stream_type, self.label_bitrate, self.label_qc, self.label_qs, self.label_description]
				labels = ["%s: %s" % (_("Name"), self.html_escape(self.selection[1])), "%s: %s" % (_("Channel Group"), self.html_escape(self.channel_treeview_model[self.channel_treeview_model.get_path(self.channel_treeview_model.iter_parent(s_iter))][1])), "%s: %s" % (_("Classification"), self.html_escape(self.selection[4])), "%s: %s" % (_("Stream Format"), self.html_escape(self.selection[5].upper())), "Bitrate: %d kb/s" % self.selection[6], "%s: %d" % (_("QC"), self.selection[7]), "%s: %d" % (_("QS"), self.selection[8]), "%s: %s" % (_("Description"), self.html_escape(self.selection[2]))]
				self.set_label_group(label_group, labels)
		
			else:
				label_group = [self.label_name, self.label_channel_group, self.label_classification, self.label_stream_type, self.label_bitrate, self.label_qc, self.label_qs, self.label_description]
				labels = ["%s: %s" % (_("Name"), self.html_escape(self.selection[1])), "%s: %d" % (_("Channels"), self.get_iter_child_count(s_iter)), "%s: %s" % (_("Description"), self.html_escape(self.selection[2])), "" ,"" ,"" ,"" ,""]
				self.set_label_group(label_group, labels)
		else:
			self.selection = None
			label_group = [self.label_name, self.label_channel_group, self.label_classification, self.label_stream_type, self.label_bitrate, self.label_qc, self.label_qs, self.label_description]
			self.set_label_group(label_group)
	
	def on_refresh_channel_guide_clicked(self, src, data=None):
		self.update_channel_guide_progress.set_fraction(0)
		self.channel_guide_label.hide()
		self.update_channel_guide_progress.show()
	
		if self.channel_guide_worker != None:
			if self.channel_guide_worker.running == False:
				self.channel_guide_worker = None
			
				self.channel_guide_worker = UpdateChannelGuideThread(self)
				self.channel_guide_worker.start()
		else:
			self.channel_guide_worker = UpdateChannelGuideThread(self)
			self.channel_guide_worker.start()
	
	def on_menu_screenshot_activate(self, src, data=None):
		screenshot = self.vlc.screenshot()
		print(screenshot)
	
	def on_menu_preferences_activate(self, src, data=None):
		od = OptionsDialog(self)
	
	def on_menu_stay_on_top_toggled(self, src, data=None):
		self.window.set_keep_above(src.get_active())
	
	def on_menu_show_controls_toggled(self, src, data=None):
		self.toggle_menu_controls()
		
	def toggle_menu_controls(self):
		self.vlc.toggle_fullwindow()

	def on_window_key_press_event(self, src, event, data=None):
		if event.keyval == gtk.keysyms.F11:
			if self.vlc.is_playing():
				self.menu_fullscreen.activate()
			return True
		elif gtk.gdk.keyval_name(event.keyval) in ["h", "H"]:
			if not self.fullscreen:
				self.toggle_menu_controls()
			return True
		elif event.keyval == gtk.keysyms.Escape:
			if self.fullscreen:
				self.toggle_fullscreen()
			return True
		elif gtk.gdk.keyval_name(event.keyval) in ["f", "F"]:
			if self.vlc.is_playing():
				self.menu_fullscreen.activate()
			return True
		
		return False
	
	def on_channel_treeview_button_press_event(self, src, event, data=None):
		if event.button == 3:
			x = int(event.x)
			y = int(event.y)
			time = event.time
			pthinfo = self.channel_treeview.get_path_at_pos(x, y)
			if pthinfo is not None:
				path, col, cellx, celly = pthinfo
				self.channel_treeview.grab_focus()
				self.channel_treeview.set_cursor( path, col, 0 )
				if self.channel_treeview_model.iter_has_child(self.channel_treeview_model.get_iter(path)) == False:
					self.context_menu.popup( None, None, None, event.button, time)
		return False

	def get_iter_child_count(self, parent_iter):
		i = 0
		
		child = self.channel_treeview_model.iter_children(parent_iter)
		
		while child != None:
			child = self.channel_treeview_model.iter_next(child)
			i += 1
		
		return i
		
	def update_status_bar_text(self, txt):
		if self.status_bar != None:
			self.status_bar_text = txt
	
	def set_volume(self, volume):
		self.vlc.set_volume(volume)
		
	def start_vlc(self):
		self.vlc.play_media()
		self.vlc.set_volume(self.player_volume)
		return True
			
	def stop_vlc(self):
		self.vlc.stop_media()
		
	def play_channel(self, channel_url=None, title=None):
		self.show_url.set_sensitive(True)
		self.menu_add_bookmark.set_sensitive(True)
		if self.fork_sop != None:
			if self.fork_sop.is_running() == True:
				self.fork_sop.kill_sop()
		
			s = pySocket.pySocket()
			if (self.inbound_port == None or self.outbound_port == None) or (not s.is_available(self.config_manager.server(), self.inbound_port) or not s.is_available(self.config_manager.server(), self.outbound_port)):
				self.inbound_port, self.outbound_port = self.get_ports()
			
			if self.inbound_port == None or self.outbound_port == None:
				self.window.destroy()
			else:
				self.sop_stats = Listen(self.config_manager.server(), self.outbound_port)
			
				if channel_url != None:
					self.channel_url = channel_url
					if title == None:
						self.window.set_title("%s - %s" % (channel_url, self.window_title))
			
				if title != None:
					self.window.set_title("%s - %s" % (title, self.window_title))
				else:
					records = self.db_operations.retrieve_bookmark_by_address(self.channel_url)
					if len(records) > 0:
						self.window.set_title("%s - %s" % (records[0][0], self.window_title))
					else:
						records = self.db_operations.retrieve_channel_guide_record_by_address(self.channel_url)
						if len(records) > 0:
							self.window.set_title("%s - %s" % (records[0][0], self.window_title))
				try:
					self.fork_sop.fork_sop(self.channel_url, str(self.inbound_port), str(self.outbound_port))
					self.menu_add_bookmark.set_sensitive(True)
					self.menu_fullscreen.set_sensitive(True)

					self.outbound_media_url = "http://%s:%d/tv.asf" % (self.config_manager.server(), self.outbound_port)
					self.vlc.set_media_url(self.outbound_media_url)
					self.ui_worker.startup()
				except Exception as ex:
					x, y = ex
					self.update_statusbar(y)
		


	def on_play_button_clicked(self, src, data=None):
		if self.channel_url != None:
			self.play_channel(self.channel_url)
		
	def lookup_title(self, title):
		if self.title[:len("sop://")] == "sop://".lower():
			records = self.db_operations.retrieve_bookmark_by_address(channel_url)
			if len(records) > 0:
				self.channel_url_entry.set_text(records[0][0])
			else:
				records = self.db_operations.retrieve_channel_guide_record_by_address(channel_url)
				if len(records) > 0:
					self.channel_url_entry.set_text(records[0][0])
				else:
					self.play_channel(channel_url)
		else:
			
			if len(records) > 0:
				self.play_channel(records[0][2], title)
			
	def on_exit(self, widget, data=None):
		self.config_manager.player_width(self.window.get_allocation()[2])
		self.config_manager.player_height(self.window.get_allocation()[3])
		
		if self.channel_selection_pane.get_property("visible") == True and self.media_box.get_property("visible") == True:	
			self.config_manager.display_pane_position(self.display_pane.get_position())
		
		if self.channel_properties_pane.get_property("visible") == True and self.media_box.get_property("visible") == False:
			self.config_manager.channel_guide_pane_position(self.channel_guide_hpane.get_position())
			
		self.config_manager.show_channel_guide(self.show_channel_guide.get_active())
		self.config_manager.player_volume(int(self.volume.get_value()))
		
		self.ui_worker.stop()
		if self.fork_sop != None:
			if self.fork_sop.is_running() == True:
				self.vlc.stop_media()
				self.vlc.exit_media()
				self.fork_sop.kill_sop()
			
		gtk.main_quit()
		self = None
	
	def add_bookmark(self, channel_name, url=None):
		if url == None:
			url = self.channel_url
		
		self.db_operations.insert_bookmark(channel_name, url)
		self.populate_bookmarks()
		
		if url == self.channel_url:
			self.window.set_title("%s - %s" % (channel_name, self.window_title))
	
	def update_statusbar(self, text):
		if self.status_bar != None:
			self.status_bar.push(1, text)
		
	def set_title(self, title="pySopCast"):
		self.window.set_title(title)	
		
	def html_escape(self, text):
		html_escape_table = {
			"&": "&amp;",
			'"': "&quot;",
			"'": "&apos;",
			">": "&gt;",
			"<": "&lt;",
			}
		"""Produce entities within text."""
		L=[]
		for c in text:
			L.append(html_escape_table.get(c,c))
		return "".join(L)
		
if __name__ == '__main__':
	def print_usage_and_exit():
		print("Usage: sopcast-player [SOP_ADDRESS] [IN-BOUND_PORT OUT-BOUND_PORT]")
		sys.exit(1)
		
	if len(sys.argv) > 1:
		if len(sys.argv) == 2 and sys.argv[1][:len("sop://".lower())] == "sop://".lower():
				pySop = pySopCast(sys.argv[1])
				pySop.main()
				
		elif len(sys.argv) == 4 and sys.argv[1][:len("sop://".lower())] == "sop://".lower():
			try:
				pySop = pySopCast(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
				pySop.main()
			except ValueError:
				print_usage_and_exit()
		else:
			print_usage_and_exit()
	else:
		pySop = pySopCast()
		pySop.main()
	
