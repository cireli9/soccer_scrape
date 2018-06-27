import pandas as pd
import numpy as np
import os

cwd = os.getcwd()

fileList = []

for folder in os.listdir():
    if os.path.isdir(os.path.join(cwd, folder)):
        for fileName in os.listdir(os.path.join(cwd, folder)):
            if fileName.endswith('.xlsx') and fileName.startswith('soccer'):

                filePath = os.path.join(os.path.join(cwd,folder),fileName)
                fileList.append((filePath, fileName))

print("got files")
print(fileList)

writer = pd.ExcelWriter('Liverpool_data.xlsx')

for i in range(len(fileList)):
    temp = []
    xls = pd.ExcelFile(fileList[i][0])
    df = xls.parse(xls.sheet_names[0])

    for index, row in df.iterrows():
        if "Liverpool" in row["Teams"]:
            temp.append(row)

    #output = np.stack(temp, axis = -1)
    output_df = pd.DataFrame(temp)

    output_df.to_excel(writer, fileList[i][1])

    print("wrote" + str(i))

writer.save()

print("done")

