import numpy as np
import pandas as pd
from functools import lru_cache


class CreditData:
    def __init__(self, seed: int = 42):
        self.seed = seed
    
    def __hash__(self):
        return hash((self.seed))
    
    def __eq__(self, other):
        return (self.seed == other.seed)
    
    @lru_cache(maxsize=64)
    def generateData(self,  
                     credit_years: int, 
                     pop_sample: int, 
                     dti_ratio: float, 
                     late_payments: int, 
                     job_yrs: int, 
                     monthly_income: float,
                     base_id: int = 0) -> pd.DataFrame:
        
        rng = np.random.default_rng(self.seed)
        
        #ID
        application_id = np.arange(base_id, base_id + pop_sample)
        
        #Basic data and foundations, all natural numbers
        age = rng.integers(25, 70, size=pop_sample)
        age_of_credit = np.clip(rng.poisson(lam=credit_years, size=pop_sample), 0, 15)
        job_years = np.clip(rng.poisson(lam=job_yrs, size=pop_sample), 0, 25)
        open_accounts = np.clip(rng.poisson(lam=6, size=pop_sample) + 1, 1, 25) 

        #Capacity
        monthly_income = np.clip(rng.lognormal(mean=np.log(monthly_income), sigma=0.45, size=pop_sample), 1600, 25000)
        debt_to_income = np.clip(rng.beta(dti_ratio, 1, size=pop_sample), 0, 1)
        credit_utilization = np.clip(rng.beta(1.1, 2.9, size=pop_sample), 0, 1)

        #Behaviour
        recent_inquiries = np.clip(rng.poisson(lam=0.8, size=pop_sample), 0, 5)
        late_payments_12m = np.clip(rng.poisson(lam=late_payments, size=pop_sample), 0, 12)

        #Creating DataFrame
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
        })

        return df
    
if __name__ == "__main__":
    generator = CreditData()
    df = generator.generateData(
        credit_years=4,
        pop_sample=1000,
        dti_ratio=0.35,
        late_payments=3,
        job_yrs=6,
        monthly_income=5000
    )
    print(df)