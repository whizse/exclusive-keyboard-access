#!/usr/bin/python3
import os
import ioctl_opt
import fcntl
import ctypes
import struct
import sys

device = ""

try:
    device = sys.argv[1]
except IndexError:
    try:
        import pyudev
        ctx = pyudev.Context()
        allDev = ctx.list_devices(subsystem='input', ID_BUS='usb')

        foundDev = []
        print("Found the following USB input devices: \n")
        count = 0
        for dev in allDev:
            if dev.device_node is not None:
                count += 1
                foundDev.append(dev.device_node)
                print(str(count), end =". ")
                print(dev['ID_SERIAL'], end=" ") # e.g. Logitech_HID_compliant_keyboard
                print(dev.device_node) # e.g. /dev/input/event/7
                # print(dev['ID_VENDOR_ID']) # e.g. 046d
                # print(dev['ID_MODEL_ID']) # e.g. c30e

                print()
        print("Select a device (1 to %s)" % str(len(foundDev)), end=" ")
        i = int(input())
        i -= 1
        device = foundDev[i]
    except ImportError:
        print("Install pyudev or provide a /dev/input node to use.")
        exit(0)

print("Using device " + device)

try:
    fd = open(device, 'rb')
except FileNotFoundError:
    print("No such device, is it connected?")
    exit(0)
except PermissionError:
    print("Insufficent permission to read, run me as root!")
    exit(0)

# from input-event-codes.h
# type can be EV_SYN, EV_KEY or EV_MSC
EV_KEY = 1
KEY_DOWN = 1

# from input.h:
EVIOCGNAME = lambda len: ioctl_opt.IOC(ioctl_opt.IOC_READ, ord('E'), 0x06, len)
EVIOCGRAB = lambda len: ioctl_opt.IOW(ord('E'), 0x90, ctypes.c_int)
name = ctypes.create_string_buffer(256)

# also from input.h
event_format = "llHHI"
event_size = struct.calcsize(event_format)

fcntl.ioctl(fd, EVIOCGNAME(256), name, True)
print("Device calls itself: " + name.value.decode('UTF-8'))

print("Grabbing device for exclusive access.")
print("Enter numbers, press enter (Ctrl-C to exit).")
fcntl.ioctl(fd, EVIOCGRAB(1), True)

youwrote = []

e_sec = "" # unix epoch second
e_usec = "" # unix epoch microsecond
e_type = "" # EV_SYN, EV_KEY, EV_MSC etc
e_code = "" # keycode, see http://www.comptechdoc.org/os/linux/howlinuxworks/linux_hlkeycodes.html
e_val = "" # keydown = 1, keyup = 0

while True:
    try:
        byte = fd.read(event_size)
        e_sec, e_usec, e_type, e_code, e_val = struct.unpack(event_format, byte)
        if e_type == EV_KEY and e_val == KEY_DOWN:
            # Ugly mapping of number keys to their values
            e_code -= 1 
            if e_code >= 1 and e_code <= 10:
                if e_code == 10:
                    print(str(0), end="")
                    youwrote.append(str(0))
                else:
                    print(str(e_code), end="")
                    youwrote.append(str(e_code))
                sys.stdout.flush()
            elif e_code == 27: # enter minus one
                print()
                print("You wrote: " + ''.join(youwrote))
                youwrote = []
    except (KeyboardInterrupt, SystemExit, OSError):
        fd.close()
        print("\rGoodbye!")
        exit(0)
