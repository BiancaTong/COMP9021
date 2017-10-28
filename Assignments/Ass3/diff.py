## written by Bianca Tong for comp9021 Ass3 ##
import sys
import re
class DiffCommandsError(Exception):
    def __init__(self,message):
        self.message=message
class DiffCommands():
    def __init__(self,x):
        if not self._check_correct_commands(x):
            raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
            return
        self.x=x
        return
    def __str__(self):
        file=[]
        with open(self.x) as fn:
            for line in fn:
                line=line[:-1]
                file.append(line)
            return '\n'.join(file)
    def list_diff(self):
        file=[]
        with open(self.x) as fn:
            for line in fn:
                file.append(line)
        return file
    def _check_correct_commands(self,file_name):
        file=[]
        file_end=[]
        with open(file_name) as fn:
            for line in fn:
                a=re.match(r'^(\d)+(?:,(\d+))?d(\d+)$|^(\d)+?a(\d)+(?:,(\d+))?$|^(\d)+(?:,(\d+))?c(\d)+(?:,(\d+))?$',line)
                if a is None:
                    return False
                b=re.match(r'1+(?:,(\d+))?d1',line)
                if b is not None:
                    return False
                file.append(line)
        for i in range(0,len(file)):
            filef=[]
            S=file[i][0]
            for m in range(1,len(file[i])):
                if file[i][m].isdigit():
                    if S!=0:
                        S=S+file[i][m]
                    else:
                        S=file[i][m]
                elif file[i][m]=='a' or file[i][m]=='d' or file[i][m]=='c':
                    filef.append(S)
                    filef.append(file[i][m])
                    break
                elif file[i][m]==',':
                    filef.append(S)
                    S=0
            S=file[i][m+1]
            for n in range(m+2,len(file[i])):
                if file[i][n].isdigit():
                    if S!=0:
                        S=S+file[i][n]
                    else:
                        S=file[i][n]
                elif file[i][n]==',':
                    filef.append(S)
                    S=0
                elif file[i][n]=='\n':
                    filef.append(S)
                    break
            file_end.append(filef)
        for i in range(0,len(file_end)):
            if 'c' in file_end[i]:
                ci=file_end[i].index('c')
                if i>0 and i<len(file_end)-1:
                    if 'd' in file_end[i-1]:
                        di=file_end[i-1].index('d')
                        if int(file_end[i][ci-1])-1==int(file_end[i-1][di-1]):
                            return False
                    if 'd' in file_end[i+1]:
                        di=file_end[i+1].index('d')
                        if int(file_end[i][ci-1])+1==int(file_end[i+1][di-1]):
                            return False
                if i==0:
                    if 'd' in file_end[i+1]:
                        di=file_end[i+1].index('d')
                        if int(file_end[i][ci-1])+1==int(file_end[i+1][di-1]):
                            return False
                if i==len(file_end)-1:
                    if 'd' in file_end[i-1]:
                        di=file_end[i-1].index('d')
                        if int(file_end[i][ci-1])-1==int(file_end[i-1][di-1]):
                            return False
                num=0
                for j in range(0,i):
                    if 'd' in file_end[j]:
                        dj=file_end[j].index('d')
                        if int(dj)==1:
                            num-=1
                        elif int(dj)==2:
                            num-=int(file_end[j][1])-int(file_end[j][0])+1
                    if 'a' in file_end[j]:
                        aj=file_end[j].index('a')
                        if len(file_end[j])==3:
                            num+=1
                        elif len(file_end[j])==4:
                            num+=int(file_end[j][3])-int(file_end[j][2])+1
                    if 'c' in file_end[j]:
                        cj=file_end[j].index('c')
                        if int(cj)==1 and len(file_end[j])==4:
                            num+=int(file_end[j][3])-int(file_end[j][2])
                        elif int(cj)==2 and len(file_end[j])==4:
                            num-=int(file_end[j][1])-int(file_end[j][0])
                        elif int(cj)==2 and len(file_end[j])==5:
                            num+=(int(file_end[j][4])-int(file_end[j][3]))-(int(file_end[j][1])-int(file_end[j][0]))
                if int(file_end[i][0])+num!=int(file_end[i][ci+1]):
                    return False
        return True

class OriginalNewFiles():
    def __init__(self,f1,f2):
        self.f1=f1
        self.f2=f2
        return
    def is_a_possible_diff(self,diff_file):
        diff=[]
        f_old=[]
        f_new=[]
        with open(self.f1)as fn_old:
            for line in fn_old:
                f_old.append(line)
        with open(self.f2)as fn_new:
            for line in fn_new:
                f_new.append(line)
        file=diff_file.list_diff()
        for i in range(0,len(file)):
            filef=[]
            S=file[i][0]
            for m in range(1,len(file[i])):
                if file[i][m].isdigit():
                    if S!=0:
                        S=S+file[i][m]
                    else:
                        S=file[i][m]
                elif file[i][m]=='a' or file[i][m]=='d' or file[i][m]=='c':
                    filef.append(S)
                    filef.append(file[i][m])
                    break
                elif file[i][m]==',':
                    filef.append(S)
                    S=0
            S=file[i][m+1]
            for n in range(m+2,len(file[i])):
                if file[i][n].isdigit():
                    if S!=0:
                        S=S+file[i][n]
                    else:
                        S=file[i][n]
                elif file[i][n]==',':
                    filef.append(S)
                    S=0
                elif file[i][n]=='\n':
                    filef.append(S)
                    break
            diff.append(filef)
        for i in range(0,len(diff)):
            if 'd' in diff[i]:
                dj=diff[i].index('d')
                if len(f_old)<=int(diff[i][0])-2 or len(f_new)<=int(diff[i][-1])-1:
                    return False
                if f_old[int(diff[i][0])-2]!=f_new[int(diff[i][-1])-1]:
                    if int(diff[i][0])-1==0:
                        if f_old[int(diff[i][dj-1])]!=f_new[int(diff[i][-1])-1]:
                            return False
                    else:
                        return False
            if 'a' in diff[i]:
                if len(f_old)<=int(diff[i][0])-1 or len(f_new)<=int(diff[i][2])-2:
                    return False
                if f_old[int(diff[i][0])-1]!=f_new[int(diff[i][2])-2]:
                    if int(diff[i][0])-1==0:
                        if f_old[0]!=f_new[int(diff[i][2])+2]:
                            return False
            if 'c' in diff[i]:
                ci=diff[i].index('c')
                if len(f_old)<=int(diff[i][0])-2 or len(f_new)<=int(diff[i][ci+1])-2:
                    return False
                if f_old[int(diff[i][0])-2]!=f_new[int(diff[i][ci+1])-2]:
                    return False
        return True
    def output_diff(self,diff_file):
        diff=[]
        old_file=[]
        new_file=[]
        with open(self.f1)as fn_old:
            for line in fn_old:
                old_file.append(line)
        with open(self.f2)as fn_new:
            for line in fn_new:
                new_file.append(line)
        file=diff_file.list_diff()
        for i in range(0,len(file)):
            filef=[]
            S=file[i][0]
            for m in range(1,len(file[i])):
                if file[i][m].isdigit():
                    if S!=0:
                        S=S+file[i][m]
                    else:
                        S=file[i][m]
                elif file[i][m]=='a' or file[i][m]=='d' or file[i][m]=='c':
                    filef.append(S)
                    filef.append(file[i][m])
                    break
                elif file[i][m]==',':
                    filef.append(S)
                    S=0
            S=file[i][m+1]
            for n in range(m+2,len(file[i])):
                if file[i][n].isdigit():
                    if S!=0:
                        S=S+file[i][n]
                    else:
                        S=file[i][n]
                elif file[i][n]==',':
                    filef.append(S)
                    S=0
                elif file[i][n]=='\n':
                    filef.append(S)
                    break
            diff.append(filef)
        for j in range(0,len(file)):
            if 'd' in file[j]:
                print(file[j],end='')
                dj=diff[j].index('d')
                if int(dj)==1:
                    print('< '+old_file[int(diff[j][0])-1],end='')
                elif int(dj)==2:
                    for i in range(int(diff[j][0])-1,int(diff[j][1])):
                        print('< '+old_file[i],end='')
            if 'a' in file[j]:
                print(file[j],end='')
                aj=diff[j].index('a')
                if len(diff[j])==3:
                    print('> '+new_file[int(diff[j][2])-1],end='')
                elif len(diff[j])==4:
                    for i in range(int(diff[j][2])-1,int(diff[j][3])):
                        print('> '+new_file[i],end='')
            if 'c' in file[j]:
                print(file[j],end='')
                cj=diff[j].index('c')
                if int(cj)==1 and len(diff[j])==3:
                    print('< '+old_file[int(diff[j][0])-1],end='')
                    print('---')
                    print('> '+new_file[int(diff[j][2])-1],end='')
                elif int(cj)==1 and len(diff[j])==4:
                    print('< '+old_file[int(diff[j][0])-1],end='')
                    print('---')
                    for i in range(int(diff[j][2])-1,int(diff[j][3])):
                        print('> '+new_file[i],end='')
                elif int(cj)==2 and len(diff[j])==4:
                    for i in range(int(diff[j][0])-1,int(diff[j][1])):
                        print('< '+old_file[i],end='')
                    print('---')
                    print('> '+new_file[int(diff[j][3])-1],end='')
                elif int(cj)==2 and len(diff[j])==5:
                    for i in range(int(diff[j][0])-1,int(diff[j][1])):
                        print('< '+old_file[i],end='')
                    print('---')
                    for i in range(int(diff[j][3])-1,int(diff[j][4])):
                        print('> '+new_file[i],end='')
        return
    def output_unmodified_from_original(self,diff_file):
        diff=[]
        old_file=[]
        new_file=[]
        num=0
        with open(self.f1)as fn_old:
            for line in fn_old:
                old_file.append(line)
        with open(self.f2)as fn_new:
            for line in fn_new:
                new_file.append(line)
        file=diff_file.list_diff()
        for i in range(0,len(file)):
            filef=[]
            S=file[i][0]
            for m in range(1,len(file[i])):
                if file[i][m].isdigit():
                    if S!=0:
                        S=S+file[i][m]
                    else:
                        S=file[i][m]
                elif file[i][m]=='a' or file[i][m]=='d' or file[i][m]=='c':
                    filef.append(S)
                    filef.append(file[i][m])
                    break
                elif file[i][m]==',':
                    filef.append(S)
                    S=0
            S=file[i][m+1]
            for n in range(m+2,len(file[i])):
                if file[i][n].isdigit():
                    if S!=0:
                        S=S+file[i][n]
                    else:
                        S=file[i][n]
                elif file[i][n]==',':
                    filef.append(S)
                    S=0
                elif file[i][n]=='\n':
                    filef.append(S)
                    break
            diff.append(filef)
        for j in range(0,len(diff)):
            if 'd' in diff[j]:
                dj=diff[j].index('d')
                if int(dj)==1:
                    del old_file[int(diff[j][0])-1+num]
                    old_file.insert(int(diff[j][0])-1+num,'...\n')
                elif int(dj)==2:
                    del old_file[int(diff[j][0])-1+num:int(diff[j][1])+num]
                    old_file.insert(int(diff[j][0])-1+num,'...\n')
                    num-=int(diff[j][1])-int(diff[j][0])
            if 'c' in diff[j]:
                cj=diff[j].index('c')
                if int(cj)==1 and len(diff[j])==3:
                    del old_file[int(diff[j][0])-1+num]
                    old_file.insert(int(diff[j][0])-1+num,'...\n')
                elif int(cj)==1 and len(diff[j])==4:
                    del old_file[int(diff[j][0])-1+num]
                    old_file.insert(int(diff[j][0])-1+num,'...\n')
                elif int(cj)==2 and len(diff[j])==4:
                    del old_file[int(diff[j][0])-1+num:int(diff[j][1])+num]
                    old_file.insert(int(diff[j][0])-1+num,'...\n')
                    num-=int(diff[j][1])-int(diff[j][0])
                elif int(cj)==2 and len(diff[j])==5:
                    del old_file[int(diff[j][0])-1+num:int(diff[j][1])+num]
                    old_file.insert(int(diff[j][0])-1+num,'...\n')
                    num-=int(diff[j][1])-int(diff[j][0])
        for i in range(0,len(old_file)):
            print(old_file[i],end='')
        return
    def output_unmodified_from_new(self,diff_file):
        diff=[]
        old_file=[]
        new_file=[]
        num=0
        with open(self.f1)as fn_old:
            for line in fn_old:
                old_file.append(line)
        with open(self.f2)as fn_new:
            for line in fn_new:
                new_file.append(line)
        file=diff_file.list_diff()
        for i in range(0,len(file)):
            filef=[]
            S=file[i][0]
            for m in range(1,len(file[i])):
                if file[i][m].isdigit():
                    if S!=0:
                        S=S+file[i][m]
                    else:
                        S=file[i][m]
                elif file[i][m]=='a' or file[i][m]=='d' or file[i][m]=='c':
                    filef.append(S)
                    filef.append(file[i][m])
                    break
                elif file[i][m]==',':
                    filef.append(S)
                    S=0
            S=file[i][m+1]
            for n in range(m+2,len(file[i])):
                if file[i][n].isdigit():
                    if S!=0:
                        S=S+file[i][n]
                    else:
                        S=file[i][n]
                elif file[i][n]==',':
                    filef.append(S)
                    S=0
                elif file[i][n]=='\n':
                    filef.append(S)
                    break
            diff.append(filef)
        for j in range(0,len(diff)):
            if 'a' in diff[j]:
                aj=diff[j].index('a')
                if len(diff[j])==3:
                    del new_file[int(diff[j][2])-1+num]
                    new_file.insert(int(diff[j][2])-1+num,'...\n')
                elif len(diff[j])==4:
                    del new_file[int(diff[j][2])-1+num:int(diff[j][3])+num]
                    new_file.insert(int(diff[j][2])-1+num,'...\n')
                    num-=int(diff[j][3])-int(diff[j][2])
            if 'c' in diff[j]:
                cj=diff[j].index('c')
                if int(cj)==1 and len(diff[j])==3:
                    del new_file[int(diff[j][2])-1+num]
                    new_file.insert(int(diff[j][2])-1+num,'...\n')
                elif int(cj)==1 and len(diff[j])==4:
                    del new_file[int(diff[j][2])-1+num:int(diff[j][3])-1+num]
                    new_file.insert(int(diff[j][2])-1+num,'...\n')
                    num-=int(diff[j][3])-int(diff[j][2])
                elif int(cj)==2 and len(diff[j])==4:
                    del new_file[int(diff[j][3])-1+num]
                    new_file.insert(int(diff[j][3])-1+num,'...\n')
                elif int(cj)==2 and len(diff[j])==5:
                    del new_file[int(diff[j][3])-1+num:int(diff[j][4])+num]
                    new_file.insert(int(diff[j][3])-1+num,'...\n')
                    num-=int(diff[j][4])-int(diff[j][3])
        for i in range(0,len(new_file)):
            print(new_file[i],end='')
        return
    def get_all_diff_commands(self):
        pass
if __name__ == '__main__':
    import doctest
    doctest.testmod()
