# This file is executed on every boot (including wake-boot from deepsleep)
import esp, machine
esp.osdebug(None)
#import webrepl
#webrepl.start()

machine.freq(240000000)
cpuf = machine.freq()
print('cpu: {0} MHz'.format(cpuf))

logfiles = []   # Keep track of log files to monitor size and close them if too big
MAIN_FILE_LOGGING = False  # Enable if wanting all modules to write to a single log file. Will use safer 'with' (open/close).
MAIN_FILE_NAME = "complete.log"    # Had to enable 'sync_all_file_types' to get .log files to copy over in pymakr
MAIN_FILE_MODE = "a"       # Should be either a or ab append mode
initial_open_mode = "w"    # Open with 'w' to start a new log file. Can change to 'a' to keep older logs.
if MAIN_FILE_LOGGING:
    with open(MAIN_FILE_NAME, initial_open_mode) as f:
        f.write("cpu freq: {0} MHz\n".format(cpuf/10**6))
        f.write("All module debugging will write to file: {0} with mode: {1}\n".format(MAIN_FILE_NAME, MAIN_FILE_MODE))
    print("All module debugging will write to file: {0} with mode: {1}\n".format(MAIN_FILE_NAME, MAIN_FILE_MODE))
    logfiles.append(MAIN_FILE_NAME)