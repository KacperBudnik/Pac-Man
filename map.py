import numpy as np
import random

def map_generator(m:int=9, n:int=5):

    if m<5 or n<3:
        print("błędne wartości przyjmuję m=9, n=5")
        m=9
        n=5

    map=[[0 for _ in range(n)] for _ in range(m)]
    map[m//3][1]=map[m//3+1][1]=map[m//3][0]=map[m//3+1][0]=-1

    kolejny=1
    for i in np.random.permutation(range(m)):
        for j in np.random.permutation(range(n)):
            if map[i][j]==0:
                map[i][j]=kolejny
                g=[[i,j]]
                ile=1
                for _ in range(15):
                    h=g[random.randrange(0,len(g))]
                    for k in np.random.permutation([[1,0],[-1,0],[0,1],[0,-1]]):
                        if 0<=h[0]+k[0]<m and 0<=h[1]+k[1]<n:
                            if map[h[0]+k[0]][h[1]+k[1]]==0:
                                map[h[0]+k[0]][h[1]+k[1]]=kolejny
                                g.append([h[0]+k[0],h[1]+k[1]])
                                ile+=1
                                if ile == 4:
                                    break
                    else:
                        continue
                    break
            kolejny+=1


    maps=[]
    for i in map:
        maps.append([])
        maps[-1]=i[::-1]+i[1:]

        
    #plt.imshow(maps,cmap='hot')
    #plt.show()

    map=[[0 for _ in range(3*(2*n-1)+2)] for _ in range(3*m+2)]
    map=[[0 for _ in range(3*(2*n-1)+1+2)] for _ in range(3*m+2+1)]

    for i in range(1,3*m+2+1-2):
        map[i][1]=map[i][3*(2*n-1)+1]=1
    for i in range(1,3*(2*n-1)+2):
        map[1][i]=map[3*m+1][i]=1


    for i in range(len(maps)-1):
        for j in range(len(maps[0])):
            if maps[i][j]!=maps[i+1][j]:
                map[1+3*i+3][1+3*j+1]=map[1+3*i+3][1+3*j+2]=map[1+3*i+3][1+3*j+3]=map[1+3*i+3][1+3*j]=1

    for i in range(len(maps)):
        for j in range(len(maps[0])-1):
            if maps[i][j]!=maps[i][j+1]:
                map[1+3*i][1+3*j+3]=map[1+3*i+1][1+3*j+3]=map[1+3*i+2][1+3*j+3]=1

    return map

    #plt.imshow(map,cmap='hot')
    #plt.show()







