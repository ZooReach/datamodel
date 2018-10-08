#!/usr/bin/env python
# coding: utf-8

# In[16]:

from constants import *
import csv
import json as json
import pandas as pd
from IPython.display import display, HTML
chiroptera_dataset_filepath = "../data/note_chiroptera_database.csv"


# In[17]:


def read_data_file(file_path):
    dataset = []
    with open(file_path, "r") as data_file:
        csv_reader = csv.reader(data_file)
        header = csv_reader.next()
        for row in csv_reader:
            dataset.append(row)
    df_dataset = pd.DataFrame(dataset, columns = header)
    return df_dataset


# In[24]:


def processEndemicStatus(rawData):

    result = rawData.split('to')[0].lower().rstrip()
    endemicStatus = None
    
    if (result == ENDEMIC_STATUS):
        endemicStatus = True
    elif(result == NON_ENDEMIC_STATUS):
        endemicStatus = False
    return endemicStatus

def processEndemicRegion(rawData):
    result = rawData.split(' ')
    direction = ''
    region =''
    for x in result:
        if(x.lower() in DIRECTION):
            direction = x
        elif(x.lower() in REGION):
            region = x
    return (direction+region)

def isRegionAvailable(data):
    for x in REGION:
        #print(x)
        if(x in data.lower()):
            
            return True
    return False

def processEndemicSubRegion(rawData):
    result = ''
    if ('(' in rawData):
        result = rawData.split('(')[1].strip(') .')
    elif(isRegionAvailable(rawData) == False): # To Handle case 'Endemic to India'
        resultList = rawData.split('to')
        if(len(resultList) > 2):
           result = resultList[1].strip(' ')
        
    return json.dumps(result.split(','))
    

df_chiroptera = read_data_file(chiroptera_dataset_filepath)
endemic_status_data = df_chiroptera["Endemic status"]
df_chiroptera['IsEndemic'] = endemic_status_data.apply(lambda x:processEndemicStatus(x))
df_chiroptera['Endemic Region'] = endemic_status_data.apply(lambda x:processEndemicRegion(x))
df_chiroptera['Endemic SubRegion'] = endemic_status_data.apply(lambda x:processEndemicSubRegion(x))
temp ='Endemic to South Asia'
display(HTML(df_chiroptera.to_html()))


#common_names = df_chiroptera["Common names"]


# In[ ]:




