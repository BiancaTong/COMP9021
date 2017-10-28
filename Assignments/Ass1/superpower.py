## written by Bianca Tong for comp9021 ass1 q1 ## 
import sys
import copy
#an arbitrary number of (postive or negtive)
try:
	heros=[int(x) for x in input('Please input the heroes\' powers: ').split()]
except ValueError:
	print('Sorry, these are not valid power values.')
	sys.exit()
for i in heros:
	if i==0:
		print('Sorry, these are not valid power values.')
		sys.exit()
#a nonnegative integer nb_of_swiches
nb_of_swiches=input('Please input the number of power flips: ')
try:
	nb_of_swiches=int(nb_of_swiches)
	if nb_of_swiches<0 or nb_of_swiches>len(heros):
		raise ValueError
except ValueError:
    print('Sorry, this is not a valid number of power flips.')
    sys.exit()

#switch can more than once
nb_of_swiches1=nb_of_swiches
heros_ordered_positive1=[]
for i in heros:
	if i<0:
		i=i*(-1)
		heros_ordered_positive1.append(i)
	else:
		heros_ordered_positive1.append(i)
heros_ordered_positive1=sorted(heros_ordered_positive1,reverse=True)

heros_ordered1=sorted(heros)
for i in range(0,len(heros_ordered1)):
	if nb_of_swiches1!=0:
		if heros_ordered1[i] in heros_ordered_positive1:
			continue
		else:
			heros_ordered1[i]=heros_ordered1[i]*(-1)
			nb_of_swiches1-=1
	else:
		break
heros_ordered1=sorted(heros_ordered1)
if nb_of_swiches1!=0:
	heros_ordered1[0]=heros_ordered1[0]*pow((-1),nb_of_swiches1)
sum_power1=sum(heros_ordered1)
print('Possibly flipping the power of the same hero many times, the greatest achievable power is {}.'.format(sum_power1))

#swich must less than 1
nb_of_swiches2=nb_of_swiches
heros_ordered2=sorted(heros)
for i in range(0,len(heros_ordered2)):
	if nb_of_swiches2!=0:
		heros_ordered2[i]=heros_ordered2[i]*(-1)
		nb_of_swiches2-=1
	else:
		break
sum_power2=sum(heros_ordered2)
print('Flipping the power of the same hero at most once, the greatest achievable power is {}.'.format(sum_power2))

#swich only concecutive heros
nb_of_swiches3=nb_of_swiches
heros_new3=copy.deepcopy(heros)
sum_power3=[]
for i in range(0,len(heros_new3)-nb_of_swiches3+1):
	heros_change3=copy.deepcopy(heros)
	for j in range(i,i+nb_of_swiches3):
		heros_change3[j]=heros_change3[j]*(-1)
	sum_power3.append(sum(heros_change3))
sum_power3_max=max(sum_power3)
print('Flipping the power of nb_of_flips many consecutive heroes, the greatest achievable power is {}.'.format(sum_power3_max))

#swich concecutive heros without nb_of_swiches
heros_new4=copy.deepcopy(heros)
sum_power4=[]
for i in range(0,len(heros_new4)):
	heros_change4=copy.deepcopy(heros)
	for x in range(0,len(heros_new4)-i+1):
		for j in range(i,i+x):
			heros_change4[j]=heros_change4[j]*(-1)
		sum_power4.append(sum(heros_change4))
sum_power4_max=max(sum_power4)
print('Flipping the power of arbitrarily many consecutive heroes, the greatest achievable power is {}.'.format(sum_power4_max))


