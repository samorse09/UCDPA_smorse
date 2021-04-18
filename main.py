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
dstatus_num = header_data['Late_delivery_risk'].value_counts()
print(dstatus_num)

#add column for late status
status =  []
for value in header_data['Late_delivery_risk']:
    if value == 1:
        status.append("Late")
    else:
        status.append('On_Time')
header_data['Late_Status'] = status
print(header_data.head())

is_late = header_data[header_data['Late_Status'] == 'Late']
on_time = header_data[header_data['Late_Status'] == 'On_Time']

print(np.shape(is_late))
print(np.shape(on_time))

lates_region = is_late['Order Region'].value_counts()
print(lates_region)

ontime_region = on_time['Order Region'].value_counts()
print(ontime_region)

total_byregion = header_data['Order Region'].value_counts()
print(total_byregion)

percent_byregion = lates_region / total_byregion
print(percent_byregion)



