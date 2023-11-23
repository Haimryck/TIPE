import random
import matplotlib.pyplot as plt
import numpy as np

#creer un code, check la reponse, afficher les indices

C=['A','B','C','D','E','F','G','H','I','J','K','L']

def gen_code(size,color):  #generation de code de taille:"size" et de nombre de couleurs:"color"
    L=[]
    for i in range(0,size):
        L.append(C[random.randint(0,color-1)])
    return L

#print(gen_code(4,6))

def guess_check(secret_code,guess):
    good=0       #bien placé/mal placé
    bad=0
    newcode=secret_code.copy()
    for i in range(0,len(secret_code)):
        if guess[i]==secret_code[i]:
            good = good +1
            if newcode[i]==1:
                bad = bad -1
                for j in range(i+1,len(secret_code)):
                    if guess[i]==newcode[j]:
                        bad = bad +1
                        newcode[j]=1
                        break
            newcode[i]=0
        else:
            for j in range(0,len(secret_code)):
                if guess[i]==newcode[j]:
                    bad = bad +1
                    newcode[j]=1
                    break
    return (good,bad)

#print(guess_check(['H', 'E', 'G', 'E'],['E','E','G','G']))

def jouer(a,b,c):
    code=gen_code(a,b)
    a=0
    b=0
    guesses=[0]
    while a<c:
        print("Turn: ",a)
        guess=input("What's your guess?").split(' ')
        checked=guess_check(code,guess)
        for i in range(0,len(guesses)-1):
            if guess==guesses[i]:
                print("Already played...")
                b=1
        if checked==(len(code),0):
            return "Well played!"
        elif b==0:
            print(checked)
            guesses.append(guess)
            a=a+1
        b=0
    return "Oh no...you go out of turns...",code

'''
def all_code0(size,color):
    L=[]
    return all_code1(size,color,L)


def all_code1(size,color,L):
    size=size-1
    M=[]
    if size==0:
        return L
    else:
        for i in range(0,color):
            all_code1(size,color,L)'''

'''def all_code(size,color): ###pb de size
    L=[]
    for i in range(0,color):
        for j in range(0,color):
            for f in range(0,color):
                for h in range(0,color):
                    L.append([C[i],C[j],C[f],C[h]])
    return L'''


def efficacity_test_grosbg(size,color,List):
    allcode=List(size,color)
    L=[0]*12
    for i in range(0,len(allcode)):
        turn=grosbg(allcode[i],allcode)
        L[turn-1]+=1
    total=0
    moy=0
    for i in range(0,len(L)):
        total+=L[i]
        moy+=(i+1)*L[i]
    moy=moy/total
    return (L,total,"moy:",moy)



##################################################################################
'''Premier programme de résolution, choix aléatoire parmis les codes plausibles'''
##################################################################################

def grosbg0(size,color):
    secret_code=gen_code(size,color)
    print(secret_code)
    return grosbg(secret_code,all_code(size,color))


def grosbg(secret_code,all_code):
    L=all_code.copy()
    first=L[0]
    M=[]
    a=1
    while guess_check(secret_code,first) != (len(first),0):
#        print(first)
#        print(guess_check(secret_code,first))
        for i in range(0,len(L)):
            if guess_check(L[i],first)==guess_check(secret_code,first):
                M.append(L[i])
        L=M.copy()
        M=[]
        first=L[0]
        a=a+1
    return a



###########################################################################
'''Deuxième programme de résolution en utilisant une stratégie gloutonne'''
###########################################################################

#on peut réutiliser grosbg mais en triant allcode selon l'entropie, le programme va donc choisir le code le plus entropique

def tri_entropy(size,color):
    code=all_code(size,color)
    C=[[] for i in range(size)]
    for i in range(len(code)):
        A=[]
        for j in range(size):
            if code[i][j] not in A:
                A.append(code[i][j])
        a=len(A)
        C[size-a].append(code[i])
    return [item for sublist in C for item in sublist]


#########################################################
'''Troisième programme de résulotion utilisant min/max'''
#########################################################



def min_max_ini(size,color):
    allcode=all_code(size,color)
    maxresp={}
    respmax={}
    a=0
    for i in range(size+1):
        for j in range(size-i+1):
            if i!=size-1 or j!=1:
                maxresp[(i,j)]=a
                respmax[a]=(i,j)
                a+=1
    depth=0
    joueur=True
    position=1
    return min_max(position,depth,joueur,allcode,maxresp)[0]

def min_max(code,depth,joueur,allcode,maxresp):
    if len(allcode)==1:
        return [depth+1,allcode[0]]
    elif len(allcode)==0:
        return [0]

    if joueur==False:
        m=[0]
        m.append(code)
        Resp=[[] for i in range(len(maxresp))]
        for i in range(len(allcode)):
            Resp[maxresp[guess_check(allcode[i],code)]].append(allcode[i])
        for j in range(len(Resp)-1):
            m.append(min_max(None,depth,True,Resp[j],maxresp))
        m.append([depth,code])
        for j in range(2,len(m)):
            if m[j][0]>m[0]:
                m[0]=m[j][0]

    elif joueur==True:
        m=[np.inf]
        for i in range(len(allcode)):
            m.append(min_max(allcode[i],depth+1,False,allcode,maxresp))
        for j in range(1,len(m)):
            if m[j][0]<m[0]:
                m[0]=m[j][0]
    return m
































###########################################################
'''Affichage des résultats des programmes dans un graphe'''
###########################################################


cycle_color=('#FF0000','#EF00FF','#2B00FF','#00E6FF','#00FF2B','#FFFF00','#B0D0D3','#C08497','#F7AF9D','#000000')

def affichage_color_simple(size,color_max):
    x=[i for i in range(1,13)]
    lab=[]
    for i in range(1,color_max+1):
        result=efficacity_test_grosbg(size,i,all_code)
        lab.append(str(i)+" colors code, moy: "+str(round(result[-1],2)))
        plt.plot(x,np.array(result[0])/result[1]*100,color=cycle_color[i-1],marker='+')
        plt.legend(lab)
    plt.xlabel('Number of guesses')
    plt.ylabel('%')
    plt.title('simple strategy for a size of '+str(size))
    plt.show()
    return None

def affichage_color_entropy(size,color_max):
    x=[i for i in range(1,13)]
    lab=[]
    for i in range(1,color_max+1):
        result*=efficacity_test_grosbg(size,i,tri_entropy)
        lab.append(str(i)+" colors code, moy: "+str(round(result[-1],2)))
        plt.plot(x,np.array(result[0])/result[1]*100,color=cycle_color[i-1],marker='+')
        plt.legend(lab)
    plt.xlabel('Number of guesses')
    plt.ylabel('%')
    plt.title('entropy strategy for a size of '+str(size))
    plt.show()
    return None



def affichage_size_simple(color,size_max):
    x=[i for i in range(1,13)]
    lab=[]
    for i in range(1,size_max+1):
        result=efficacity_test_grosbg(i,color,all_code)
        lab.append(str(i)+" size code, moy: "+str(round(result[-1],2)))
        plt.plot(x,np.array(result[0])/result[1]*100,color=cycle_color[i-1],marker='+')
        plt.legend(lab)
    plt.xlabel('Number of guesses')
    plt.ylabel('%')
    plt.title('simple strategy for '+str(color)+' colors')
    plt.show()
    return None

def affichage_size_entropy(color,size_max):
    x=[i for i in range(1,13)]
    lab=[]
    for i in range(1,size_max+1):
        result=efficacity_test_grosbg(i,color,tri_entropy)
        lab.append(str(i)+" size code, moy: "+str(round(result[-1],2)))
        plt.plot(x,np.array(result[0])/result[1]*100,color=cycle_color[i-1],marker='+')
        plt.legend(lab)
    plt.xlabel('Number of guesses')
    plt.ylabel('%')
    plt.title('entropy strategy for '+str(color)+' colors')
    plt.show()
    return None

############################################################
'''Nouveau all_code qui prend en compte la taille du code'''
############################################################

def all_code(size,color):
    m=[[] for i in range(color**size)]
    size0=size
    return new_all_code(size,color,m,size0)

def new_all_code(size,color,m,size0):
    if size<=0:
        return m
    a=0
    n=len(m)
    diff=n//(color**(size0-size+1))
    b=diff
    while a<n:
        for i in range(color):
            for j in range(a,b):
                m[j].append(C[i])
            a,b=b,b+diff
    return new_all_code(size-1,color,m,size0)











