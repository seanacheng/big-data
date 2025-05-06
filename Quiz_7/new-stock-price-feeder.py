#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import time, sys
import pathlib
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
# print (sys.path, file=sys.stderr)

aapl_data = pd.read_csv('twelvedata_stocks_AAPL.csv')
aapl_data["symbol"] = "AAPL"
msft_data = pd.read_csv('twelvedata_stocks_MSFT.csv')
msft_data["symbol"] = "MSFT"

dates = aapl_data.iloc[::-1]['datetime']
init_date = list(dates)[0]
last_hist_date = list(dates)[-1]

stocks = pd.concat([aapl_data, msft_data])

df = stocks.sort_values(by='datetime')

init_delay_seconds = 30
interval = 1

print ('Sending stock prices from %10s to %10s ...' % (str(init_date)[:10], str(last_hist_date)[:10]), flush=True, file=sys.stderr)
print ("... one data row sent every %d seconds ..." % (interval), flush=True, file=sys.stderr)
print ('... beginning in %02d seconds ...' % (init_delay_seconds), flush=True, file=sys.stderr)

from tqdm import tqdm
for left in tqdm(range(init_delay_seconds)):
    time.sleep(0.5)

for idx, row in df.iterrows():
    row.add
    print (json.dumps(row.to_dict()), flush=True)
    time.sleep(float(interval))
