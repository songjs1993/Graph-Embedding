'''
Reference implementation of node2vec. 

Author: Aditya Grover

For more details, refer to the paper:
node2vec: Scalable Feature Learning for Networks
Aditya Grover and Jure Leskovec 
Knowledge Discovery and Data Mining (KDD), 2016
'''

import argparse
import numpy as np
import networkx as nx
from gensim.models import Word2Vec
# from numpy import *

def make_swiss_roll(n_samples=100, noise=0.0, random_state=None):  
    #Generate a swiss roll dataset.  
    t = 1.5 * np.pi * (1 + 2 * random.rand(1, n_samples))  
    
    x = t * np.cos(t) * 1.0
    y = 10 * random.rand(1, n_samples)      # 这里乘的系数不同，会导致最终结果的一个宽度不同
    z = t * np.sin(t) * 1.0
    X = np.concatenate((x, y, z))  
    X += noise * random.randn(3, n_samples)  
    X = X.T  
    t = np.squeeze(t)   # 每个点有一个值，表示其颜色，对于之后处理SimRank来说，需要换另外一种方式处理
    return X, t  

def laplaEigen(dataMat,k,t):  
    m,n=shape(dataMat)
    W=mat(zeros([m,m]))  
    D=mat(zeros([m,m]))  
    for i in range(m):  
        k_index=knn(dataMat[i,:],dataMat,k)  
        for j in range(k):  
            sqDiffVector = dataMat[i,:]-dataMat[k_index[j],:]  
            sqDiffVector=array(sqDiffVector)**2  
            sqDistances = sqDiffVector.sum()  
            W[i,k_index[j]]=math.exp(-sqDistances/t)  
            D[i,i]+=W[i,k_index[j]]  
    L=D-W  
    Dinv=np.linalg.inv(D)  
    X=np.dot(D.I,L)  
    lamda,f=np.linalg.eig(X)  
    return lamda,f  
    
def knn(inX, dataSet, k):  
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet  
    sqDiffMat = array(diffMat)**2  
    sqDistances = sqDiffMat.sum(axis=1)  
    distances = sqDistances**0.5  
    sortedDistIndicies = distances.argsort()      
    return sortedDistIndicies[0:k]  

dataMat, color = make_swiss_roll(n_samples=1000)  
lamda,f=laplaEigen(dataMat,10,15.0) 

fm,fn =shape(f)
print('fm,fn:',fm,fn  )

lamdaIndicies = argsort(lamda)  
first=0  
second=0  
print(lamdaIndicies[0], lamdaIndicies[1])
for i in range(fm):  
    if lamda[lamdaIndicies[i]].real > 1e-5 :    # 找到特征值比较小的，但是不为0的！
        print(lamda[lamdaIndicies[i]])
        first=lamdaIndicies[i]  
        second=lamdaIndicies[i+1]  
        break  
print(first, second)

redEigVects = f[:,lamdaIndicies]
fig=plt.figure('origin')
ax1 = fig.add_subplot(111, projection='3d')
ax1.scatter(dataMat[:, 0], dataMat[:, 1], dataMat[:, 2], c=color,cmap=plt.cm.Spectral)  

fig=plt.figure('lowdata')  
ax2 = fig.add_subplot(111)
ax2.scatter(f[:,first], f[:,second],  c=color, cmap=plt.cm.Spectral)  
plt.show()  


# if __name__ == "__main__":
