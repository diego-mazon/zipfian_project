
# coding: utf-8

# In[3]:

import pandas as pd
import numpy as np
from __future__ import division
import seaborn
import matplotlib.pyplot as plt
get_ipython().magic(u'pylab inline')


# In[4]:

raw = pd.read_csv('HMXPC13_DI_v2_5-14-14.csv')


# In[5]:

#creating clean data. Without binarization. With nans 
clean = raw
#creating numeric column for the grades (they were strings)
clean['grade_num'] = raw.grade.convert_objects(convert_numeric=True)
# grade has been replaced by grade_num
del clean['grade']
# contains no info
del clean['roles']
# all registered(1)
del clean['registered']
# this course was weird.  See documentation
clean = clean[clean.course_id != 'HarvardX/CS50x/2012']
# inconsistent data
clean = clean[clean.incomplete_flag != 1]
del clean['incomplete_flag']


# In[9]:

clean.to_csv('clean.csv')


# In[30]:

#creating clean_bin
clean = raw = pd.read_csv('clean.csv')
clean_bin = clean


# In[31]:

#binarizing countries
a = pd.get_dummies(clean_bin.final_cc_cname_DI)
countries = list(a.columns)
clean_bin [countries] = a
del clean_bin['final_cc_cname_DI']
del clean_bin['Unknown/Other']


# In[32]:

#binarizing gender
b = pd.get_dummies(clean.gender)
clean_bin [list(b.columns)] = b
del clean_bin['gender']


# In[33]:

list(clean_bin.LoE_DI.unique())[1:]


# In[34]:

# making degree numerical
#list(clean_bin.LoE_DI.unique())[1:]=["Bachelor's", 'Secondary', "Master's", 'Doctorate', 'Less than Secondary']
clean_bin = clean_bin.replace(list(clean_bin.LoE_DI.unique())[1:], [2, 1, 3, 4, 0])


# In[42]:

# renaming and reordering columns
clean_bin.rename(columns={'course_id': 'course', 'userid_DI': 'student', 'LoE_DI': 'degree', 'YoB': 'birth', 'start_time_DI': 'registration', 'last_event_DI': 'last_event', 'grade_num': 'grade', 'f': 'female', 'm': 'male'  }, inplace=True)
col=[u'course', u'student', u'female', u'male', u'birth', u'degree', u'viewed', u'explored',  u'registration', u'last_event', u'nevents', u'ndays_act', u'nplay_video', u'nchapters', u'nforum_posts', u'grade', u'certified', u'Australia', u'Bangladesh', u'Brazil', u'Canada', u'China', u'Colombia', u'Egypt', u'France', u'Germany', u'Greece', u'India', u'Indonesia', u'Japan', u'Mexico', u'Morocco', u'Nigeria', u'Other Africa', u'Other East Asia', u'Other Europe', u'Other Middle East/Central Asia', u'Other North & Central Amer., Caribbean', u'Other Oceania', u'Other South America', u'Other South Asia', u'Pakistan', u'Philippines', u'Poland', u'Portugal', u'Russian Federation', u'Spain', u'Ukraine', u'United Kingdom', u'United States']
clean_bin = clean_bin[col]


# In[43]:

# saving
clean_bin.to_csv('clean_bin.csv')


# In[44]:

# creating new dataset: filling nan with mean. 397944 students. All columns are numeric,
# but course, student, registration, and last_event. Birth and degree still
# contain nan values
df = pd.read_csv('clean_bin.csv')


# In[47]:

df['viewed'] = df.viewed.fillna(clean_bin.viewed.mean())
df['explored'] = df.explored.fillna(clean_bin.explored.mean())
df['nevents'] = df.nevents.fillna(clean_bin.nevents.mean())
df['ndays_act'] = df.ndays_act.fillna(clean_bin.ndays_act.mean())
df['nplay_video'] = df.nplay_video.fillna(clean_bin.nplay_video.mean())
df['nchapters'] = df.nchapters.fillna(clean_bin.nchapters.mean())
df['nforum_posts'] = df.nforum_posts.fillna(clean_bin.nforum_posts.mean())
df['grade'] = df.grade.fillna(clean_bin.grade.mean())


# In[55]:

# removing unintetionally created column (index)
del df['Unnamed: 0']


# In[63]:

# removing users who didn't participate beyond registration
df.dropna(subset = ['last_event'], inplace=True)


# In[68]:

df.to_csv('data.csv')


# In[ ]:



