import pandas as pd
import numpy as np

class DataModel: #p for parameter
    def __init__(self, 
                 p_payment_history: float = 0.35, 
                 p_credit_utilization: float = 0.3,
                 p_credit_history: float = 0.15,
                 p_capacity: float = 0.1,
                 p_recent_inquiries: float = 0.1
                 ):
        
        self.p_payment_history = p_payment_history
        self.p_credit_utilization = p_credit_utilization 
        self.p_credit_history = p_credit_history
        self.p_capacity = p_capacity
        self.p_recent_inquiries = p_recent_inquiries
    
    #we are creating model based on kaggle dataset
    def create_model(self, df: pd.DataFrame) -> pd.DataFrame:
        print(df.head())
        
if __name__ == "__main__":
    df = pd.read_csv(r"C:\Users\mturakiewicz\Desktop\python\CreditScore\Credit\data\Credit_df.csv")
    print(df.head())