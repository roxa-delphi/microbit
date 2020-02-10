import cb
import time

class MyCentralManagerDelegate (object):
  def __init__(self):
    pass

  def did_discover_peripheral(self, p):
    print('+++ peripheral: %s (%s)' % (p.name, p.uuid))


delegate = MyCentralManagerDelegate()
print('Scanning for peripherals...')

cb.set_central_delegate(delegate)
cb.scan_for_peripherals()

time.sleep(3)
cb.reset()
print('disconnected')

