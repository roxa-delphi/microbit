#
# Remote control Folo by PS3 controller
#   left  stick : move forward or back
#   right stick : turn left or right
#   X           : end
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
      #print("{0}, {1}, {2}, {3}".format(ds3_time, ds3_val, ds3_type, ds3_num))

      # X button to end
      if ds3_num == 0 and ds3_type == 1:
        #print(" move stop")
        chPin.write(b"\x0d\x00")
        chPin.write(b"\x0e\x00")
        #print(" rotate stop")
        chPin.write(b"\x0f\x00")
        chPin.write(b"\x10\x00")
        per.disconnect()
        return

      # right stick to rotate
      if ds3_num == 3 and ds3_type == 2:

        if abs(ds3_val) < 4000:
          #print(" rotate stop")
          chPin.write(b"\x0f\x00")
          chPin.write(b"\x10\x00")
        elif ds3_val > 0 :
          val = ds3_val>>7
          #print(" rotate right %d" %val)
          chPin.write(b"\x0f\x00")
          chPin.write(b"\x10" + val.to_bytes(1, 'little'))
        else :
          ds3_val = -ds3_val
          val = ds3_val>>7
          #print(" rotate left  %d" %val)
          chPin.write(b"\x10\x00")
          chPin.write(b"\x0f" + val.to_bytes(1, 'little'))

      # left stick to move
      if ds3_num == 1 and ds3_type == 2:

        if abs(ds3_val) < 4000:
          #print(" move stop")
          chPin.write(b"\x0d\x00")
          chPin.write(b"\x0e\x00")
        elif ds3_val > 0 :
          val = ds3_val>>7
          #print(" move back    %d" %val)
          chPin.write(b"\x0d\x00")
          chPin.write(b"\x0e" + val.to_bytes(1, 'little'))
        else :
          ds3_val = -ds3_val
          val = ds3_val>>7
          #print(" move forward %d" %val)
          chPin.write(b"\x0e\x00")
          chPin.write(b"\x0d" + val.to_bytes(1, 'little'))


      time.sleep(0.01)
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

  print("Remote control Folo by PS3 controller")
  print("  left  stick : move to forward or back")
  print("  right stick : turn left or right")
  print("  Button X    : End")

  main(chPin)








