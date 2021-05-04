'''
3 methods to read/write a file
    1         2          3
f.write() ujson.dump pickle.dump
f.read()  ujson.load pickle.load

'''

f = open("log.py", "r")
f.read()
f.readline().rstrip("\n")
f.close()

from array import array
import ujson

a = array('f', range(10))
a = {"key1":1, "key2":2}
f = open('test.csv', 'w')
with open('log.py', 'w') as f:
    ujson.dump(tuple(a), f)

ujson.dump(a, f)

f = open('test.csv', 'r')
with open('log.py', 'r') as f:
    z = array('f', ujson.load(f))

z = ujson.load(f)
print(z)
''' To use pickle just search/replace ujson with pickle

JSON (universal format that works with other languages like js) supports most Python data types
pickle (python specific) supports all python types
Have to convert arrays to tuple since it is not a native data type
'''
dir(uos)
dir(f)
dir(str)
dir(list)
dir(dict)