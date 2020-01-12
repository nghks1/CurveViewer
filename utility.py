import pandas as pd


def generate_table(df):
    cols = df.drop('Date',axis=1).columns
    data = [[None for i in range(len(cols))] for j in range(len(cols))]
    for i in range(0, len(cols)):
        for j in range (0,len(cols)):
            if i<j:
                data[i][j]= round((df[cols[j]].head(1)- df[cols[i]].head(1))*100,1)
            elif i == j:
                data[i][j] = 0
            else:
                data[i][j] =""
    data = pd.DataFrame(data)
    data.columns = cols
    data.insert(0,' ',cols)

    return data.to_dict('records')