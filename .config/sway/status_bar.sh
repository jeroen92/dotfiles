uptime_formatted=$(uptime | cut -d ',' -f1 | cut -d ' ' -f4,5)

date_formatted=$(date "+%a %F %H %M")

linux_version=$(uname -r | cut -d '-' -f1)

battery_status=$(cat /sys/class/power_supply/BAT0/status)

battery=`upower --enumerate | grep BAT`
battery_info=`upower --show-info $battery`
battery_time=`echo $battery_info | grep 'time to empty'`
battery_percentage=`echo $battery_info | grep 'percentage'`
battery_state=`echo $battery_info | grep 'state'`
