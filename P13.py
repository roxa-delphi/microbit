#
# Folo move to forward
#   output to I/O P13
#
# Usages> python3 P13.py
#

from bluepy import btle
import binascii
import time

devadr     = "e4:1e:1f:1f:f4:49"

uuid_svc_iopin   = "e95d127b-251d-470a-a062-fa1922dfa9a8"
uuid_pin_io_conf = "e95db9fe-251d-470a-a062-fa1922dfa9a8"
uuid_pin_ad_conf = "e95d5899-251d-470a-a062-fa1922dfa9a8"
uuid_pin_data    = "e95d8d00-251d-470a-a062-fa1922dfa9a8"


per = btle.Peripheral(devadr, btle.ADDR_TYPE_RANDOM)

svcPinIO = per.getServiceByUUID(uuid_svc_iopin)

#pin13 as Analog
chPinAD  = svcPinIO.getCharacteristics(uuid_pin_ad_conf)[0]
chPinAD.write(b"\x00\x20\x00")

#pin13 as Output
chPinIO  = svcPinIO.getCharacteristics(uuid_pin_io_conf)[0]
chPinIO.write(b"\x00\x00\x00")

#pin13 output to 255
chPin    = svcPinIO.getCharacteristics(uuid_pin_data)[0]
#chPin.write(b"\x0d\xff")
#chPin.write(b"\x0d\x80")
chPin.write(b"\x0d\x50")

time.sleep(2)

#stop
chPin.write(b"\x0d\x00")

per.disconnect()

