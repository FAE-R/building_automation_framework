import pandas as pd
import glob
import os


path = os.path.dirname(os.path.abspath(__file__))

### read csv data and save in pickle ####

# df = pd.read_csv(path + "/elsysCO2_dp_list_berlin.csv", sep=';')
# print(df)
# df.to_pickle(path + "/elsysCO2_dp_list_berlin.pkl")


# see all pickle files ##

all_files = glob.glob(os.path.join(path, "*.pkl"))

data_point_lists = []

for filename in all_files:
    df = pd.read_pickle(filename)
    data_point_lists.append(df)


result = pd.concat(data_point_lists, ignore_index=True)

# print(result)
# result = result.drop_duplicates(subset=['table_id'])
# print(result[result.duplicated(subset=['data_point_name'])])

print(result[result.duplicated(subset=['table_id'])])
# result = result.drop_duplicates(subset=['data_point_name'])
# print(result)
