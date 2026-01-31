import numpy as np
from numpy import exp
import scipy.stats
from scipy.optimize import curve_fit


# greeks for black scholes: https://www.macroption.com/black-scholes-formula/
# V Option Price
# S Stock Price
# K Strike Price
# T Time till expiration in years
# r risk free rate (as 0.04)
# q dividend rate (as 0.02)
# sigma implied volatility

def black_scholes_call_implied_volatility(V, S, K, T, r, q):
    func = lambda sigma: V - black_scholes_call_price(S, K, T, r, q, sigma)
    sigma = 0
    try:
        sigma = scipy.optimize.brentq(func, -100, 100, xtol=0.001)
    except:
        print('black_scholes_call_implied_volatility failed: ' + str(V) + ' ' + str(S) + ' ' + str(K) + ' ' + str(
            T) + ' ' + str(r) + ' ' + str(q))
    return sigma



def black_scholes_put_implied_volatility(V, S, K, T, r, q):
    func = lambda sigma: V - black_scholes_put_price(S, K, T, r, q, sigma)
    sigma = 0
    try:
        sigma = scipy.optimize.brentq(func, -100, 100, xtol=0.001)
    except:
        print('black_scholes_put_implied_volatility failed: ' + str(V) + ' ' + str(S) + ' ' + str(K) + ' ' + str(
            T) + ' ' + str(r) + ' ' + str(q))
    return sigma


def black_scholes_call_price(S, K, T, r, q, sigma):
    d1 = (np.log(S / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * np.exp(-q * T) * scipy.special.ndtr(d1) - K * np.exp(-r * T) * scipy.special.ndtr(d2)


def black_scholes_put_price(S, K, T, r, q, sigma):
    d1 = (np.log(S / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * scipy.special.ndtr(-d2) - S * np.exp(-q * T) * scipy.special.ndtr(-d1)


def black_scholes_call_delta(S, K, T, r, q, sigma):
    d1 = (np.log(S / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    return np.exp(-q * T) * scipy.special.ndtr(d1)


def black_scholes_put_delta(S, K, T, r, q, sigma):
    d1 = (np.log(S / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    return np.exp(-q * T) * (scipy.special.ndtr(d1) - 1)


def black_scholes_gamma(S, K, T, r, q, sigma):
    d1 = (np.log(S / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    return np.exp(-q * T) * scipy.stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))


def black_scholes_call_theta(S, K, T, r, q, sigma):
    trading_days = 252
    d1 = (np.log(S / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    a = S * sigma * np.exp(-q * T) * scipy.stats.norm.pdf(d1) / (2 * np.sqrt(T))
    b = r * K * np.exp(-r * T) * scipy.special.ndtr(d2)
    c = q * S * np.exp(-q * T) * scipy.special.ndtr(d1)
    return (1 / trading_days) * (-a - b + c)


def black_scholes_put_theta(S, K, T, r, q, sigma):
    trading_days = 252
    d1 = (np.log(S / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    a = S * sigma * np.exp(-q * T) * scipy.stats.norm.pdf(d1) / (2 * np.sqrt(T))
    b = r * K * np.exp(-r * T) * scipy.special.ndtr(-d2)
    c = q * S * np.exp(-q * T) * scipy.special.ndtr(-d1)
    return (1 / trading_days) * (-a + b - c)


# Example input for black_scholes_put_delta
S = 100  # Stock price
K = 110  # Strike price
T = 1.0  # Time to expiration in years
r = 0.05  # Risk-free interest rate
q = 0.0  # Dividend yield
sigma = 0.5  # Implied volatility

# Calculate the put delta
put_delta = black_scholes_put_delta(S, K, T, r, q, sigma)
print("Put Delta:", put_delta)