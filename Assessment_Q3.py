#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as plt
from IPython.display import display


# In[2]:


df1_raw = pd.read_csv('table_1.csv')


# # Q3

# In[142]:


df1_raw.head(5)


# In[198]:


def flatten_nested_list(l):
    return [item for sublist in l for item in sublist]


# In[199]:


def to_string(row):
    split_code = row.split(',')
    return [x for x in split_code]


# In[200]:


def binary_encoding(row, baseline):
    comparison_bool = [i in row for i in baseline]
    return [int(x) for x in comparison_bool]


# In[230]:


# Used to flatten a nested list
def flatten_nested_list(l):
    return [item for sublist in l for item in sublist]

# Used to separate each code into its own string
def to_string(row):
    split_code = row.split(',')
    return [x for x in split_code]

# Used to encode all reason codes using binary notation
def binary_encoding(row, baseline):
    comparison_bool = [i in row for i in baseline]
    return [int(x) for x in comparison_bool]

# Processing the dataset using the helper functions above and return the processed dataframe
def reason_code_processing(df_raw, column_name):
    df = df_raw.copy() # Using .copy() to avoid seeting with copy warning
    
    # 1. Extract the reason_code column and convert them into lists of integers for downstream processing
    df['code_int'] = df[column_name].apply(lambda row: to_string(row))
    
    # 2. Combine all reason codes into one list and apply set() to obtain non-duplicated union of all codes
    l = list(df['code_int'])
    flattened_list = flatten_nested_list(l)
    flattened_list_sorted = sorted(list(set(flattened_list)), key = int) 
    # ^sort the reason code from smallest to biggest 'magnitude' for better viewing
    # ^The flattened_list_sorted contains a list of reason codes that are the union of all reason codes without duplicates
    # ^This list can be act as the "master list" for comparing each row to see if it contains each code
    
    # 3. Compare each row with the above flattened list and save the binary results in a new column
    df['comparison_binary'] = df['code_int'].apply(lambda row: binary_encoding(row, flattened_list_sorted))
    
    # 4. Explode the binary list into columns using the flattened list as column names
    exploded_code = pd.DataFrame(df['comparison_binary'].tolist(), 
                                 columns = flattened_list_sorted,
                                 index = df.index)
    df_new = pd.concat([df, exploded_code], axis=1) # Using concat to avoid seeting with copy warning
    df_new.drop(columns = ['code_int', 'comparison_binary'], inplace = True) # Drop unncessary columns
    
    return df_new


# In[236]:


df1_raw = pd.read_csv('table_1.csv') # Read original data file
df1_processed_2 = reason_code_processing(df1_raw, 'reason_code') # Apply the above function to process data
df1_processed_2.display()
df1_processed_2.to_excel('table_2_processed.xlsx', index=False) # Save the processed data to local as an excel file


# In[231]:


df1_processed = reason_code_processing(df1_raw[['reason_code']], 'reason_code')
df1_processed.head(10)

