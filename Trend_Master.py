# url https://kite.trade/connect/login?api_key=bo8zwjhads913zkl&v=3
# crudeM CMtoken=[53556999],crude Ctoken=[53556743]
# pos_instrument_token=kite.positions()['day'][0]['instrument_token']
# pos_instrument_quantity=kite.positions()['day'][0]['quantity']
# public_token= '81050eef4528c1946fbbdbe020c9813a'
# refresh_token= 'c1qxb49G5kmt5a62mZXzCU5CmrNQBj4T'
# variety="regular",
# order_id = kite.place_order(variety='CO',tradingsymbol="CRUDEOILM18APRFUT",exchange=kite.EXCHANGE_MCX,transaction_type=kite.TRANSACTION_TYPE_BUY,quantity=1,or
# der_type=kite.ORDER_TYPE_MARKET,product=kite.PRODUCT_CO,trigger_price=4090)
# kite.exit_order(variety='CO',order_id=order_id)
#SBIN=[128028676]
""""" t1=kite.orders()#   for i in range(len(t1)): print(t1[i]['status_message'])  #
for i in range(len(t1)): if (t1[i]['status']=='TRIGGER PENDING'):  print(t1[i]['order_id']) """

from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
from threading import Thread


api_key = "bo8zwjhads913zkl"
api_secret = "gvx3ilgcmgd9kbope2ty7f4qffddwwwg"
request_token = "DSDw9gA19tYJ4uNAhkFvDod7EbnnM0XA"
access_token = "GnjjRzFHp2JcRvCK0VhbbLtUMd45kkux"
kite = KiteConnect(api_key=api_key)
#data = kite.generate_session(request_token, api_secret)
#access_token=data['access_token']
#print(access_token)
kws = KiteTicker(api_key, access_token)
kite.set_access_token(access_token)


class c1:
    ltp = 0
    i = 0
    tc = 0
    trades = 0
    order_id_buy = 0
    order_id_sell=0
    trade_price=0
    buy=0
    sell=0
    sl=5
    sl_p=0
    sl_adjust=2
    tradingsymbol = "CRUDEOILM18APRFUT"
    CRUDEOIL18APRFUT = [53556743]
    CRUDEOILM18APRFUT=[53556999]
    SBIN = [128028676]
    token=CRUDEOILM18APRFUT
    type='s'


def on_ticks(ws, ticks):

    c1.tc = c1.tc + 1
    c1.ltp = ticks[0]["last_price"]
    print("Ticking....LTP", c1.ltp)
    if (c1.tc==0):
        alg.algo_init_trade()
    alg.algo_sl_adjust()
    alg.algo_trade_change()



def on_connect(ws, response):
    ws.subscribe(c1.token)
    ws.set_mode(ws.MODE_LTP, c1.token)


class orders :

    def sell():

        c1.sl_p = c1.ltp + c1.sl
        c1.order_id_sell = kite.place_order(variety='CO', tradingsymbol=c1.tradingsymbol, exchange=kite.EXCHANGE_MCX,transaction_type = kite.TRANSACTION_TYPE_SELL, quantity = 1,order_type = kite.ORDER_TYPE_MARKET, product = kite.PRODUCT_CO,trigger_price = c1.sl_p)
        c1.trade_price = kite.order_trades(c1.order_id_sell)[0]['average_price']
        print("sold at:", c1.trade_price)




    def buy():

         c1.sl_p = c1.ltp - c1.sl
         c1.order_id_buy = kite.place_order(variety='CO', tradingsymbol=c1.tradingsymbol, exchange=kite.EXCHANGE_MCX,
                                          transaction_type=kite.TRANSACTION_TYPE_BUY, quantity=1,
                                          order_type=kite.ORDER_TYPE_MARKET, product=kite.PRODUCT_CO,
                                          trigger_price=c1.sl_p)
         c1.trade_price = kite.order_trades(c1.order_id_buy)[0]['average_price']
         print("purchased at :", c1.trade_price)





class algos :

    def algo_init_trade():
        if(c1.type=='b'):
           orders.buy()

        elif(c1.type=='s'):
            orders.sell()

        else :
            orders.buy()
            orders.sell()


    def algo_sl_adjust():
        print("Trade profit monitoring :",c1.trade_price,c1.sl_p)

        if(c1.type=='b' and c1.ltp>(c1.sl_p+c1.sl+c1.sl_adjust)):
                adj=c1.sl_p+(c1.ltp-(c1.sl_p+c1.sl+c1.sl_adjust))
                kite.modify_order(variety='CO',order_id=int(c1.order_id_buy)+1,trigger_price=adj)
                c1.sl_p=adj
                print('buy SL adjusted to:',adj)


        if (c1.type=='s' and c1.ltp < (c1.sl_p-c1.sl-c1.sl_adjust) ):
                adj = c1.sl_p-((c1.sl_p-c1.sl-c1.sl_adjust)-c1.ltp)
                kite.modify_order(variety='CO',order_id=int(c1.order_id_buy)+1,trigger_price=adj)
                c1.sl_p = adj
                print('sell SL adjusted to :',adj)

    def algo_trade_change():

        if((c1.ltp<=c1.sl_p) and c1.type=='b'):
            print('Trade changed to SELL')
            orders.sell()
            c1.type='s'
        elif((c1.ltp >= c1.sl_p) and c1.type=='s'):
            print('Trade changed to BUY')
            orders.buy()
            c1.type='b'












alg=algos

kws.on_connect = on_connect

kws.on_ticks = on_ticks


t1 = Thread(target=kws.connect)
t1.start()

