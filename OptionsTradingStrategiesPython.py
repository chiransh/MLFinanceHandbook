import numpy as np
import pandas as pd
import itertools
def function(X0, K, T, r, u, d, N, type_put_call = "call"):
    
  print("Options Calculator:")
  print("X0 : %2d, K : %2d, u : %5.2f, d : %5.4f, N : %2d" % (X0, K,u,d,N))
  p_star = (1-d)/(u-d)
  p_up = p_star
  p_down = 1 - p_star
  print("p* : %5.4f" % (p_star))

  columns=['Value','difference']+['X'+str(i) for i in range(N+1)]+['V'+str(i) for i in range(N+1)]+['HS'+str(i) for i in range(1,N+1)]
  table = pd.DataFrame(0.0,index= list(itertools.product("ud", repeat=N)),columns=columns)
  table.index=[''.join(i) for i in table.index]
  table['X0']=float(X0)
  print(table)
  for index,col in table.iterrows():
    base_price = X0
    for t in range (1,N+1): 
      # 
      i = index[0:t].count("u")
      j = t - i
      stock_price = base_price * u**i * d**j
      table.at[index,'X'+str(t)] = stock_price
      #
    if type_put_call == "call":
      difference = max(stock_price - K,0)
    if type_put_call == "put":
      difference = max(K - stock_price,0)
    table.at[index,'difference'] = difference
    #
    table.at[index,'Value'] = difference
    table.at[index,'V'+str(N)] = difference
    
  for t in range (N-1,-1,-1): 
    for index,col in table.iterrows():        
      #
      index_char = index[t]
      #
      if index_char == "u":
        change_char = "d"
        new_index = index[0:t] + change_char + index[t+1:]  
        option_price = p_up * table.loc[index,'V'+str(t+1)] + table.loc[new_index,'V'+str(t+1)] * p_down
        if type_put_call == "call": option_price = max(0, option_price, table.loc[index,'X'+str(t)] - K)
        if type_put_call == "put": option_price = max(0, option_price, K - table.loc[index,'X'+str(t)])
      if index_char == "d":
        change_char = "u"
        new_index = index[0:t] + change_char + index[t+1:]  
        option_price = p_up * table.loc[new_index,'V'+str(t+1)] + table.loc[index,'V'+str(t+1)] * p_down        
        if type_put_call == "call":
            option_price = max(0, option_price, table.loc[index,'X'+str(t)] - K)
        if type_put_call == "put":
            option_price = max(0, option_price, K - table.loc[index,'X'+str(t)])

      table.at[index,'V'+str(t)] = option_price
      V0 = option_price
        
  for index,col in table.iterrows():        
    for t in range (N,0,-1): 
      # 
      if (table.loc[index,'X'+str(t)] - table.loc[index,'X'+str(t-1)]) != 0:
        hedging_strategy = (table.loc[index,'V'+str(t)] - table.loc[index,'V'+str(t-1)]) / (table.loc[index,'X'+str(t)] - table.loc[index,'X'+str(t-1)])

        table.at[index,'HS'+str(t)] = hedging_strategy

  return table

X0=95
K=90
T= 1 # year
r= 0  # 
u=1.17 #(Group 7)
d =1/u
N = 5

# ------------------- Q1  ------------------------
function(X0, K, T, r, u, d, N, "call")

# The price of the option is:
# V0 : $16.03


Value	difference	X0	X1	X2	X3	X4	X5	V0	V1	V2	V3	V4	V5	HS1	HS2	HS3	HS4	HS5
uuuuu	118.282563	118.282563	95.0	111.150000	130.045500	152.153235	178.019285	208.282563	16.031779	26.286641	41.425343	62.153235	88.019285	118.282563	0.634976	0.801180	0.937585	1.000000	1.000000
uuuud	62.153235	62.153235	95.0	111.150000	130.045500	152.153235	178.019285	152.153235	16.031779	26.286641	41.425343	62.153235	88.019285	62.153235	0.634976	0.801180	0.937585	1.000000	1.000000
uuudu	62.153235	62.153235	95.0	111.150000	130.045500	152.153235	130.045500	152.153235	16.031779	26.286641	41.425343	62.153235	40.045500	62.153235	0.634976	0.801180	0.937585	1.000000	1.000000
uuudd	21.150000	21.150000	95.0	111.150000	130.045500	152.153235	130.045500	111.150000	16.031779	26.286641	41.425343	62.153235	40.045500	21.150000	0.634976	0.801180	0.937585	1.000000	1.000000
uuduu	62.153235	62.153235	95.0	111.150000	130.045500	111.150000	130.045500	152.153235	16.031779	26.286641	41.425343	23.709196	40.045500	62.153235	0.634976	0.801180	0.937585	0.864561	1.000000
uudud	21.150000	21.150000	95.0	111.150000	130.045500	111.150000	130.045500	111.150000	16.031779	26.286641	41.425343	23.709196	40.045500	21.150000	0.634976	0.801180	0.937585	0.864561	1.000000
uuddu	21.150000	21.150000	95.0	111.150000	130.045500	111.150000	95.000000	111.150000	16.031779	26.286641	41.425343	23.709196	9.746544	21.150000	0.634976	0.801180	0.937585	0.864561	0.706096
uuddd	0.000000	0.000000	95.0	111.150000	130.045500	111.150000	95.000000	81.196581	16.031779	26.286641	41.425343	23.709196	9.746544	0.000000	0.634976	0.801180	0.937585	0.864561	0.706096
uduuu	62.153235	62.153235	95.0	111.150000	95.000000	111.150000	130.045500	152.153235	16.031779	26.286641	13.347579	23.709196	40.045500	62.153235	0.634976	0.801180	0.641586	0.864561	1.000000
uduud	21.150000	21.150000	95.0	111.150000	95.000000	111.150000	130.045500	111.150000	16.031779	26.286641	13.347579	23.709196	40.045500	21.150000	0.634976	0.801180	0.641586	0.864561	1.000000
ududu	21.150000	21.150000	95.0	111.150000	95.000000	111.150000	95.000000	111.150000	16.031779	26.286641	13.347579	23.709196	9.746544	21.150000	0.634976	0.801180	0.641586	0.864561	0.706096
ududd	0.000000	0.000000	95.0	111.150000	95.000000	111.150000	95.000000	81.196581	16.031779	26.286641	13.347579	23.709196	9.746544	0.000000	0.634976	0.801180	0.641586	0.864561	0.706096
udduu	21.150000	21.150000	95.0	111.150000	95.000000	81.196581	95.000000	111.150000	16.031779	26.286641	13.347579	4.491495	9.746544	21.150000	0.634976	0.801180	0.641586	0.380706	0.706096
uddud	0.000000	0.000000	95.0	111.150000	95.000000	81.196581	95.000000	81.196581	16.031779	26.286641	13.347579	4.491495	9.746544	0.000000	0.634976	0.801180	0.641586	0.380706	0.706096
udddu	0.000000	0.000000	95.0	111.150000	95.000000	81.196581	69.398787	81.196581	16.031779	26.286641	13.347579	4.491495	0.000000	0.000000	0.634976	0.801180	0.641586	0.380706	0.000000
udddd	0.000000	0.000000	95.0	111.150000	95.000000	81.196581	69.398787	59.315203	16.031779	26.286641	13.347579	4.491495	0.000000	0.000000	0.634976	0.801180	0.641586	0.380706	-0.000000
duuuu	62.153235	62.153235	95.0	81.196581	95.000000	111.150000	130.045500	152.153235	16.031779	7.266940	13.347579	23.709196	40.045500	62.153235	0.634976	0.440517	0.641586	0.864561	1.000000
duuud	21.150000	21.150000	95.0	81.196581	95.000000	111.150000	130.045500	111.150000	16.031779	7.266940	13.347579	23.709196	40.045500	21.150000	0.634976	0.440517	0.641586	0.864561	1.000000
duudu	21.150000	21.150000	95.0	81.196581	95.000000	111.150000	95.000000	111.150000	16.031779	7.266940	13.347579	23.709196	9.746544	21.150000	0.634976	0.440517	0.641586	0.864561	0.706096
duudd	0.000000	0.000000	95.0	81.196581	95.000000	111.150000	95.000000	81.196581	16.031779	7.266940	13.347579	23.709196	9.746544	0.000000	0.634976	0.440517	0.641586	0.864561	0.706096
duduu	21.150000	21.150000	95.0	81.196581	95.000000	81.196581	95.000000	111.150000	16.031779	7.266940	13.347579	4.491495	9.746544	21.150000	0.634976	0.440517	0.641586	0.380706	0.706096
dudud	0.000000	0.000000	95.0	81.196581	95.000000	81.196581	95.000000	81.196581	16.031779	7.266940	13.347579	4.491495	9.746544	0.000000	0.634976	0.440517	0.641586	0.380706	0.706096
duddu	0.000000	0.000000	95.0	81.196581	95.000000	81.196581	69.398787	81.196581	16.031779	7.266940	13.347579	4.491495	0.000000	0.000000	0.634976	0.440517	0.641586	0.380706	0.000000
duddd	0.000000	0.000000	95.0	81.196581	95.000000	81.196581	69.398787	59.315203	16.031779	7.266940	13.347579	4.491495	0.000000	0.000000	0.634976	0.440517	0.641586	0.380706	-0.000000
dduuu	21.150000	21.150000	95.0	81.196581	69.398787	81.196581	95.000000	111.150000	16.031779	7.266940	2.069813	4.491495	9.746544	21.150000	0.634976	0.440517	0.205266	0.380706	0.706096
dduud	0.000000	0.000000	95.0	81.196581	69.398787	81.196581	95.000000	81.196581	16.031779	7.266940	2.069813	4.491495	9.746544	0.000000	0.634976	0.440517	0.205266	0.380706	0.706096
ddudu	0.000000	0.000000	95.0	81.196581	69.398787	81.196581	69.398787	81.196581	16.031779	7.266940	2.069813	4.491495	0.000000	0.000000	0.634976	0.440517	0.205266	0.380706	0.000000
ddudd	0.000000	0.000000	95.0	81.196581	69.398787	81.196581	69.398787	59.315203	16.031779	7.266940	2.069813	4.491495	0.000000	0.000000	0.634976	0.440517	0.205266	0.380706	-0.000000
ddduu	0.000000	0.000000	95.0	81.196581	69.398787	59.315203	69.398787	81.196581	16.031779	7.266940	2.069813	0.000000	0.000000	0.000000	0.634976	0.440517	0.205266	0.000000	0.000000
dddud	0.000000	0.000000	95.0	81.196581	69.398787	59.315203	69.398787	59.315203	16.031779	7.266940	2.069813	0.000000	0.000000	0.000000	0.634976	0.440517	0.205266	0.000000	-0.000000
ddddu	0.000000	0.000000	95.0	81.196581	69.398787	59.315203	50.696755	59.315203	16.031779	7.266940	2.069813	0.000000	0.000000	0.000000	0.634976	0.440517	0.205266	-0.000000	0.000000
ddddd	0.000000	0.000000	95.0	81.196581	69.398787	59.315203	50.696755	43.330559	16.031779	7.266940	2.069813	0.000000	0.000000	0.000000	0.634976	0.440517	0.205266	-0.000000	-0.000000




#--------------------------Q2 ----------------------------------

function(X0, K, T, r, u, d, N, "put")

# The price of the option is:
# V0 : $11.03


Value	Payoff	X0	X1	X2	X3	X4	X5	V0	V1	V2	V3	V4	V5	HS1	HS2	HS3	HS4	HS5
uuuuu	0.000000	0.000000	95.0	111.150000	130.045500	152.153235	178.019285	208.282563	11.031779	5.136641	1.379843	0.000000	0.000000	0.000000	-0.365024	-0.198820	-0.062415	0.000000	0.000000
uuuud	0.000000	0.000000	95.0	111.150000	130.045500	152.153235	178.019285	152.153235	11.031779	5.136641	1.379843	0.000000	0.000000	0.000000	-0.365024	-0.198820	-0.062415	0.000000	-0.000000
uuudu	0.000000	0.000000	95.0	111.150000	130.045500	152.153235	130.045500	152.153235	11.031779	5.136641	1.379843	0.000000	0.000000	0.000000	-0.365024	-0.198820	-0.062415	-0.000000	0.000000
uuudd	0.000000	0.000000	95.0	111.150000	130.045500	152.153235	130.045500	111.150000	11.031779	5.136641	1.379843	0.000000	0.000000	0.000000	-0.365024	-0.198820	-0.062415	-0.000000	-0.000000
uuduu	0.000000	0.000000	95.0	111.150000	130.045500	111.150000	130.045500	152.153235	11.031779	5.136641	1.379843	2.559196	0.000000	0.000000	-0.365024	-0.198820	-0.062415	-0.135439	0.000000
uudud	0.000000	0.000000	95.0	111.150000	130.045500	111.150000	130.045500	111.150000	11.031779	5.136641	1.379843	2.559196	0.000000	0.000000	-0.365024	-0.198820	-0.062415	-0.135439	-0.000000
uuddu	0.000000	0.000000	95.0	111.150000	130.045500	111.150000	95.000000	111.150000	11.031779	5.136641	1.379843	2.559196	4.746544	0.000000	-0.365024	-0.198820	-0.062415	-0.135439	-0.293904
uuddd	8.803419	8.803419	95.0	111.150000	130.045500	111.150000	95.000000	81.196581	11.031779	5.136641	1.379843	2.559196	4.746544	8.803419	-0.365024	-0.198820	-0.062415	-0.135439	-0.293904
uduuu	0.000000	0.000000	95.0	111.150000	95.000000	111.150000	130.045500	152.153235	11.031779	5.136641	8.347579	2.559196	0.000000	0.000000	-0.365024	-0.198820	-0.358414	-0.135439	0.000000
uduud	0.000000	0.000000	95.0	111.150000	95.000000	111.150000	130.045500	111.150000	11.031779	5.136641	8.347579	2.559196	0.000000	0.000000	-0.365024	-0.198820	-0.358414	-0.135439	-0.000000
ududu	0.000000	0.000000	95.0	111.150000	95.000000	111.150000	95.000000	111.150000	11.031779	5.136641	8.347579	2.559196	4.746544	0.000000	-0.365024	-0.198820	-0.358414	-0.135439	-0.293904
ududd	8.803419	8.803419	95.0	111.150000	95.000000	111.150000	95.000000	81.196581	11.031779	5.136641	8.347579	2.559196	4.746544	8.803419	-0.365024	-0.198820	-0.358414	-0.135439	-0.293904
udduu	0.000000	0.000000	95.0	111.150000	95.000000	81.196581	95.000000	111.150000	11.031779	5.136641	8.347579	13.294914	4.746544	0.000000	-0.365024	-0.198820	-0.358414	-0.619294	-0.293904
uddud	8.803419	8.803419	95.0	111.150000	95.000000	81.196581	95.000000	81.196581	11.031779	5.136641	8.347579	13.294914	4.746544	8.803419	-0.365024	-0.198820	-0.358414	-0.619294	-0.293904
udddu	8.803419	8.803419	95.0	111.150000	95.000000	81.196581	69.398787	81.196581	11.031779	5.136641	8.347579	13.294914	20.601213	8.803419	-0.365024	-0.198820	-0.358414	-0.619294	-1.000000
udddd	30.684797	30.684797	95.0	111.150000	95.000000	81.196581	69.398787	59.315203	11.031779	5.136641	8.347579	13.294914	20.601213	30.684797	-0.365024	-0.198820	-0.358414	-0.619294	-1.000000
duuuu	0.000000	0.000000	95.0	81.196581	95.000000	111.150000	130.045500	152.153235	11.031779	16.070359	8.347579	2.559196	0.000000	0.000000	-0.365024	-0.559483	-0.358414	-0.135439	0.000000
duuud	0.000000	0.000000	95.0	81.196581	95.000000	111.150000	130.045500	111.150000	11.031779	16.070359	8.347579	2.559196	0.000000	0.000000	-0.365024	-0.559483	-0.358414	-0.135439	-0.000000
duudu	0.000000	0.000000	95.0	81.196581	95.000000	111.150000	95.000000	111.150000	11.031779	16.070359	8.347579	2.559196	4.746544	0.000000	-0.365024	-0.559483	-0.358414	-0.135439	-0.293904
duudd	8.803419	8.803419	95.0	81.196581	95.000000	111.150000	95.000000	81.196581	11.031779	16.070359	8.347579	2.559196	4.746544	8.803419	-0.365024	-0.559483	-0.358414	-0.135439	-0.293904
duduu	0.000000	0.000000	95.0	81.196581	95.000000	81.196581	95.000000	111.150000	11.031779	16.070359	8.347579	13.294914	4.746544	0.000000	-0.365024	-0.559483	-0.358414	-0.619294	-0.293904
dudud	8.803419	8.803419	95.0	81.196581	95.000000	81.196581	95.000000	81.196581	11.031779	16.070359	8.347579	13.294914	4.746544	8.803419	-0.365024	-0.559483	-0.358414	-0.619294	-0.293904
duddu	8.803419	8.803419	95.0	81.196581	95.000000	81.196581	69.398787	81.196581	11.031779	16.070359	8.347579	13.294914	20.601213	8.803419	-0.365024	-0.559483	-0.358414	-0.619294	-1.000000
duddd	30.684797	30.684797	95.0	81.196581	95.000000	81.196581	69.398787	59.315203	11.031779	16.070359	8.347579	13.294914	20.601213	30.684797	-0.365024	-0.559483	-0.358414	-0.619294	-1.000000
dduuu	0.000000	0.000000	95.0	81.196581	69.398787	81.196581	95.000000	111.150000	11.031779	16.070359	22.671026	13.294914	4.746544	0.000000	-0.365024	-0.559483	-0.794734	-0.619294	-0.293904
dduud	8.803419	8.803419	95.0	81.196581	69.398787	81.196581	95.000000	81.196581	11.031779	16.070359	22.671026	13.294914	4.746544	8.803419	-0.365024	-0.559483	-0.794734	-0.619294	-0.293904
ddudu	8.803419	8.803419	95.0	81.196581	69.398787	81.196581	69.398787	81.196581	11.031779	16.070359	22.671026	13.294914	20.601213	8.803419	-0.365024	-0.559483	-0.794734	-0.619294	-1.000000
ddudd	30.684797	30.684797	95.0	81.196581	69.398787	81.196581	69.398787	59.315203	11.031779	16.070359	22.671026	13.294914	20.601213	30.684797	-0.365024	-0.559483	-0.794734	-0.619294	-1.000000
ddduu	8.803419	8.803419	95.0	81.196581	69.398787	59.315203	69.398787	81.196581	11.031779	16.070359	22.671026	30.684797	20.601213	8.803419	-0.365024	-0.559483	-0.794734	-1.000000	-1.000000
dddud	30.684797	30.684797	95.0	81.196581	69.398787	59.315203	69.398787	59.315203	11.031779	16.070359	22.671026	30.684797	20.601213	30.684797	-0.365024	-0.559483	-0.794734	-1.000000	-1.000000
ddddu	30.684797	30.684797	95.0	81.196581	69.398787	59.315203	50.696755	59.315203	11.031779	16.070359	22.671026	30.684797	39.303245	30.684797	-0.365024	-0.559483	-0.794734	-1.000000	-1.000000
ddddd	46.669441	46.669441	95.0	81.196581	69.398787	59.315203	50.696755	43.330559	11.031779	16.070359	22.671026	30.684797	39.303245	46.669441	-0.365024	-0.559483	-0.794734	-1.000000	-1.000000


# --------------Q3 ----------------------------

import numpy as np
import pandas as pd
import itertools
def function(X0, K, T, r, u, d, N, type_put_call = "call", barrier_level ="0"):
    
  print("Options Calculator:")
  print("X0 : %2d, K : %2d, u : %5.2f, d : %5.4f, N : %2d" % (X0, K,u,d,N))
  p_star = (1-d)/(u-d)
  p_up = p_star
  p_down = 1 - p_star
  print("p* : %5.4f" % (p_star))

  columns=['Value','difference']+['X'+str(i) for i in range(N+1)]+['V'+str(i) for i in range(N+1)]+['HS'+str(i) for i in range(1,N+1)]
  table = pd.DataFrame(0.0,index= list(itertools.product("ud", repeat=N)),columns=columns)
  table.index=[''.join(i) for i in table.index]
  table['X0']=float(X0)
  print(table)
  for index,col in table.iterrows():
    base_price = X0
    for t in range (1,N+1): 
      # 
      i = index[0:t].count("u")
      j = t - i
      stock_price = base_price * u**i * d**j
      table.at[index,'X'+str(t)] = stock_price
    if type == "knockout":
        if type_put_call == "call":
          if stock_price >= 130:  
            stock_price = 0
            base_price = 0
        if type_put_call == "put":
          if stock_price <= barrier_level:
            stock_price = 0
            base_price = 0    
    table.at[index,'X'+str(t)] = stock_price
      #
    if type_put_call == "call":
      difference = max(stock_price - K,0)
    if type_put_call == "put":
      difference = max(K - stock_price,0)
    table.at[index,'difference'] = difference
    #
    table.at[index,'Value'] = difference
    table.at[index,'V'+str(N)] = difference
    
  for t in range (N-1,-1,-1): 
    for index,col in table.iterrows():        
      #
      index_char = index[t]
      #
      #
      if index_char == "u":
        change_char = "d"
        new_index = index[0:t] + change_char + index[t+1:]  
        option_price = p_up * table.loc[index,'V'+str(t+1)] + table.loc[new_index,'V'+str(t+1)] * p_down
      if index_char == "d":
        change_char = "u"
        new_index = index[0:t] + change_char + index[t+1:]  
        option_price = p_up * table.loc[new_index,'V'+str(t+1)] + table.loc[index,'V'+str(t+1)] * p_down        

      table.at[index,'V'+str(t)] = option_price
      V0 = option_price
        
  for index,col in table.iterrows():        
    for t in range (N,0,-1): 
      # 
      if (table.loc[index,'X'+str(t)] - table.loc[index,'X'+str(t-1)]) != 0:
        hedging_strategy = (table.loc[index,'V'+str(t)] - table.loc[index,'V'+str(t-1)]) / (table.loc[index,'X'+str(t)] - table.loc[index,'X'+str(t-1)])

        table.at[index,'HS'+str(t)] = hedging_strategy

  return table

X0=100
K=100
T= 1 # year
r= 0  # 
u=1.17 #(Group 7)
d =1/u
N = 5
Barrier_L=130
function(X0, K, T, r, u, d, N ,"call",Barrier_L)

# Value of call option is calculated by 
# (Sigma H(ω)*probabilities) = 17*5 *0.4608^3*(1-0.4608)^2 = 2.418 


	Value	Payoff	X0	X1	X2	X3	X4	X5	V0	V1	V2	V3	V4	V5	HS1	HS2	HS3	HS4	HS5
uuuuu	0.000000	0.000000	95.0	111.150000	130.045500	152.153235	178.019285	208.282563	11.031779	5.136641	1.379843	0.000000	0.000000	0.000000	-0.365024	-0.198820	-0.062415	0.000000	0.000000
uuuud	0.000000	0.000000	95.0	111.150000	130.045500	152.153235	178.019285	152.153235	11.031779	5.136641	1.379843	0.000000	0.000000	0.000000	-0.365024	-0.198820	-0.062415	0.000000	-0.000000
uuudu	0.000000	0.000000	95.0	111.150000	130.045500	152.153235	130.045500	152.153235	11.031779	5.136641	1.379843	0.000000	0.000000	0.000000	-0.365024	-0.198820	-0.062415	-0.000000	0.000000
uuudd	0.000000	0.000000	95.0	111.150000	130.045500	152.153235	130.045500	111.150000	11.031779	5.136641	1.379843	0.000000	0.000000	0.000000	-0.365024	-0.198820	-0.062415	-0.000000	-0.000000
uuduu	0.000000	0.000000	95.0	111.150000	130.045500	111.150000	130.045500	152.153235	11.031779	5.136641	1.379843	2.559196	0.000000	0.000000	-0.365024	-0.198820	-0.062415	-0.135439	0.000000
uudud	0.000000	0.000000	95.0	111.150000	130.045500	111.150000	130.045500	111.150000	11.031779	5.136641	1.379843	2.559196	0.000000	0.000000	-0.365024	-0.198820	-0.062415	-0.135439	-0.000000
uuddu	0.000000	0.000000	95.0	111.150000	130.045500	111.150000	95.000000	111.150000	11.031779	5.136641	1.379843	2.559196	4.746544	0.000000	-0.365024	-0.198820	-0.062415	-0.135439	-0.293904
uuddd	8.803419	8.803419	95.0	111.150000	130.045500	111.150000	95.000000	81.196581	11.031779	5.136641	1.379843	2.559196	4.746544	8.803419	-0.365024	-0.198820	-0.062415	-0.135439	-0.293904
uduuu	0.000000	0.000000	95.0	111.150000	95.000000	111.150000	130.045500	152.153235	11.031779	5.136641	8.347579	2.559196	0.000000	0.000000	-0.365024	-0.198820	-0.358414	-0.135439	0.000000
uduud	0.000000	0.000000	95.0	111.150000	95.000000	111.150000	130.045500	111.150000	11.031779	5.136641	8.347579	2.559196	0.000000	0.000000	-0.365024	-0.198820	-0.358414	-0.135439	-0.000000
ududu	0.000000	0.000000	95.0	111.150000	95.000000	111.150000	95.000000	111.150000	11.031779	5.136641	8.347579	2.559196	4.746544	0.000000	-0.365024	-0.198820	-0.358414	-0.135439	-0.293904
ududd	8.803419	8.803419	95.0	111.150000	95.000000	111.150000	95.000000	81.196581	11.031779	5.136641	8.347579	2.559196	4.746544	8.803419	-0.365024	-0.198820	-0.358414	-0.135439	-0.293904
udduu	0.000000	0.000000	95.0	111.150000	95.000000	81.196581	95.000000	111.150000	11.031779	5.136641	8.347579	13.294914	4.746544	0.000000	-0.365024	-0.198820	-0.358414	-0.619294	-0.293904
uddud	8.803419	8.803419	95.0	111.150000	95.000000	81.196581	95.000000	81.196581	11.031779	5.136641	8.347579	13.294914	4.746544	8.803419	-0.365024	-0.198820	-0.358414	-0.619294	-0.293904
udddu	8.803419	8.803419	95.0	111.150000	95.000000	81.196581	69.398787	81.196581	11.031779	5.136641	8.347579	13.294914	20.601213	8.803419	-0.365024	-0.198820	-0.358414	-0.619294	-1.000000
udddd	30.684797	30.684797	95.0	111.150000	95.000000	81.196581	69.398787	59.315203	11.031779	5.136641	8.347579	13.294914	20.601213	30.684797	-0.365024	-0.198820	-0.358414	-0.619294	-1.000000
duuuu	0.000000	0.000000	95.0	81.196581	95.000000	111.150000	130.045500	152.153235	11.031779	16.070359	8.347579	2.559196	0.000000	0.000000	-0.365024	-0.559483	-0.358414	-0.135439	0.000000
duuud	0.000000	0.000000	95.0	81.196581	95.000000	111.150000	130.045500	111.150000	11.031779	16.070359	8.347579	2.559196	0.000000	0.000000	-0.365024	-0.559483	-0.358414	-0.135439	-0.000000
duudu	0.000000	0.000000	95.0	81.196581	95.000000	111.150000	95.000000	111.150000	11.031779	16.070359	8.347579	2.559196	4.746544	0.000000	-0.365024	-0.559483	-0.358414	-0.135439	-0.293904
duudd	8.803419	8.803419	95.0	81.196581	95.000000	111.150000	95.000000	81.196581	11.031779	16.070359	8.347579	2.559196	4.746544	8.803419	-0.365024	-0.559483	-0.358414	-0.135439	-0.293904
duduu	0.000000	0.000000	95.0	81.196581	95.000000	81.196581	95.000000	111.150000	11.031779	16.070359	8.347579	13.294914	4.746544	0.000000	-0.365024	-0.559483	-0.358414	-0.619294	-0.293904
dudud	8.803419	8.803419	95.0	81.196581	95.000000	81.196581	95.000000	81.196581	11.031779	16.070359	8.347579	13.294914	4.746544	8.803419	-0.365024	-0.559483	-0.358414	-0.619294	-0.293904
duddu	8.803419	8.803419	95.0	81.196581	95.000000	81.196581	69.398787	81.196581	11.031779	16.070359	8.347579	13.294914	20.601213	8.803419	-0.365024	-0.559483	-0.358414	-0.619294	-1.000000
duddd	30.684797	30.684797	95.0	81.196581	95.000000	81.196581	69.398787	59.315203	11.031779	16.070359	8.347579	13.294914	20.601213	30.684797	-0.365024	-0.559483	-0.358414	-0.619294	-1.000000
dduuu	0.000000	0.000000	95.0	81.196581	69.398787	81.196581	95.000000	111.150000	11.031779	16.070359	22.671026	13.294914	4.746544	0.000000	-0.365024	-0.559483	-0.794734	-0.619294	-0.293904
dduud	8.803419	8.803419	95.0	81.196581	69.398787	81.196581	95.000000	81.196581	11.031779	16.070359	22.671026	13.294914	4.746544	8.803419	-0.365024	-0.559483	-0.794734	-0.619294	-0.293904
ddudu	8.803419	8.803419	95.0	81.196581	69.398787	81.196581	69.398787	81.196581	11.031779	16.070359	22.671026	13.294914	20.601213	8.803419	-0.365024	-0.559483	-0.794734	-0.619294	-1.000000
ddudd	30.684797	30.684797	95.0	81.196581	69.398787	81.196581	69.398787	59.315203	11.031779	16.070359	22.671026	13.294914	20.601213	30.684797	-0.365024	-0.559483	-0.794734	-0.619294	-1.000000
ddduu	8.803419	8.803419	95.0	81.196581	69.398787	59.315203	69.398787	81.196581	11.031779	16.070359	22.671026	30.684797	20.601213	8.803419	-0.365024	-0.559483	-0.794734	-1.000000	-1.000000
dddud	30.684797	30.684797	95.0	81.196581	69.398787	59.315203	69.398787	59.315203	11.031779	16.070359	22.671026	30.684797	20.601213	30.684797	-0.365024	-0.559483	-0.794734	-1.000000	-1.000000
ddddu	30.684797	30.684797	95.0	81.196581	69.398787	59.315203	50.696755	59.315203	11.031779	16.070359	22.671026	30.684797	39.303245	30.684797	-0.365024	-0.559483	-0.794734	-1.000000	-1.000000
ddddd	46.669441	46.669441	95.0	81.196581	69.398787	59.315203	50.696755	43.330559	11.031779	16.070359	22.671026	30.684797	39.303245	46.669441	-0.365024	-0.559483	-0.794734	-1.000000	-1.000000