import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, brier_score_loss



def calc(sel_tab, selection, t_pop_sample, t_dti_ratio, t_late_payments, t_job_yrs, m_income):

    np.random.seed(45)

    #Population & Ids
    n = t_pop_sample
    application_id = np.arange(90000, 90000 + n)

    #Divide parameters to 3 section

    #First one: basic data and foundations.
    age = np.random.randint(25, 70, size=n) 
    job_years = np.clip(np.random.poisson(lam=t_job_yrs, size=n), 0, 25)
    open_accounts = np.clip(np.random.poisson(lam=6, size=n) + 1, 1, 25)

    #Capacity and possibilities
    monthly_income = np.clip(np.random.lognormal(mean=np.log(m_income), sigma=0.45, size=n), 1600, 25000)
    debt_to_income = np.clip(np.random.beta(t_dti_ratio, 1, size=n), 0, 1)
    credit_utilization = np.clip(np.random.beta(1.1, 2.9, size=n), 0, 1)
    
    #Behaviour
    recent_inquiries = np.clip(np.random.poisson(lam=0.8, size=n), 0, 5)
    late_payments_12m = np.clip(np.random.poisson(lam=t_late_payments, size=n), 0, 12)


    log_income = np.log1p(monthly_income-1200)
    
    #Define model
    z = (
        2.2 * debt_to_income
        + 0.6 * late_payments_12m
        + 0.2 * recent_inquiries
        + 0.17 * (open_accounts - 5)
        - 0.125 * job_years
        + 0.02 * (age - 50)
        + np.random.normal(0.0, 0.1, size=n)
        - 1.5
        - (credit_utilization * 2.5 * (log_income - np.log1p(np.median(monthly_income))))
    )
    
    #Defaulted 12m
    p_default = 1 / (1 + (np.exp(-z)))
    default_12m = np.random.binomial(1, p_default)

    #df
    df = pd.DataFrame({
        "application_id": application_id,
        "age": age,
        "monthly_income": monthly_income,
        "debt_to_income": debt_to_income,
        "credit_utilization": credit_utilization,
        "late_payments_12m": late_payments_12m,
        "job_years": job_years,
        "open_accounts": open_accounts,
        "recent_inquiries": recent_inquiries,
        "default_12m": default_12m,
        "p_def" : p_default,
        "log_income" : log_income,
        "z" : z,
        "median_1p" : np.log1p(np.median(monthly_income))
    
    })

    #Columns 
    col_features = ["age", "monthly_income", "debt_to_income", "credit_utilization", "late_payments_12m", "job_years", "open_accounts", "recent_inquiries", "log_income", "z", "median_1p"]

    
    means = df.groupby("paid_12m")[col_features].mean().T
    means.columns = ["Paid", "non-paid"]
    
    means["diff"] = means["non-paid"] - means["Paid"]

    df["decile"] = pd.qcut(df[sel_tab], 10, labels=False)
    decile_df = df[col_features + ["decile", "paid_12m"]].groupby(["decile"]).mean()
    

    fig = px.bar(decile_df, x=decile_df.index, y="paid_12m")
    
    return fig, decile_df
    
if __name__ == "__main__":
    print(calculations(1000, 0.3, 1, 6))
    
        
