#!/usr/bin/python3
import os
import sys
import evdev

# Docs http://python-evdev.readthedocs.io/en/latest/tutorial.html

device = ""

try:
    dev_path = sys.argv[1]
    try:
        device = evdev.InputDevice(dev_path)
    except PermissionError:
        print("Insufficent permission to read, run me as root!")
        exit(0)

except IndexError:
    foundDev = []
    allDev = [evdev.InputDevice(dev) for dev in evdev.list_devices()]
    if len(allDev) == 0:
        print("No devices found, run me as root!")
        exit(0)
    print("Found the following USB input devices: ")
    count = 0
    for device in allDev:
        if "usb" in device.phys:
            count += 1
            foundDev.append(device)
            print(str(count) + ". " + device.name, device.fn)

    print("Select a device (1 to %s)" % str(len(foundDev)), end=" ")
    i = int(input())
    i -= 1
    device = foundDev[i]

print("Using device " + device.fn)

print("Grabbing device for exclusive access.")
device.grab()
print("Enter numbers, press enter (Ctrl-C to exit).")

youwrote = []

try:
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY and event.value == 1:
            e_code = event.code - 1
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
    device.ungrab()
    print("\rGoodbye!")
    exit(0)
