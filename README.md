These are two small proof of concept scripts for having exclusive
access to a keyboard in Linux using the EVIOCGRAB ioctl.

These scripts are provided as a stepping stone for a program handling
input from USB devices like bar code readers that show up as normal
keyboards.

-------------------------------------------------------------------------------

exclusive-keyboard.py only requires [python-ioctl-opt](https://github.com/vpelletier/python-ioctl-opt) (included) and
optionally uses [pyudev](https://pyudev.readthedocs.io/en/latest/) to find suitable devices.

The other script uses [python-evdev](http://python-evdev.readthedocs.io/en/latest/), not available as a package in
Debian. It also has a minor bug(?) in a generator:

`Exception ignored in: <bound method InputDevice.__del__ of InputDevice('/dev/input/event15')>
`

In spite of this, using python-evdev is the preferred solution. It's
shorter, cleaner and future-proof.

-------------------------------------------------------------------------------

Some devices provide two /dev/input nodes, both can be grabbed, but
only one provides keystrokes. 

If you accidentally grab the only keyboard (the one you're using) just
unplug it and plug it back in. 
