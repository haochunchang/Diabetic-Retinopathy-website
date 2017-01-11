# Simply average three classification result and output to kaggleDiabetes.result

import pandas as pd

fl=[ "kaggleDiabetes1_epoch65_sample.test",
     "kaggleDiabetes2_epoch44_sample.test",
     "kaggleDiabetes3_epoch46_sample.test",
   ]

#########################################################################################

# Read in 
kd1 = pd.read_csv(fl[0], sep = ",", index_col = 0, names = ['name', 'No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR'])
kd2 = pd.read_csv(fl[1], sep = ",", index_col = 0, names = ['name', 'No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR'])
kd3 = pd.read_csv(fl[2], sep = ",", index_col = 0, names = ['name', 'No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR'])

# Unify index names
kd1.index = [i.split("/")[-1] for i in kd1.index]
kd2.index = [i.split("/")[-1] for i in kd2.index]
kd3.index = [i.split("/")[-1] for i in kd3.index]

kd = (kd1 + kd2 + kd3) / 3.0
kd.index.rename('name', inplace = True)

kd.to_csv("kaggleDiabetes.result", sep = ",", index = True)
if __name__ == "__main__":
    print(kd)
