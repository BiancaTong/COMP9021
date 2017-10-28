## written by Bianca Tong for comp 9021 ass1 q2 ##
import os.path
import sys
import re
from collections import defaultdict

#whether has such file
try:
    filename=input('Please enter the name of the file you want to get data from: ')
    cable_new=[]
    for i in open(filename,'r').read().split():
        if i!=' ':
            cable_new.append(i)
    #cable_original=open(filename,'r')
except IOError:
	print('Sorry, there is no such file.')
	sys.exit()
#cable_original.close

#whether it is an increasing positive integer sequence
for i in range(0,len(cable_new)):
    if cable_new[i].isdigit()==False:
        print('Sorry, input file does not store valid data.')
        sys.exit()
for i in range(0,len(cable_new)):
    cable_new[i]=int(cable_new[i])
for i in range(0,len(cable_new)):
    if len(cable_new)<=1 or cable_new[i]==0:
        print('Sorry, input file does not store valid data.')
        sys.exit()
    elif i<len(cable_new)-1 and cable_new[i]>=cable_new[i+1]:
        print('Sorry, input file does not store valid data.')
        sys.exit()
    else:
        continue

#compute intervals
cable_interval=[]
for i in range(0,len(cable_new)-1):
    cable_interval.append(cable_new[i+1]-cable_new[i])

#compute longest ride
num=1
cable_interval_same_num=[]
for i in range(0,len(cable_interval)-1):
    if cable_interval[i]==cable_interval[i+1]:
        num+=1
    else:
        if num>=2:
            cable_interval_same_num.append(num)
            num=1

#build perfect ride
number_right=1
number_left=0
number=1
cable_interval_same_number1=[]
cable_interval_same_number2=[]
cable_interval_same_number=[]
for i in range(0,len(cable_new)):
    if i==0:
        for m in range(i+1,len(cable_new)):
            if cable_new[i]+cable_interval[i]*m in cable_new:
                number+=1
            else:
                cable_interval_same_number.append(number)
                break
    elif i<len(cable_new)-1:
        for j in range(1,len(cable_new)):
            if cable_new[i]+cable_interval[i]*j in cable_new:
                number_right+=1
            else:
                cable_interval_same_number1.append(number_right)
                number_right=1
                break
        for k in range(1,len(cable_new)):
            if cable_new[i]-cable_interval[i]*k in cable_new:
                number_left+=1
            else:
                cable_interval_same_number2.append(number_left)
                number_left=0
                break
for i in range(0,len(cable_interval_same_number1)):
    cable_interval_same_number.append(cable_interval_same_number1[i]+cable_interval_same_number2[i])

#print result
if num==len(cable_interval):
    print('The ride is perfect!')
    print('The longest good ride has a length of:',num)
    print('The minimal number of pillars to remove to build a perfect ride from the rest is: 0')
else:
    remove_num=len(cable_new)-max(cable_interval_same_number)
    print('The ride could be better...')
    print('The longest good ride has a length of:',max(cable_interval_same_num))
    print('The minimal number of pillars to remove to build a perfect ride from the rest is:',remove_num)
