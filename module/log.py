# -*- coding: utf-8 -*-

#Author: Jason Hou
#Date: 2013/06/07

'''trace log handle library
This module is an trace log handle library that:
	- output the trace log info with time stamp
'''

__version__ = '0.2'
__all__ = ['trace']

from datetime import datetime

class trace:
	
	''' the clase is used to output the tracelog info '''	
	
	def __init__(self,logFile,verbose=True,echo=True):
		'''
		logFile:	 specify the logFile with full path;
		verbose:	 if False, output less time detail(without date);
		echo:		 if False, trace info won't display in command line.
		'''
		self.logFile=logFile
		self.verbose=verbose
		self.echo=echo
	
	def timestamp(self,verbose):
		'''return the current timestamp string'''
		if not self.verbose:
			return str(datetime.now())[-15:-3]
		else:
			return str(datetime.now())[:-3]

	def trace(self,str):
		'''add str as log info to logfile'''
		logInfo=(self.timestamp(self.verbose) + '\t' + str + '\n')
		if self.echo:
			print logInfo
		f=open(self.logFile,'a+')
		try:
			f.write(logInfo)
		except:
			print "file I/O error"
		finally:
			f.close()

if __name__ == 	'__main__':
	t=trace('main_test.txt',False,True)
	t.trace('*' * 40)
	t.trace('start' + '\t' + t.timestamp(1))
	t.trace('this is a test')
	t.trace('end' + '\t' + t.timestamp(1))
	t.trace('*' * 40)