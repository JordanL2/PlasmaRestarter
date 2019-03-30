#!/usr/bin/python3

# Deps:
# python-pydbus

from pydbus import *
from gi.repository import GLib
import subprocess
import sys
from datetime import *


class ShellRestarter():

    def __init__(self):
        self.armed = False
        self.monitors = self.get_active_monitors()
        self.output("{} monitors found".format(self.monitors))

        kscreen_backend = SessionBus().get("org.kde.KScreen", "/backend")
        kscreen_backend.configChanged.connect(self.config_changed_callback)

        loop = GLib.MainLoop()
        loop.run()


    def config_changed_callback(self, config):
        self.output("Received config changed signal:")

        # Get active monitor count
        outputs_enabled = 0
        for output in config['outputs']:
            if output['connected'] and output['enabled']:
                outputs_enabled += 1
        self.output("    {} monitors connected".format(outputs_enabled))
        
        # If the monitor count is higher than the expected number, increase the expected number
        if outputs_enabled > self.monitors:
            self.output("    Increased monitor count from {} to {}".format(self.monitors, outputs_enabled))
            self.monitors = outputs_enabled

        # If the monitor count is lower than the expected number, then we should restart when the count is back up to normal
        elif outputs_enabled < self.monitors and not self.armed:
            self.output("    Number of monitors dropped from {} to {} - armed restart".format(self.monitors, outputs_enabled))
            self.armed = True

        # If the monitor count dropped previously, but is now back up to what it should be, restart shell
        if outputs_enabled == self.monitors and self.armed:
            self.output("    Number of monitors is back up to {} - performing restart".format(self.monitors))
            self.restart()
            self.armed = False

        # Remember the last monitor count
        self.last_output_count = outputs_enabled

    def get_active_monitors(self):
        return int(self.call("xrandr --listactivemonitors | tail -n+2 | wc -l"))

    def restart(self):
        self.output("        Restarting shell...")
        self.call("killall plasmashell ; sleep 2 ; kstart5 plasmashell >/dev/null 2>&1 &")
        self.output("        Restarted")

    def call(self, command):
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = result.stdout.decode('utf-8').rstrip("\n")
        stderr = result.stderr.decode('utf-8').rstrip("\n")
        return stdout

    def output(self, message):
        # Output timestamped message
        currenttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(currenttime + ' - ' + message)
        # This is needed when outputting to a log, otherwise messages will be buffered
        sys.stdout.flush()


if __name__ == '__main__':
    ShellRestarter()
