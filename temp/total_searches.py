import pandas as pd

s1 = pd.read_csv('data/1.csv', sep='|', index_col=None)
s2 = pd.read_csv('data/2.csv', sep='|', index_col=None)
s3 = pd.read_csv('data/3.csv', sep='|', index_col=None)

# sum the totallookups
total = s1['totallookups'].sum() + s2['totallookups'].sum() + s3['totallookups'].sum()
print(total)