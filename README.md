# esp32logging
uos.listdir([dir])
uos.mkdir(path)
uos.remove(path)
uos.rmdir(path)
uos.rename(old_path, new_path)

ntptime.settime(timezone=8, server = 'ntp.ntsc.ac.cn')
Synchronize local time

timezone - Time zone time difference, the default is East Eight District, compensation 8 hours
server - You can specify the time server yourself, server is a string type. The default time server is “ntp.ntsc.ac.cn” .
Example:

from mpython import *
import ntptime

mywifi=wifi()
mywifi.connectWiFi('tang','tang123456')

print("Local time before synchronization：%s" %str(time.localtime()))
ntptime.settime()
print("Local time after synchronization：%s" %str(time.localtime()))

r Opens a file for reading only. The file pointer is placed at the beginning of the file. This is the default mode.
rb Opens a file for reading only in binary format. The file pointer is placed at the beginning of the file. This is the default mode.
r+ Opens a file for both reading and writing. The file pointer placed at the beginning of the file.	
rb+ Opens a file for both reading and writing in binary format. The file pointer placed at the beginning of the file.	
w Opens a file for writing only. Overwrites the file if the file exists. If the file does not exist, creates a new file for writing.	
wb Opens a file for writing only in binary format. Overwrites the file if the file exists. If the file does not exist, creates a new file for writing.	
w+ Opens a file for both writing and reading. Overwrites the existing file if the file exists. If the file does not exist, creates a new file for reading and writing.	
wb+ Opens a file for both writing and reading in binary format. Overwrites the existing file if the file exists. If the file does not exist, creates a new file for reading and writing.	
a Opens a file for appending. The file pointer is at the end of the file if the file exists. That is, the file is in the append mode. If the file does not exist, it creates a new file for writing.	
ab Opens a file for appending in binary format. The file pointer is at the end of the file if the file exists. That is, the file is in the append mode. If the file does not exist, it creates a new file for writing.	
a+ Opens a file for both appending and reading. The file pointer is at the end of the file if the file exists. The file opens in the append mode. If the file does not exist, it creates a new file for reading and writing.
ab+ Opens a file for both appending and reading in binary format. The file pointer is at the end of the file if the file exists. The file opens in the append mode. If the file does not exist, it creates a new file for reading and writing.
