## written by Bianca Tong for comp 9021 ass1 q3 ##
import os.path
import sys
from collections import deque
import re

#whether has such file
try:
	filename=input('Please enter the name of the file you want to get data from: ')
	tunnel_original=open(filename,'r')
	tunnel_lines=tunnel_original.readlines()
	tunnel_new=[]
	tunnel_new1=[]
	tunnel_new2=[]
	for line in tunnel_lines:
		if line.split():
			tunnel_new.append(line.split())
	for i in tunnel_new[0]:
		if i!=' ':
			tunnel_new1.append(i)
	for j in tunnel_new[1]:
		if j!=' ':
			tunnel_new2.append(j)
except IOError:
	print('Sorry, there is no such file.')
	sys.exit()
tunnel_original.close

#whether it has two lines of at last two integers(positive or negetive) with same number
for i in range(0,len(tunnel_new1)):
	if tunnel_new1[i].isdigit()==False and tunnel_new2[i].isdigit()==False:
		print('Sorry, input file does not store valid data.')
		sys.exit()

#transfer from string to int list
for i in range(0,len(tunnel_new1)):
	tunnel_new1[i]=int(tunnel_new1[i])
	tunnel_new2[i]=int(tunnel_new2[i])
for i in range(0,len(tunnel_new1)):
	if len(tunnel_new)!=2 or len(tunnel_new1)!=len(tunnel_new2) or len(tunnel_new1)<=1 or tunnel_new1[i]==0 or tunnel_new2[i]==0:
		print('Sorry, input file does not store valid data.')
		sys.exit()
	elif tunnel_new1[i]<=tunnel_new2[i]:
		print('Sorry, input file does not store valid data.')
		sys.exit()


#compute west
for i in range(0,len(tunnel_new1)):
	if tunnel_new1[i]<=tunnel_new2[0]:
		west_num=i
		break

#compute inside longest distance
inside_numlist=[]
for j in range(0,len(tunnel_new1)-1):
	min_tunnel=tunnel_new1[j]
	max_tunnel=tunnel_new2[j]
	inside_num=1
	for i in range(j,len(tunnel_new1)-1):
		min_tunnel=min(min_tunnel,tunnel_new1[i+1])
		max_tunnel=max(max_tunnel,tunnel_new2[i+1])
		tunnel_interval=min_tunnel-max_tunnel
		if tunnel_interval<=0:
			inside_numlist.append(inside_num)
			break
		elif i==len(tunnel_new1)-2:
			inside_numlist.append(inside_num+1)
			break
		else:
			inside_num+=1
#print result
print('From the west, one can into the tunnel over a distance of',west_num)
print('Inside the tunnel, one can into the tunnel over a maximum distance of',max(inside_numlist))
