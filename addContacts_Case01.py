

# Case01 - Pressure Test Case , add AddContactsNum contacts #
#     preconditions:  Phone already has at least one contact #

# Verison         : 0.1
# Date            : 2013.06.07
# Author          : Robin Zhang <askpepsi88@gmail.com>
# Description     : create addContact_Case01 case , it's for add contacts pressure test.

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
import datetime


AddContactsNum = 5
CaseResultCount = 0


# connecting device #
try:
    print str(datetime.datetime.now())+"  "+"connecting device"
    device = MonkeyRunner.waitForConnection(10.0)
    print str(datetime.datetime.now())+"  "+"connecting success"
except:
    print str(datetime.datetime.now())+"  "+"connecting fail, please check and run script again"
    pass


# start People activity #
device.wake()
device.press('KEYCODE_HOME','DOWN_AND_UP')
MonkeyRunner.sleep(2)
device.startActivity(component = 'com.android.contacts/.activities.PeopleActivity')
MonkeyRunner.sleep(5)


# add contact #
for i in range(AddContactsNum):
    try:
        # shot Ref Image and save #
        print str(datetime.datetime.now())+"  "+"shot RefImage"
        refImage = device.takeSnapshot().getSubImage((339,126,93,25))
        refImage.writeToFile('./RefImage.png','png')
        print str(datetime.datetime.now())+"  "+"RefImage save success"
        MonkeyRunner.sleep(2)
        
        # add contact stpes #
        print str(datetime.datetime.now())+"  "+"add contact"+str(i)+" start"
        device.touch(430,760,'DOWN_AND_UP')
        MonkeyRunner.sleep(3)
        device.type('test0'+str(i))
        device.touch(50,410,'DOWN_AND_UP')
        device.type('00'+str(i))
        MonkeyRunner.sleep(3)
        device.touch(76,74,'DOWN_AND_UP')
        MonkeyRunner.sleep(5)
        device.press('KEYCODE_BACK','DOWN_AND_UP')
        print str(datetime.datetime.now())+"  "+"add contact"+str(i)+" end"
        MonkeyRunner.sleep(5)

        # shot Cmp Image and save #
        print str(datetime.datetime.now())+"  "+"shot cmpImage"
        cmpImage = device.takeSnapshot().getSubImage((339,126,93,25))
        cmpImage.writeToFile('./CmpImage.png','png')
        print str(datetime.datetime.now())+"  "+"cmpImage save success"
        MonkeyRunner.sleep(2)
        
        # judge this round pass or fail #
        if not cmpImage.sameAs(refImage):
            print str(datetime.datetime.now())+"  "+"add success"
            CaseResultCount += 1
        else:
            print str(datetime.datetime.now())+"  "+"add fail , case stop"
            break
        
        print str(datetime.datetime.now())+"  "+"round"+str(i)+" over"
        print "*******************************************************"
        MonkeyRunner.sleep(3)           
            
    except:
        print "Exception detected , action of this round is wrong"
        print "Kill contacts and restart"
        device.shell("am force-stop com.android.contacts")
        MonkeyRunner.sleep(3)
        device.startActivity(component = 'com.android.contacts/.activities.PeopleActivity')
        MonkeyRunner.sleep(5)


# judge Case01 pass or not #        
if CaseResultCount== AddContactsNum:
    print str(datetime.datetime.now())+"  "+"Case01 PASS!"
    device.shell("am force-stop com.android.contacts")
else:
    print str(datetime.datetime.now())+"  "+"Case01 FAIL!"
    device.shell("am force-stop com.android.contacts")



