#!/usr/bin/env python
# coding: utf-8

# In[184]:


import pandas as pd
import enum
from IPython.display import display, HTML as html


# In[185]:


class Threat_Concern(enum.Enum):
    LEAST_CONCERN = "Least Concern"
    DATA_DEFICIENT = "Data Deficient"
    NEAR_THREATENED = "Near Threatened"
    CRITICALLY_ENDANGERED = "Critically Endangered"
    ENDANGERED = "Endangered"
    VULNERABLE = "Vulnerable"


# In[186]:


class Nation(enum.Enum):
    INDIA = "India"
    NEPAL = "Nepal"
    PAKISTAN = "Pakistan"
    SRI_LANKA = "Sri Lanka"


# In[187]:


CHIROPTERA_FILE_PATH = "Data/chiroptera_database.csv"
chiroptera_database = pd.read_csv(CHIROPTERA_FILE_PATH)
nation_wise_status = chiroptera_database["National Status - 1"]


# In[188]:


status_list = []
for status in nation_wise_status:
    if(type(status) == str):
        status_list.append(status.split("\n"))
    else:
        status_list.append([])
print(status_list)
#chiroptera_database.insert(5, "Nation-wise Status", nation_wise_status)


# In[189]:


#print(chiroptera_database["Nation-wise Status"])


# In[190]:


status_series = pd.Series(status_list)
print(status_series)


# In[191]:


def extract_country(country_status):
    countries = []
    for item in country_status:
        country = item.split(" ")[0]
        if(country == "Sri"):
            country = country + " " + item.split(" ")[1]
        countries.append(country)
    return countries


# In[192]:


# countries = []
# for country_status in status_series:
#     if(country_status.count > 0):
#         countries.append(extract_country(country_status))
#     else:
#         countries.append([])
# print(countries)


# In[193]:


print(extract_country(status_series[0]))


# In[194]:


def find_threat_concern(string):
    for concern in Threat_Concern:      
        if(string.lower().find(concern.value.lower()) != -1):
            return concern


# In[195]:


def extract_threat_concern(country_status):
    threat_concerns  = []
    for item in country_status:
       threat_concerns.append(find_threat_concern(item))
    return threat_concerns


# In[196]:


print(status_series[0])
print(extract_country(status_series[0]))
print(extract_threat_concern(status_series[0]))


# In[197]:


def generate_dictionary(countries, threat_concerns):
    country_to_concern_list = []
    if (len(countries) != len(threat_concerns)):
        raise Exception("Inconsistent list sizes")
    elif(len(countries) > 0):
        for (country, threat_concern) in zip(countries, threat_concerns):
            dictionary = {}
            dictionary["country"] = country
            dictionary["concern"] = threat_concern
            country_to_concern_list.append(dictionary)
    return country_to_concern_list


# In[198]:


def extract_country_and_status_as_json(country_status):
    country_status_dictionary_list = []
    for item in country_status:
        country_status_dictionary = {}
        country = extract_country(item)
        threat_concern = extract_threat_concern(item)
        country_to_concern = generate_dictionary(country, threat_concern)
        country_status_dictionary_list.append(country_to_concern)
        #country_status_dictionary[country]
        #country_status_dictionary_list.append(country_status_dictionary)
        
    return country_status_dictionary_list


# In[199]:


country_criteria = extract_country_and_status_as_json(status_series)
dataframe = pd.DataFrame({"National status" : nation_wise_status, "JSON" : country_criteria})
dataframe.to_excel("dataframe.xlsx")
display(html(dataframe.to_html()))


# In[200]:


countries = []
for country_status in status_series:
    if(country_status.count > 0):
        countries.append(extract_country_and_status_as_json(country_status))
    else:
        countries.append([])
print(countries)


# In[178]:


some_random_string = "Kafka on the shore"
kafka = some_random_string.split(" ")[0]
kafka_on = kafka + " " + some_random_string.split(" ")[1]
print(some_random_string)
print(kafka_on)


# In[ ]:


kafka_on_the_shore = "Kafka on the shore"
kafka = "Kafkaa"
kafka_on_the_shore.find(kafka)

