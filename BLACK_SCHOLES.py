import numpy as np
import scipy.stats as ss
import time

'''------------------------------------------------------------------------------------------*
black_scholes.py will prompt the user for the current stock price, strike price, continuously
compunded risk-free interest rate, stock volatility, time to maturity of current stock, and 
whether it is a call or a put option. Once given this data, the program will compute the 
Black-Scholes price of the option and display it to the user. 
-- Once the code is written to compute volatility and time to maturity of an option, will be 
able to add that into this program, then have it access the database to pull out the other 
necessary data instead of prompting the user for it.

SO = spot price of underlying asset (current stock price)
T = time to maturity ((T-t) in wikipedia page)
K = strike price
r = risk free rate
sigma = volatility
*-----------------------------------------------------------------------------------------'''

#Prompt user for stock price, strike price, interest rate, volatility and time to maturity.
SO = float(raw_input("Current stock price: "))
K = float(raw_input("Strike price of option: "))
r = float(raw_input("continuously compounded risk-free rate: "))
sigma = float(raw_input("volatility of the stock price per year: "))
T = float(raw_input("time to maturity of current option (in trading years): "))

#Prompt user for Call or Put.
Otype = raw_input("Enter C for call option, P for put option: ")

#Define the Black and Scholes functions.
def d1(SO, K, r, sigma, T):
    return (np.log(SO/K) + (r + sigma**2 / 2) * T)/(sigma * np.sqrt(T))

def d2(SO, K, r, sigma, T):
    return (np.log(SO/K) + (r - sigma**2 / 2) * T)/(sigma * np.sqrt(T))

def BlackScholes(type, SO, K, r, sigma, T):
    if type =="C":
        return SO* ss.norm.cdf(d1(SO, K, r, sigma, T)) - K * np.exp(-r * T) * ss.norm.cdf(d2(SO, K, r, sigma, T))
    else:
        return K * np.exp(-r * T) * ss.norm.cdf(-d2(SO, K, r, sigma, T)) - SO * ss.norm.cdf(-d1(SO, K, r, sigma, T))

'''print "SO\tstock price at time 0:", SO
print "K\tstrike price:", K
print "r\tcontinuously compounded risk-free rate:", r
print "sigma\tvolatility of the stock price per year:", sigma
print "T\ttime to maturity in trading years:", T'''

#Compute the Black-Scholes price as well as the time necessary to compute the Black-Scholes price and display both to the user. 
t = time.time()
c_BS = BlackScholes(Otype, SO, K, r, sigma, T)
elapsed=time.time()-t
print "c_BS\tBlack-Sholes price:", c_BS, "Time needed to compute: ", elapsed
