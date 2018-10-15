from kiteconnect import KiteConnect

#tradingsymbol:NIFTY18OCTFUT,instrument_token: 12438530
# index : NIFTY 50, instrument_token: 256265

#tradingsymbol:BANKNIFTY18OCTFUT, instrument_token: 12434434
#index : NIFTYBANK,instrument_token: 260105

#NIFTY18OCT10500CE :14517762 , NIFTY18OCT10500PE:14518018, CRUDEOIL18OCTFUT: 53835015



api_key='d1zkjgaordrrjgis'
api_secret='owe9bi50r9f8lr71jvvqesm5m86p1emf'
kite=KiteConnect(api_key=api_key)
inst=kite.instruments('NFO')
print(inst)

for i in range(len(inst)):
    if(inst[i]['instrument_type']=='FUT' and inst[i]['lot_size']==75) :print(inst[i])

for i in range(len(inst)):
    if(inst[i]['tradingsymbol']=='NIFTY 50':print(inst[i])