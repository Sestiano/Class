import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Class/IntroPy/European_Ski_Resorts.csv')


df = df.sort_values(by='TotalSlope', ascending=False)

grouped = df.groupby('Resort')['Country'].apply(lambda x: x.mode()[0])
print('Printing Grouped')
print(grouped)

austria_df = df[df['Country'] == 'Austria']
plt.figure(figsize=(10, 6))
plt.hist(austria_df['TotalLifts'], bins=20, edgecolor='black')
plt.title('Distribution of Lifts in Austrian Ski Resorts')
plt.xlabel('Number of Lifts')
plt.ylabel('Frequency')
plt.show()