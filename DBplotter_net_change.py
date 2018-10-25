import sqlite3
from matplotlib import pyplot as plt
import time

conn = sqlite3.connect('tmp.db')
cur=conn.cursor()
data=[]
symbols=[]
symbols2=['GOLDM18NOVFUT','CRUDEOIL18NOVFUT']
#symbols2=['BANKNIFTY18OCTFUT','NIFTY18OCTFUT','USDINR18OCTFUT','CRUDEOIL18NOVFUT']
ltp_nifty50=10443.95#kite.ltp(256265)['256265']['last_price']
ltp_niftybank=25177#kite.ltp(260105)['260105']['last_price']

strike_nifty50=100*int(ltp_nifty50/100)-400
strike_niftybank=100*int(ltp_niftybank/100)-400


for i in range(8):
    symbols.append("NIFTY18OCT"+str(strike_nifty50+(100*i))+"CE")
    symbols.append("NIFTY18OCT"+str(strike_nifty50+(100*i))+"PE")
    symbols.append("BANKNIFTY18OCT"+str(strike_niftybank+(100*i))+"CE")
    symbols.append("BANKNIFTY18OCT"+str(strike_niftybank+(100*i))+"PE")

symbols.append("NIFTY18OCTFUT")
symbols.append("BANKNIFTY18OCTFUT")
symbols.append("BANKNIFTY18OCT25400PE")
symbols.append("BANKNIFTY18OCT25200CE")

symbols=symbols2

val={}
val_p={}
val_0={}
#print(symbols)
for j in range(len(symbols)):
    cur.execute("delete from " + symbols[j] + " where ltq=0 or vol=0 or oi=0 or last_price=0 or sell_quantity=0 or buy_quantity=0")
    cur.execute("select * from " + symbols[j]+" limit 10000")#  where (rowid>55000)")
    data = cur.fetchall()
    val.update({symbols[j]: {'ltp': [], 'oi': [], 'vol': [], 'bq': [], 'sq': [], 'ltq': []}})
    val_p.update({symbols[j]: {'ltp': [], 'oi': [], 'vol': [], 'bq': [], 'sq': [], 'ltq': []}})
    val_0.update({symbols[j]: {'ltp': [], 'oi': [], 'vol': [], 'bq': [], 'sq': [], 'ltq': []}})
    vp=data[0][1]
    vpv=data[0][2]
    pdiff=data[0][0]
    oi_diff = []
    p_diff=[]
    v_diff = []
    for i in range(len(data)):
        oi_diff.append(data[i][1]-vp)
        v_diff.append(data[i][2]-vpv)
        p_diff.append(data[i][0]-pdiff)
        val[symbols[j]]['ltp'].append(data[i][0])
        val[symbols[j]]['oi'].append(data[i][1])
        val[symbols[j]]['vol'].append(v_diff[i])
        val[symbols[j]]['bq'].append((v_diff[i])-abs(oi_diff[i]))
        val[symbols[j]]['sq'].append(oi_diff[i])
        val[symbols[j]]['ltq'].append((p_diff[i]))
        pdiff = data[i][0]
        vp=data[i][1]
        vpv=data[i][2]

#print(val_p)
conn.commit()
conn.close()

for i in val:
    for k in val[i]:
        val_0[i][k].append((val[i][k][0])/100)
#print(val_0)




for i in val:
    for k in val[i]:
        for j in range(len(val[i][k])):
            a=val[i][k][j]
            b=val_0[i][k][0]
            #print(val[i][k][0])
            #print('p',i,k,a/b)
            #print(symbols)
            #val_p[i][k].append(a/b)

#print("val_p",val_p)







#print(val_0)

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
        k=0
        for i in val:
            k=1
            for j in val[i]:
                plt.subplot(6,1,k)
                plt.plot(val[i][j])
                plt.suptitle(i)
                plt.ylabel(j)
                k=k+1
                #cursor=Cursor(useblit=True)
            plt.show()

    def p3():
        k=0
        for i in val:
            k=1
            for j in val[i]:
                plt.subplot(6,1,k)
                plt.plot(val[i][j])
                plt.suptitle(i)
                plt.ylabel(j)
                k=k+1
                #cursor=Cursor(useblit=True)
            plt.show()


#print(val_p)

#plots.=p1()
#plt.ion()
#print(val_0)
plots.p2()

#plots.p1()
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
