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

import gtk
import locale
import math
import sys
import os
import pySopCastConfigurationManager
import locale
import gettext

cur_locale = locale.setlocale(locale.LC_ALL, "")

gtk.glade.bindtextdomain("sopcast-player")
gtk.glade.textdomain("sopcast-player")

gettext.bindtextdomain("sopcast-player")
gettext.textdomain("sopcast-player")

lang = gettext.translation("sopcast-player", languages=[cur_locale], fallback=True)
lang.install('sopcast-player')

def is_chinese():
	return not locale.setlocale(locale.LC_ALL, "")[:len("zh".lower())] != "zh".lower()

class OptionsDialog:
	def __init__(self, parent):
		self.parent = parent
		self.run()
		
	
	def run(self):	
		gladefile = "%s/%s" % (os.path.realpath(os.path.dirname(sys.argv[0])), "../ui/Options.glade")
		
		tree = gtk.glade.XML(gladefile, "window")
	
		dialog = tree.get_widget("window")
		dialog.set_title("%s - %s" % (_("Preferences"), "SopCast Player"))
		dialog.set_transient_for(self.parent.window)
			
		# Default retrieval
		static_ports_default = self.parent.config_manager.use_static_ports()
		inbound_port_default = self.parent.config_manager.inbound_static_port()
		outbound_port_default = self.parent.config_manager.outbound_static_port()
	
		external_player_default = self.parent.config_manager.use_external_player()
		external_player_command_default = self.parent.config_manager.external_player_command()
	
		channel_guide_url_default = self.parent.config_manager.channel_guide_url()
		language_combobox_default = self.parent.config_manager.channel_guide_language()

		# Widget variables
		static_ports = tree.get_widget("static_ports")
		inbound_port = tree.get_widget("inbound_port")
		outbound_port = tree.get_widget("outbound_port")
		static_ports_children = ( inbound_port, outbound_port )
	
		external_player = tree.get_widget("external_player")
		external_player_command = tree.get_widget("external_player_command")
	
		channel_guide_url = tree.get_widget("channel_guide_url")
	
		language_combobox = tree.get_widget("language_combobox")
	
	
		# Signal functions and helpers
		def set_widgets_sensitive(widgets, sensitive):
			for widget in widgets:
				widget.set_sensitive(sensitive)
	
		def on_static_ports_toggled(src, data=None):
			set_widgets_sensitive(static_ports_children, src.get_active())
			self.parent.config_manager.use_static_ports(src.get_active())
			self.parent.static_ports = src.get_active()
		
			if self.parent.static_ports == False:
				self.parent.inbound_port = None
				self.parent.outbound_port = None
			else:
				self.parent.inbound_port = int(inbound_port.get_value())
				self.parent.outbound_port = int(outbound_port.get_value())
	
		def on_inbound_port_value_changed(src, data=None):
			if src.get_value() == outbound_port.get_value():
				src.set_value(src.get_value() + 1)
			else:
				self.parent.config_manager.inbound_static_port(int(src.get_value()))
				self.parent.inbound_port = int(src.get_value())
		
		def on_outbound_port_value_changed(src, data=None):
			if src.get_value() == inbound_port.get_value():
				src.set_value(src.get_value() + 1)
			else:
				self.parent.config_manager.outbound_static_port(int(src.get_value()))
				self.parent.outbound_port = int(src.get_value())
	
		def on_external_player_toggled(src, data=None):
			external_player_command.set_sensitive(src.get_active())
			#print src.get_active()
			self.parent.config_manager.use_external_player(src.get_active())
		
			if src.get_active():
				self.parent.external_player_command = external_player_command.get_text()
				self.parent.set_media_player_visible(False)
			else:
				self.parent.external_player_command = None
				self.parent.set_media_player_visible(True)
			#TODO: Mashup the player window to only show channel guide and set ui_worker to launch external command
	
		def on_external_player_command_focus_out_event(src, event, data=None):
			if external_player_command.get_text() != external_player_command_default:
				self.parent.config_manager.external_player_command(src.get_text())
			
				self.parent.external_player_command = external_player_command.get_text()
				#TODO: Mashup the player window to only show channel guide and set ui_worker to launch external command
	
		def on_channel_guide_url_focus_out_event(src, event, data=None):
			if src.get_text() != channel_guide_url_default:
				self.parent.config_manager.channel_guide_url(src.get_text())
				self.parent.channel_guide_url = src.get_text()
	
		def on_language_combobox_changed(src, data=None):
			chinese = False
			self.parent.config_manager.channel_guide_language(src.get_active_text())
		
			if src.get_active_text() == _("Chinese"):
				chinese = True
		
			self.parent.populate_channel_treeview(chinese)
			self.parent.channel_guide_language = src.get_active_text()
				
				
		# Setup widget defaults
		static_ports.set_active(static_ports_default)
		set_widgets_sensitive(static_ports_children, static_ports_default)
		inbound_port.set_value(inbound_port_default)
		outbound_port.set_value(outbound_port_default)
	
		external_player.set_active(external_player_default)
		external_player_command.set_text(external_player_command_default)
		external_player_command.set_sensitive(external_player_default)
	
		channel_guide_url.set_text(channel_guide_url_default)
	
		if is_chinese() == False:
			language_combobox.insert_text(0, _("English"))
			language_combobox.insert_text(1, _("Chinese"))
		else:
			language_combobox.insert_text(0, _("Chinese"))				
			language_combobox.insert_text(1, _("English"))
	
		if is_chinese() == False:
			if language_combobox_default == _("English"):
				language_combobox.set_active(0)
			else:
				language_combobox.set_active(1)
		else:
			if language_combobox_default == _("Chinese"):
				language_combobox.set_active(0)
			else:
				language_combobox.set_active(1)

		# Signal connect
		dic = { "on_static_ports_toggled" : on_static_ports_toggled,
			"on_inbound_port_value_changed" : on_inbound_port_value_changed,
			"on_outbound_port_value_changed" : on_outbound_port_value_changed,
			"on_external_player_toggled" : on_external_player_toggled,
			"on_external_player_command_focus_out_event" : on_external_player_command_focus_out_event,
			"on_channel_guide_url_focus_out_event" : on_channel_guide_url_focus_out_event,
			"on_language_combobox_changed" : on_language_combobox_changed}
		tree.signal_autoconnect(dic)
	
		dialog.run()
	
		# Post-response action area
		dialog.destroy()
