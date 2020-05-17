# Codeless Kext for Microsoft Pro IntelliMouse

This is a codeless kext for the Microsoft Pro IntelliMouse, it prevents the default macOS keyboard drivers from hijacking the device.

## Install

We'll have to disable System Integrity Protection (SIP) or else it won't let us install unsinged kext's (which is probably a good thing).
Only execute the following steps if fully you understand the implications of it.

1. Restart your Mac and while retarting it, hold Command (⌘) + R.
This will get you into revovery mode, navigate to the top bar "MacOS Utilities" -> "Utilities" -> "Terminal" and execute the following command:
```shell
csrutil disable
```
2. Exit out of the recovery mode and restart your machine.
3. Once you're back to your desktop and logged in, open up the  terminal and execute the following command in the directory this README is contained in.
```shell
sudo ./install-kext.sh
```

## Uninstall

Once you're done configuring your mouse, it's probably wise to uninstall the codeless kext for this device and re-enable SIP.

1. Open up the terminal and execute the following command in the directory this README is contained in.
```shell
sudo ./uninstall-kext.sh
```
2. Restart your Mac and while retarting it, hold Command (⌘) + R. This will get you into revovery mode, navigate to the top bar "MacOS Utilities" -> "Utilities" -> "Terminal" and execute the following command:
```shell
csrutil enable
```
