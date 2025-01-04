#!/usr/bin/env python
# coding: utf-8

# ### Want to run some quick data quality checks? Here are 10 pandas one-liners that'll come in handy.

# ##### Here’s a small sample dataset simulating e-commerce transactions with common data quality issues such as missing values, inconsistent formatting, and potential outliers:

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# Sample e-commerce transaction data

data = {
    "TransactionID": [101, 102, 103, 104, 105],
    "CustomerName": ["Jane Rust", "june young", "June Doe", None, "JANE RUST"],
    "Product": ["Laptop", "Phone", "Laptop", "Tablet", "Phone"],
    "Price": [1200, 800, 1200, -300, 850],  # Negative value indicates an issue
    "Quantity": [1, 2, None, 1,1],  # Missing value
    "TransactionDate": ["2024-12-01", "2024/12/01", "01-12-2024", None, "2024-12-01"],
}

df = pd.DataFrame(data)

# Display the DataFrame
print(df)


# ## 

# ##### Before going ahead, let’s get some basic info on the dataframe: 

# In[3]:


df.info()


# ## 

# ## 1. Check for Missing Values

# ##### This one-liner checks each column for missing values and sums them up.m

# In[4]:


missing_values = df.isnull().sum()
print("Missing Values:\n", missing_values)


# ## 

# ## 2. Identify Incorrect Data Types

# ##### Reviewing data types is important. For example, TransactionDate should be a datetime type, but it’s not so in the example. 

# In[5]:


print("Data Types:\n", df.dtypes)


# ## 

# ## 3. Convert Dates to a Consistent Format
# 

# ##### This one-liner converts ‘TransactionDate’ to a consistent datetime format. Any unconvertible values—invalid formats—are replaced with NaT (Not a Time).`

# In[6]:


df["TransactionDate"] = pd.to_datetime(df["TransactionDate"], errors="coerce")
print(df["TransactionDate"])


# ## 

# ## 4. Find Outliers in Numeric Columns

# ##### Finding outliers in numeric columns is another important check. However, you’ll need some domain knowledge to identify potential outliers. Here, we filter the rows where the ‘Price’ is less than 0, flagging negative values as potential outliers.

# In[7]:


outliers = df[df["Price"] < 0]
print("Outliers:\n", outliers)


# ## 

# ## 5. Detect Duplicate Records

# ##### This checks for duplicate rows based on ‘CustomerName’ and ‘Product’, ignoring unique TransactionIDs. Duplicates might indicate repeated entries. 

# In[8]:


duplicates = df.duplicated(subset=["CustomerName", "Product"], keep=False)
print("Duplicate Records:\n", df[duplicates])


# ## 

# ## 6. Standardize Text Data

# ##### Standardizes CustomerName by removing extra spaces and ensuring proper capitalization ( "jane rust" → "Jane Rust").

# In[9]:


df["CustomerName"] = df["CustomerName"].str.strip().str.title()
print(df["CustomerName"])


# ## 

# ## 7. Validate Data Ranges

# ##### With numeric values, ensuring they lie within the expected range is necessary. Let’s check if all prices fall within a realistic range, say 0 to 5000. Rows with price values outside this range are flagged.

# In[10]:


invalid_prices = df[~df["Price"].between(0, 5000)]
print("Invalid Prices:\n", invalid_prices)


# ## 

# ## 8. Count Unique Values in a Column

# ##### Let’s get an overview of how many times each product appears using the `value-counts()` method. This is useful for spotting typos or anomalies in categorical data.

# In[11]:


unique_products = df["Product"].value_counts()
print("Unique Products:\n", unique_products)


# ## 

# ## 9. Check for Inconsistent Formatting Across Columns

# ##### Detects inconsistently formatted entries in 'CustomerName'. This regex flags names that may not match the expected title case format.

# In[12]:


inconsistent_names = df["CustomerName"].str.contains(r"[A-Z]{2,}", na=False)
print("Inconsistent Formatting in Names:\n", df[inconsistent_names])


# ## 

# ## 10. Identify Rows with Multiple Issues

# ##### This identifies rows with more than one issue, such as missing values, negative prices, or invalid dates, for focused attention during cleaning.

# In[13]:


issues = df.isnull().sum(axis=1) + (df["Price"] < 0) + (~df["TransactionDate"].notnull())
problematic_rows = df[issues > 1]
print("Rows with Multiple Issues:\n", problematic_rows)

