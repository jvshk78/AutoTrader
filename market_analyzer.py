from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import logging
from threading import Thread
from matplotlib import pyplot as plt


api_key='d1zkjgaordrrjgis'
api_secret='owe9bi50r9f8lr71jvvqesm5m86p1emf'
request_token='ptrZs5a3JToJOb4vbW4vxnwMJSM3v2RI'
access_token='CrmTQ097FzEgR7J3dtzXsdndcGlHzUAN'
public_token= 'EaEtK3DCbVBe7AmfH0DQWNtlrWBVwScG'
kite=KiteConnect(api_key=api_key)

#print(kite.login_url())
#data = kite.generate_session(request_token, api_secret=api_secret)
kite.set_access_token(access_token)
#print(data)

#print(kite.ltp(12438530))
#print(kite.ltp(256265))
#inst=kite.instruments('NFO')
##############################################TICKER###################################################


class var():
    tc=0
    ticks={}
    inst_index=[256265,260105]
    #inst_all=[14512130,14514690,14517762,14598658,14605058,14512386,14515970,14518018,14598914,14607362,12438530,12434434,311555,368643,370947]
    inst_all = [311555, 368643, 370947]

    data={}

inst=kite.instruments('CDS')
for i in range(len(inst)):
    for j in range(len(var.inst_all)):
        if inst[i]['instrument_token']==var.inst_all[j]:
            var.data.update({inst[i]['tradingsymbol']:{'tradingsymbol':inst[i]['tradingsymbol'],'instrument_token':inst[i]['instrument_token'],'last_price':[],'oi':[],'vol':[],'buy_quantity':[],'sell_quantity':[],'ltq':[]}})



logging.basicConfig(level=logging.DEBUG)

# Initialise
kws = KiteTicker(api_key, access_token)

plt.ion()
fig1, ax1 = plt.subplots(6,len(var.inst_all))

for i in range(len(var.inst_all)):
    for key in var.data:
        if var.inst_all[i]==var.data[key]['instrument_token']:
            ax1[0,i].set_title(var.data[key]['tradingsymbol'])

ax1[0, 0].set_ylabel("LTP")
ax1[1, 0].set_ylabel("VOL")
ax1[2, 0].set_ylabel("OI")
ax1[3, 0].set_ylabel("BUY_qty")
ax1[4, 0].set_ylabel("SELL_qty")
ax1[5, 0].set_ylabel("LTQ")
plt.show()

#plt.plot()
#plt.pause(0.01)
#plt.show()
#fig2, ax2 = plt.subplots(len(var.inst_call), 2)
#fig, ax = plt.subplots(len(var.inst_index), 2)

def on_ticks(ws,data):
    var.ticks=data
    # Callback to receive ticks.
    logging.debug("Ticks: {}".format(data))
    #print(ticks)
    #print(len(ticks))

    #var.tc=var.tc+1
    #if var.tc>=1000:
        #var.tc=0
       # plt.close()

    pt.run()




def on_connect(ws, response):
    # Callback on successful connect.
     ws.subscribe(var.inst_all)
     ws.set_mode(ws.MODE_FULL, var.inst_all)




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

        for i in range(len(var.ticks)):
            for key in var.data:
                if (var.ticks[i]['instrument_token'] == var.data[key]['instrument_token']):
                    var.data[key]['last_price'].append(var.ticks[i]['last_price'])
                    var.data[key]['oi'].append(var.ticks[i]['oi'])
                    var.data[key]['vol'].append(var.ticks[i]['volume'])
                    var.data[key]['buy_quantity'].append(var.ticks[i]['buy_quantity'])
                    var.data[key]['sell_quantity'].append(var.ticks[i]['sell_quantity'])
                    var.data[key]['ltq'].append(var.ticks[i]['last_quantity'])

        for i in range(len(var.inst_all)):
            for key in var.data:
                if var.inst_all[i] == var.data[key]['instrument_token']:
                    ax1[0,i].plot(var.data[key]['last_price'])
                    plt.pause(0.01)
                    ax1[1, i].plot(var.data[key]['vol'])
                    plt.pause(0.01)
                    ax1[2, i].plot(var.data[key]['oi'])
                    plt.pause(0.01)
                    ax1[3,i].plot(var.data[key]['buy_quantity'])
                    plt.pause(0.01)
                    ax1[4, i].plot(var.data[key]['sell_quantity'])
                    plt.pause(0.01)
                    ax1[5, i].plot(var.data[key]['ltq'])
                    plt.pause(0.01)
                #plt.show()




       # print(var.data)


pt = plotter()
pt.start()
kws.connect()
