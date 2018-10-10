#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import enum
from IPython.display import display, HTML as html


class ThreatConcern(enum.Enum):
    LEAST_CONCERN = "Least Concern"
    DATA_DEFICIENT = "Data Deficient"
    NEAR_THREATENED = "Near Threatened"
    CRITICALLY_ENDANGERED = "Critically Endangered"
    ENDANGERED = "Endangered"
    VULNERABLE = "Vulnerable"


class Nation(enum.Enum):
    INDIA = "India"
    NEPAL = "Nepal"
    PAKISTAN = "Pakistan"
    SRI_LANKA = "Sri Lanka"


def extract_column_as_list(column):
    status_list = []
    for status in column:
        if type(status) == str:
            status_list.append(status.split("\n"))
        else:
            status_list.append([])
    return status_list


def extract_countries(row):
    countries = []
    for item in row:
        country = item.split(" ")[0]
        if country == "Sri":
            country = country + " " + item.split(" ")[1]
        countries.append(country)
    return countries


def find_threat_concern(item):
    for concern in ThreatConcern:
        if item.lower().find(concern.value.lower()) != -1:
            return concern


def extract_threat_concerns(row):
    threat_concerns = []
    for item in row:
        threat_concerns.append(find_threat_concern(item))
    return threat_concerns


def generate_dictionary(countries, threat_concerns):
    country_concern = []
    if len(countries) != len(threat_concerns):
        raise Exception("Inconsistent list sizes")
    elif len(countries) > 0:
        for (country, threat_concern) in zip(countries, threat_concerns):
            dictionary = {"country": country, "concern": threat_concern}
            country_concern.append(dictionary)
    return country_concern


def extract_country_and_status_as_dictionary(country_status):
    country_concern_list = []
    for row in country_status:
        countries = extract_countries(row)
        threat_concerns = extract_threat_concerns(row)
        country_concern = generate_dictionary(countries, threat_concerns)
        country_concern_list.append(country_concern)
    return country_concern_list


CHIROPTERA_FILE_PATH = "../Data/chiroptera_database.csv"
chiroptera_database = pd.read_csv(CHIROPTERA_FILE_PATH)
nation_wise_status = chiroptera_database["National Status - 1"]

status_series = pd.Series(extract_column_as_list(nation_wise_status))

country_criteria = extract_country_and_status_as_dictionary(status_series)

dataframe = pd.DataFrame({"National status": nation_wise_status, "JSON": country_criteria})
dataframe.to_excel("../data/national_status.xlsx")