
# ***YouTube Data Harvesting and Warehousing***




## Introduction

YouTube is an American online video sharing and social media platform ,it was launched on February 14, 2005, by Steve Chen, Chad Hurley, and Jawed Karim. It is owned by Google and is the second most visited website, after Google Search.it has grown into a global phenomenon, serving as a hub for entertainment, education, and community engagement. With its vast user base and diverse content library, YouTube has become a powerful tool for individuals, creators, and businesses to share their stories, express themselves, and connect with audiences worldwide. 

This project extracts the particular youtube channel datas like playlist data,video data and comment data by using the youtube channel id, processes the data, and stores it in the MongoDB database and It has the option to migrate the data to MySQL tables from MongoDB then analyse the data and give the results depending on the user questions.
![image](https://github.com/Sujayaadesh/YouTube_Data_Harvesting_and_Warehousing./assets/125663811/c82614c5-e50b-4f4d-ac0e-8767568a4f86)

## Guide

## Tools:
       Virtual code
       Python 3.11.0
       Python compiler
       Mongo Database
       MySQL
       Youtube API key

##  Libraries to install
       pip install google-api-python-client, pymongo, mysql-connector-python, pymysql, pandas, streamlit.

## Import Libraries
#### Youtube libraries
    import googleapiclient.discovery

    from googleapiclient.errors import HttpError

#### Streamlit
    import streamlit as st

#### MongoDB
    from pymongo import MongoClient

#### SQL library
    import mysql.connector

#### Pandas
    import pandas as pd

#### 
    from datetime import datetime
   

## PROCESS

### 1.Extract Data
Extract the youtube channel data by using channel id ,with the help of youtube API

### 2.Transfer and Load Data 
After extraction ,those datas has been transferred into dictionary formate and load to the MongoDB and it also has option to migrate those unstructured data in MongoDB into structured one (MySql)
## Exploratory Data Analysis Process

### 1- Access SQL database

Create a connection to the MySQL server and access the specified MySQL DataBase by using mysql connector library and access tables.

### 2 - DATA Filter

Filter and process the collected data from the tables according to the given requirements by using SQL queries and transform the processed data into a Table format.

### 3 - Visualization

Atlast, create a Dashboard by using Streamlit and give options on the Dashboard to the user and select a question from that menu to analyse the data and show the output in Dataframe Table .

## User Guide 

### 1-Data Collection 

Take the channel id form the youtube channel that you want and paste it in input box and click the ***Extract Data and Store in Mongo***  button

### 2 - Migration 

select the channel name that you want migrate and click the ***Migrate to MySQL*** button to migrate the mentioned channel data to Mysql Database from tha Mongo Database

### 3 - Channel Data Analysis

Select a question according to your needs from the ***options*** and you can get those data in dataframe table formate 

![image](https://github.com/Sujayaadesh/YouTube_Data_Harvesting_and_Warehousing./assets/125663811/60266ad3-3b89-435d-8b7c-af179e0e5734)
