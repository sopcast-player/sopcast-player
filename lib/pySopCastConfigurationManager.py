# pySopCast implementation of ConfigurationManager
# Copyright (C) 2009-2011 Jason Scheunemann <jason.scheunemann@yahoo.com>.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from ConfigurationManager import *
import os
import locale

class ChannelGuideLanguages:
	ENGLISH = 0
	CHINESE = 1

class ChannelGuideLayout:
	UNITY = 0
	DUAL_WINDOW = 1
	
class ChannelGuideAutoRefresh:
	NEVER = 0
	DAILY = 1
	PROGRAM_START = 2

cur_locale = locale.setlocale(locale.LC_ALL, "")

def is_chinese():
	return not cur_locale[:len("zh".lower())] != "zh".lower()

class pySopCastConfigurationManager(ConfigurationManager):
	def __init__(self):
		ConfigurationManager.__init__(self, os.path.expanduser('~/.pySopCast/pySopCast.cfg'))
		
		if is_chinese() == True:
			language = _("Chinese")
			channel_guide = "http://channel.sopcast.com/gchlxml"
		else:
			language = _("English")
			channel_guide = "http://www.sopcast.com/gchlxml"
					     
		self.add_section("player", { "show_toolbar" : True,
					     "static_ports" : False,
					     "width" : 600,
					     "height" : 400,
					     "div_position" : 300,
					     "show_channel_guide" : True,
					     "inbound_port" : 8901,
					     "outbound_port" : 8902,
					     "volume" : 100,
					     "server" : "127.0.0.1",
					     "channel_guide_width" : 80,
					     "external_player" : False,
					     "external_player_command" : "mplayer -ontop -geometry 100%%:100%%",
					     "channel_timeout" : 3,
					     "stay_on_top" : False,
					     "show_channel_guide_toolbar_item" : True,
					     "new_bindings" : True,
					     "layout" : ChannelGuideLayout.UNITY })
						  
		self.add_section("ChannelGuide", {  "width" : 600,
						    "height" : 400,
						    "auto_refresh" : False,
						    "auto_refresh_frequency" : ChannelGuideAutoRefresh.NEVER,
						    "channel_guide_language" : language,
						    "last_updated" : "Never",
						    "url" : channel_guide,
						    "div_position" : 200 })
		self.read()
	
	def uses_new_bindings(self, value=None):
		return self.__getter_setter("getboolean", "player", "new_bindings", value)
	
	def player_width(self, value=None):
		return self.__getter_setter("getint", "player", "width", value)
	
	def player_height(self, value=None):
		return self.__getter_setter("getint", "player", "height", value)
		
	def inbound_static_port(self, value=None):
		return self.__getter_setter("getint", "player", "inbound_port", value)
	
	def outbound_static_port(self, value=None):
		return self.__getter_setter("getint", "player", "outbound_port", value)
		
	def server(self, value=None):
		return self.__getter_setter("get", "player", "server", value)
		
	def display_pane_position(self, value=None):
		return self.__getter_setter("getint", "player", "div_position", value)
		
	def player_volume(self, value=None):
		return self.__getter_setter("getint", "player", "volume", value)
	
	def show_channel_guide(self, value=None):
		return self.__getter_setter("getboolean", "player", "show_channel_guide", value)
		
	def use_static_ports(self, value=None):
		return self.__getter_setter("getboolean", "player", "static_ports", value)
		
	def stay_on_top(self, value=None):
		return self.__getter_setter("getboolean", "player", "stay_on_top", value)
		
	def use_external_player(self, value=None):
		return self.__getter_setter("getboolean", "player", "external_player", value)

	def external_player_command(self, value=None):
		return self.__getter_setter("get", "player", "external_player_command", value)
	
	def channel_guide_url(self, value=None):
		return self.__getter_setter("get", "ChannelGuide", "url", value)
	
	def channel_guide_language(self, value=None):
		return self.__getter_setter("get", "ChannelGuide", "channel_guide_language", value)

	def channel_guide_pane_position(self, value=None):
		return self.__getter_setter("getint", "ChannelGuide", "div_position", value)
		
	def channel_guide_width(self, value=None):
		return self.__getter_setter("getint", "ChannelGuide", "width", value)
	
	def channel_timeout(self, value=None):
		return self.__getter_setter("getint", "player", "channel_timeout", value)
	
	def __getter_setter(self, function, section, parameter, value=None):
		if value is None:
			return getattr(super(pySopCastConfigurationManager, self), function)(section, parameter)
		else:
			self.set(section, parameter, value)
			self.write()
			
			return
	
