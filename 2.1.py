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


# In[16]:





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


# In[8]:


def getEval(userID,filmID):
    userID=userID-1
    
    usersK = simMatrix.iloc[userID,:].sort_values(ascending=False)
    
    badColumns = []
    for trgtId in range(0,movieRating.count()[0]):
        if(getFilmRating(trgtId,filmID) == -1 and trgtId!= userID):
            badColumns.append(trgtId)


    usersK = usersK[:4]
    usersK = usersK.drop(badColumns, errors='ignore')

    sumSim = np.abs(usersK.sum())
    usersSim = usersK.to_dict();
    
    res = 0
    for trgtID, sim in usersSim.items():
        rvi = getFilmRating(trgtID,filmID)
        rv = getMean(trgtID);
        res = res + sim*(rvi-rv)
    eval = getMean(userID)+(res/sumSim)
    return [round(eval.item(0),3),usersK]


# In[31]:





# In[26]:


res = {}
userID = 26
bestFilm = {}

for i in range(0,len(movieRating.columns)-1):
    rvi = getFilmRating(userID-1,i)
    maxK = 0
    if(rvi == -1):
        evalRes = getEval(userID, i)
        res['Movie '+ str(i+1)] = evalRes[0]
        if(len(bestFilm)==0):
            maxK=len(evalRes[1])
            bestFilm.clear()
            bestFilm['Movie '+ str(i+1)] = evalRes[0]
        if(len(evalRes[1])>=maxK and  bestFilm[next(iter(bestFilm))] < evalRes[0]):
            maxK = evalRes[1]
            bestFilm.clear()
            bestFilm['Movie ' + str(i + 1)] = evalRes[0]
print(res)


# In[11]:


# best_film = {}
# best_film[max(res, key=res.get)] = res[max(res, key=res.get)]
# best_film


# In[12]:


resJson = {
    'user': userID,
    '1': res,
    '2': bestFilm
}
print(resJson)
import json
with open('result.json', 'w') as fp:
    json.dump(resJson, fp, indent=4)

