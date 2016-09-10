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
import sqlite3

class DatabaseOperations(object):
	def __init__(self):
		create_tables = False
		if os.path.isdir(os.path.expanduser(r'~/.pySopCast/')) == False:
			os.mkdir(os.path.expanduser('~/.pySopCast/'))
			
		if os.path.exists(os.path.expanduser(r'~/.pySopCast/pySopCast.db')) == False:
			create_tables = True
			

		if create_tables == True:
			conn = self.db_connect()
			cursor = conn.cursor()		
			cursor.execute('CREATE TABLE bookmarks (id INTEGER PRIMARY KEY, channel_name VARCHAR(100), channel_url VARCHAR(255))')
			cursor.execute('CREATE TABLE channel_groups (id INTEGER PRIMARY KEY, type INT, en_name VARCHAR(255), cn_name VARCHAR(255), ' \
				'name VARCHAR(255), description VARCHAR(1024))')
			cursor.execute('CREATE TABLE channels (id INTEGER PRIMARY KEY, type INTEGER, btype INTEGER, language VARCHAR(255), ' \
				'en_name VARCHAR(255), cn_name VARCHAR(255), name VARCHAR(255), status INTEGER, region_en VARCHAR(255), ' \
				'region_cn VARCHAR(255), region VARCHAR(255), class_en VARCHAR(255), class_cn VARCHAR(255), class INTEGER, ' \
				'user_count INTEGER, sn INTEGER, visit_count INTEGER, start_from VARCHAR(255), stream_type VARCHAR(255), ' \
				'kbps INTEGER, qs INTEGER, qc INTEGER, sop_address VARCHAR(255), cn_description VARCHAR(1024), ' \
				'description VARCHAR(1024), channel_group_id INTEGER)')
			
			conn.commit()	
			conn.close()
			
		self.conn = None
		self.cursor = None
			
	def db_connect(self):			
		return sqlite3.connect(os.path.expanduser('~/.pySopCast/pySopCast.db'))
			
	def insert_bookmark(self, channel_name, channel_url):
		conn = self.db_connect()
		row = (channel_name, channel_url)
		cursor = conn.cursor()
		cursor.execute('INSERT INTO bookmarks VALUES (null, ?, ?)', row)
		conn.commit()
		conn.close()
		
	def insert_channel_group(self, row):
		if not self.conn:
			self.conn = self.db_connect()
			self.cursor = self.conn.cursor()
			
		self.cursor.execute('INSERT INTO channel_groups VALUES (?, ?, ?, ?, ?, ?)', row)
	
	def commit_channel_guide(self):
		self.cursor.execute('VACUUM')
		self.conn.commit()
		self.conn.close()
		self.conn = None
		self.cursor = None

		
	def insert_channel(self, row):
		if not self.conn:
			self.conn = self.db_connect()
			self.cursor = self.conn.cursor()
		
		self.cursor.execute('INSERT INTO channels VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)
		
	def truncate_channels(self):
		if not self.conn:
			self.conn = self.db_connect()
			self.cursor = self.conn.cursor()
			
		self.cursor.execute('DELETE FROM channels')
		
	def retrieve_other_channel_group_id(self):
		conn = self.db_connect()
		cursor = conn.cursor()
		cursor.execute("SELECT id FROM channel_groups WHERE name='Other'")
		data = cursor.fetchall()
		conn.close()
		return data
		
	def truncate_channel_groups(self):
		if not self.conn:
			self.conn = self.db_connect()
			self.cursor = self.conn.cursor()
		self.cursor.execute('DELETE FROM channel_groups')
		
	def retrieve_bookmark_by_channel_name(self, channel_name):
		conn = self.db_connect()
		cursor = conn.cursor()
		row = [channel_name.lower()]
		cursor.execute("SELECT * FROM bookmarks WHERE lower(channel_name)=?", row)
		data = cursor.fetchall()
		conn.close()
		return data
		
	def retrieve_bookmark_by_address(self, sop_address):
		conn = self.db_connect()
		cursor = conn.cursor()
		row = [sop_address.lower()]
		cursor.execute("SELECT channel_name FROM bookmarks WHERE lower(channel_url)=?", row)
		data = cursor.fetchall()
		conn.close()
		return data
		
	def retrieve_channel_guide_record_by_address(self, sop_address):
		conn = self.db_connect()
		cursor = conn.cursor()
		row = [sop_address.lower()]
		cursor.execute("SELECT en_name, cn_name, name FROM channels WHERE lower(sop_address)=?", row)
		data = cursor.fetchall()
		conn.close()
		return data
		
	def retrieve_channel_guide_record_by_channel_name(self, channel_name):
		conn = self.db_connect()
		cursor = conn.cursor()
		row = [channel_name.lower()]
		cursor.execute("SELECT sop_address FROM channels WHERE lower(en_name)=?", row)
		data = cursor.fetchall()
		conn.close()
		return data
		
	def retrieve_channels_by_channel_group_id(self, channel_group_id):
		conn = self.db_connect()
		cursor = conn.cursor()
		row = [channel_group_id]
		cursor.execute("SELECT id, en_name, description, region, class_en, stream_type, kbps, qs, qc, sop_address FROM channels WHERE channel_group_id=?", row)
		data = cursor.fetchall()
		conn.close()
		return data
		
	def retrieve_channels_by_channel_group_id_cn(self, channel_group_id):
		conn = self.db_connect()
		cursor = conn.cursor()
		row = [channel_group_id]
		cursor.execute("SELECT id, cn_name, cn_description, region_cn, class_cn, stream_type, kbps, qs, qc, sop_address FROM channels WHERE channel_group_id=?", row)
		data = cursor.fetchall()
		conn.close()
		return data
		
	def retrieve_channel_groups(self):
		conn = self.db_connect()
		cursor = conn.cursor()
		cursor.execute("SELECT id, en_name, description FROM channel_groups")
		data = cursor.fetchall()
		conn.close()
		return data
		
	def retrieve_channel_groups_cn(self):
		conn = self.db_connect()
		cursor = conn.cursor()
		cursor.execute("SELECT id, cn_name, description FROM channel_groups")
		data = cursor.fetchall()
		conn.close()
		return data
		
	def retrieve_bookmarks(self):
		conn = self.db_connect()
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM bookmarks')
		data = cursor.fetchall()
		conn.close()
		return data
		
	def delete_bookmark(self, row_id):
		conn = self.db_connect()
		cursor = conn.cursor()
		row = (row_id)
		cursor.execute("DELETE FROM bookmarks WHERE id=%s" % row_id)
		conn.commit()
		conn.close()
		
	def update_bookmark(self, bookmark_name, bookmark_url, bookmark_id):
		conn = self.db_connect()
		cursor = conn.cursor()
		row = (bookmark_name, bookmark_url, bookmark_id)
		cursor.execute('UPDATE bookmarks SET bookmark_name=?, bookmark_url=? WHERE id=?', row)
		conn.commit()
		conn.close()
