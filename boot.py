# This file is executed on every boot (including wake-boot from deepsleep)
import esp, machine
from mytools import rtcdate
esp.osdebug(None)
#import webrepl
#webrepl.start()

CPUFREQ = 240000000

#rtc = machine.RTC()    # If using local network time comment out rtc.datetime(xxx)
#rtc.datetime((2021, 5, 6, 0, 12, 55, 0, 0)) #(year, month, day, weekday, hours, minutes, seconds, subseconds)
#print('RTC datetime: {0}'.format(rtcdate(rtc.datetime())))  
MAIN_FILE_LOGGING = False  # Enable if wanting all modules to write to a single log file. Will use safer 'with' (open/close).
MAIN_FILE_NAME = "complete.log"    # Had to enable 'sync_all_file_types' to get .log files to copy over in pymakr
MAIN_FILE_MODE = "a"       # Should be either a or ab append mode
logfiles = []   # Keep track of log files to monitor size and close them if too big