import sqlite3
from matplotlib import pyplot as plt


conn = sqlite3.connect('01_11_18.db')
cur=conn.cursor()
data=[]
symbols=[]
symbols2=['USDINR18NOVFUT']
#symbols2=['TATAMOTORS','IOC','SBIN','YESBANK','BANKNIFTY18NOVFUT','CRUDEOIL18NOVFUT','GOLDM18NOVFUT','USDINR18NOVFUT','NIFTY18NOVFUT','NIFTY18NOV10100CE','NIFTY18NOV10100PE','BANKNIFTY18NOV24700CE','BANKNIFTY18NOV24700PE']

symbols=symbols2

val={}

for j in range(len(symbols)):
    #cur.execute("delete from " + symbols[j] + " where ltq=0 or vol=0 or oi=0 or last_price=0 or sell_quantity=0 or buy_quantity=0")
    #cur.execute("select last_price from " + symbols[j])# +" limit 10000")
    cur.execute("select last_price,oi,vol from " + symbols[j])# +" limit 5000")
    data = cur.fetchall()
    val.update({symbols[j]: {'ltp': [],'oi':[],'vol':[],'ltp_dir':[],'oi_dir':[],'vol_dir':[]}})


    pdiff=data[0][0]
    oidiff=data[0][1]
    vdiff=data[0][2]
    vvdiff=0

    p_diff=[]
    oi_diff=[]
    v_diff=[]

    h1=0
    h2=0
    h3=0


    for i in range(len(data)):

        p_diff.append(data[i][0]-pdiff)
        oi_diff.append(data[i][1]-oidiff)
        v_diff.append(data[i][2]-vdiff)


        val[symbols[j]]['ltp'].append(data[i][0])
        val[symbols[j]]['ltp_dir'].append((h1))

        if p_diff[i]!=0:
            s=abs(p_diff[i])/p_diff[i]
            h1=h1+s

        pdiff = data[i][0]


        val[symbols[j]]['oi'].append(data[i][1])
        val[symbols[j]]['oi_dir'].append((h2))

        if oi_diff[i]!=0:
            s=abs(oi_diff[i])/oi_diff[i]
            h2=h2+s

        oidiff = data[i][1]

        val[symbols[j]]['vol'].append(v_diff[i])
        val[symbols[j]]['vol_dir'].append((h3))

        if v_diff[i] > vvdiff:
            h3 = h3 + 1
        elif v_diff[i] < vvdiff:
            h3 = h3 -1

        vvdiff=v_diff[i]
        vdiff = data[i][2]

    """""
    plt.plot(val[symbols[j]]['ltp_dir'],label='pdiff')
    plt.plot(val[symbols[j]]['oi_dir'],label='oidiff')
    plt.legend()
    plt.show()
    """""

conn.commit()
conn.close()

class plots():
     def p2():

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


plots.p2()
plt.show()


