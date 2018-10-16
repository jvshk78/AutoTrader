from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import logging
from matplotlib import pyplot as plt


api_key='d1zkjgaordrrjgis'
api_secret='owe9bi50r9f8lr71jvvqesm5m86p1emf'
request_token='93DbHWLMyrGl5Q1FEhUCetRwFv2ZAO3A'
access_token='e6hF73KPIIyEejVcmFLJNrgZ3wVTL9fY'
public_token= 'pyqYebsfHJ7o7XILjvtxG22IzV0R1s5I'

kite=KiteConnect(api_key=api_key)

#print(kite.login_url())
#data = kite.generate_session(request_token, api_secret=api_secret)
kite.set_access_token(access_token)
#print(data)

#print(kite.ltp(12438530))
#print(kite.ltp(256265))

##############################################TICKER###################################################

class var():
    tc=0
    a=[]
    b=[]
    c=[]
    inst=[53835015]


logging.basicConfig(level=logging.DEBUG)

# Initialise
kws = KiteTicker(api_key, access_token)

#plt.ion()
fig,ax1=plt.subplots(3,2)
ax1[0,0].set_title('Volume')
ax1[1,0].set_title("OI")
ax1[0,1].set_title("LTP")

def on_ticks(ws, ticks):
    # Callback to receive ticks.
    #logging.debug("Ticks: {}".format(ticks))
    #print(ticks)
    #print(len(ticks))
    var.tc=var.tc+1
    if var.tc>=1000:
        var.a.clear()
        var.b.clear()
        var.c.clear()
        var.tc=0
        plt.close()




    for i in range(len(ticks)):

        if(ticks[i]['instrument_token']== var.inst[0]):
            var.a.append(ticks[i]['volume'])
        #elif(ticks[i]['instrument_token']== 14518018):
            var.b.append(ticks[i]['oi'])
            var.c.append(ticks[i]['last_price'])

        ax1[0,0].plot(var.a)
        plt.pause(0.01)

        ax1[1,0].plot(var.b)
        plt.pause(0.01)

        ax1[0,1].plot(var.c)
        plt.pause(0.01)


    plt.show()


def on_connect(ws, response):
    # Callback on successful connect.
     ws.subscribe(var.inst)
     ws.set_mode(ws.MODE_FULL, var.inst)

def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()

# Assign the callbacks.
plt.ion()
kws.on_ticks = on_ticks
kws.on_connect = on_connect
#kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()
