
from bluepy import btle
import binascii

devadr     = "e4:1e:1f:1f:f4:49"

uuid_svc_button = "e95d9882-251d-470a-a062-fa1922dfa9a8"
uuid_button_a   = "e95dda90-251d-470a-a062-fa1922dfa9a8"
uuid_button_b   = "e95dda91-251d-470a-a062-fa1922dfa9a8"

hndButton_A = 0
hndButton_B = 0

class MyDelegate(btle.DefaultDelegate):
  def __init__(self):
    btle.DefaultDelegate.__init__(self)

  def handleNotification(self, hd, data):
    c_data = binascii.b2a_hex(data)

    if hd == hndButton_A:
      print("Button_A %s" %(c_data))

    if hd == hndButton_B:
      print("Button_B %s" %(c_data))

    #print("hd=%X, data=%s" %(hd, c_data))


per = btle.Peripheral(devadr, btle.ADDR_TYPE_RANDOM)

svcButton   = per.getServiceByUUID(uuid_svc_button)

chButton_A  = svcButton.getCharacteristics(uuid_button_a)[0]
hndButton_A = chButton_A.getHandle()
per.writeCharacteristic(hndButton_A + 1, b"\x01\x00", True)

chButton_B  = svcButton.getCharacteristics(uuid_button_b)[0]
hndButton_B = chButton_B.getHandle()
per.writeCharacteristic(hndButton_B + 1, b"\x01\x00", True)

per.setDelegate(MyDelegate())

while True:
  if per.waitForNotifications(0.1):
    continue

