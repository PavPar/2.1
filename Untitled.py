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
    ratings = movieRating.iloc[[usrIndexA,usrIndexB],range(1,len(movieRating.columns))]
    badColumns = ratings[ratings == -1].dropna(axis=1, how='all').columns
    moviesWithRating = ratings.drop(axis=1, columns=badColumns)


    a = moviesWithRating.iloc[0,:].apply(lambda x: x*x).sum()
    b = moviesWithRating.iloc[1,:].apply(lambda x: x*x).sum()
    
    a = math.sqrt(a)
    b = math.sqrt(b)
    
    sumAB = (moviesWithRating.iloc[0,:] * moviesWithRating.iloc[1,:]).sum()
    res = sumAB/(a*b)
    return res


# In[12]:


def getMean(userID):
    temp = movieRating.iloc[[userID],range(1,len(movieRating.columns))]
    res = temp.mean(axis=1)
    return res.values[0]


# In[4]:


def getFilmRating(userID,filmID):
    rating = movieRating.iloc[[userID],range(1,len(movieRating.columns))]
    return  rating.iloc[[0],[filmID]].values


# In[5]:


def getSumSim(userID):
    res=0;
    for i in range(0,len(movieRating.count()+1)):
        res = res + abs(sim(userID,i))
    return res;


# In[6]:


def getSmthng(userID,filmID):
    res=0;
    for i in range(0,len(movieRating.count()+1)):
        rvi = getFilmRating(i,filmID)
        
        
        usersSim = sim(userID,i)
        
        rv = getMean(i);
        
        res = res + usersSim*(rvi-rv)
        
    return res


# In[7]:


def getEval(userID,filmID):
    sumSum = getSumSim(userID);
    smthng = getSmthng(userID,filmID)
    return getMean(userID)+(smthng/sumSum)


# In[8]:


getEval(27,0)


# In[13]:


res = {}
for i in range(0,len(movieRating.columns)-1):
    rvi = getFilmRating(22,i)
    if(rvi == -1):
        res[i+1] = getEval(22,i);
print(res)


# In[10]:


movieRating.iloc[[22],range(1,len(movieRating.columns))][movieRating == -1].dropna(axis=1)


# In[11]:


target = movieRating.iloc[[22],range(1,len(movieRating.columns))][movieRating == -1]
for i in range(0,len(target)-1):
    rvi = getFilmRating(22,i)
    if(rvi):
        res.append(getEval(22,i))
print(res)

