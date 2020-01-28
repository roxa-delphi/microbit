#
# Remote control Folo by PS3 controller
#   left stick  : move forward and back
#   right stick : turn left and right
#   B           : end
#
# Usages> python3 folo_control.py
#

from bluepy import btle
import binascii
import struct
import time

devadr           = "e4:1e:1f:1f:f4:49"
uuid_svc_iopin   = "e95d127b-251d-470a-a062-fa1922dfa9a8"
uuid_pin_io_conf = "e95db9fe-251d-470a-a062-fa1922dfa9a8"
uuid_pin_ad_conf = "e95d5899-251d-470a-a062-fa1922dfa9a8"
uuid_pin_data    = "e95d8d00-251d-470a-a062-fa1922dfa9a8"

device_path  = "/dev/input/js0"
EVENT_FORMAT = "LhBB"
EVENT_SIZE   = struct.calcsize(EVENT_FORMAT)


def main(chPin):

  with open(device_path, "rb") as device :
    event = device.read(EVENT_SIZE)

    while event :
      (ds3_time, ds3_val, ds3_type, ds3_num) = struct.unpack(EVENT_FORMAT, event)
      print("{0}, {1}, {2}, {3}".format(ds3_time, ds3_val, ds3_type, ds3_num))

      if ds3_num == 0 and ds3_type == 1:
        per.disconnect()
        return

      if ds3_num == 3 and ds3_type == 2:
        val = ds3_val / 256
        if val == 0:
          print(" rotate stop")
          chPin.write(b"\x0f\x00")
          chPin.write(b"\x10\x00")
        elif val > 0 :
          print(" rotate right %d" %val)
          chPin.write(b"\x0f\xff")
          chPin.write(b"\x10\x00")
        else :
          print(" rotate left  %d" %val)
          chPin.write(b"\x0f\x00")
          chPin.write(b"\x10\xff")

      if ds3_num == 1 and ds3_type == 1:
        if ds3_val == 1 :
          print("O")
          chPin.write(b"\x0d\x80")
          time.sleep(1)
          chPin.write(b"\x0d\x80")


      #time.sleep(0.2)
      event = device.read(EVENT_SIZE)


if __name__ == "__main__" :

  per = btle.Peripheral(devadr, btle.ADDR_TYPE_RANDOM)

  svcPinIO = per.getServiceByUUID(uuid_svc_iopin)

  #pin13-16 as Analog
  chPinAD = svcPinIO.getCharacteristics(uuid_pin_ad_conf)[0]
  chPinAD.write(b"\x00\xe0\x01\x00")

  #pin13-16 as Output
  chPinIO = svcPinIO.getCharacteristics(uuid_pin_io_conf)[0]
  chPinIO.write(b"\x00\x00\x00\x00")

  #pin
  chPin = svcPinIO.getCharacteristics(uuid_pin_data)[0]

  main(chPin)








