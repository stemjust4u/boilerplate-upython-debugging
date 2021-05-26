
Pin	|	 IN_PUP/PWM_ERROR	|	 IN_PUP_V	|	 IN_PDOWN	|	 IN_PDOWN_V	|	 OUT_LO	|	 OUT_HI	|
----	|	----	|	----	|	----	|	----	|	----	|	----	|
2	|	0	|	**0.57**	|	0	|	0	|	0	|	3.3	|
4	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
5	|	1	|	3.3	|	1	|	**2.42**	|	0	|	3.3	|
12	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
13	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
14	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
18	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
19	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
21	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
22	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
23	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
25	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
26	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
27	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
32	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
33	|	1	|	3.3	|	0	|	0	|	0	|	3.3	|
35	|	0	|	**0.46**	|	0	|	**1.33**	|	 na	|	 na	|
36(VP)	|	0	|	**1.11**	|	0	|	0	|	 na	|	 na	|
39(VN)	|	0	|	0	|	0	|	**0.47**	|	 na	|	 na	|


localtime = (2021, 5, 6, 12, 55, 0, 0, 0) #(year, month, day, hour, minute, second, weekday, yearday)
print(utime.time())    # integer, seconds since 1/1/2000, returned from RTC.  Add hrs*3600 for adjustment
print((utime.localtime()))   # current time from RTC is returned. If seconds/integer is passed to it it converts to 8-tuple
print(localdate((utime.localtime())))

86400 seconds in a day, 3600 seconds in an hour

t =utime.mktime((2018,8,16,22,0,0,3,0))  # enter a 8-tuple which expresses time as per localtime. mktime returns an integer, number of seconds since 1/1/2000
t += 4*3600
utime.localtime(t)
or
utime.localtime(utime.mktime(utime.localtime()) + 3*3600)


absolute value
import math
math.fabs(x)
