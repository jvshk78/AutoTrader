from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import logging
from matplotlib import pyplot as plt


api_key='d1zkjgaordrrjgis'
api_secret='owe9bi50r9f8lr71jvvqesm5m86p1emf'
request_token='neDeyA1xuMgtXcSsvFHefjWbwksWQClM'
access_token='0bMObxywbA6nZJv9A8u5QeC501W40SIZ'
public_token= 'OS7aGbpO3T9SrXQOMTd2zEi9OZc82mfp'

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
    inst_index=[256265,260105]
    inst_fut=[12438530, 12434434]
    inst_call=[14512130,14514690,14517762,14598658,14605058]
    inst_put=[14512386,14515970,14518018,14598914,14607362]
    inst_all=[14512130,14514690,14517762,14598658,14605058,14512386,14515970,14518018,14598914,14607362,256265,260105,12438530,12434434]

    oi=['oi1','oi2','oi3','oi4','oi5']
    ltp=['ltp1','ltp2','ltp3','ltp4','ltp5']

    oi_call={'oi1':[],'oi2':[],'oi3':[],'oi4':[],'oi5':[]}
    oi_put = {'oi1': [], 'oi2': [], 'oi3': [], 'oi4': [], 'oi5': []}

    ltp_call={'ltp1':[],'ltp2':[],'ltp3':[],'ltp4':[],'ltp5':[]}
    ltp_put = {'ltp1': [], 'ltp2': [], 'ltp3': [], 'ltp4': [], 'ltp5': []}
    index_val=[[],[]]
    fut_val=[[],[]]
    span_val=[[],[]]



#logging.basicConfig(level=logging.DEBUG)

# Initialise
kws = KiteTicker(api_key, access_token)

plt.ion()
fig1,ax1=plt.subplots(len(var.inst_call),2)
fig2,ax2=plt.subplots(len(var.inst_call),2)
fig,ax=plt.subplots(len(var.inst_index),2)

def on_ticks(ws, ticks):
    # Callback to receive ticks.
    #logging.debug("Ticks: {}".format(ticks))
    #print(ticks)
    #print(len(ticks))
    var.tc=var.tc+1
    if var.tc>=1000:
        var.tc=0
        plt.close()

    for i in range(len(ticks)):
        for j in range(len(var.inst_call)):
            if(ticks[i]['instrument_token']== var.inst_call[j]):
                    var.oi_call[var.oi[j]].append(ticks[i]['oi'])
                    var.ltp_call[var.ltp[j]].append(ticks[i]['last_price'])

        for j in range(len(var.inst_put)):
            if (ticks[i]['instrument_token'] == var.inst_put[j]):
                var.oi_put[var.oi[j]].append(ticks[i]['oi'])
                var.ltp_put[var.ltp[j]].append(ticks[i]['last_price'])

        for j in range(len(var.inst_index)):
            if (ticks[i]['instrument_token'] == var.inst_index[j]):
                var.index_val[j].append(ticks[i]['last_price'])
                print("index",var.index_val)

        for j in range(len(var.inst_fut)):
            if (ticks[i]['instrument_token'] == var.inst_fut[j]):
                var.fut_val[j].append(ticks[i]['last_price'])
                print("future",var.fut_val)

        #var.span_val[0].append(var.fut_val[0][len(var.fut_val[0])-1] - var.index_val[0][len(var.index_val[0])-1])
       # var.span_val[1].append(var.fut_val[1][len(var.fut_val[1])-1] - var.index_val[1][len(var.index_val[1])-1])

    for i in range(len(var.inst_call)):
        ax2[i,0].plot(var.oi_call[var.oi[i]])
        plt.pause(0.01)
        ax2[i, 1].plot(var.oi_put[var.oi[i]])
        plt.pause(0.01)

        ax1[i, 0].plot(var.ltp_call[var.ltp[i]])
        plt.pause(0.01)
        ax1[i, 1].plot(var.ltp_put[var.ltp[i]])
        plt.pause(0.01)

    ax[0,0].plot(var.index_val[0])
    plt.pause(0.01)
    ax[0, 0].plot(var.fut_val[0])
    plt.pause(0.01)

    ax[0,1].plot(var.index_val[1])
    plt.pause(0.01)
    ax[0, 1].plot(var.fut_val[1])
    plt.pause(0.01)

    #ax[1,0].plot(var.span_val[0])
    #plt.pause(0.01)
    #ax[1,1].plot(var.span_val[1])
    #plt.pause(0.01)



    plt.show()


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
kws.connect()
