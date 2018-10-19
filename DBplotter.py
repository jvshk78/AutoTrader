import sqlite3
from matplotlib import pyplot as plt
import time
#from data_logger import symbols


ltp_nifty50=10443.95#kite.ltp(256265)['256265']['last_price']
ltp_niftybank=25177#kite.ltp(260105)['260105']['last_price']
strike_nifty50=100*int(ltp_nifty50/100)-400
strike_niftybank=100*int(ltp_niftybank/100)-400

symbols=[]
for i in range(9):
    symbols.append("NIFTY18OCT"+str(strike_nifty50+(100*i))+"CE")
    symbols.append("NIFTY18OCT"+str(strike_nifty50+(100*i))+"PE")
    symbols.append("BANKNIFTY18OCT"+str(strike_niftybank+(100*i))+"CE")
    symbols.append("BANKNIFTY18OCT"+str(strike_niftybank+(100*i))+"PE")


#st=["NIFTY18OCT10000CE","NIFTY18OCT10100PE","NIFTY18OCT10200PE","NIFTY18OCT10300PE","NIFTY18OCT10400PE","NIFTY18OCT10500PE","NIFTY18OCT10600PE","NIFTY18OCT10500PE","NIFTY18OCT10500PE","NIFTY18OCT10500PE",]
data=[]
ltp=[]
oi=[]
vol=[]
buyq=[]
sellq=[]
ltq=[]
d={}
conn = sqlite3.connect('inst6.db')
cur=conn.cursor()
for i in range(len(symbols)):
    cur.execute("select * from " + symbols[i])
    data=cur.fetchall()
    d.update({symbols[i]:data})

i=0
for i in range(len(data)):
    ltp.append(data[i][1])
    oi.append(data[i][2])
    vol.append(data[i][3])
    buyq.append(data[i][4])
    sellq.append(data[i][5])
    ltq.append(data[i][6])
plt.ion()
plt.subplot(511)
plt.suptitle(symbols[5])
plt.plot(ltp)
plt.title("ltp ")
plt.ylabel(str(data[i][1]))

plt.subplot(512)
plt.plot(oi)
plt.title("oi ")
plt.ylabel(str(data[i][2]))

#plt.subplot(613)
#plt.plot(vol)
#plt.title("vol")

plt.subplot(513)
plt.plot(buyq)
plt.title("bq ")
plt.ylabel(str(data[i][4]))

plt.subplot(514)
plt.plot(sellq)
plt.title("sq ")
plt.ylabel(str(data[i][5]))
plt.subplot(515)
plt.plot(ltq)
plt.title("ltq ")
plt.ylabel(str(data[i][6]))
plt.pause(0.1)

plt.show(block=True)
print(d)


