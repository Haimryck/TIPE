import random

#creer un code, check la reponse, afficher les indices

C=['A','B','C','D','E','F','G','H','I','J']

def gen_code(size,color):  #generation de code de taille:"size" et de nombre de couleurs:"color"
    L=[]
    for i in range(0,size):
        L.append(C[random.randint(0,color-1)])
    return L

#print(gen_code(4,6))

def guess_check(secret_code,guess):
    good=0       #bien placé/mal placé
    bad=0
    a=0          #pour éviter les doublons
    newcode=secret_code.copy()
    for i in range(0,len(secret_code)):
        if guess[i]==secret_code[i]:
            good = good +1
            if newcode[i]==1:
                bad = bad -1
                for j in range(i+1,len(secret_code)):
                    if guess[i]==newcode[j] and a==0:
                        bad = bad +1
                        a=1
                        newcode[j]=1
                    a=0
            newcode[i]=0
        else:
            for j in range(0,len(secret_code)):
                if guess[i]==newcode[j] and a==0:
                    bad = bad +1
                    a=1
                    newcode[j]=1
            a=0
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

def all_code(color): ###pb de size
    L=[]
    for i in range(0,color):
        for j in range(0,color):
            for f in range(0,color):
                for h in range(0,color):
                    L.append([C[i],C[j],C[f],C[h]])
    return L
            

def efficacity_test(size,color,prog): ###pb de longueur des tours max
    allcode=all_code(color)
    L=[0]*10
    for i in range(0,len(allcode)):
        turn=grosbg(size,color,allcode[i],allcode)
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
    return grosbg(size,color,secret_code,all_code(color))

 
def grosbg(size,color,secret_code,all_code): ###size pour first nn defini
    L=all_code.copy()
    first=L[0]
    M=[]
    a=1
    while guess_check(secret_code,first) != (size,0):
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


def tri_entropie(L):
    if len(L)==1:
        return L
    else:
        n=len(L)//2
        l1=L[:n]
        l2=L[n:]
        return fusion(tri_entropie(l1),tri_entropie(l2))
        
def fusion(l1,l2):
    n=len(l1)+len(l2)
    i=0
    j=0
    L=[]
    for h in range(n):
        if len(l1)==i:
            L.append(l2[j])
            j+=1
        elif len(l2)==j:
            L.append(l1[i])
            i+=1
        elif l1[i]<l2[j]:
            L.append(l1[i])
            i+=1
        else:
            L.append(l2[j])
            j+=1
    return L















