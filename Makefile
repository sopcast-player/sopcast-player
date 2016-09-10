#!/usr/bin/make -f

#! /usr/bin/python
# Copyright (C) 2009-2012 Jason Scheunemann <jason.scheunemann@yahoo.com>.
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

NAME ?= sopcast-player
PREFIX ?= /usr
DATADIR ?= $(PREFIX)/share
INSTALLDIR ?= $(DATADIR)/$(NAME)
BINDIR ?= $(PREFIX)/bin
EXECUTABLE ?= $(BINDIR)/$(NAME)
LOCALE ?= locale
LOCALEDIR ?= $(DATADIR)/$(LOCALE)
ICONBASEDIR ?= $(DATADIR)/icons/hicolor
ICONDIR ?= $(ICONBASEDIR)/scalable/apps
DESKDIR ?= $(DATADIR)/applications
INSTALL ?= install -p
#GCONF_TOOL_EXEC ?= gconftool-2
EDIT ?= sed -e 's|@DATADIR@|$(DATADIR)|g' \
	    -e 's|@NAME@|$(NAME)|g' \
	    -e 's|@PYTHON@|$(PYTHON)|g' \
	    -e 's|@INSTALLDIR@|$(INSTALLDIR)|g' \
	    -e 's|@ICONDIR@|$(ICONDIR)|g' \
	    -e 's|@DESTDIR@|$(DESTDIR)|g' \
	    -e 's|@EXECUTABLE@|$(EXECUTABLE)|g'
PYTHON ?= /usr/bin/python
CFLAGS ?= -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions \
          -fstack-protector --param=ssp-buffer-size=4
VLC_BINDINGS_DIR ?= pyvlc_bindings
VLC_BINDINGS_GENERATE_DIR ?= $(VLC_BINDINGS_DIR)/generated
VERSION ?= 0.8.5

gtk_update_icon_cache = gtk-update-icon-cache -f -t $(ICONBASEDIR)

build: language desktop schema byte-compile
	
desktop:
	#@if test -z "$(DESTDIR)"; then \
	#	sed -e 's|@PYTHON@|$(PYTHON)|g' -e 's|@DIR@|$(INSTALLDIR)|g' -e 's|@NAME@|$(NAME)|g' $(NAME).in > $(NAME); \
	#else \
	#	sed -e 's|@PYTHON@|$(PYTHON)|g' -e 's|@DIR@|$(DESTDIR)/$(NAME)|g' -e 's|@NAME@|$(NAME)|g' $(NAME).in > $(NAME); \
	#fi
	$(EDIT) $(NAME).in > $(NAME)

schema:
	$(EDIT) $(NAME).schemas.in > $(NAME).schemas

byte-compile:
	$(PYTHON) -c 'import compileall, re; compileall.compile_dir("lib", rx=re.compile("/[.]svn"), force=1)'

language:
	@echo "Generating language files..."
	@for trln in po/*.po; do \
	   lang=`basename $${trln%.*}`; \
	   mkdir -p $(LOCALE)/$$lang/LC_MESSAGES/; \
	   msgfmt $$trln -o $(LOCALE)/$$lang/LC_MESSAGES/$(NAME).mo; \
	done

clean:
	@for file in .pyc .py~ .so .mo .o; do \
	   echo "cleaning $$file files..." ; \
	   find . -name "*$$file" | xargs rm -f -- ; \
	done
	rm -fr $(LOCALE) || :
	rm -f $(NAME) || :
	
	rm -rf sopcast-player.schemas
	
install:
	@if [ $(PREFIX) != "/usr" ]; then \
		$(EDIT) $(NAME).in > $(NAME); \
	fi
	
	#@if test -z "$(DESTDIR)"; then \
	#	sed -e 's|@PYTHON@|$(PYTHON)|g' -e 's|@DIR@|$(DESTDIR)/$(NAME)|g' -e 's|@NAME@|$(NAME)|g' $(NAME).in > $(NAME); \
	#fi
	
	$(INSTALL) -dm 0755 $(DESTDIR)$(INSTALLDIR)/resources
	$(INSTALL) -dm 0755 $(DESTDIR)$(INSTALLDIR)/lib
	$(INSTALL) -dm 0755 $(DESTDIR)$(INSTALLDIR)/ui
	$(INSTALL) -dm 0755 $(DESTDIR)$(BINDIR)
	$(INSTALL) -dm 0755 $(DESTDIR)$(LOCALEDIR)
	$(INSTALL) -dm 0755 $(DESTDIR)$(ICONDIR)
	$(INSTALL) -dm 0755 $(DESTDIR)$(DESKDIR)
	$(INSTALL) -m 0644 lib/* $(DESTDIR)$(INSTALLDIR)/lib
	$(INSTALL) -m 0644 ui/* $(DESTDIR)$(INSTALLDIR)/ui
	$(INSTALL) -m 0644 $(NAME).schemas $(DESTDIR)$(INSTALLDIR)/resources
	$(INSTALL) -m 0755 $(NAME) $(DESTDIR)$(BINDIR)
	@for trln in $(LOCALE)/* ; do \
	   lang=`basename $$trln` ; \
	   $(INSTALL) -dm 0755 $(DESTDIR)$(LOCALEDIR)/$$lang/LC_MESSAGES ; \
	   $(INSTALL) -m 0644 $(LOCALE)/$$lang/LC_MESSAGES/* $(DESTDIR)$(LOCALEDIR)/$$lang/LC_MESSAGES ; \
	done
	$(INSTALL) -m 0644 $(NAME).desktop $(DESTDIR)$(DESKDIR)
	$(INSTALL) -m 0644 $(NAME).svg $(DESTDIR)$(ICONDIR)
	#$(GCONF_TOOL_EXEC) --install-file=$(DESTDIR)$(INSTALLDIR)/resources/$(NAME).schemas
	if test -z "$(DESTDIR)"; then \
		echo "Updating GTK icon cache."; \
		$(gtk_update_icon_cache); \
	else \
		echo "*** Icon cache not updated.  After install, run this:"; \
		echo "***   $(gtk_update_icon_cache)"; \
	fi

uninstall:
	rm -fr $(DESTDIR)$(INSTALLDIR)
	rm $(DESTDIR)$(BINDIR)/$(NAME)
	rm $(DESTDIR)$(LOCALEDIR)/*/LC_MESSAGES/$(NAME).mo
	rm $(DESTDIR)$(DESKDIR)/$(NAME).desktop
	rm $(DESTDIR)$(ICONDIR)/$(NAME).svg
