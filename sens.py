#
# dump micro:bit pitch and role through bluetool
#
# Usages> python3 sens.py
#

from bluepy.btle import Peripheral
import bluepy.btle as btle
import binascii
import struct
from time import sleep

HANDLE_BUTTON_A = 0x003a
HANDLE_BUTTON_B = 0x003d
HANDLE_ACCELE   = 0x0027

devadr     = "e4:1e:1f:1f:f4:49"

exflag = False

class MyDelegate(btle.DefaultDelegate):
  def __init__(self, params):
    btle.DefaultDelegate.__init__(self)

  def handleNotification(self, cHandle, data):
    global exflag
    c_data = binascii.b2a_hex(data)

    if cHandle == 0x27 :
      accX = struct.unpack('h', data[0:2] )[0]
      accY = struct.unpack('h', data[2:4] )[0]
      accZ = struct.unpack('h', data[4:6] )[0]
      strX = "Flat"
      strY = "Flat"
      if accX > 700  : strX = "Plus"
      if accX < -700 : strX = "Minus"
      if accY > 700  : strY = "Plus"
      if accY < -700 : strY = "Minus"
      
      #print("%s: %d, %d, %d : %s %s" %(c_data, accX, accY, accZ, strX, strY))
      print("pitch = %s : role = %s" %(accY, accX))
      return

    b = ""
    if cHandle == 0x3a : #left button
      b = "button1"
      if data[0] == 0x02 : exflag = True

    if cHandle == 0x3d : #right button
      b = "button2"
      if data[0] == 0x02 : exflag = True

    print("%s %X: %s" %(b, cHandle, c_data))


class MyPeripheral(Peripheral):
  def __init__(self, addr):
    Peripheral.__init__(self, addr, addrType="random")


def main():
  peri = MyPeripheral(devadr)
  peri.setDelegate(MyDelegate(btle.DefaultDelegate))

  #Button
  peri.writeCharacteristic(HANDLE_BUTTON_A + 1, b"\x01\x00", True)
  peri.writeCharacteristic(HANDLE_BUTTON_B + 1, b"\x01\x00", True)

  #acc
  #peri.writeCharacteristic(0x002a, b"\x50\x00", True)
  peri.writeCharacteristic(HANDLE_ACCELE + 1, b"\x01\x00", True)

  while exflag == False:
    if peri.waitForNotifications(1.0):
      #sleep(0.3)
      continue
  
  peri.disconnect()


if __name__ == "__main__":
  main()

