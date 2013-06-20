# -*- coding: utf-8 -*-

#Author: Jason Hou
#Date: 2013/06/18

############################ CHANGE HISTORY ############################

# VERSION : 0.2 Second Release 18-Jun-13 Jason Hou
# REASON : Update implementation
# REFERENCE : 
# DESCRIPTION : 1. add change history and function document string
#				2. update getView(), isReady() method
#				3. update the isEmpty() to goEdit() to avoid the misunderstanding
#				4. new add back, check method

# VERSION : 0.1 First Release 16-Jun-13 Jason Hou
# REASON : First implementation
# REFERENCE : 
# DESCRIPTION : 1. Create the basic contacts module framework
#				2. encapsulate the findView method using method getView()

############################ CHANGE HISTORY ############################

__version__ = '0.2'

import os,sys
try:
    for p in os.environ['PYTHONPATH'].split(';'):
       if not p in sys.path:
          sys.path.append(p)
except:
    pass

from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice,MonkeyImage
from com.dtmilano.android.viewclient import ViewClient,View
from log import trace

logPath = r'D:\Android\test_log'
logName = 'case_log.txt'
logFile = logPath + '\\' + logName

trace = trace(logFile).trace

package = 'com.android.contacts'
activity = '.activities.PeopleActivity'
componentName = package + '/' + activity
	
def sleep(duration = 1):
	'''
	Monkey sleep
	
	@type duration: int
	@param duration: how long to sleep
	'''
	MonkeyRunner.sleep(duration)
	
class contacts:
	'''
	contacts class
	'''
	def __init__(self, device, devID='emulator-5554',sample = False):
		'''
		constructor
		
		@type device: MonkeyDevice
        @param device: The device or emulator connected
		@type devID: str
        @param serialno: the serial number of the device or emulator to connect to
		@type sample: boolean
		@param sample: whether take snapshot as an sampling
		'''
		self.device=device
		self.sample=sample
		self.startStatus=False
		'''the status which indicate whether the contacts activity is started'''
		self.vc=ViewClient(device, devID)
		#use below code to remove the status bar from the snapshot
		width = int(device.getProperty('display.width'))
		height = int(device.getProperty('display.height'))
		density = device.getProperty('display.density')
		if density == .75:
			statusBarHeight = 19
		elif density == 1.5:
			statusBarHeight = 38
		elif density == 2.0:
			statusBarHeight = 50
		else:
			statusBarHeight = 25
		self.snap_rect = 0, statusBarHeight, width, height - statusBarHeight

	def start(self):
		'''
		start the contacts activity and set the startStatus True if contacts is ready.
		'''
		self.device.startActivity(component=componentName)
		sleep(3)
		self.startStatus = self.isReady()
	def back(self):
		'''
		press back
		'''
		self.device.press('KEYCODE_BACK','DOWN_AND_UP')
	def getView(self,str,cD=False,iD=False):
		'''
		get the view with the specified text, content description or viewId
		@type str: str
		@param str: the query string
		@type cD: boolean
		@param cD: whether handle the query str as content description
		@type iD: boolean
		@param iD: whether handle the query str as viewId
		
		@return: the view found
		'''
		self.vc.dump()
		sleep(3)
		if not cD:
			if not iD:
				return self.vc.findViewWithText(str)
			else:
				return self.vc.findViewById(str)
		else:
			return self.vc.findViewWithContentDescription(str)
			
	def isReady(self):
		'''
		check whether the contacts is ready.
		'''
		while True:
			view=self.getView('Contact list is being updated to reflect the change of language.')
			if not view:
				trace('Contacts is ready')
				break
			else:
				trace('Contacts is not ready, please wait!')
				sleep(2)
		return True
	
	def goEdit(self):
		'''
		check whether the contact is empty, then select adding and go to edit view.
		
		@return: True
		'''
		self.check()
		view=self.getView('Create a new contact')
		if view:
			view.touch()
			trace('Click "Create a new contact"')
			view=self.getView('Keep local')
			if view:
				view.touch()
				trace('Select "Keep local"')
		else:
			view=self.getView('Add Contact',True)
			view.touch()
			trace('Click "Add Contact"')
		return True
		
	def check(self):
		'''
		check whether the contacts is started before other operation about contacts
		
		@return: True
		'''
		if not self.startStatus:
			trace("Wrong code! please start contacts firstly in you code")
			raise SyntaxError('contacts should be start firstly!')
		return True
		
	def snapshot(self,title):
		'''
		take snapshot
		@type title: str
		@param title: specify the title of snapshot
		'''
		snapName = title + '.png' 
		snapFile = logPath + '\\' + snapName
		result = self.device.takeSnapshot().getSubImage(self.snap_rect)
		result.writeToFile(snapFile,'png')
	
	def addContact(self,name='',phone='',email=''):
		#notice firstly call self.goEdit()
		pass
				
	def editDetails(self,name='',phone='',email='',notes='',address='',nickname=''):
		'''
		edit contact details
		'''	
		self.check()
		view = self.getView('id/no_id/27',iD=True)
		view.touch()
		sleep(4)
		trace('enter contact OK')
		
		self.device.press('KEYCODE_MENU','DOWN_AND_UP')
		view = self.getView('Edit')
		view.touch()
		sleep(3)
		trace('enter contact edit view OK')
		
		if not name=='':
			self.editName(name)
				
		if not phone=='':
			if self.getDetails('Phone'):
				self.editPhone(phone)
			else:
				self.editPhone(phone,add=True)
	
		self.back()
		sleep(3)
		self.back()
	
	def getDetails(self,getItem):
		if self.getView(getItem):
			return True
		else:
			self.device.drag((240,750),(240,50),5.0)
			sleep(1)
			if self.getView(getItem):
				return True
			else:
				return False
	
	def editName(self,name):
		trace("edit contact's name")
		self.check()
		
		#find EditText of Name
		view = self.getView('id/no_id/27',iD=True)
		
		#edit name
		self.device.drag(view.getXY(),view.getXY(),3.0)
		self.device.press('KEYCODE_DEL','DOWN_AND_UP')
		view.type(name)
		sleep(1)
		trace("edit contact's name OK")

	def editPhone(self,phone,add=False):
		trace("edit contact's phone")
		self.check()
		
		if not add:
			trace('edit phone with no add')
			
			#find EditText of Phone
			view = self.getView('Phone')
			editId = 'id/no_id/'+str(int((view.getId())[-2:])+6)
			view = self.getView(editId,iD=True)
			
			#edit phone number
			self.device.drag(view.getXY(),view.getXY(),3.0)
			self.device.press('KEYCODE_DEL','DOWN_AND_UP')
			view.type(phone)
			sleep(1)
			trace('edit phone with no add OK')
			
		else:
			trace('edit phone with add')
			
			#touch 'Add another field'
			view = self.getView('Add another field')
			view.touch()
			sleep(3)
			
			#touch 'Phone' and edit 
			view = self.getView('Phone')
			view.touch()
			sleep(2)
			self.device.type(phone)
			sleep(1)
			trace('edit phone with add OK')
			
	def editEmail(self,email):
		pass
	
	def search(self,str):
		pass
	
	def sort(self):
		pass
		
	def favorite(self,name=''):
		pass
		
if __name__ == '__main__':
	device=MonkeyRunner.waitForConnection()
	trace('start testing...')
	c=contacts(device)
	c.start()
	#c.addContact(name='jason',phone='123')
	c.editDetails(name='test',phone='123456')
	#c.search('jason')
	#c.sort()
	#c.favorite('jason')
	trace('end testing')