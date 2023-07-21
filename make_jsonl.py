import pandas as pd

df = pd.read_csv(
    'datas\make_GPT_dataset\data001.csv', 
    usecols=[0,1], 
    names=['prompt','completion'], 
    skiprows=2)
df.head()

df.to_json("datas\make_GPT_dataset\data001.jsonl", orient='records', lines=True,force_ascii=False)