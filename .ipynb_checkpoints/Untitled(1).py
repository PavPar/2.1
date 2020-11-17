#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import math as m
import json
import numpy as np

user = 26
index_user = user - 1
negOne = -1
k = 4

data = pd.read_csv("data.csv", index_col = 0)
print(data.iloc[index_user])


# Функция подсчёта среднего у user:

# In[2]:


def MeanUser(data, index):
    count = 0
    sum = 0
    for item in data.iloc[index]:
        if(item != negOne):
            sum += item
            count += 1
    return sum / count


# Функция, которая ищет k user'ов, у которых есть оценка для фильма:

# In[3]:


def FindUsers(data, index_film, k):
    ind_users = []
    for i in range(1, k + 1):
        if(data.iloc[i][index_film] != negOne):
            ind_users.append(i)
    return ind_users


# Функция расчёта метрики косинуса sim:

# In[4]:


def sim(data, index1, index2):
    col1 = data.iloc[index1]
    col2 = data.iloc[index2]
    count = len(col1)
    sumUp = 0
    sumDown1 = 0
    sumDown2 = 0
    for i in range(0, count):
        if((col1[i] != negOne) & (col2[i] != negOne)):
            sumUp = sumUp + col1[i] * col2[i]
            sumDown1 = sumDown1 + col1[i] * col1[i]
            sumDown2 = sumDown2 + col2[i] * col2[i]
    return sumUp / ((sumDown1 ** .5) * (sumDown2 ** .5))


# Задание 1:

# Высчитаем метрики для пар - наш пользователь со всеми остальными:

# In[5]:


l = []
for i in range(0, len(data)):  
    l.append(sim(data, index_user, i))


# Отсортируем пользователей по метрике:

# In[6]:


dataCopy = data.copy()
for i in range(1, len(dataCopy)):
    for j in range(0, len(dataCopy) - i):
        if(l[j] < l[j + 1]):
            a, b = dataCopy.iloc[j, :].copy(), dataCopy.iloc[j+1, :].copy()
            dataCopy.iloc[j, :], dataCopy.iloc[j+1, :] = b, a
            t = l[j]
            l[j] = l[j+1]
            l[j+1]=t


# Высчитаем оценки:

# In[7]:


dictMarks = {}
meanRightUser = MeanUser(dataCopy, 0)
for i in range(0, len(dataCopy.columns)):
    if(dataCopy.iloc[0][i] == negOne):
        index_users = FindUsers(dataCopy, i, k)
        sumSim = 0
        sumSimAbs = 0
        for item in index_users:
            #tempSim = sim(data, 0, index_users[j])
            tempSim = l[item]
            sumSim = sumSim + tempSim * (dataCopy.iloc[item][i] - MeanUser(dataCopy, item))
            sumSimAbs = sumSimAbs + m.fabs(tempSim)
        dictMarks.update({"movie " + str(i+1) : round(meanRightUser + (sumSim / sumSimAbs), 3)})
dictMarks


# Задание 2:

# In[8]:


dataDays = pd.read_csv("context_day.csv", index_col = 0).T
dataPlaces = pd.read_csv("context_place.csv", index_col = 0).T

weeknd1 = "Sat"
weeknd2 = "Sun"
home = "h"


# Функция подсчёта средней оценки у фильма:

# In[9]:


def MeanFilm(data, index_film):
    data = data.T
    sum = 0
    count = 0
    for mark in data.iloc[index_film]:
        if(mark != negOne):
            sum += mark
            count +=1
    return sum / count


# Функция подсчёта процента посмотревших на выходных:

# In[10]:


def PercWeekends(data, index_film):
    watchedOnWeekend = 0
    watchedTotal = 0
    for mark in data.iloc[index_film]:
        mark = mark.strip(' ')
        if(mark != str(negOne)):
            watchedTotal += 1
            if((mark == weeknd1) | (mark == weeknd2)):
                watchedOnWeekend += 1
    return watchedOnWeekend / watchedTotal


# Функция подсчёта процента посмотревших дома:

# In[11]:


def PercHome(data, index_film):
    watchedHome = 0
    watchedTotal = 0
    for mark in data.iloc[index_film]:
        mark = mark.strip(' ')
        if(mark != str(negOne)):
            watchedTotal += 1
            if(mark == home):
                watchedHome += 1
    return watchedHome / watchedTotal


# Функция поиска фильмов:

# In[12]:


def FindFilms(data, index_user):
    l = []
    d = data.iloc[index_user]
    for i in range(0, len(d)):
        if(d[i] == negOne):
            l.append(i)
    return l


# Расчёт оценки - ср. знач. * % посмотревших в выходные * % посмотревших дома:

# Причём оценки будут лежать в диапазоне от 0 до 5: 2 * 0.0% * 0.0% - худший вариант и 5 * 1.0% * 1.0% - лучший

# In[13]:


def BestFilm(d, dDays, dPlaces, index_user):
    l = []
    films = FindFilms(d, index_user)
    for index in films:
        l.append(MeanFilm(d, index) * PercWeekends(dDays, index) * PercHome(dPlaces, index))  
    print(l)
    film = {'movie ' + str(int(films[l.index(max(l))]) + 1) : round(max(l), 3)}
    return film

bestFilm = BestFilm(data, dataDays, dataPlaces, index_user)
print(bestFilm)


# In[14]:


answer = {"user": user, "1": dictMarks, "2": bestFilm}
print(answer)


# In[15]:


with open('answer.json', 'w', encoding = 'utf-8') as f:
    json.dump(answer, f, ensure_ascii = False, indent = 4)


# In[ ]:




