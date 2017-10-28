## written by Bianca Tong for comp9021 ass2 ##
import os.path
import sys
import re
import copy
from math import sqrt
from math import cos
from math import sin
from math import pi
from collections import defaultdict
import pdb
from argparse import ArgumentParser
from re import sub
from statistics import mean
from itertools import count
from math import ceil
from PIL import Image
sys.setrecursionlimit(5000)
def display(L):
    for i in range(len(L)):
        for j in range(len(L[0])):
            width=len(str(L[i][j]))
            if L[i][j]:
                print('{:{}d}'.format(L[i][j], width) + ' ' * (3-width), end = '')
            else:
                print('{:{}s}'.format(' ', width) + ' ' * (3-width), end = '')
        print()
    print()
parser = ArgumentParser()
##parser.add_argument('--file', required = True)
parser.add_argument('-print', dest='pp',action='store_true',required = False)
parser.add_argument('--file', dest='filename', required = True)
##parser.add_argument('--nb_of_pixels', dest = 'nb_of_pixels', required = False)
args = parser.parse_args()
filename = args.filename
pp = args.pp
try:
    L_first=[]
    L_orig=[]
    with open(args.filename) as fn:
        for line in fn:
            i=line.split()
            i=list(' '.join(i))
            for j in i:
                if j!=' ':
                    L_first.append(j)
            if L_first!=[]:
                L_orig.append(L_first)
            L_first=[]
except IOError:
    print('Incorrect input.')
    sys.exit()
Ld=[list(map(int, row)) for row in L_orig]
try:
    if len(Ld)>=2 and len(Ld)<=50 and len(Ld[0])>=2 and len(Ld[0])<=50:
        for i in range(0,len(Ld)):
            for j in range(0,len(Ld[0])):
                if Ld[i][j]==1 or Ld[i][j]==0:
                    continue
                else:
                    raise ValueError
    else:
        raise ValueError
except ValueError:
    print('Incorrect input.')
    sys.exit()
neibour=[[-1,0],[-1,+1],[0,+1],[+1,+1],[+1,0],[+1,-1],[0,-1],[-1,-1]]
#neibour_=[[+1,0],[+1,+1],[0,+1],[-1,+1],[-1,0],[-1,-1],[0,-1],[+1,-1]]
def check_edge(L,m,n,direct):
    if m>=0 and m<len(L) and n>=0 and n<len(L[0]) and direct<8:
        return 1
    else:
        return 0
def check_stop(L,m,n,m_n,n_n,direct):
    if check_edge(L,m,n,direct)==0 or check_edge(L,m_n,n_n,direct)==0:
        return 1
    elif m==m_n and n==n_n:
        return 2
    else:
        return 3
def find_1(L,m,n,dire,nbb):
    if check_edge(L,m,n,dire):
        neib_m=m+neibour[dire][0]
        neib_n=n+neibour[dire][1]
        if check_edge(L,m,n,dire) and check_edge(L,neib_m,neib_n,dire):
                if L[neib_m][neib_n]==1:
                    nbb=0
                    neib_m-=neibour[dire][0]
                    neib_n-=neibour[dire][1]
                    return (neib_m,neib_n,dire)
                elif L[neib_m][neib_n]!=1:
                    if dire<7 and nbb<=8:
                        neib_m-=neibour[dire][0]
                        neib_n-=neibour[dire][1]
                        nbb+=1
                        dire+=1
                        return find_1(L,neib_m,neib_n,dire,nbb)
                    elif dire>=7 and nbb<=8:
                        neib_m-=neibour[dire][0]
                        neib_n-=neibour[dire][1]
                        nbb+=1
                        dire=0
                        return find_1(L,neib_m,neib_n,dire,nbb)
                    else:
                        nbb=0
                        neib_m = False
                        neib_n = False
                        return (neib_m,neib_n,dire)
        elif check_stop(L,m,n,neib_m,neib_n,dire)==1:
            if dire<7 and nbb<=8:
                neib_m-=neibour[dire][0]
                neib_n-=neibour[dire][1]
                nbb+=1
                dire+=1
                return find_1(L,neib_m,neib_n,dire,nbb)
            elif dire>=7 and nbb<=8:
                neib_m-=neibour[dire][0]
                neib_n-=neibour[dire][1]
                nbb+=1
                dire=0
                return find_1(L,neib_m,neib_n,dire,nbb)
            else:
                nbb=0
                neib_m = False
                neib_n = False
                return (neib_m,neib_n,dire)
    return (neib_m,neib_n,dire)
def back_point(L,m_m,n_n,m,n,direction):
    #pdb.set_trace()
    if direction !=[]:
        direct=direction.pop()
        m=m_m-neibour[direct][0]
        n=n_n-neibour[direct][1]
        dire=0
        nbb=0
        neib_m,neib_n,dirr=find_1(L,m,n,dire,nbb)
        if (neib_m is not False) and (neib_n is not False):
            return(neib_m,neib_n,dirr,L)
        else:
            L[m][n]=100
            #display(L)
            return back_point(L,m,n,m,n,direction)
        return (True,True,True,L)
    else:
        return (True,True,True,L)
def find_poly(L,m,n,m_m,n_n,num,direct,nb,direction,poly_x,poly_y):
    if check_edge(L,m,n,direct):
        neib_m=m_m+neibour[direct][0]
        neib_n=n_n+neibour[direct][1]
        if check_stop(L,m,n,neib_m,neib_n,direct)==3:
            if L[neib_m][neib_n]==1 or L[neib_m][neib_n]==100:
                L[neib_m][neib_n]=num
                direction.append(direct)
                poly_x.append(neib_m)
                poly_y.append(neib_n)
                if direct<=2:
                    direct+=5
                else:
                    direct=direct+4-7
                nb=0
                return find_poly(L,m,n,neib_m,neib_n,num,direct,nb,direction,poly_x,poly_y)
            else:
                if direct<7 and nb<=8:
                    neib_m-=neibour[direct][0]
                    neib_n-=neibour[direct][1]
                    direct+=1
                    nb+=1
                    return find_poly(L,m,n,neib_m,neib_n,num,direct,nb,direction,poly_x,poly_y)
                elif direct>=7 and nb<=8:
                    neib_m-=neibour[direct][0]
                    neib_n-=neibour[direct][1]
                    direct=0
                    nb+=1
                    return find_poly(L,m,n,neib_m,neib_n,num,direct,nb,direction,poly_x,poly_y)
                else:
                    nb=0
                    neib_m-=neibour[direct][0]
                    neib_n-=neibour[direct][1]
                    L[neib_m][neib_n]=100
                    if direction!=[]:
                        neib_mm,neib_nn,dirr,Lc=back_point(L,neib_m,neib_n,neib_m,neib_n,direction)
                        #display(Lc)
                        if neib_mm is not True and neib_nn is not True:
                            neib_m=neib_mm
                            neib_n=neib_nn
                            direct=dirr
                            L=copy.deepcopy(Lc)
                        else:
                            return(L,num-1,direction,poly_x,poly_y)
                    else:
                        return(L,num,direction,poly_x,poly_y)
                    return find_poly(L,m,n,neib_m,neib_n,num,direct,nb,direction,poly_x,poly_y)
        elif check_stop(L,m,n,neib_m,neib_n,direct)==1:
            if direct<7 and nb<=8:
                neib_m-=neibour[direct][0]
                neib_n-=neibour[direct][1]
                direct+=1
                nb+=1
                return find_poly(L,m,n,neib_m,neib_n,num,direct,nb,direction,poly_x,poly_y)
            elif direct>=7 and nb<=8:
                neib_m-=neibour[direct][0]
                neib_n-=neibour[direct][1]
                direct=0
                nb+=1
                return find_poly(L,m,n,neib_m,neib_n,num,direct,nb,direction,poly_x,poly_y)
            else:
                nb=0
                neib_m-=neibour[direct][0]
                neib_n-=neibour[direct][1]
                L[neib_m][neib_n]=100
                if direction!=[]:
                    neib_mm,neib_nn,dirr,Lc=back_point(L,neib_m,neib_n,neib_m,neib_n,direction)
                    #display(Lc)
                    if neib_mm is not True and neib_nn is not True:
                        neib_m=neib_mm
                        neib_n=neib_nn
                        direct=dirr
                        L=copy.deepcopy(Lc)
                    else:
                        return(L,num-1,direction,poly_x,poly_y)
                else:
                    return(L,num,direction,poly_x,poly_y)
                return find_poly(L,m,n,neib_m,neib_n,num,direct,nb,direction,poly_x,poly_y)
        elif check_stop(L,m,n,neib_m,neib_n,direct)==2:
            if len(direction)>1:
                nb=0
                direction.append(direct)
                return(L,num,direction,poly_x,poly_y)
            else:
                change_1(L,num)
                return(L,num-1,direction,poly_x,poly_y)
    return(L,num,direction,poly_x,poly_y)
    #display(L)
def change_1(L,num):
    for i in range(0,len(L)):
        for j in range(0,len(L[0])):
            if L[i][j]==num:
                L[i][j]=1
    return(L)
def change_100(L):
    for i in range(0,len(L)):
        for j in range(0,len(L[0])):
            if L[i][j]==100:
                L[i][j]=1
    return(L)
def colour_shapes(L,num):
    direction=[]
    poly_x=[]
    poly_y=[]
    dire=[]
    nb=0
    direct=0
    #num=2
    Lm=copy.deepcopy(L)
    for i in range(0,len(Lm)):
        for j in range(0,len(Lm[0])):
            if Lm[i][j]==1:
                Lm[i][j]=num
                poly_x.append(i)
                poly_y.append(j)
                Ls,num,dire,polyx,polyy=find_poly(Lm,i,j,i,j,num,direct,nb,direction,poly_x,poly_y)
                change_100(Ls)
                Lm=copy.deepcopy(Ls)
                #display(L)
                num+=1
                nb=0
                direct=0
                direction=[]
                poly_x=[]
                poly_y=[]
            elif Lm[i][j]==0:
                Lm[i][j]=0
    #print(polyx)
    return(Lm,num,dire,polyx,polyy)
def exist_num(num,L):
    for i in range(0,len(L)):
            for j in range(0,len(L[0])):
                if L[i][j]==num:
                    return True
                else:
                    continue
    return False
def poly(L,num):
    poly_p=copy.deepcopy(L)
    for i in range(0,len(L)):
        for j in range(0,len(L[0])):
            if L[i][j]==num:
                poly_p[i][j]=1
            else:
                poly_p[i][j]=0
    poly_pp,numm,dire,s,d=colour_shapes(poly_p,num)
    #print(s)
    return(poly_pp,dire,s,d)
def perimeter(L):
    num=2
    perimeter=[]
    while exist_num(num,L):
        poly_p,dire,m,n=poly(L,num)
        a=0
        b=0
        for i in range(0,len(dire)):
            if dire[i]==0 or dire[i]==2 or dire[i]==4 or dire[i]==6:
                a+=1
            else:
                b+=1
        perimeter_p1=("%.1f" %(0.4*a))
        if a!=0 and b==0:
            perimeter.append(str(perimeter_p1))
        elif a==0 and b!=0:
            perimeter.append(str(b)+'*sqrt(.32)')
        else:
            perimeter.append(str(perimeter_p1)+' + '+str(b)+'*sqrt(.32)')
        #print(perimeter)
        num+=1
    return(perimeter)
def area(L):
    num=2
    area1=[]
    areaf=[]
    while exist_num(num,L):
        poly_p,dire,px,py=poly(L,num)
        px.append(px[0])
        py.append(py[0])
        for i in range(0,len(px)):
            if px[i]==0:
                px[i]=0
            elif px[i]>0:
                px[i]=0.4*px[i]
        for j in range(0,len(py)):
            if py[j]==0:
                py[j]=0
            elif py[j]>0:
                py[j]=0.4*py[j]
        px.reverse()
        py.reverse()
        a=0
        b=0
        for i in range(0,len(px)-1):
            a+=px[i]*py[i+1]
            b+=py[i]*px[i+1]
        area_p="%.2f" %((a-b)/2)
        #area_p_f=round((a-b)/2,1)
        #area_p_f=float("%.2f" %((a-b)/2))
        area_p_f=float((a-b)/2)
        area1.append(area_p)
        areaf.append(area_p_f)
        num+=1
    return(area1,areaf)
def convex(L):
    num=2
    convex=[]
    while exist_num(num,L):
        poly_p,dire,px,py=poly(L,num)
        for i in range(0,len(dire)-1):
            if (dire[i+1]==dire[i]+5) or (dire[i+1]==dire[i]+6) or (dire[i+1]==dire[i]+7) or (dire[i]>2 and dire[i+1]==dire[i]+5-8) or (dire[i]>1 and dire[i+1]==dire[i]+6-8) or (dire[i]>0 and dire[i+1]==dire[i]+7-8):
                convex.append('no')
                break
            else:
                if i==len(dire)-2:
                    convex.append('yes')
                else:
                    continue
        num+=1
    return(convex)
def rotation(L):
    nb=1
    poly_p=copy.deepcopy(L)
    #90
    poly_rot=copy.deepcopy(L)
    flag1=False
    for i in range(0,len(poly_p)):
        for j in range(0,len(poly_p[0])):
            if j>=len(poly_p) or len(poly_p)-1-i>=len(poly_p[0]) or j<0 or len(poly_p)-1-i<0:
                flag1=True
                break
            else:
                poly_rot[j][len(poly_p)-1-i]=poly_p[i][j]
        if flag1:
            break
        else:
            continue
    if flag1==False:
        flag2=False
        for i in range(0,len(poly_p)):
            for j in range(0,len(poly_p[0])):
                if poly_rot[i][j]!=poly_p[i][j]:
                    nb-=1
                    flag2=True
                    break
                else:
                    continue
            if flag2:
                break
            else:
                continue
        nb+=1
    #print(nb)
    #180
    poly_rot=copy.deepcopy(L)
    flag1=False
    for i in range(0,len(poly_p)):
        for j in range(0,len(poly_p[0])):
            if len(poly_p)-1-i>=len(poly_p) or len(poly_p[0])-1-j>=len(poly_p[0]) or len(poly_p)-1-i<0 or len(poly_p[0])-1-j<0:
                flag1=True
                break
            else:
                poly_rot[len(poly_p)-1-i][len(poly_p[0])-1-j]=poly_p[i][j]
        if flag1:
            break
        else:
            continue
    if flag1==False:
        flag2=False
        for i in range(0,len(poly_p)):
            for j in range(0,len(poly_p[0])):
                if poly_rot[i][j]!=poly_p[i][j]:
                    nb-=1
                    flag2=True
                    break
                else:
                    continue
            if flag2:
                break
            else:
                continue
        nb+=1
    #print(nb)
    #270
    poly_rot=copy.deepcopy(L)
    flag1=False
    for i in range(0,len(poly_p)):
        for j in range(0,len(poly_p[0])):
            if i>=len(poly_p[0]) or len(poly_p)-1-j>=len(poly_p) or i<0 or len(poly_p)-1-j<0:
                flag1=True
                break
            else:
                poly_rot[len(poly_p)-1-j][i]=poly_p[i][j]
        if flag1:
            break
        else:
            continue
    if flag1==False:
        flag2=False
        for i in range(0,len(poly_p)):
            for j in range(0,len(poly_p[0])):
                if poly_rot[i][j]!=poly_p[i][j]:
                    nb-=1
                    flag2=True
                    break
                else:
                    continue
            if flag2:
                break
            else:
                continue
        nb+=1
    return nb
def nb_rotation(L):
    num=2
    rotat=[]
    while exist_num(num,L):
        point_x=[]
        point_y=[]
        cx=0
        cy=0
        nb=0
        poly_p,dire,px,py=poly(L,num)
        ax=min(px)
        bx=max(px)
        ay=min(py)
        by=max(py)
        poly_pp=[[0 for i in range(0,by-ay+1)] for i in range(0,bx-ax+1)]
        for i in range(ax,bx+1):
            for j in range(ay,by+1):
                poly_pp[i-ax][j-ay]=poly_p[i][j]
        nb=rotation(poly_pp)
        rotat.append(nb)
        num+=1
    return(rotat)
def in_poly(pointx,pointy,L,num):
    px,py=vertex(L,num)
    if pointx>min(px) and pointx<max(px) and pointy>min(py) and pointy<max(py):
        p1x=px[0]
        p1y=py[0]
        flag=False
        for i in range(1,len(px)):
            p2x=px[i]
            p2y=py[i]
            if (pointx==p1x and pointy==p1y) or (pointx==p2x and pointy==p2y):
                return True
            if (p2y<pointy and p1y>=pointy) or (p2y>=pointy and p1y<pointy):
                if (p2y==p1y):
                    x=(p1x+p2x)/2
                else:
                    x=p2x-(p2y-pointy)*(p2x-p1x)/(p2y-p1y)  
                if (x==pointx):
                    return True
                if (x>pointx):
                    flag=not flag 
                else:
                    pass
            else:
                pass
            p1x=p2x
            p1y=p2y
        if flag:
            return True
        else:
            return False
    else:
        return False
def vertex(L,num):
    poly_p,dire,px,py=poly(L,num)
    dire.append(dire[0])
    point_x=[]
    point_y=[]
    for i in range(0,len(dire)-1):
        if dire[i]!=dire[i+1]:
            if i<len(dire)-2:
                point_x.append(px[i+1]*0.4)
            else:
                point_x.append(px[i+1-len(px)]*0.4)
    for j in range(0,len(dire)-1):
        if dire[j]!=dire[j+1]:
            if j<len(dire)-2:
                point_y.append(py[j+1]*0.4)
            else:
                point_y.append(py[j+1-len(py)]*0.4)
    return(point_x,point_y)
def depth(L):
    num=2
    dep=[]
    ccx=[]
    ccy=[]
    nb=0
    while exist_num(num,L):
        cx=0
        cy=0
        point_x,point_y=vertex(L,num)
        for m in range(0,len(point_x)):
            cx+=point_x[m]
            cy+=point_y[m]
        cx=float("%.2f" %(cx/len(point_x)))
        cy=float("%.2f" %(cy/len(point_y)))
        #print(cx)
        ccx.append(cx)
        ccy.append(cy)
        num+=1
    area_p,area_f=area(L)
    for i in range(2,num):
        nb=0
        poly_numi,direi,pxi,pyi=poly(L,i)
        for j in range(2,num):
            poly_num,dire,px,py=poly(L,j)
            if float(area_p[j-2])>float(area_p[i-2]):
                if ccx[j-2]==ccx[i-2] and ccy[j-2]==ccy[i-2]:
                    if min(pxi)>min(px) and max(pxi)<max(px) and min(pyi)>min(py) and max(pyi)<max(py):
                        nb+=1
                elif in_poly(ccx[i-2],ccy[i-2],poly_num,j):
                    if min(pxi)>min(px) and max(pxi)<max(px) and min(pyi)>min(py) and max(pyi)<max(py):
                        nb+=1
        dep.append(nb)
    return dep
L_color,num,dire,x,y=colour_shapes(Ld,2)
if exist_num(1,L_color):
    print('Cannot get polygons as expected.')
    sys.exit()
per=perimeter(L_color)
are1,aref=area(L_color)
con=convex(L_color)
rot=nb_rotation(L_color)
dep=depth(L_color)
##no -print
if not pp:
    for i in range(0,len(per)):
        print('Polygon {}:'.format(i+1))
        print('    Perimeter: {}'.format(per[i]))
        print('    Area: {}'.format(are1[i]))
        print('    Convex: {}'.format(con[i]))
        print('    Nb of invariant rotations: {}'.format(rot[i]))
        print('    Depth: {}'.format(dep[i]))
##with -print
nd=0
Depth=[]
while nd<=max(dep):
    D=[]
    for i in range(0,len(dep)):
        if dep[i]==nd:
            D.append(i)
    Depth.append(D)
    nd+=1
color=[]
for i in range(0,len(aref)):
    if aref[i]==max(aref):
        color.append(0)
    elif aref[i]==min(aref):
        color.append(100)
    else:
        c=(max(aref)-aref[i])/(max(aref)-min(aref))*100
        #c=round(c,1)
        #c=round(c)
        if c-int(c)>=0.5:
            c=int(c)+1
        else:
            c=int(c)
        color.append(c)
np=2
px=[]
py=[]
while exist_num(np,L_color):
    point_x,point_y=vertex(L_color,np)
    length_x=len(point_x)
    point_x.insert(0,point_x[length_x-1])
    point_x.pop()
    length_y=len(point_y)
    point_y.insert(0,point_y[length_y-1])
    point_y.pop()
    px.append(point_x)
    py.append(point_y)
    np+=1
tex_file=str(filename)[:-4]+'.tex'
if pp:
    with open(tex_file, 'w') as latex_file:
        print('\\documentclass[10pt]{article}\n'
              '\\usepackage{tikz}\n'
              '\\usepackage[margin=0cm]{geometry}\n'
              '\\pagestyle{empty}\n'
              '\n'
              '\\begin{document}\n'
              '\n'
              '\\vspace*{\\fill}\n'
              '\\begin{center}\n'
              '\\begin{tikzpicture}[x=0.4cm, y=-0.4cm, thick, brown]', file=latex_file)
        print('\\draw[ultra thick] ({}, {}) -- ({}, {}) -- ({}, {}) -- ({}, {}) -- cycle;'.format(0,0,len(Ld[0])-1,0,len(Ld[0])-1,len(Ld)-1,0,len(Ld)-1),file=latex_file)
        for n in range(0,nd):
            print('%Depth {}'.format(n),file=latex_file)
            for i in range(0,len(Depth[n])):
                print('\\filldraw[fill=orange!{}!yellow] '.format(color[Depth[n][i]]),end='',file=latex_file)
                for m in range(0,len(px[Depth[n][i]])):
                    print('({}, {}) -- '.format(round(py[Depth[n][i]][m]/0.4),round(px[Depth[n][i]][m]/0.4)),end='',file=latex_file)
                print('cycle;',file=latex_file)
        print('\\end{tikzpicture}\n'
              '\\end{center}\n'
              '\\vspace*{\\fill}\n'
              '\n'
              '\\end{document}',file=latex_file)
