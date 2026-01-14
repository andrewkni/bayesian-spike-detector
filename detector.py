from market import *
import numpy as np
import time

# Input market ticker here
ticker = "KXNBAGAME-26JAN13SASOKC-SAS"

# Calibrate parameter thresholds of the bot
# EX: a "large" delta_vol differs by market, so you need to define what is "large"
def calibrate():
    duration = 1 * 60 # calibration duration

    delta_vols = []
    delta_spreads = []
    delta_prices = []

    prev_market = fetch_market(ticker)
    init_time = time.time()

    # Collects parameter values over time period
    while time.time() < duration + init_time:
        time.sleep(5)
        curr_market = fetch_market(ticker, prev_market)

        delta_vols.append(curr_market['delta_vol'])
        delta_spreads.append(curr_market['delta_spread'])
        delta_prices.append(curr_market['delta_price'])

        prev_market = curr_market

    delta_vols = np.array(delta_vols)
    delta_spreads = np.array(delta_spreads)
    delta_prices = np.array(delta_prices)

    # Computes percentiles of parameters to determine how much change is "large" or "small"
    # Modify percentiles to determine conservativeness of bot
    # default values ensure bot works in extreme markets (such as when vol = 0 for long times)
    thresholds = {
        "vol_low": max(1, int(np.percentile(delta_vols, 25))),
        "vol_high": max(5, int(np.percentile(delta_vols, 75))),
        "spread_low": max(0, int(np.percentile(delta_spreads, 25))),
        "spread_high": max(1, int(np.percentile(delta_spreads, 75))),

        "price_low" : min(-2, int(np.percentile(delta_prices, 5))),
        "price_high": max(2, int(np.percentile(delta_prices, 95))),
    }

    return thresholds

def main():
    alpha = 2 # evidence that move is a fake spike
    beta = 8 # evidence that move is a real repricing

    print("Calibrating model...")
    thresholds = calibrate()
    print(thresholds)


if __name__ == '__main__':
    main()