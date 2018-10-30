import sqlite3
from matplotlib import pyplot as plt


conn = sqlite3.connect('30_10_18.db')
cur=conn.cursor()
data=[]
symbols=[]
symbols2=['BANKNIFTY18NOVFUT','NIFTY18NOVFUT']
#symbols2=['CRUDEOIL18NOVFUT','GOLDM18NOVFUT','USDINR18NOVFUT','NIFTY18NOVFUT','NIFTY18NOV10100CE','NIFTY18NOV10100PE','BANKNIFTY18NOVFUT','BANKNIFTY18NOV24700CE','BANKNIFTY18NOV24700PE']

symbols=symbols2

val={}


for j in range(len(symbols)):
    cur.execute("delete from " + symbols[j] + " where ltq=0 or vol=0 or oi=0 or last_price=0 or sell_quantity=0 or buy_quantity=0")
    cur.execute("select last_price from " + symbols[j])#+" where rowid >4200 and rowid<=4300") #  where (rowid>55000)")
    data = cur.fetchall()
    val.update({symbols[j]: {'ltp': [],'ltp_dir':[]}})
    vp=data[0][0]
    pdiff=data[0][0]
    p_diff=[]


    h = []
    hv=[]

    h1=0
    hv1=0

    for i in range(len(data)):
        p_diff.append(data[i][0]-pdiff)
        val[symbols[j]]['ltp'].append(data[i][0])
        val[symbols[j]]['ltp_dir'].append((h1))
        if p_diff[i]!=0:
            s=abs(p_diff[i])/p_diff[i]
            h1=h1+s
            h.append(h1)
        pdiff = data[i][0]
        vp=data[i][0]

conn.commit()
conn.close()

class plots():
     def p2():
        k=0
        for i in val:
            k=1
            for j in val[i]:
                plt.subplot(2,1,k)
                plt.plot(val[i][j])
                plt.suptitle(i)
                plt.ylabel(j)
                k=k+1
                #cursor=Cursor(useblit=True)
            plt.show()


plots.p2()
plt.show()
