import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, brier_score_loss

np.random.seed(45)

def main():

    n = 5000 

    application_id = np.arange(90000, 90000 + n)
    age = np.random.randint(25, 70, size=n) 
    monthly_income = np.random.lognormal(mean=np.log(4500), sigma=0.45, size=n)
    monthly_income = np.clip(monthly_income, 800, 25000)

    debt_to_income = np.clip(np.random.beta(0.7, 2, size=n), 0, 1)
    credit_utilization = np.clip(np.random.beta(1.1, 2.9, size=n), 0, 1)

    late_payments_12m = np.clip(np.random.poisson(lam=0.25, size=n), 0, 12)
    job_years = np.clip(np.random.poisson(lam=6, size=n), 0, 25)

    open_accounts = np.clip(np.random.poisson(lam=6, size=n) + 1, 1, 25)
    recent_inquiries = np.clip(np.random.poisson(lam=0.8, size=n), 0, 5)

    log_income = np.log1p(monthly_income)
    print(log_income)
    z = (
        2 * debt_to_income
        + 1.9 * credit_utilization
        + 0.8 * late_payments_12m
        + 0.27 * recent_inquiries
        + 0.17 * (open_accounts - 5)
        - 0.30 * log_income
        - 0.125 * job_years
        - 0.02 * (-age + 50)
        + np.random.normal(0.0, 0.23, size=n)
        - 1.3
    )
    p_default = 1 / (1 + (np.exp(-z)))
    paid_12m = np.random.binomial(1, p_default)

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
        "paid_12m": paid_12m,
        "p_def" : p_default
    })

    col_features = ["age", "monthly_income", "debt_to_income", "credit_utilization", "late_payments_12m", "job_years", "open_accounts", "recent_inquiries"]
    stats = pd.DataFrame(df[["age", "monthly_income", "debt_to_income", "credit_utilization", "late_payments_12m", "job_years", "open_accounts", "recent_inquiries", "paid_12m"]].describe())
    
    means = df.groupby("paid_12m")[col_features].mean().T
    means.columns = ["Paid", "non-paid"]
    
    means["diff"] = means["non-paid"] - means["Paid"]
    df["dti_decile"] = pd.qcut(df["debt_to_income"], 10, labels=False)
    df_viz = df[col_features + ["dti_decile", "paid_12m"]].groupby(["dti_decile"]).mean()
    plt.bar(df_viz.index, df_viz["paid_12m"])
    plt.title("Risk modelling credit score")
    plt.xlabel("DTI Decile")
    plt.ylabel("Default Rate")
    plt.show()
    return df_viz
if __name__ == "__main__":
    df = main()
    print(df)
