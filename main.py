from boot import MAIN_FILE_LOGGING, MAIN_FILE_MODE, MAIN_FILE_NAME, logfiles # Not needed but helps with python intellisense (syntax highlighting)
import ulogging, micropython
from timer import Timer
import utime, uos
from machine import Pin, ADC, PWM
import gc
gc.collect()
micropython.alloc_emergency_exception_buf(100)

'''
ulogging from https://github.com/peterhinch
CRITICAL = 50
ERROR    = 40
WARNING  = 30
INFO     = 20
DEBUG    = 10
NOTSET   = 0
Update boot.py MAIN_FILE_LOGGING flag if wanting all modules to log to same file 
'''

# If wanting all modules to write to the same MAIN FILE then enable MAIN_FILE_LOGGING in boot.py
# If wanting modules to each be able to write to individual files then make sure autoclose=True (safe with file open/close)
# If wanting a single module to quickly write to a log file then only enable one module and set autoclose=False
logger_log_level= 10
logger_setup = 1  # 0 for basicConfig, 1 for custom logger with RotatingFileHandler (RFH)
FileMode = 2 # If logger_setup ==1  then access to modes below
            #  FileMode == 1 # no log file
            #  FileMode == 2 # write to log file

logfile = __name__ + '.log'
if logger_setup == 0: # Use basicConfig logger
    ulogging.basicConfig(level=logger_log_level) # Change logger global settings
    logger_main = ulogging.getLogger(__name__)
elif logger_setup == 1 and FileMode == 1:        # Using custom logger
    logger_main = ulogging.getLogger(__name__)
    logger_main.setLevel(logger_log_level)
elif logger_setup == 1 and FileMode == 2 and not MAIN_FILE_LOGGING: # Using custom logger with output to log file
    logger_main = ulogging.getLogger(__name__, logfile, mode='w', autoclose=True, filetime=5000)  # w/wb to over-write, a/ab to append, autoclose (with method), file time in ms to keep file open
    logger_main.setLevel(logger_log_level)
    logfiles.append(logfile)
elif logger_setup == 1 and FileMode == 2 and MAIN_FILE_LOGGING:            # Using custom logger with output to main log file
    logger_main = ulogging.getLogger(__name__, MAIN_FILE_NAME, MAIN_FILE_MODE, 0)  # over ride with MAIN_FILE settings in boot.py
    logger_main.setLevel(logger_log_level)

logger_main.info('{0} {1}'.format(utime.localtime(), logger_main))

@Timer
def integer(n):
    for i in range(n):
        x = 1 + 1

@Timer
def float(n):
    for i in range(n):
        x = 1.5 + 1.5

@Timer
def getpinvalue(pin):
    return pin.value()

@Timer
def setpinvalue(pin, value):
    pin.value(value)

@Timer
def set_4_pins(pins, value):
    for pin in pins:
        pin.value(value)

@Timer
def get_4_pins_list(pins, outgoing):
    outgoing[0] = pins[0].value()
    outgoing[1] = pins[1].value()
    outgoing[2] = pins[2].value()
    outgoing[3] = pins[3].value()
    return outgoing

@Timer
def get_4_pins_list_loop(pins, outgoing):
    for i, pin in enumerate(pins):
        outgoing[i] = pin.value()
    return outgoing

@Timer
def get_4_pins_dict(pins, outgoing):
    outgoing['0'] = pins[0].value()
    outgoing['1'] = pins[1].value()
    outgoing['2'] = pins[2].value()
    outgoing['3'] = pins[3].value()
    return outgoing

@Timer
def getADC(pin):
    return pin.read()

@Timer
def getADC_4pins(pins, outgoing):
    outgoing[0] = pins[0].read()
    outgoing[1] = pins[1].read()
    outgoing[2] = pins[2].read()
    outgoing[3] = pins[3].read()
    return outgoing

@Timer
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

print('Log file clean up')
ftotal = 0
for file in logfiles:
    filesize = uos.stat(file)[6]/1000
    print('file:{0} size: {1:.1f}kb '.format(file, filesize))
    ftotal += filesize
    with open(file, 'r') as f:
        print('{0} line 1: {1}'.format(file, f.readline().rstrip("\n")))
        print('           line 2: {0}'.format(f.readline().rstrip("\n")))
        print('           line 3: {0}'.format(f.readline().rstrip("\n")))
        print('Closed file: {0}'.format(file))
print('Logfiles used in program: {0:.1f}kb'.format(ftotal))

ftotal = 0
for file in uos.listdir("/lib"):
    ftotal += uos.stat("/lib/" + file)[6]/1000
print('All /lib files: {0:.1f}kb'.format(ftotal))

for file in uos.listdir():
    ftotal += uos.stat(file)[6]/1000
print('TOTAL: {0:.1f}kb'.format(ftotal))
    
