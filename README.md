# PlasmaRestarter

A daemon to work around a multi-monitor bug in Plasma Shell.

When the monitors wake up from sleep, the task managers can get confused and both show tasks from one monitor. To work around this, we can automatically restart Plasma.

The script receives events from the org.kde.KScreen /backend DBus bus. When the monitor count drops, then increases back to normal, a reconnection event is considered to have happened, and Plasma is restarted.

This daemon will not cope with a dynamic monitor setup, where you may be connecting and disconnecting external monitors. It is only designed to work with static setups. It will cope with the monitor count increasing, but when the monitor count legitimately decreases the daemon will need to be restarted.

## Dependencies
python-pydbus

## Setup
Clone directory to somewhere on your system / home dir.

Go to Plasma System Settings > Workspace > Startup and Shutdown > Autostart > Add program > select the plasmarestarter shell script.
