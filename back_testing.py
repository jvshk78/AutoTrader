import sqlite3



conn = sqlite3.connect('31_10_18.db')
cur=conn.cursor()
data=[]
symbols=[]
symbols2=['CRUDEOIL18NOVFUT']
tpb=4940
tps=4900
ts=0
pt=50
sl=20
#symbols2=['TATAMOTORS','IOC','SBIN','YESBANK','BANKNIFTY18NOVFUT','CRUDEOIL18NOVFUT','GOLDM18NOVFUT','USDINR18NOVFUT','NIFTY18NOVFUT','NIFTY18NOV10100CE','NIFTY18NOV10100PE','BANKNIFTY18NOV24700CE','BANKNIFTY18NOV24700PE']

symbols=symbols2

val={}

for j in range(len(symbols)):
    cur.execute("select last_price from " + symbols[j])
    data = cur.fetchall()
    val.update({symbols[j]: {'ltp': []}})


    for i in range(len(data)):
        val[symbols[j]]['ltp'].append(data[i][0])



for i in val:

    profit = 0
    k=0
    t=0
    tr={'buy':[],'buy_cl':[],'buy_sl':[],'sell':[],'sell_cl':[],'sell_sl':[]}

    ts=0



    for j in (range(len(val[i]['ltp']))):
##########################BUY##############################
            if val[i]['ltp'][j] >=tpb and ts==0:
                t = val[i]['ltp'][j]
                ts=1
                k=k+1
                tr['buy'].append(t)

            elif val[i]['ltp'][j]>=(t+pt) and ts==1:
                profit=(val[i]['ltp'][j]-t)
                k = k + 1
                ts=0
                tr['buy_cl'].append(val[i]['ltp'][j])
            elif val[i]['ltp'][j] <= (t - sl) and ts == 1:
                profit = (val[i]['ltp'][j] - t)
                ts = 0
                k = k + 1
                tr['buy_sl'].append(val[i]['ltp'][j])
##########################SELL##############################
            elif val[i]['ltp'][j] <=tps and ts==0:
                t=val[i]['ltp'][j]
                ts=-1
                k = k + 1
                tr['sell'].append(t)
            elif val[i]['ltp'][j] <= (t -pt) and ts == -1:
                profit = (t-val[i]['ltp'][j])
                k = k + 1
                ts=0
                tr['sell_cl'].append(val[i]['ltp'][j])
            elif val[i]['ltp'][j] >= (t+sl) and ts == -1:
                profit = (t-val[i]['ltp'][j])
                ts=0
                k = k + 1
                tr['sell_sl'].append(val[i]['ltp'][j])


    print(val[i]['ltp'][j],k,tr,ts,profit)




