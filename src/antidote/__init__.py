#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# gedit-antidote/__init__.py
# Copyright (C) 2013  Stephane Galland <galland@arakhne.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

#---------------------------------
# IMPORTS
#---------------------------------

# Import standard python libs
import os
import gettext
import time
# Dbus
import dbus
# Include the Glib, Gtk and Gedit libraries
from gi.repository import GObject, Gtk, Gedit, GdkPixbuf, PeasGtk
# plugin's libs
from .utils import runner

#---------------------------------
# INTERNATIONALIZATION
#---------------------------------

gettext.textdomain('gedit-antidote')
_T = gettext.gettext

#---------------------------------
# Static Methods
#---------------------------------

# Load an icon from the plugin directory
def get_plugin_icon(icon_name):
	return GdkPixbuf.Pixbuf.new_from_file(
		os.path.join(
			os.path.dirname(__file__),
			'icons', '24', icon_name+'.png'))

# Replies if the active document is a TeX document
def is_TeX_document(document):
	if document:
		language = document.get_language()
		if language and language.get_id()=='latex':
			return True
	return False

#---------------------------------
# CLASS AntidotePlugin
#---------------------------------

class AntidotePlugin(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
	__gtype_name__ = "AntidotePlugin"
	window = GObject.property(type=Gedit.Window)

	# Constructor
	def __init__(self):
		GObject.Object.__init__(self)
		self._antidote_icon = None # Icon of Antidote

	# Invoked when the configuration window is open
	def do_create_configure_widget(self):
		return Gtk.Label("Test")

	# Invoked when the plugin is activated 
	def do_activate(self):
		self._antidote_icon = get_plugin_icon('antidote')
		self._add_ui()

	# Invoke when the plugin is desactivated
	def do_deactivate(self):
		runner.kill_all_runners()
		self._remove_ui()

	# Invoke when the UI is updated
	def do_update_state(self):
		document = self.window.get_active_document()
		self._antidote_action_group.set_sensitive(document is not None)

	# Add any contribution to the Gtk UI
	def _add_ui(self):
		# Get the UI manager
		manager = self.window.get_ui_manager()
		# Create the actions
		self._antidote_action_group = Gtk.ActionGroup("AntidoteActionGroup")
		self._antidote_action_group.add_actions([
			('AntidoteLaunch',
			None, 
			_T("Grammar and spell checking with Antidote..."), 
			None, _T("Launch Antidote for grammar and spell checking."), 
			self._on_launch_antidote),
			])
		manager.insert_action_group(self._antidote_action_group)
		# Link the icons
		self._antidote_action_group.get_action('AntidoteLaunch').set_gicon(self._antidote_icon)
		# Add the uis
		ui_path = os.path.join(os.path.dirname(__file__), 'ui')
		self._ui_merge_ids = []
		for ui_file in [ 'menu.ui', 'toolbar.ui' ]:
			ui_file = os.path.join(ui_path, ui_file)
			self._ui_merge_ids.append(manager.add_ui_from_file(ui_file))
		manager.ensure_update()

	# Remove the contribution to the Gtk UI
	def _remove_ui(self):
		# Remove the Gtk Widgets
		manager = self.window.get_ui_manager()
		manager.remove_action_group(self._antidote_action_group)
		for merge_id in self._ui_merge_ids:
			manager.remove_ui(merge_id)
		manager.ensure_update()

	# Invoked when the user want to launch Antidote
	def _on_launch_antidote(self, action, data=None):
		document = self.window.get_active_document()
		if document:
			if document.is_untouched():
				print "Saving"
				is_untitled = document.is_untitled()
				is_deleted = document.get_deleted()
				is_readonly = document.get_readonly()
				if not is_untitled and not is_deleted and not is_readonly :
					document.save(Gedit.DocumentSaveFlags.IGNORE_MTIME)
			if is_TeX_document(document):
				self._launch_antidote_on_document(document)
			else:
				self._launch_antidote_on_document(document)

	# Launch Antidote
	def _launch_antidote_on_document(self, document):
		assert document

		start_iter = document.get_start_iter()
		end_iter = document.get_end_iter()
		text = document.get_text(start_iter, end_iter, False)
		text = "Hello."

		dbus_session = dbus.SessionBus()

		if not dbus_session.name_has_owner('com.druide.antidote.a7.agentantidote.v1'):
			# Launch the agent from inside Gedit
			thread = runner.Runner()
			thread.start()

			# Wait for the launching
			end_time = time.time() + 10
			while not dbus_session.name_has_owner('com.druide.antidote.a7.agentantidote.v1') and time.time()<=end_time:
				time.sleep( 0.0001 )

			# Test if the agent was launched
			if not dbus_session.name_has_owner('com.druide.antidote.a7.agentantidote.v1'):
				dialog = Gtk.MessageDialog(self.window, Gtk.DialogFlags.MODAL, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, _T("Cannot launch the Antidote agent"))
				answer = dialog.run()
				dialog.destroy()
				return

		antidote = dbus_session.get_object(
			'com.druide.antidote.a7.agentantidote.v1',
			'/com/druide/antidote/a7/agentantidote/v1')
		v = antidote.AntidoteEnFermeture()
		#v = antidote.EnregistreCorrectionDuTexteur("theid", text)
		#v = antidote.DonneSiCourrielEstTraitee(text)
		#v = antidote.EnregistreCourrielTraitee(text)
		print v

