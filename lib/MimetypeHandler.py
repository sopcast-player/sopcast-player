#!/usr/bin/python

import os

class WriteHandler:
	def write(self):
		homedir = os.path.expanduser('~')
		handler_dir = homedir + "/.local/share/applications"
		handler_file = "/sopcast-player.desktop"
		mimeapps_file = "/mimeapps.list"

		handler_file_contents = [
			"[Desktop Entry]\n",
			"Name=SopCast Player\n",
			"Exec=sopcast-player %u\n",
			"Icon=sopcast-player\n",
			"Type=Application\n",
			"Terminal=false\n",
			"Categories=GNOME;AudioVideo;P2P;Video;TV;GTK;\n",
			"MimeType=x-scheme-handler/sop;\n" ]

		mimeapps_file_contents = [
			"[Added Associations]\n",
			"x-scheme-handler/sop=sopcast-player.desktop;\n" ]


		#Check if user's local/share/application path exists
		if not os.path.exists(handler_dir):
			os.makedirs(handler_dir)
	
		#Check if sopcast-player.desktop exists
		try:
			FILE = open(handler_dir + handler_file, "r")	
		except IOError as e:
			FILE = open(handler_dir + handler_file, "w")
			FILE.writelines(handler_file_contents)
		finally:
			FILE.close()
	
		#Check if mimeapps.list exists
		try:
			FILE = open(handler_dir + mimeapps_file, "r")	
		except IOError as e:
			FILE = open(handler_dir + mimeapps_file, "w")
			FILE.writelines(mimeapps_file_contents)
		finally:
			FILE.close()
	
		#Make sure handler is in file, else write it
		FILE = open(handler_dir + mimeapps_file, "rw")
		lines = FILE.readlines()
		FILE.close()

		found = False

		for line in lines:
			if "x-scheme-handler/sop=sopcast-player.desktop;" in line:
				found = True
		
		i = 0

		if not found:
			#handler not found, try to find
			for line in lines:
				i += 1
				if "[Added Associations]" in line:
					found = True
					break
	
			if found:
				current_line = 0
				FILE = open(handler_dir + mimeapps_file, "w")
		
				for line in lines:
					current_line += 1
			
					if current_line == i + 1:
						FILE.write(mimeapps_file_contents[1])
				
					FILE.write(line)
			
				FILE.close()
			else:
				#section not found
				FILE = open(handler_dir + mimeapps_file, "w")
				FILE.writelines(lines)
				FILE.write("\n")
				FILE.writelines(mimeapps_file_contents)
				FILE.close()
				
if __name__ == "__main__":
	handler = WriteHandler()
	handler.write()
