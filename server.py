#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2015 breakwall
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import time
import sys
import threading
import os

if __name__ == '__main__':
	import inspect
	os.chdir(os.path.dirname(os.path.realpath(inspect.getfile(inspect.currentframe()))))

import server_pool
import db_transfer
import speedtest_thread
import auto_thread
import auto_block
from shadowsocks import shell
from configloader import load_config, get_config

class MainThread(threading.Thread):
	def __init__(self, obj):
		threading.Thread.__init__(self)
		self.obj = obj

	def run(self):
		self.obj.thread_db(self.obj)

	def stop(self):
		self.obj.thread_db_stop()

def main():
	shell.check_python()
	if False:
		db_transfer.DbTransfer.thread_db()
	else:
		if get_config().API_INTERFACE == 'mudbjson':
			threadMain = MainThread(db_transfer.MuJsonTransfer)
		else:
			threadMain = MainThread(db_transfer.DbTransfer)
		threadMain.start()
		
		threadSpeedtest = threading.Thread(group = None, target = speedtest_thread.speedtest_thread, name = "speedtest", args = (), kwargs = {}) 
		threadSpeedtest.start()
		
		threadAutoexec = threading.Thread(group = None, target = auto_thread.auto_thread, name = "autoexec", args = (), kwargs = {})  
		threadAutoexec.start()
		
		threadAutoblock = threading.Thread(group = None, target = auto_block.auto_block_thread, name = "autoblock", args = (), kwargs = {})  
		threadAutoblock.start()
		
		try:
			while threadMain.is_alive():
				time.sleep(10)
		except (KeyboardInterrupt, IOError, OSError) as e:
			import traceback
			traceback.print_exc()
			threadMain.stop()

if __name__ == '__main__':
	main()

