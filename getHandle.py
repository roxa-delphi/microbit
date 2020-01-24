#
# output UUID and Handle and properties
#
# Usages> python3 getHandle.py xx:xx:xx:xx:xx:xx
#

import sys
import bluepy

def main() :
  try:
    peri = bluepy.btle.Peripheral()
    peri.connect(devadr, bluepy.btle.ADDR_TYPE_RANDOM)

  except:
    print("device connect error")
    sys.exit()

  charas = peri.getCharacteristics()
  for chara in charas :
    print("------------------------------------------")
    print(" UUID : %s" % chara.uuid )
    print(" Handle %04X : %s" %(chara.getHandle(), chara.propertiesToString()))

  peri.disconnect()


if __name__ == "__main__" :
  if len(sys.argv) == 1:
    print("Usage: getHandle.py BLE_DEVICE_ADDRESS")
    sys.exit()
  devadr = sys.argv[1]

  main()

