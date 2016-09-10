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

import DatabaseOperations
import os
import sys
from xml.dom.minidom import parse

class Language:
	ENGLISH = 0
	CHINESE = 1


class ImportChannelGuide(object):
	def __init__(self):
		self.db_operations = DatabaseOperations.DatabaseOperations()
	
	def getText(self, nodelist):
		rc = ""
	 	for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				rc = node.data
		return rc
		
	def attribute_exists(self, element, attribute):
		found = False
		
		if element.getAttribute(attribute) != "":
			found = True
		
		return found
		
	def get_english(self, element):
		value = None
		if self.attribute_exists(element, "en"):
			if element.attributes["en"].value != "":
				value = element.attributes["en"].value
				
		if value == None:
			if self.getText(element.childNodes) != "":
				value = self.getText(element.childNodes)
		
		if value == None:
			if self.attribute_exists(element, "cn"):
				if element.attributes["cn"].value != "":
					value = element.attributes["cn"].value
		
		return value
		
		
	def get_chinese(self, element):
		value = None
		if self.attribute_exists(element, "cn"):
			if element.attributes["cn"].value != "":
				value = element.attributes["cn"].value
				
		if value == None:
			if self.getText(element.childNodes) != "":
				value = self.getText(element.childNodes)
		
		if value == None:
			if self.attribute_exists(element, "en"):
				if element.attributes["en"].value != "":
					value = element.attributes["en"].value
		
		return value
		
	def get_default(self, element):
		value = None
		
		if self.getText(element.childNodes) != "":
			value = self.getText(element.childNodes)
		
		if value == None:
			if self.attribute_exists(element, "en"):
				if element.attributes["en"].value != "":
					value = element.attributes["en"].value
		
		if value == None:
			if self.attribute_exists(element, "cn"):
				if element.attributes["cn"].value != "":
					value = element.attributes["cn"].value
		
		return value
	
	def get_child_tag_translation(self, element, tag_name, language=None):
		value = None
		
		temp = element.getElementsByTagName(tag_name)[0]
		
		if language == Language.ENGLISH:
			value = self.get_english(temp)
		elif language == Language.CHINESE:
			value = self.get_chinese(temp)
		elif language == None:
			value = self.get_default(temp)
			
		return value
		
	def get_tag_translation(self, element, language=None):
		value = None
		
		if language == Language.ENGLISH:
			value = self.get_english(element)
		elif language == Language.CHINESE:
			value = self.get_chinese(element)
		elif language == None:
			value = self.get_default(element)
			
		return value
	
	def get_tag_attribute(self, element, attribute):
		value = None
		if self.attribute_exists(element, attribute):
			if element.attributes[attribute].value != "":
				value = element.attributes[attribute].value
		
		return value
		
	def get_child_tag_attribute(self, element, child_tag, attribute):
		return self.get_tag_attribute(element.getElementsByTagName(child_tag)[0], attribute)
		
	def get_child_tag_value(self, element, tag_name):
		return self.get_tag_value(element.getElementsByTagName(tag_name)[0])
		
	def get_tag_value(self, element):
		value = None
		while value == None:
			if self.getText(element.childNodes) != "":
				value = self.getText(element.childNodes)
			else:
				if len(element.childNodes) > 0:
					for el in element.childNodes:
						if element.getElementsByTagName(el.tagName)[0] != "":
							temp = element.getElementsByTagName(el.tagName)[0]
							self.get_tag_value(temp)
						element = el
				else:
					value = ""
		return value
		
	def format_description(self, description):
		value = None
		
		if description[:len("Description:")].lower() == "Description:".lower():
			value = description[len("Description:"):len(description)]
		else:
			value = description
			
		return value.lstrip()
		
	def get_channel_group_info(self, channel_group):
		info = [int(self.get_tag_attribute(channel_group, "id")),
			int(self.get_tag_attribute(channel_group, "type")),
			self.get_tag_translation(channel_group, Language.ENGLISH),
			self.get_tag_translation(channel_group, Language.CHINESE),
			self.get_tag_value(channel_group),
			self.format_description(self.get_tag_attribute(channel_group, "description"))]
		
		return info
		
	def get_channel_info(self, channel, channel_group_id):
		info = [int(self.get_tag_attribute(channel, "type")),
			int(self.get_tag_attribute(channel, "btype")),
			self.get_tag_attribute(channel, "language"),
			self.get_child_tag_translation(channel, "name", Language.ENGLISH),
			self.get_child_tag_translation(channel, "name", Language.CHINESE),
			self.get_child_tag_translation(channel, "name"),
			int(self.get_child_tag_value(channel, "status")),
			self.get_child_tag_translation(channel, "region", Language.ENGLISH),
			self.get_child_tag_translation(channel, "region", Language.CHINESE),
			self.get_child_tag_translation(channel, "region"),
			self.get_child_tag_translation(channel, "class", Language.ENGLISH),
			self.get_child_tag_translation(channel, "class", Language.CHINESE),
			int(self.get_child_tag_translation(channel, "class")),
			int(self.get_child_tag_value(channel, "user_count")),
			int(self.get_child_tag_value(channel, "sn")),
			int(self.get_child_tag_value(channel, "visit_count")),
			self.get_child_tag_value(channel, "start_from"),
			self.get_child_tag_value(channel, "stream_type"),
			int(self.get_child_tag_value(channel, "kbps")),
			int(self.get_child_tag_value(channel, "qs")),
			int(self.get_child_tag_value(channel, "qc")),
			self.get_child_tag_value(channel, "sop_address"),
			self.format_description(self.get_child_tag_translation(channel, "description", Language.CHINESE)),
			self.format_description(self.get_child_tag_value(channel, "description")),
			channel_group_id]
			
		return info

	def update_database(self, url):
		self.db_operations.truncate_channel_groups()
		self.db_operations.truncate_channels()
		
		f = open(url)
		doc = parse(f)
		f.close()

		for channel_group in doc.getElementsByTagName("group"):			
			channels = channel_group.getElementsByTagName("channel")			
			
			if len(channels) > 1:
				channel_group_info =  self.get_channel_group_info(channel_group)
				self.db_operations.insert_channel_group(channel_group_info)	
				for channel in channels:
					self.db_operations.insert_channel(self.get_channel_info(channel, channel_group_info[0]))
				channels = None
		channel_group = None
		
		self.db_operations.insert_channel_group([sys.maxint, 0, 'Other', 'Other', 'Other', 'Channel group to catch all un-categorized channels'])
		
		for channel_group in doc.getElementsByTagName("group"):	
			channels = channel_group.getElementsByTagName("channel")
			if len(channels) == 1:
				for channel in channels:
					self.db_operations.insert_channel(self.get_channel_info(channel, sys.maxint))
					
		self.db_operations.commit_channel_guide()
		doc = None
		
if __name__ == '__main__':
	i = ImportChannelGuide()
	i.update_database()
	
	while 1: i =1
