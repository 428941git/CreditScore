import numpy as np 
import pandas as pd 



def main():
    np.random.seed(45)
    
    n = 5000 
    application_id = np.arange(100000, 100000 + n)

    age = np.random.randint(21, 70, size=n) 
    monthly_income = np.random.lognormal(mean=np.log(4500), sigma=0.45, size=n)
    monthly_income = np.clip(monthly_income, 800, 25000)

    debt_to_income = np.clip(np.random.beta(2.2, 5.5, size=n), 0, 1)


if __name__ == "__main__":
    main()
