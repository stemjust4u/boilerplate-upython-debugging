from boot import MAIN_FILE_LOGGING, MAIN_FILE_MODE, MAIN_FILE_NAME, CPUFREQ, logfiles # Not needed but helps with python intellisense (syntax highlighting)
import ulogging, micropython
from timer import Timer, TimerFunc
from mytools import pcolor, rtcdate, localdate
import utime, uos
from machine import Pin, ADC, PWM, RTC
import machine
import gc
gc.collect()
micropython.alloc_emergency_exception_buf(100)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')

machine.freq(CPUFREQ)

initial_open_mode = "w"    # Open with 'w' to start a new log file. Can change to 'a' to keep older logs.
if MAIN_FILE_LOGGING:
    with open(MAIN_FILE_NAME, initial_open_mode) as f:
        f.write("cpu freq: {0} GHz\n".format(CPUFREQ/10**9)) 
        f.write("All module debugging will write to file: {0} with mode: {1}\n".format(MAIN_FILE_NAME, MAIN_FILE_MODE))
        if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            f.write('{0}, woke from a deep sleep'.format(utime.localtime()))
    print("All module debugging will write to file: {0} with mode: {1}\n".format(MAIN_FILE_NAME, MAIN_FILE_MODE))
    logfiles.append(MAIN_FILE_NAME)

# If wanting all modules to write to the same MAIN FILE then enable MAIN_FILE_LOGGING in boot.py
# If wanting modules to each be able to write to individual files then make sure autoclose=True (safe with file open/close)
# If wanting a single module to quickly write to a log file then only enable one module and set autoclose=False
logger_log_level= 10
logger_type = "custom"  # 'basic' for basicConfig or 'custom' for custom logger
FileMode = 1 # If logger_type == 'custom'  then access to modes below
            #  FileMode == 1 # no log file
            #  FileMode == 2 # write to log file
logfile = __name__ + '.log'
if logger_type == 'basic': # Use basicConfig logger
    ulogging.basicConfig(level=logger_log_level) # Change logger global settings
    logger_main = ulogging.getLogger(__name__)
elif logger_type == 'custom' and FileMode == 1:        # Using custom logger
    logger_main = ulogging.getLogger(__name__)
    logger_main.setLevel(logger_log_level)
elif logger_type == 'custom' and FileMode == 2 and not MAIN_FILE_LOGGING: # Using custom logger with output to log file
    logger_main = ulogging.getLogger(__name__, logfile, mode='w', autoclose=True, filetime=5000)  # w/wb to over-write, a/ab to append, autoclose (with method), file time in ms to keep file open
    logger_main.setLevel(logger_log_level)
    logfiles.append(logfile)
elif logger_type == 'custom' and FileMode == 2 and MAIN_FILE_LOGGING:            # Using custom logger with output to main log file
    logger_main = ulogging.getLogger(__name__, MAIN_FILE_NAME, MAIN_FILE_MODE, 0)  # over ride with MAIN_FILE settings in boot.py
    logger_main.setLevel(logger_log_level)

logger_main.info('localtime: {0}'.format(localdate(utime.localtime())))

t = Timer()
t.start()

@TimerFunc
def integer(n):
    for i in range(n):
        x = 1 + 1

@TimerFunc
def float(n):
    for i in range(n):
        x = 1.5 + 1.5

@TimerFunc
def getpinvalue(pin):
    return pin.value()

@TimerFunc
def setpinvalue(pin, value):
    pin.value(value)

@TimerFunc
def set_4_pins(pins, value):
    for pin in pins:
        pin.value(value)

@TimerFunc
def get_4_pins_list(pins, outgoing):
    outgoing[0] = pins[0].value()
    outgoing[1] = pins[1].value()
    outgoing[2] = pins[2].value()
    outgoing[3] = pins[3].value()
    return outgoing

@TimerFunc
def get_4_pins_list_loop(pins, outgoing):
    for i, pin in enumerate(pins):
        outgoing[i] = pin.value()
    return outgoing

@TimerFunc
def get_4_pins_dict(pins, outgoing):
    outgoing['0'] = pins[0].value()
    outgoing['1'] = pins[1].value()
    outgoing['2'] = pins[2].value()
    outgoing['3'] = pins[3].value()
    return outgoing

@TimerFunc
def getADC(pin):
    return pin.read()

@TimerFunc
def getADC_4pins(pins, outgoing):
    outgoing[0] = pins[0].read()
    outgoing[1] = pins[1].read()
    outgoing[2] = pins[2].read()
    outgoing[3] = pins[3].read()
    return outgoing

@TimerFunc
def setPWM(pin):
    pin.duty(75)  

n=10
integer(n)
logger_main.debug('{0} ran {1} times'.format(utime.localtime(), n))

float(n)
logger_main.debug('{0} ran {1} times'.format(utime.localtime(), n))

pinlist = [5, 4, 2, 16]
io_pin = [0]*len(pinlist)
for i, pin in enumerate(pinlist):
    io_pin[i] = Pin(pin, Pin.OUT) # 2 is the internal LED

set_4_pins(io_pin, 0)

pin = 32
adc = ADC(Pin(pin))
adc.atten(ADC.ATTN_11DB)

pin = 23
pwm = PWM(Pin(pin), 50)

onoff = getpinvalue(io_pin[2])
logger_main.debug(onoff)
setpinvalue(io_pin[2], 1)
utime.sleep_ms(1000)
setpinvalue(io_pin[2], 0)

outgoing = [0]*len(pinlist)
data = get_4_pins_list(io_pin, outgoing)
logger_main.debug(data)

data = get_4_pins_list_loop(io_pin, outgoing)
logger_main.debug(data)

adcpins = [32, 33, 34, 35]
adc_pin = [0]*len(adcpins)
for i, pin in enumerate(adcpins):
    adc_pin[i] = ADC(Pin(pin))
    adc_pin[i].atten(ADC.ATTN_11DB)
adcdata = getADC_4pins(adc_pin, outgoing)
logger_main.debug(adcdata)

outgoing = {}
data = get_4_pins_dict(io_pin, outgoing)
logger_main.debug(data)

adcvalue = getADC(adc)

setPWM(pwm)

logger_main.info("Total time: {0} ms".format(t.stop()/1000))

logger_main.info('Log file clean up')
ftotal = 0
for file in logfiles:
    filesize = uos.stat(file)[6]/1000
    logger_main.info('file:{0} size: {1:.1f}kb '.format(file, filesize))
    ftotal += filesize
    with open(file, 'r') as f:
        logger_main.info('{0} line 1: {1}'.format(file, f.readline().rstrip("\n")))
        logger_main.info('           line 2: {0}'.format(f.readline().rstrip("\n")))
        logger_main.info('           line 3: {0}'.format(f.readline().rstrip("\n")))
        logger_main.info('Closed file: {0}'.format(file))
logger_main.info('Logfiles used in program: {0:.1f}kb'.format(ftotal))

ftotal = 0
for file in uos.listdir("/lib"):
    ftotal += uos.stat("/lib/" + file)[6]/1000
logger_main.info('All /lib files: {0:.1f}kb'.format(ftotal))

for file in uos.listdir():
    ftotal += uos.stat(file)[6]/1000
logger_main.info('{0}TOTAL: {1:.1f}kb{2}'.format(pcolor.BOW, ftotal, pcolor.ENDC))