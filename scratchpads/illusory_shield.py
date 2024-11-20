import pandas as pd
from mage_ai.io.file import FileIO

filepath = "/home/src/Downloads/Data 2018-2023/Project/2023/202302889.json"
df = pd.DataFrame(FileIO().load(filepath))
print(df)