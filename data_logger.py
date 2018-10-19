from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import logging
from threading import Thread

import sqlite3

api_key='d1zkjgaordrrjgis'
api_secret='owe9bi50r9f8lr71jvvqesm5m86p1emf'
request_token='dbKPPnGGwAhfDqxmR4LxDGKO8nYCdCq1'
access_token='StMbcnM2Ya8OBfFnQsgSuuG0pfFpiQAN'
public_token= 'MfurE0Mk3exQqf2csdbcDK0apzPyogaf'
kite=KiteConnect(api_key=api_key)

#print(kite.login_url())
#data = kite.generate_session(request_token, api_secret=api_secret)
kite.set_access_token(access_token)
#print(data)

#print(kite.ltp(12438530))
#print(kite.ltp(256265))
#inst=kite.instruments('NFO')

############################################DATABASE OPERATIONS##################################################
ltp_nifty50=10443.95#kite.ltp(256265)['256265']['last_price']
ltp_niftybank=25188#kite.ltp(260105)['260105']['last_price']

strike_nifty50=100*int(ltp_nifty50/100)-400
strike_niftybank=100*int(ltp_niftybank/100)-400

index=[256265,260105]
fut=[12438530,12434434]
symbols_codes={}
symbols=[]
symbol_tokens=[]

for i in range(9):
    symbols.append("NIFTY18OCT"+str(strike_nifty50+(100*i))+"CE")
    symbols.append("NIFTY18OCT"+str(strike_nifty50+(100*i))+"PE")
    symbols.append("BANKNIFTY18OCT"+str(strike_niftybank+(100*i))+"CE")
    symbols.append("BANKNIFTY18OCT"+str(strike_niftybank+(100*i))+"PE")


symbols.append("NIFTY18OCTFUT")
symbols.append("BANKNIFTY18OCTFUT")



inst=kite.instruments('NFO')
for i in range(len(inst)):
    for j in range(len(symbols)):
        if inst[i]['tradingsymbol']==symbols[j]:
            symbols_codes.update({inst[i]['tradingsymbol']:{'tradingsymbol':inst[i]['tradingsymbol'],'instrument_token':inst[i]['instrument_token'],'last_price':[],'oi':[],'vol':[],'buy_quantity':[],'sell_quantity':[],'ltq':[]}})
            symbol_tokens.append(inst[i]['instrument_token'])

#print(symbols)
#print(symbols_codes)


conn=sqlite3.connect('inst6.db')
for key in symbols_codes:
    conn.execute("create table if not exists " + key + " (instrument_token int not null,last_price int not null,oi int not null,vol int not null,buy_quantity int not null,sell_quantity int not null,ltq int not null)")

conn.execute("create table if not exists indx(nifty50 int not null,banknifty int not null)")
conn.commit()

##############################################################################################################################



##############################################TICKER###################################################


class var():
    tc=0
    ticks={}





logging.basicConfig(level=logging.DEBUG)

# Initialise
kws = KiteTicker(api_key, access_token)



def on_ticks(ws,data):
    var.ticks=data
    # Callback to receive ticks.
    #logging.debug("Ticks: {}".format(data))
    #print(ticks)
    #print(len(ticks))

    #var.tc=var.tc+1
    #if var.tc>=1000:
        #var.tc=0
       # plt.close()

    pt.run()




def on_connect(ws, response):
    # Callback on successful connect.
     ws.subscribe(symbol_tokens)
     ws.set_mode(ws.MODE_FULL, symbol_tokens)




def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()

# Assign the callbacks.

kws.on_ticks = on_ticks
kws.on_connect = on_connect
#kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.


class plotter(Thread):
    def __init__(self):
        Thread.__init__(self)


    def run(self):

        for key in symbols_codes:
            for j in range(len(var.ticks)):
                if (var.ticks[j]['instrument_token'] == symbols_codes[key]['instrument_token']):
                    conn.execute("insert into " + key + "(instrument_token ,last_price ,oi ,vol ,buy_quantity ,sell_quantity,ltq) values(?,?,?,?,?,?,?)",
                        (var.ticks[j]['instrument_token'],var.ticks[j]['last_price'],var.ticks[j]['oi'],var.ticks[j]['volume'],var.ticks[j]['buy_quantity'],var.ticks[j]['sell_quantity'],var.ticks[j]['last_quantity']))
                if (var.ticks[j]['instrument_token']==256265):
                    conn.execute("insert into indx (nifty50) values(?)",(var.ticks[j]['last_price']))
                if(var.ticks[j]['instrument_token']==260105):
                    conn.execute("insert into indx (banknifty) values(?)", (var.ticks[j]['last_price']))
                conn.commit()
                #print(var.ticks)








pt = plotter()
pt.start()
kws.connect()

#conn = sqlite3.connect('inst.db')
#cur=conn.cursor()
#cur.execute("select * from NIFTY18OCT10500PE")
#data=cur.fetchall()
