class tc(Thread):
    def __init__(self):
        Thread.__init__(self)
        print("New", c1.tc)

    def run(self):
        flag = 0
        trig = 0
        time.sleep(1)

        while (c1.tc < (c1.tc + 1)):
            if (c1.ltp >= 4190 and flag == 0):
                print("BuyK")
                c1.trades = c1.trades + 1
                flag = 1
                trig = 4189
                # c1.order_id = kite.place_order(variety='CO',tradingsymbol="CRUDEOILM18APRFUT",exchange=kite.EXCHANGE_MCX,transaction_type=kite.TRANSACTION_TYPE_BUY,quantity=1,order_type=kite.ORDER_TYPE_MARKET,product=kite.PRODUCT_CO,trigger_price=trig)
                while (c1.ltp >= trig):
                    print("watchng buy, Trigger,trades :", trig, c1.trades)
                    time.sleep(2)
                # c1.order_id = kite.place_order(variety='CO',tradingsymbol="CRUDEOILM18APRFUT",exchange=kite.EXCHANGE_MCX,transaction_type=kite.TRANSACTION_TYPE_SELL,quantity=1,order_type=kite.ORDER_TYPE_MARKET,product=kite.PRODUCT_CO,trigger_price=trig)
                print("Sold(square off)")
                c1.trades = c1.trades + 1
                flag = 0

            if (c1.ltp <= 4189 and flag == 0):
                print("sellK")
                c1.trades = c1.trades + 1
                flag = 2
                trig = 4190
                # c1.order_id = kite.place_order(variety='CO',tradingsymbol="CRUDEOILM18APRFUT",exchange=kite.EXCHANGE_MCX,transaction_type=kite.TRANSACTION_TYPE_SELL,quantity=1,order_type=kite.ORDER_TYPE_MARKET,product=kite.PRODUCT_CO,trigger_price=trig)
                while (c1.ltp <= trig):
                    print("watchng sell,Trigger,trades:", trig, c1.trades)
                    time.sleep(2)
                # c1.order_id = kite.place_order(variety='CO',tradingsymbol="CRUDEOILM18APRFUT",exchange=kite.EXCHANGE_MCX,transaction_type=kite.TRANSACTION_TYPE_BUY,quantity=1,order_type=kite.ORDER_TYPE_MARKET,product=kite.PRODUCT_CO,trigger_price=trig)
                print("baught(square off)")
                c1.trades = c1.trades + 1
                flag = 0


#tc1 = tc()
#tc1.start()


c1.order_id_buy = kite.place_order(variety='CO', tradingsymbol=c1.tradingsymbol, exchange=kite.EXCHANGE_MCX,
                                          transaction_type=kite.TRANSACTION_TYPE_BUY, quantity=1,
                                          order_type=kite.ORDER_TYPE_LIMIT,price= 4180, product=kite.PRODUCT_CO,
                                           trigger_price=4170)

kite.modify_order(variety='CO',trigger_price=4160,parent_order_id=c1.order_id_buy,order_id=c1.order_id_buy,order_type=kite.ORDER_TYPE_SLM)

modify_order(	self, variety, order_id, parent_order_id=None, quantity=None, price=None, order_type=None,
                 trigger_price=None, validity=None, disclosed_quantity=None)

c1.order_id_sell = kite.place_order(variety='REGULAR', tradingsymbol=c1.tradingsymbol, exchange=kite.EXCHANGE_MCX,
                                          transaction_type=kite.TRANSACTION_TYPE_BUY, quantity=1,
                                          order_type=kite.ORDER_TYPE_SLM,trigger_price=4310,product=kite.PRODUCT_MIS)

c1.order_id_buy = kite.place_order(variety='REGULAR', tradingsymbol=c1.tradingsymbol, exchange=kite.EXCHANGE_MCX,
                                          transaction_type=kite.TRANSACTION_TYPE_BUY, quantity=1,
                                          order_type=kite.ORDER_TYPE_SLM,trigger_price=4310,product=kite.PRODUCT_MIS)
