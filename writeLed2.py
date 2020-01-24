#
# put "Hello" to LED
#
# Usages> python3 writeLed2.py
#

import time
from bluepy import btle

devadr     = "e4:1e:1f:1f:f4:49"

uuid_service_led = "e95dd91d-251d-470a-a062-fa1922dfa9a8"
uuid_led_text    = "e95d93ee-251d-470a-a062-fa1922dfa9a8"


per = btle.Peripheral(devadr, btle.ADDR_TYPE_RANDOM)

svcLed = per.getServiceByUUID(uuid_service_led)
chLedText = svcLed.getCharacteristics(uuid_led_text)[0]
chLedText.write("Hello".encode("utf-8"))
time.sleep(5)

per.disconnect()


