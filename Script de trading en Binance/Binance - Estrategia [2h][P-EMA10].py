# BINANCE - TF 2 hs - Cruce MACD - Activo: parametrizable

# PENDIENTES: 
# 1) Cómo es el formato de las open_orders, para ver cómo tomar el id (para cancelar)
# 2) Probar filtro de penetración a las MM para filtrar falsos quiebres (ej MM*1,015 - Filtro de 1,5%) (ya codificado)



# IMPORTAMOS TODAS LAS LIBRERÍAS Y MÓDULOS NECESARIOS:
# Propias de la librería de Binance:
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

# Otras:
import pandas as pd
from datetime import timedelta, datetime
import ta
from ta.trend import EMAIndicator
import smtplib

# PARÁMETROS GENERALES
activo = "BNBUSDT"
longitud_EMA = 10

# CREDENCIALES BINANCE
API_KEY = '########'
API_SECRET = '#########'
binance_client = Client(API_KEY, API_SECRET)


while True:
    # Obtengo datos de mi cuenta
    tenencia_activo = binance_client.get_asset_balance(asset='BNB')['free']
    disponible = binance_client.get_asset_balance(asset='USDT')['free']
    
    # Obtengo data financiera, formateo a dataframe, depuro columnas, formateo fecha y dejo data preparada
    data_raw = binance_client.get_historical_klines(activo, Client.KLINE_INTERVAL_2HOUR, '7 day ago UTC')
    data = pd.DataFrame(data_raw, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', '5', '6', '7', '8', '9', '10'])
    data['Date'] = pd.to_datetime(data['Date'], unit='ms', utc=True)
    data.set_index('Date', inplace=True)
    data['EMA: ' + str(longitud_EMA)] = EMAIndicator(data['Close'], longitud_EMA, False).ema_indicator()
    data = data.iloc[:, [3,11]]
    data.dropna(inplace = True)
            
    # OPERACIONES     
    # Evaluamos si hay órdenes abiertas. Si las hay, las cancelamos y volvemos a evaluar
    open_orders = binance_client.get_open_orders(symbol = activo)
        if open_orders == True:
            result = client.cancel_order(
            symbol= activo,
            orderId= open_orders[0]) # Pendiente: averiguar qué indice tiene el id de Orden, desconozco el formato
    
    # Evaluamos comprar:
    if disponible > 10:       # Si hay saldo disponible (al menos U$D 10)
        if (data['Close'][-1] > (data['EMA: ' + str(longitud_EMA)][-1]  * 1.015):     # Evalúo posición del activo para comprar            
            compra = binance_client.order_market_buy(symbol = activo, quantity = (disponible*0.95)/data['Close'][-1])
            #compra = binance_client.create_order(symbol='BNBUSDT', side='BUY', type='MARKET', quantity = (disponible*0.95)/data['Close'][-1])
            mensaje = f"[COMPRA] {round(cantidad,2} {activo} - en U$D {round(data['Close'][-1], 2)}. Total= U$D {round(cantidad*data['Close'][-1],2)}"
            subject = mensaje
            message = mensaje
            message = 'Subject: {}\n\n{}'.format(subject, message)
            server.sendmail('papeleta.quant@gmail.com', 'licsmgonzalez@gmail.com', message)
            print("Mail enviado con señal de compra")

    # Evaluamos venta sí y sólo sí tenemos tenencia del activo y dicha tenencia valorizada es mayor a U$D 10 (lo exige Binance)
    if (tenencia_activo > 0) and (tenencia_activo * data['Close'][-1] > 10):
        if (data['Close'][-1] < (data['EMA: ' + str(longitud_EMA)][-1] * 0.985):                
            venta = binance_client.order_market_sell(symbol = activo, quantity = tenencia_activo)  # Vendemos todo
            #venta = binance_client.create_order(symbol='BNBUSDT', side='SELL', type='MARKET', quantity = tenencia_activo)
            mensaje = f"[VENTA] {round(tenencia_activo,2} {activo} - en U$D {round(data['Close'][-1], 2)}. Total= U$D {round(tenencia_activo*data['Close'][-1],2)}"
            subject = mensaje
            message = mensaje
            message = 'Subject: {}\n\n{}'.format(subject, message)
            server.sendmail('papeleta.quant@gmail.com', 'licsmgonzalez@gmail.com', message)
            print("Mail enviado con señal de compra")
    time.sleep(60)