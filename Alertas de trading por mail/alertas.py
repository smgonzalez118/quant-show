import yfinance
import ta
from datetime import datetime
from ta.trend import EMAIndicator
import smtplib

# NOTA: si no funciona yfinance, desinstalar y volver a instalar
# Solucionado el problema de las señales de compra (no había puesto índice de vela en la MM 200)
# Solucionado? Testear: Cómo hacer para que no mande dos veces la misma señal. Puede ser con un diccionario par-valor para cada TF
# que se limpie cada día y almacene la posición/estado enviado o no. Usar el ejemplo del curso de Python para A.D. Revisás
# Si está esa clave (el activo) y tiene X valor, no se manda la señal. Si no, manda la señal y cambia el valor.
# Meter filtro de dos velas para evitar señales falsas para comprar y para vender.

# PARÁMETROS GENERALES
activos = ['TECO2.BA', 'YPFD.BA', 'TXAR.BA', 'GGAL.BA', 'ALUA.BA', 'PAMP.BA', 'BMA.BA', 'LOMA.BA', 'TGSU2.BA', 
            'BBAR.BA', 'CRES.BA', 'CVH.BA', 'BYMA.BA', 'HARG.BA', 'MIRG.BA', 'SUPV.BA', 'VALO.BA', 'TGNO4.BA', 
            'TRAN.BA', 'AGRO.BA', 'COME.BA', 'MDT', 'C', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'DISN', 'V', 'TSLA', 
            'BABA', 'JPM', 'JNJ', 'NVDA', 'WMT', 'HD', 'PG', 'PYPL', 'AMAT', 'INTC', 'ADBE', 'NFLX', 'XOM', 'VZ', 
            'KO', 'ABT', 'CSCO', 'TM', 'T', 'CRM', 'NKE', 'PFE', 'TMO', 'MRK', 'CVX', 'PEP', 'WFC', 'TXN', 'MCD', 
            'VALE', 'QCOM', 'RDS', 'MO', 'BA', 'AMD', 'CAT', 'JD', 'AXP', 'GE', 'GS', 'IBM', 'MMM', 'LMT', 'TGT', 
            'SNAP', 'MELI', 'GILD', 'BIDU', 'SBUX', 'BMY', 'TWTR', 'FCX', 'HMC', 'NEM', 'DE', 'ABEV', 'EBAY', 'HPQ', 
            'BIIB', 'AIG', 'BBD', 'SLB', 'BBV', 'GRMN', 'BSBR', 'BNG', 'SUZ', 'GOLD', 'VIV', 'SID', 'EBR', 'GGB', 
            'TXR', 'TRIP', 'X', 'SBS', 'XROX', 'GLNT', 'AUY', 'BRFS', 'CDE', 'ERJ', 'CELU', 'ADGO', 'DD', 'ARCO', 
            'DESP', 'ITUBC', 'SNP', 'ING', 'CX', 'ADI', 'CS', 'SCCO', 'HL', 'BCS', 'ITUB', 'BCS', 'ERIC', 'UNH', 
            'ORAN', 'LYG', 'UNPD', 'ETSYD', 'DEO', 'PSX', 'ACH', 'INFY', 'BB', 'HSBC', 'HAL', 'AMGN', 'ORCL', 'WBA', 
            'KMB', 'GLW', 'SAP', 'SNA', 'PBR', 'GPRK', 'UGP', 'NGG', 'VOD', 'YY', 'TOT', 'DOCU', 'PAAS', 'SAN', 
            'PTR', 'USB', 'PKS', 'BA-C', 'BRKB', 'HMY', 'HON', 'UL', 'OGZD', 'BK', 'AEM', 'HNP', 'LVS', 'RTX', 
            'SQ', 'SHOP', 'ABBV', 'TSM', 'FDX', 'HWM', 'TEN', 'SONY', 'BIOX', 'NVS', 'NUE', 'MA', 'CL', 'NOKA', 
            'RIO', 'FSLR', 'LLY', 'BHP', 'AMX', 'UNP', 'HSY', 'ETSY', 'HOG', 'SPOT', 'SNOW', 'CAAP', 'GSK', 
            'VIST', 'EFX', 'COST', 'CAH', 'AVGO', 'MSI', 'ZM', 'SAMI.BA', 'BRIO.BA', 'FERR.BA', 'BPAT.BA', 
            'CEPU.BA', 'CTIO.BA', 'IRCP.BA', 'MOLA.BA', 'IRSA.BA', 'MTR.BA', 'EDN.BA', 'PGR.BA', 'RIGO.BA', 
            'LEDE.BA', 'PATA.BA', 'MOLI.BA', 'RICH.BA', 'BHIP.BA', 'CAPX.BA', 'CECO2.BA', 'INVJ.BA', 'METR.BA', 
            'GBAN.BA', 'BOLT.BA', 'GAMI.BA', 'CGPA2.BA', 'AUSO.BA', 'GCLA.BA', 'CADO.BA', 'MORI.BA', 'OEST.BA', 
            'DGCU2.BA', 'TGLT.BA', 'DYCA.BA', 'HAVA.BA', 'GRIM.BA', 'INTR.BA', 'CARC.BA', 'SEMI.BA', 'LONG.BA', 
            'DOME.BA', 'GARO.BA', 'FIPL.BA', 'ROSE.BA', 'POLL.BA', 'TEFO.BA']



hora_max = datetime.strptime("17:30:00", "%X").time()
hora_min = datetime.strptime("10:30:00", "%X").time()
hora_reinicio_reg = datetime.strptime("10:25:00", "%X").time()

longitud_EMA_MCP = 10
longitud_EMA_CP = 20
longitud_EMA_MP = 50
longitud_EMA_LP = 100
EMA_filtro = 200

registro_alertas = {}   # {'activo1' : [MCP(0), CP(1), MD(2), LP(3)], 'activo2' : [MCP, CP, MD, LP], etc...} donde 1 = S.C. y 0 = S.V
for activo in activos:
    registro_alertas[activo] = [None, None, None, None]
print(registro_alertas)


# Registro de alertas
if datetime.now().time() == hora_reinicio_reg:
    registro_alertas = {}


# Configuración del correo
server = smtplib.SMTP('smtp.gmail.com' , 587)
server.starttls()
server.login('papeleta.quant@gmail.com' , '###########')
                      

'''
while datetime.now().time() <= hora_min:
    print("Aún no abrió el mercado...")
    time.sleep(600)
'''


#while True and datetime.now().time() >= hora_min and datetime.now().time() <= hora_max:
while True:
    for activo in activos:
        try:
            # Limpiamos mensajes
            subject= ''
            message= ''
            message = 'Subject: {}\n\n{}'.format(subject, message)
            mensaje = ''
            
            print(f"####### Revisando {activo}")
            # Obtengo data y calculo medias móviles
            data = yfinance.Ticker(activo).history(period="2y",interval="1d")
            data['EMA: ' + str(longitud_EMA_MCP)] = EMAIndicator(data['Close'], longitud_EMA_MCP, False).ema_indicator()
            data['EMA: ' + str(longitud_EMA_CP)] = EMAIndicator(data['Close'], longitud_EMA_CP, False).ema_indicator()
            data['EMA: ' + str(longitud_EMA_MP)] = EMAIndicator(data['Close'], longitud_EMA_MP, False).ema_indicator()
            data['EMA: ' + str(longitud_EMA_LP)] = EMAIndicator(data['Close'], longitud_EMA_LP, False).ema_indicator()
            data['EMA: ' + str(EMA_filtro)] = EMAIndicator(data['Close'], EMA_filtro, False).ema_indicator()
              
            # Quito las filas con NAs y tenemos dataframe armado
            data.dropna(inplace = True)
            
            
            # Evaluamos situación para el activo, para el MUY CORTO PLAZO:
            # Sólo entramos a las señales alcistas si el Precio > EMA 200
            if data['Close'][-1] > data['EMA: ' + str(EMA_filtro)][-1]:
                if ((data['Close'][-3] < data['EMA: ' + str(longitud_EMA_MCP)][-3]) and 
                    (data['Close'][-2] > data['EMA: ' + str(longitud_EMA_MCP)][-2]) and
                    (data['Close'][-1] > data['EMA: ' + str(longitud_EMA_MCP)][-1])):
                
                    if registro_alertas[activo][0] != 1:   # Si aún no fue enviada la señal de compra
                        mensaje = f"[COMPRA] {activo} - MUY CORTO PLAZO: en $ {round(data['Close'][-1], 2)}"
                        subject = mensaje
                        message = mensaje
                        message = 'Subject: {}\n\n{}'.format(subject, message)
                        server.sendmail('papeleta.quant@gmail.com', 'papeleta.quant@gmail.com', message)
                        print("Mail enviado con señal de compra")
                        registro_alertas[activo][0] = 1
            
            # Revisamos si hay señal de venta (MUY CORTO PLAZO)
            if ((data['Close'][-3] > data['EMA: ' + str(longitud_EMA_MCP)][-3]) and 
                (data['Close'][-2] < data['EMA: ' + str(longitud_EMA_MCP)][-2]) and
                (data['Close'][-1] < data['EMA: ' + str(longitud_EMA_MCP)][-1])):
                
                if registro_alertas[activo][0] != -1:   # Si aún no fue enviada la señal de venta
                    mensaje = f"[VENTA] {activo} - MUY CORTO PLAZO: en $ {round(data['Close'][-1], 2)}"
                    subject = mensaje
                    message = mensaje
                    message = 'Subject: {}\n\n{}'.format(subject, message)
                    server.sendmail('papeleta.quant@gmail.com', 'papeleta.quant@gmail.com', message)
                    print("Mail enviado con señal de venta")
                    registro_alertas[activo][0] = -1
                    
                    
            # Sólo entramos a las señales alcistas si el Precio > EMA 200
            if data['Close'][-1] > data['EMA: ' + str(EMA_filtro)][-1]:                 
                # Evaluamos situación para el activo, para el CORTO PLAZO:
                if ((data['Close'][-3] < data['EMA: ' + str(longitud_EMA_CP)][-3]) and 
                    (data['Close'][-2] > data['EMA: ' + str(longitud_EMA_CP)][-2]) and
                    (data['Close'][-1] > data['EMA: ' + str(longitud_EMA_CP)][-1])):
                    
                    if registro_alertas[activo][1] != 1:    # Si aún no fue enviada la señal de compra
                        mensaje = f"[COMPRA] {activo} - CORTO PLAZO: en $ {round(data['Close'][-1], 2)}"
                        subject = mensaje
                        message = mensaje
                        message = 'Subject: {}\n\n{}'.format(subject, message)
                        server.sendmail('papeleta.quant@gmail.com', 'papeleta.quant@gmail.com', message)
                        print("Mail enviado con señal de compra")
                        registro_alertas[activo][1] = 1
            
            # Revisamos si hay señal de venta  (CORTO PLAZO)
            if ((data['Close'][-3] > data['EMA: ' + str(longitud_EMA_CP)][-3]) and 
                (data['Close'][-2] < data['EMA: ' + str(longitud_EMA_CP)][-2]) and
                (data['Close'][-1] < data['EMA: ' + str(longitud_EMA_CP)][-1])):
                
                if registro_alertas[activo][1] != -1:   # Si aún no fue enviada la señal de venta
                    mensaje = f"[VENTA] {activo} - CORTO PLAZO: en $ {round(data['Close'][-1], 2)}"
                    subject = mensaje
                    message = mensaje
                    message = 'Subject: {}\n\n{}'.format(subject, message)
                    server.sendmail('papeleta.quant@gmail.com', 'papeleta.quant@gmail.com', message)
                    print("Mail enviado con señal de venta")
                    registro_alertas[activo][1] = -1

            # Sólo entramos a las señales alcistas si el Precio > EMA 200
            if data['Close'][-1] > data['EMA: ' + str(EMA_filtro)][-1]:
                # Evaluamos situación para el activo, para el MEDIO PLAZO:
                if ((data['Close'][-3] < data['EMA: ' + str(longitud_EMA_MP)][-3]) and 
                    (data['Close'][-2] > data['EMA: ' + str(longitud_EMA_MP)][-2]) and
                    (data['Close'][-1] > data['EMA: ' + str(longitud_EMA_MP)][-1])):
                    
                    if registro_alertas[activo][2] != 1:   # Si aún no fue enviada la señal de compra
                        mensaje = f"[COMPRA] {activo} - MEDIO PLAZO: en $ {round(data['Close'][-1], 2)}"
                        subject = mensaje
                        message = mensaje
                        message = 'Subject: {}\n\n{}'.format(subject, message)
                        server.sendmail('papeleta.quant@gmail.com', 'papeleta.quant@gmail.com', message)
                        print("Mail enviado con señal de compra")
                        registro_alertas[activo][2] = 1
            
            # Revisamos si hay señal de venta  (MEDIO PLAZO)
            if ((data['Close'][-3] > data['EMA: ' + str(longitud_EMA_MP)][-3]) and 
                (data['Close'][-2] < data['EMA: ' + str(longitud_EMA_MP)][-2]) and
                (data['Close'][-1] < data['EMA: ' + str(longitud_EMA_MP)][-1])):
                
                if registro_alertas[activo][2] != -1:   # Si aún no fue enviada la señal de venta
                    mensaje = f"[VENTA] {activo} - MEDIO PLAZO: en $ {round(data['Close'][-1], 2)}"
                    subject = mensaje
                    message = mensaje
                    message = 'Subject: {}\n\n{}'.format(subject, message)
                    server.sendmail('papeleta.quant@gmail.com', 'papeleta.quant@gmail.com', message)
                    print("Mail enviado con señal de venta")
                    registro_alertas[activo][2] = -1

            # Sólo entramos a las señales alcistas si el Precio > EMA 200
            if data['Close'][-1] > data['EMA: ' + str(EMA_filtro)][-1]:
                # Evaluamos situación para el activo, para el LARGO PLAZO:
                if ((data['Close'][-3] < data['EMA: ' + str(longitud_EMA_LP)][-3]) and 
                    (data['Close'][-2] > data['EMA: ' + str(longitud_EMA_LP)][-2]) and
                    (data['Close'][-1] > data['EMA: ' + str(longitud_EMA_LP)][-1])):
                    
                    if registro_alertas[activo][3] != 1:   # Si aún no fue enviada la señal de compra
                        mensaje = f"[COMPRA] {activo} - LARGO PLAZO: en $ {round(data['Close'][-1], 2)}"
                        subject = mensaje
                        message = mensaje
                        message = 'Subject: {}\n\n{}'.format(subject, message)
                        server.sendmail('papeleta.quant@gmail.com', 'papeleta.quant@gmail.com', message)
                        print("Mail enviado con señal de compra")
                        registro_alertas[activo][3] = 1
            
            # Revisamos si hay señal de venta  (LARGO PLAZO)
            if ((data['Close'][-3] > data['EMA: ' + str(longitud_EMA_LP)][-3]) and 
                (data['Close'][-2] < data['EMA: ' + str(longitud_EMA_LP)][-2]) and
                (data['Close'][-1] < data['EMA: ' + str(longitud_EMA_LP)][-1])):
                
                if registro_alertas[activo][3] != -1:   # Si aún no fue enviada la señal de venta
                    mensaje = f"[VENTA] {activo} - LARGO PLAZO: en $ {round(data['Close'][-1], 2)}"
                    subject = mensaje
                    message = mensaje
                    message = 'Subject: {}\n\n{}'.format(subject, message)
                    server.sendmail('papeleta.quant@gmail.com', 'papeleta.quant@gmail.com', message)
                    print("Mail enviado con señal de venta")
                    registro_alertas[activo][3] = -1
        except:
            continue
server.quit()