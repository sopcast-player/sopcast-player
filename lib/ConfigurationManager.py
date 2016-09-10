# ConfigurationManager eases the use of ConfigParser
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

import ConfigParser

class ConfigurationManager(object):
	def __init__(self, file_name):
		self.__file_name = file_name
		self.__sections = { }
	
	def add_section(self, section_name, section):
		self.__sections[section_name] = section
	
	def read(self):
		config = ConfigParser.RawConfigParser()
		config.read(self.__file_name)
		
		for section_name, attributes in self.__sections.iteritems():
			for attribute_name, attribute_value in attributes.iteritems():
				if config.has_section(section_name) == True:
					if config.has_option(section_name, attribute_name):
						attributes[attribute_name] = config.get(section_name, attribute_name)
		
	def write(self):
		config = ConfigParser.RawConfigParser()
		
		for section_name, attributes in self.__sections.iteritems():
			config.add_section(section_name)
			for attribute_name, attribute_value in attributes.iteritems():
				config.set(section_name, attribute_name, str(attribute_value))
			
		configfile = open(self.__file_name, 'wb')
		config.write(configfile)
		
	def set(self, section, attribute, value):
		#print value
		self.__retrieve_attribute(section, attribute, value)
		
	def get(self, section, attribute):
		return self.__retrieve_attribute(section, attribute)
		
	def getint(self, section, attribute):
		return int(self.get(section, attribute))
	
	def getfloat(self, section, attribute):
		return float(self.get(section, attribute))
		
	def getboolean(self, section, attribute):
		return self.__parse_bool(self.get(section, attribute))
		
	def update_configuration_definitions(self):
		self.write()
		
	def __retrieve_attribute(self, section, attribute, value=None):
		config = ConfigParser.SafeConfigParser()
		config.read(self.__file_name)
		
		r_section_name, r_section = self.__retrieve_section(section)
		
		for attribute_name, attribute_value in r_section.iteritems():
			if attribute_name == attribute:
				ret_val = attribute_value
				break
				
		if value != None:
			if ret_val != None:
				r_section[attribute_name] = str(value)
						
		if ret_val != None:
			return ret_val
		else:
			raise ConfigParser.NoOptionError
			
	def __retrieve_section(self, section):
		found = False
		
		for section_name, section_dict in self.__sections.iteritems():
			if section_name == section:
				found = True
				break
		
		if found == True:
			return section_name, section_dict
		else:
			raise ConfigParser.NoSectionError
			
	def __parse_bool(self, s):
		return not s in [False, 'False', 'false', 'f', 'n', '0', '']

