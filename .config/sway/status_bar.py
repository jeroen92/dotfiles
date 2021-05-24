import humanize

from datetime import datetime
from psutil import disk_usage, sensors_battery
from sys import stdout
from time import sleep

from networkinfo import NetworkInfo


def refresh():
    diskspace = humanize.naturalsize(disk_usage('/').free, binary=True)
    battery_pct = int(sensors_battery().percent)
    battery_status = "charging" if sensors_battery().power_plugged else "discharging"
    date = datetime.now().strftime('%d/%m %H:%M:%S')
    network_info = NetworkInfo.update()
    content = f"\N{globe with meridians} {network_info.summary} | \U0001F50B {battery_pct}% {battery_status} | \N{floppy disk} {diskspace} avail. | \U0001F55E {date}"
    stdout.write(f"{content}\n")
    stdout.flush()

while True:
    refresh()
    sleep(5)
