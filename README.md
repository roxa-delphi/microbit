Control and connect micro:bit and Programming Folo

-micro:bit  
  [https://microbit.org/ja/](https://microbit.org/ja/)

-Programming Folo  
  [https://switch-education.com/products/5482/](https://switch-education.com/products/5482/)


1. scan bluetooth and search micro:bit bluetooth address
```
   % python3 scan.py
```

2. get UUID for control through bluetooth
   memo : getHandle.log
```
   % python3 getHandle.py xx:xx:xx:xx:xx
```

3. display "Hello" on micro:bit LED
```
   % python3 writeLed2.py
```

4. move forward Folo
```
   output "125" to P13 pin for move forward Folo
   % python3 P13.py
```
   
5. connect PS3 controller to Raspberry Pi 4
   memo : js_watch.log
```
   % python3 js_watch.py
```

6. remote control Folo through bluetooth by PS3 controller
```
   % python3 folo_control.py
       left  stick  : move forward or back
       right stick  : turn left or right
       X     button : end
```
