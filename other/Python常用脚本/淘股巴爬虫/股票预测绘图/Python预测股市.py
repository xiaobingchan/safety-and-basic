#http://www.360doc.com/content/16/0906/01/20558639_588703140.shtml
#pip install statsmodels
import pandas as pd
discfile='F:/600064.xlsx'
forecastnum=1
data=pd.read_excel(discfile,index_col=u'date')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
data.plot()
plt.show()
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(data).show()
from statsmodels.tsa.stattools import adfuller as ADF
print(u'ADF:',ADF(data[u'high']))
D_data=data.diff().dropna()
D_data.columns=[u'result']
D_data.plot();
plt.show()
plot_acf(D_data).show()
plt.show()
from statsmodels.graphics.tsaplots import plot_pacf
plot_pacf(D_data).show()
#print(u'ADF2:',ADF(D_data[u'result2']))
from statsmodels.stats.diagnostic import acorr_ljungbox
#print(u'result3:',acorr_ljungbox(D_data,lags=1))
from statsmodels.tsa.arima_model import ARIMA
pmax=int(len(D_data)/10)
qmax=int(len(D_data)/10)
bic_matrix=[]
for p in range(pmax)+1:
 tmp=[]
  for q in range(qmax+1):
   try:
    tmp.append(ARIMA(data,(p,1,q)).fit().bic)
   except:
    tmp.append(None)
 bic_matrix.append(tmp)
bic_matrix=pd.DataFrame(bic_matrix)
p,q=bic_matrix.stack().idxmin()
model=ARIMA(data,(p,1,q)).fit()
model.summary2()
model.forecast(1)