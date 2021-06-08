import numpy as np
import random
from PIL import Image

def map_generator(m:int=9, n:int=5,block_size:int=4):
    """ Generate random map
        :param:
            m (int): number of rows
            n (int): number of columns
            block_size (int): maximum size of block
        :return:
            (Vector{Vector}) game map"""
    if m<2 or n<2:
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
                                if ile == block_size:
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


def map_background_generation(m:int=9, n:int=5,block_size:int=4):
    """ Generate random map and its image
        :param:
            m (int): number of rows
            n (int): number of columns
            block_size (int): maximum size of block
        :return:
            (Vector) vector with game map in vector of vector in first positon and PIL image of map on secound positon """
    thickness=6
    line_width=2
    maps=map_generator(m,n,block_size)


    im= Image.new("RGB", (len(maps)*16, len(maps[0])*16), "#000000")

    for i in range(1,len(maps[0])-1):
        for j in range(1,len(maps)-1):
            if maps[j][i]==1:
                if maps[j+1][i] == 1 and maps[j+1][i+1] == 0 and maps[j][i+1] == 0:
                    im.paste((0,0,190)  ,((j+1)*16-8    ,(i+1)*16+thickness-1 ,(j+1)*16+8      ,(i+1)*16+thickness+line_width-1))
                if maps[j+1][i] == 1 and maps[j+1][i-1] == 0 and maps[j][i-1] == 0:
                    im.paste((0,0,190)  ,((j+1)*16-8    ,i*16-thickness-1 ,(j+1)*16+8      ,i*16-thickness+line_width-1))
                if maps[j][i+1] == 1 and maps[j+1][i+1] == 0 and maps[j+1][i] == 0:
                    im.paste((0,0,190)  ,((j+1)*16+thickness-1    ,(i+1)*16-8 , (j+1)*16+thickness+line_width-1      ,(i+1)*16+8))
                if maps[j][i+1] == 1 and maps[j-1][i+1] == 0 and maps[j-1][i] == 0:
                    im.paste((0,0,190)  ,(j*16-thickness-1    ,(i+1)*16-8 ,j*16-thickness+line_width-1      ,(i+1)*16+8))

    for i in range(len(maps[0])-1):
        for j in range(len(maps)-1):
            shape=[[maps[j][i],maps[j][i+1]],[maps[j+1][i],maps[j+1][i+1]]]
            if shape==[[1,1],[1,0]]:
                im.paste((0,0,190)  , ( (j+1)*16+thickness, (i+1)*16+thickness, (j+1)*16+thickness+3, (i+1)*16+thickness+3))
                im.paste((0,0,0)  , ( (j+1)*16+thickness+2, (i+1)*16+thickness+2, (j+1)*16+thickness+3, (i+1)*16+thickness+3))
                im.paste((0,0,0)  , ( (j+1)*16+thickness, (i+1)*16+thickness, (j+1)*16+thickness+1, (i+1)*16+thickness+1))
            if shape==[[1,1],[0,1]]:
                im.paste((0,0,190)  , ( (j+1)*16+thickness, i*16+thickness+1, (j+1)*16+thickness+3, i*16+thickness+4))
                im.paste((0,0,0)  , ( (j+1)*16+thickness+2, i*16+thickness+1, (j+1)*16+thickness+3, i*16+thickness+2))
                im.paste((0,0,0)  , ( (j+1)*16+thickness, i*16+thickness+3, (j+1)*16+thickness+1, i*16+thickness+4))
            if shape==[[0,1],[1,1]]:
                im.paste((0,0,190)  , ( j*16+thickness+1, i*16+thickness+1, j*16+thickness+4, i*16+thickness+4))
                im.paste((0,0,0)  , ( j*16+thickness+3, i*16+thickness+3, j*16+thickness+4, i*16+thickness+4))
                im.paste((0,0,0)  , ( j*16+thickness+1, i*16+thickness+1, j*16+thickness+2, i*16+thickness+2))
            if shape==[[1,0],[1,1]]:
                im.paste((0,0,190)  , ( j*16+thickness+1, (i+1)*16+thickness, j*16+thickness+4, (i+1)*16+thickness+3))
                im.paste((0,0,0)  , ( j*16+thickness+1, (i+1)*16+thickness+2, j*16+thickness+2, (i+1)*16+thickness+3))
                im.paste((0,0,0)  , ( j*16+thickness+3, (i+1)*16+thickness, j*16+thickness+4, (i+1)*16+thickness+1))

            if shape==[[0,0],[0,1]]: 
                im.paste((0,0,190)  , ( j*16+thickness+3, i*16+thickness*2, j*16+thickness+5, (i+1)*16+thickness+4))
                im.paste((0,0,190)  , ( j*16+thickness*2, i*16+thickness+3, (j+1)*16+thickness+3, i*16+thickness*2-1))
                im.paste((0,0,190)  , ( j*16+thickness*2-2, i*16+thickness*2-2, j*16+thickness*2+1, i*16+thickness*2+1))
                im.paste((0,0,0)  , ( j*16+thickness*2-2, i*16+thickness*2-2, j*16+thickness*2-1, i*16+thickness*2-1))
                im.paste((0,0,0)  , ( j*16+thickness*2, i*16+thickness*2, j*16+thickness*2+1, i*16+thickness*2+1))
            if shape==[[0,0],[1,0]]: 
                im.paste((0,0,190)  , ( j*16+thickness+3, i*16+thickness, j*16+thickness+5, (i+1)*16+thickness-2))
                im.paste((0,0,190)  , ( (j+1)*16-thickness+2, (i+1)*16+thickness-1, (j+1)*16+thickness+3, (i+1)*16+thickness+1))
                im.paste((0,0,190)  , ( j*16+thickness+4, (i+1)*16+thickness-3, j*16+thickness+7, (i+1)*16+thickness))
                im.paste((0,0,0)  , ( j*16+thickness+6, (i+1)*16+thickness-3, j*16+thickness+7, (i+1)*16+thickness-2,))
                im.paste((0,0,0)  , ( j*16+thickness+4, (i+1)*16+thickness-1, j*16+thickness+5, (i+1)*16+thickness))
            if shape==[[1,0],[0,0]]: 
                im.paste((0,0,190)  , ( (j+1)*16+thickness-1, i*16+thickness, (j+1)*16+thickness+1, (i+1)*16+thickness-2))
                im.paste((0,0,190)  , ( j*16+thickness*2-4, (i+1)*16+thickness-1, (j+1)*16+thickness-2, (i+1)*16+thickness+1))
                im.paste((0,0,190)  , ( (j+1)*16+thickness-3, (i+1)*16+thickness-3, (j+1)*16+thickness, (i+1)*16+thickness))
                im.paste((0,0,0)    , ( (j+1)*16+thickness-3, (i+1)*16+thickness-3, (j+1)*16+thickness-2, (i+1)*16+thickness-2))
                im.paste((0,0,0)    , ( (j+1)*16+thickness-1, (i+1)*16+thickness-1, (j+1)*16+thickness, (i+1)*16+thickness))
            if shape==[[0,1],[0,0]]: 
                im.paste((0,0,190)  , ( (j+1)*16-thickness-2, (i+1)*16-thickness-1, (j+1)*16+thickness-2, (i+1)*16-thickness+1))
                im.paste((0,0,190)  , ( (j+1)*16+thickness-1, (i+1)*16-thickness+2, (j+1)*16+thickness+1, (i+1)*16+thickness+2))
                im.paste((0,0,190)  , ( (j+1)*16+thickness-3, (i+1)*16-thickness, (j+1)*16+thickness, (i+1)*16-thickness+3))
                im.paste((0,0,0)    , ( (j+1)*16+thickness-3, (i+1)*16-thickness+2, (j+1)*16+thickness-2, (i+1)*16-thickness+3))
                im.paste((0,0,0)    , ( (j+1)*16+thickness-1,  (i+1)*16-thickness, (j+1)*16+thickness,  (i+1)*16-thickness+1))


    j=m//3*3+2
    i=n*3
    im.paste((150,150,150)  , ( j*16+thickness-2, (i-1)*16, j*16+thickness+2, (i+1)*16))

    im = im.transpose(Image.ROTATE_270)
    #im.show()

    return [im,maps]

    