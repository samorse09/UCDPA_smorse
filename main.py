import pandas as pd
import numpy as np

file1 = '/Users/smorse/Documents/GitHub/UCDPA_smorse/Data/SCMData1.csv'
data1 = pd.read_csv(file1, header=0)
print(data1.head(5))
print(data1.shape)
# count the number of missing values in each column
missing_values_count = data1.isnull().sum()
print(missing_values_count[0:25])
# droprows = data1.dropna()
# print(data1.shape, droprows.shape)
# convert to dataframe
df1 = pd.DataFrame(data1)
# remove unnecessary columns (zipcode)
df1 = df1.drop(['Customer Zipcode'], axis=1)
print(df1.shape)
print(df1.head(5))
header_data = df1.set_index('Unique ID').sort_index()
print(header_data.head(2))
hd_keys = header_data.keys()
print(hd_keys)
# Create subset to count number of individual customers
hd_cusnum = header_data.drop_duplicates(subset='Customer Id')
count_hd_cusnum = header_data.value_counts('Customer Id')
print(count_hd_cusnum)
#number of orders by customer
cusords = header_data['Customer Id'].value_counts()
print(cusords)
#create subsets by late or on time
dstatus = header_data['Late_delivery_risk'].value_counts()
print(dstatus)
#if header_data['Late_delivery_risk] == 0,
ontime = header_data[header_data['Late_delivery_risk'] == 0]
late = header_data[header_data['Late_delivery_risk'] == 1]
print(np.shape(ontime))
print(np.shape(late))
#

