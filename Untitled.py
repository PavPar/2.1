#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import math  

movieRating = pd.DataFrame(pd.read_csv('./data.csv'))
movieNames = pd.DataFrame(pd.read_csv('./movie_names.csv'))
contextPlace = pd.DataFrame(pd.read_csv('./context_place.csv'))
contextDay = pd.DataFrame(pd.read_csv('./context_day.csv'))


# In[2]:


def sim(usrIndexA,usrIndexB):
    trgtsRatings = movieRating.iloc[[usrIndexA,usrIndexB],range(1,len(movieRating.columns))]
    commonRatings = trgtsRatings[trgtsRatings != -1].dropna(axis=1)

    usrA = commonRatings.iloc[0,:]
    usrB = commonRatings.iloc[1,:]

    sumUsrA = usrA.apply(lambda x: x*x)
    sumUsrB = usrB.apply(lambda x: x*x)

    sumUsrA = math.sqrt(sumUsrA.sum())
    sumUsrB = math.sqrt(sumUsrB.sum())
    

    res = (usrA*usrB).sum()/(sumUsrA*sumUsrB)
    return res


# In[3]:


def getMean(userID):
    temp = movieRating.iloc[[userID],range(1,len(movieRating.columns))]
    res = temp[temp != -1].dropna(axis=1).mean(axis=1)
    return res.values[0]


# In[4]:


def getFilmRating(userID,filmID):
    rating = movieRating.iloc[[userID],range(1,len(movieRating.columns))]
    return  rating.iloc[[0],[filmID]].values


# In[5]:


def getSimMatrix():
    res = pd.DataFrame(np.zeros(shape=(movieRating.count()[0],movieRating.count()[0])),columns=range(0,movieRating.count()[0]))
    for usrA in range(0,movieRating.count()[0]):
        for usrB in range(0,movieRating.count()[0]):
            if(usrA != usrB):
                res.iat[usrA,usrB] = sim(usrA,usrB)
    return res


# In[6]:


simMatrix = getSimMatrix()


# In[7]:


simMatrix


# In[12]:


def getEval(userID,filmID):
    usersK = simMatrix.iloc[userID,:].sort_values(ascending=False)
    
    badColumns = []
    for trgtId in range(0,movieRating.count()[0]):
        if(getFilmRating(trgtId,filmID) == -1 and trgtId!= userID):
            badColumns.append(trgtId)
    usersK = usersK.drop(badColumns)
    
    print(badColumns)
    
    usersK = usersK[:4]
    sumSim = usersK.abs().sum()
    usersSim = usersK.to_dict();
    

    
    res = 0
    for userrfID, sim in usersSim.items():
        rvi = getFilmRating(userID,filmID)
        if(rvi != -1):
            rv = getMean(userID);
            res = res + sim*(rvi-rv)
    
    return getMean(userID)+(res/sumSim)


# In[11]:


getEval(22,6)


# In[18]:


userID = 22
filmID = 6

usersK = simMatrix.iloc[userID,:].sort_values(ascending=False)

print(usersK)

badColumns = []
for trgtId in range(0,movieRating.count()[0]):
    if(getFilmRating(trgtId,filmID) == -1 and trgtId!= userID):
        badColumns.append(trgtId)
usersK = usersK.drop(badColumns)
    
print(badColumns)
    
usersK = usersK[:4]
sumSim = usersK.abs().sum()
usersSim = usersK.to_dict();
print(usersK)    

    
res = 0
for userrfID, sim in usersSim.items():
    rvi = getFilmRating(userID,filmID)
    if(rvi != -1):
        rv = getMean(userID);
        res = res + sim*(rvi-rv)

getMean(userID)+(res/sumSim)

