from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import logging
from threading import Thread



api_key='d1zkjgaordrrjgis'
api_secret='owe9bi50r9f8lr71jvvqesm5m86p1emf'
request_token='lv4C6NnXWKzO0vJpr7Ng6TuKY1yeER75'
access_token='uI19de8AKzQKqjToZWKO6Y7gkLC4pe8x'
public_token='ceWhjfvd6dW5doZ2ug5dtDxdLgtTOkov'
kite=KiteConnect(api_key=api_key)

#print(kite.login_url())
#https://kite.trade/connect/login?api_key=d1zkjgaordrrjgis&v=3
#data = kite.generate_session(request_token, api_secret=api_secret)
#access_token=data['access_token']
#public_token= data['public_token']
kite.set_access_token(access_token)


inst=kite.instruments('MCX')




symbols_codes={}
symbols=["CRUDEOIL18NOVFUT"]
symbol_tokens=[]

for i in range(len(inst)):
    for j in range(len(symbols)):
        if inst[i]['tradingsymbol']==symbols[j]:
            symbols_codes.update({inst[i]['tradingsymbol']:{'tradingsymbol':inst[i]['tradingsymbol'],'instrument_token':inst[i]['instrument_token'],'last_price':[],'oi':[],'vol':[],'buy_quantity':[],'sell_quantity':[],'ltq':[]}})
            symbol_tokens.append(inst[i]['instrument_token'])






##############################################TICKER###################################################


class var():
    ts=0
    ticks={}
    ltp=0
    ltp_prev=0
    ltp_diff=0
    ltp_dir=0
    order_id=0
    tpb=10
    tps=-10
    tp=0


class trade_sniffer(Thread):

    def __init__(self):
        Thread.__init__(self)
        print('TI')

    def run(self):
        var.ltp = var.ticks[0]['last_price']
        print('TR')
        if var.ltp_diff!=0:
            var.ltp_dir=var.ltp_dir + abs(var.ltp_diff)/var.ltp_diff



        if var.ltp_dir>=var.tpb and var.ts==0:
            var.order_id = kite.place_order(variety=kite.VARIETY_CO, exchange=kite.EXCHANGE_MCX,
                                        tradingsymbol="CRUDEOIL18NOVFUT",
                                        transaction_type=kite.TRANSACTION_TYPE_BUY,
                                        quantity=1, product=kite.PRODUCT_CO,
                                        order_type=kite.ORDER_TYPE_MARKET,
                                        trigger_price=var.ticks[0]['last_price'] -15,
                                        stoploss=var.ticks[0]['last_price'] - 20)
            var.tp=var.ltp
            var.ts=1
            var.tpb = var.ltp_dir
            var.tps = var.ltp_dir
        elif var.ltp_dir<=var.tps and var.ts==0:
            var.order_id = kite.place_order(variety=kite.VARIETY_CO, exchange=kite.EXCHANGE_MCX,
                                        tradingsymbol="CRUDEOIL18NOVFUT",
                                        transaction_type=kite.TRANSACTION_TYPE_SELL,
                                        quantity=1, product=kite.PRODUCT_CO,
                                        order_type=kite.ORDER_TYPE_MARKET,
                                        trigger_price=var.ticks[0]['last_price'] + 15,
                                        stoploss=var.ticks[0]['last_price'] + 20)
            var.tp = var.ltp
            var.ts=1
            var.tpb = var.ltp_dir
            var.tps = var.ltp_dir
        elif var.ts==1 and var.ltp_dir>=var.tpb+10:
            kite.cancel_order(variety=kite.VARIETY_CO,order_id=var.order_id)
            var.tpb=var.ltp_dir+10
            var.tps = var.ltp_dir - 10
            var.ts=0


        elif var.ts == 1 and var.ltp_dir <= var.tps-10:
            kite.cancel_order(variety=kite.VARIETY_CO, order_id=var.order_id)
            var.ts=0
            var.tps=var.ltp_dir-10
            var.tpb = var.ltp_dir+10


        var.ltp_diff = (var.ltp - var.ltp_prev)
        print("ltp,ltp_prev,ltp_diff,ltp_dir", var.ltp, var.ltp_prev, var.ltp_diff, var.ltp_dir)
        var.ltp_prev = var.ticks[0]['last_price']








logging.basicConfig(level=logging.DEBUG)

# Initialise
kws = KiteTicker(api_key, access_token)



def on_ticks(ws,ticks):
    var.ticks=ticks
    t1.run()


def on_connect(ws, response):
    # Callback on successful connect.
     ws.subscribe(symbol_tokens)
     ws.set_mode(ws.MODE_LTP, symbol_tokens)


def on_order_update(ws,data):
    print('ORDER_UPDATE :',data['status_message'])

def on_close(ws, code, reason):
    ws.stop()

t1=trade_sniffer()
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_order_update=on_order_update
kws.on_close = on_close


kws.connect()




