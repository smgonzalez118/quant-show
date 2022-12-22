import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
import datetime as datetime
import numpy as np
from datetime import datetime, timedelta
import time
import json
#import talib as ta

yf.pdr_override()

desde = (datetime.now() - timedelta(days = 548)).strftime("%Y-%m-%d")
hasta = datetime.now().strftime("%Y-%m-%d")



activos_lideres = ['TECO2.BA', 'YPFD.BA', 'TXAR.BA', 'GGAL.BA', 'ALUA.BA', 'PAMP.BA', 'BMA.BA', 'LOMA.BA', 'TGSU2.BA', 'BBAR.BA', 'CRES.BA', 'CVH.BA', 'BYMA.BA', 'HARG.BA', 'MIRG.BA', 'SUPV.BA', 'VALO.BA', 'TGNO4.BA', 'TRAN.BA', 'AGRO.BA', 'COME.BA']
activos_general = ['SAMI.BA', 'BRIO.BA', 'FERR.BA', 'BPAT.BA', 'CEPU.BA', 'CTIO.BA', 'IRCP.BA', 'MOLA.BA', 'IRSA.BA', 'MTR.BA', 'EDN.BA', 'PGR.BA', 'RIGO.BA', 'LEDE.BA', 'PATA.BA', 'MOLI.BA', 'RICH.BA', 'BHIP.BA', 'CAPX.BA', 'CECO2.BA', 'INVJ.BA', 'METR.BA', 'GBAN.BA', 'BOLT.BA', 'GAMI.BA', 'CGPA2.BA', 'AUSO.BA', 'GCLA.BA', 'CADO.BA', 'MORI.BA', 'OEST.BA', 'DGCU2.BA', 'TGLT.BA', 'DYCA.BA', 'HAVA.BA', 'GRIM.BA', 'INTR.BA', 'CARC.BA', 'SEMI.BA', 'LONG.BA', 'DOME.BA', 'GARO.BA', 'FIPL.BA', 'ROSE.BA', 'POLL.BA', 'TEFO.BA']
cedears = ['MDT', 'C', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'DISN', 'V', 'TSLA', 'BABA', 'JPM', 'JNJ', 'NVDA', 'WMT', 'HD', 'PG', 'PYPL', 'AMAT', 'INTC', 'ADBE', 'NFLX', 'XOM', 'VZ', 'KO', 'ABT', 'CSCO', 'TM', 'T', 'CRM', 'NKE', 'PFE', 'TMO', 'MRK', 'CVX', 'PEP', 'WFC', 'TXN', 'MCD', 'VALE', 'QCOM', 'RDS', 'MO', 'BA', 'AMD', 'CAT', 'JD', 'AXP', 'GE', 'GS', 'IBM', 'MMM', 'LMT', 'TGT', 'SNAP', 'MELI', 'GILD', 'BIDU', 'SBUX', 'BMY', 'TWTR', 'FCX', 'HMC', 'NEM', 'DE', 'ABEV', 'EBAY', 'HPQ', 'BIIB', 'AIG', 'BBD', 'SLB', 'BBV', 'GRMN', 'BSBR', 'BNG', 'SUZ', 'GOLD', 'VIV', 'SID', 'EBR', 'GGB', 'TXR', 'TRIP', 'X', 'SBS', 'XROX', 'GLNT', 'AUY', 'BRFS', 'CDE', 'ERJ', 'CELU', 'ADGO', 'DD', 'ARCO', 'DESP', 'ITUBC', 'SNP', 'ING', 'CX', 'ADI', 'CS', 'SCCO', 'HL', 'BCS', 'ITUB', 'BCS', 'ERIC', 'UNH', 'ORAN', 'LYG', 'UNPD', 'ETSYD', 'DEO', 'PSX', 'ACH', 'INFY', 'BB', 'HSBC', 'HAL', 'AMGN', 'ORCL', 'WBA', 'KMB', 'GLW', 'SAP', 'SNA', 'PBR', 'GPRK', 'UGP', 'NGG', 'VOD', 'YY', 'TOT', 'DOCU', 'PAAS', 'SAN', 'PTR', 'USB', 'PKS', 'BA-C', 'BRKB', 'HMY', 'HON', 'UL', 'OGZD', 'BK', 'AEM', 'HNP', 'LVS', 'RTX', 'SQ', 'SHOP', 'ABBV', 'TSM', 'FDX', 'HWM', 'TEN', 'SONY', 'BIOX', 'NVS', 'NUE', 'MA', 'CL', 'NOKA', 'RIO', 'FSLR', 'LLY', 'BHP', 'AMX', 'UNP', 'HSY', 'ETSY', 'HOG', 'SPOT', 'SNOW', 'CAAP', 'GSK', 'VIST', 'EFX', 'COST', 'CAH', 'AVGO', 'MSI', 'ZM']
caidas = []
lista_activos = []

for activo in cedears:
    try:
        data = pdr.get_data_yahoo(activo, desde, hasta)
        maximo = data["Adj Close"].max()
        caida = round(((data["Adj Close"][-1]/maximo) - 1)*100,2)
        caidas.append(caida)
        lista_activos.append(activo)
    except:
        continue

preplanilla = {}
preplanilla["ACTIVO"] = lista_activos
preplanilla["CAIDA"] = caidas
df = pd.DataFrame(preplanilla, columns = ["ACTIVO", "CAIDA"])

ordenado = df.sort_values(by=['CAIDA'])

print(ordenado.head(20))