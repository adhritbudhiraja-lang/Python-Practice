import pandas as pd 
data = {
    "Name":["Adhrit","Adhrit_1","Adhrit_2","Adhrit_3","Adhrit_4"],
    "Age":[18,20,22,24,26],
    "Score":[100,80,90,70,60],
    "City":["Delhi","Mumbai","Chandigarh","Banglore","Delhi"]

}

df = pd.DataFrame(data)
print(df.info())