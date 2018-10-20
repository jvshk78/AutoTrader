import sqlite3
from matplotlib import pyplot as plt
import time

conn = sqlite3.connect('inst6.db')
cur=conn.cursor()
data=[]
symbols=[]

ltp_nifty50=10443.95#kite.ltp(256265)['256265']['last_price']
ltp_niftybank=25177#kite.ltp(260105)['260105']['last_price']

#strike_nifty50=100*int(ltp_nifty50/100)-200
strike_niftybank=100*int(ltp_niftybank/100)-400


#for i in range(4):
    #symbols.append("NIFTY18OCT"+str(strike_nifty50+(100*i))+"CE")
    #symbols.append("NIFTY18OCT"+str(strike_nifty50+(100*i))+"PE")
    #symbols.append("BANKNIFTY18OCT"+str(strike_niftybank+(100*i))+"CE")
    #symbols.append("BANKNIFTY18OCT"+str(strike_niftybank+(100*i))+"PE")

#symbols.append("NIFTY18OCTFUT")
#symbols.append("BANKNIFTY18OCTFUT")
#symbols.append("BANKNIFTY18OCT25400PE")
symbols.append("BANKNIFTY18OCT25400CE")


val={}


#print(symbols)
for j in range(len(symbols)):
    cur.execute("select * from " + symbols[j]+" limit 2000")
    data = cur.fetchall()
    val.update({symbols[j]: {'ltp': [], 'oi': [], 'vol': [], 'bq': [], 'sq': [], 'ltq': []}})
    for i in range(len(data)):
        val[symbols[j]]['ltp'].append(data[i][1])
        val[symbols[j]]['oi'].append(data[i][2])
        val[symbols[j]]['vol'].append(data[i][3])
        val[symbols[j]]['bq'].append(data[i][4])
        val[symbols[j]]['sq'].append(data[i][5])
        val[symbols[j]]['ltq'].append(data[i][6])
print(val)

class plots():
    def p1():
        for k in val:
            plt.subplot(511)
            plt.plot(val[k]['ltp'],label='ltp')
            plt.legend()


        for k in val:
            plt.subplot(512)
            plt.plot(val[k]['oi'],label='oi')
            plt.legend()


        for k in val:
            plt.subplot(513)
            plt.plot(val[k]['bq'],label='bq')
            plt.legend()


        for k in val:
            plt.subplot(514)
            plt.plot(val[k]['sq'],label='sq')
            plt.legend()


        for k in val:
            plt.subplot(515)
            plt.plot(val[k]['ltq'],label='ltq')
            plt.legend()
        plt.suptitle(k)
        plt.show()

    def p2():
        for k in val:
            plt.subplot(511)
            plt.plot(val[k]['ltp'],label='ltp')
            plt.legend()


        for k in val:
            plt.subplot(512)
            plt.plot(val[k]['oi'],label='oi')
            plt.legend()


        for k in val:
            plt.subplot(513)
            plt.plot(val[k]['bq'],label='bq')
            plt.legend()


        for k in val:
            plt.subplot(514)
            plt.plot(val[k]['sq'],label='sq')
            plt.legend()


        for k in val:
            plt.subplot(515)
            plt.plot(val[k]['ltq'],label='ltq')
            plt.legend()
        plt.suptitle(k)
        plt.show()

plots.p1()
#fig,ax=plt.subplots(2,2,num=10, clear=True)
"""""
ax2=plt.plot(val['NIFTY18OCTFUT']['ltp'])
plt.show()
ax3=plt.plot(val['NIFTY18OCTFUT']['vol'])
plt.show()
ax4=plt.plot(val['NIFTY18OCTFUT']['bq'])
plt.show()
ax5=plt.plot(val['NIFTY18OCTFUT']['sq'])
plt.show()
ax6=plt.plot(val['NIFTY18OCTFUT']['ltq'])
plt.show()
"""""

