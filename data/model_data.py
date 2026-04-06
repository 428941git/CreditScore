import pandas as pd
import numpy as np
from pathlib import Path


class modelData:
    def __init__(self, path: str = f"{Path(__file__).parent}/Credit_df.csv"):
        self.path = path

    def quantileMethod(self, df: pd.DataFrame) -> dict:
        quantileDict = {}
        for col in df.columns:
            quantileColumn = df[col].quantile(0.75)
            quantileDf = df[df[col] > quantileColumn]
            quantileDict.update({f"{col}": quantileDf})
        return quantileDict
    
    def getData(self):
        df = pd.read_csv(self.path)
        needed_cols = ["Age", 
                       "Annual_Income", 
                       "Credit_Utilization_Ratio",
                       "Debt_To_Income_Ratio",
                       "Number_of_Late_Payments",
                       "Defaulted",
                       "Tenure_in_Years"]
        df = df[needed_cols]
        return df

if __name__ == "__main__":
    
    data = modelData()
    df = data.getData()
    df_defaulted = df[df["Defaulted"] == 1]
    df_not_defaulted = df[df["Defaulted"] == 0]
    df_dcor = df_defaulted.corr()
    df_ndcor = df_not_defaulted.corr()
    print(df_dcor-df_ndcor)
    print(df.corr())
    
    

