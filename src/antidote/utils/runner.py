#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# gedit-antidote/utils/runner.py
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

import os
import subprocess

# Try to use the threading library if it is available
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

# List of all the runners
_all_runners = []

def kill_all_runners():
	global _all_runners
	tab = _all_runners
	_all_runners = []
	for r in tab:
		r.cancel()

# Launch AutoLaTeX inside a thread, and wait for the result
class Runner(_threading.Thread):

	def __init__(self):
		_threading.Thread.__init__(self)
		self.daemon = True
		self._cmd = [ 'AgentAntidote' ]
		self._subprocess = None

	# Cancel the execution
	def cancel(self):
		if self._subprocess:
			self._subprocess.terminate()
			self._subprocess = None

	# Run the thread
	def run(self):
		global _all_runners
		_all_runners.append(self)
		os.chdir(os.path.expanduser('~'))
		self._subprocess = subprocess.Popen(self._cmd)
		if not self._subprocess and self in _all_runners:
			_all_runners.remove(self)

