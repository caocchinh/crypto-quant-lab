import random

def generate_random_portfolio_values(keys):
    portfolio = {}
    remaining = 100
    for key in keys[:-1]:
        value = random.uniform(0, remaining)
        portfolio[key] = round(value, 2)
        remaining -= value
    portfolio[keys[-1]] = round(remaining, 2)
    return portfolio

# Example usage
keys = ['L_ALGO_3X', 'L_ETH_10X', 'L_HBAR_3X', 'L_IMX_1X', 'L_MINA_3X', 'L_OP_2X', 'L_RNDR_2X', 'L_SEI_2X', 'L_SKL_3X', 'L_SOL_3X', 'L_THETA_2X', 'L_VET_1X', 'S_ARB_2X', 'S_FTM_2X', 'S_MATIC_3X']
random_portfolio = generate_random_portfolio_values(keys)
print(random_portfolio)
