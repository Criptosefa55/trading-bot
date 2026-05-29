import pandas as pd
import numpy as np
import warnings
from tvDatafeed import TvDatafeed, Interval
import ta 


# Uyarıları gizle
warnings.simplefilter(action='ignore')

# Momentum, MFI ve WaveTrend Alpha dip kontrolü yapan fonksiyon
def momentum_mfi_wave_dip(data):
    df = data.copy()

    # Momentum hesaplama (Rate of Change - ROC)
    df['Momentum'] = ta.momentum.roc(close=df['close'], window=10)

    # MFI (Money Flow Index) hesaplama
    df['MFI'] = ta.volume.MFIIndicator(
        high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], window=14
    ).money_flow_index()

    # WaveTrend Alpha hesaplama
    n1 = 10  # Channel Length
    n2 = 21  # Average Length
    ap = (df['high'] + df['low'] + df['close']) / 3
    esa = ap.ewm(span=n1, adjust=False).mean()
    wd = (abs(ap - esa)).ewm(span=n1, adjust=False).mean()
    ci = (ap - esa) / (0.015 * wd)
    tci = ci.ewm(span=n2, adjust=False).mean()

    wt1 = tci
    wt2 = wt1.rolling(window=4).mean()

    # Dip tespiti için koşullar: wt1 ve wt2 -45 ile -75 arasında
    wt1_dip = (wt1 >= -75) & (wt1 <= -45)  # WT1 dip tespiti (sadece -75 ile -45 arasında)
    wt2_dip = (wt2 >= -75) & (wt2 <= -45)  # WT2 dip tespiti (sadece -75 ile -45 arasında)
    wave_hist = wt1 - wt2

    # WaveHistogram'ın negatif olması
    wave_hist_dip = wave_hist < 0  # Wave Histogram negatif, dip tespiti

    # Diplerde sinyaller
    df['WT1_Dip'] = wt1_dip
    df['WT2_Dip'] = wt2_dip
    df['Wave_Hist_Dip'] = wave_hist_dip

    # Diplerin ve Momentum/MFI'nin durumu
    df['Buy_Signal'] = (df['Momentum'] < 0) & (df['MFI'] < 20) & df['WT1_Dip'] & df['WT2_Dip'] & df['Wave_Hist_Dip']

    return df

# TradingView verilerini al
def get_symbols_and_data():
    tv = TvDatafeed()

   # Türkiye borsasında işlem gören hisse senetleri sembollerini liste olarak tanımlıyoruz
    symbols = [
        'BIST:BINHO', 'BIST:AVOD',  'BIST:A1CAP', 'BIST:ACSEL', 'BIST:ADEL',  'BIST:ADESE', 'BIST:ADGYO', 
        'BIST:AFYON', 'BIST:AGHOL', 'BIST:AGESA', 'BIST:AGROT', 'BIST:AHSGY', 'BIST:AHGAZ', 'BIST:AKSFA', 
        'BIST:AKFK',  'BIST:AKM',   'BIST:AKBNK', 'BIST:AKCNS', 'BIST:AKDFA', 'BIST:AKYHO', 'BIST:AKENR', 
        'BIST:AKFGY', 'BIST:AKFNI', 'BIST:AKFYE', 'BIST:ATEKS', 'BIST:AKSGY', 'BIST:AKMGY', 'BIST:AKSA', 
        'BIST:AKSEN', 'BIST:AKGRT', 'BIST:AKSUE', 'BIST:AKTVK', 'BIST:AFB',   'BIST:ALCAR', 'BIST:ALGYO', 
        'BIST:ALARK', 'BIST:ALBRK', 'BIST:ALCTL', 'BIST:ALFAS', 'BIST:ALJF',  'BIST:ALKIM', 'BIST:ALKA', 
        'BIST:AYCES', 'BIST:ALTNY', 'BIST:ALKLC', 'BIST:ALMAD', 'BIST:ALVES', 'BIST:ANSGR', 'BIST:AEFES', 
        'BIST:ANHYT', 'BIST:ASUZU', 'BIST:ANGEN', 'BIST:ANELE', 'BIST:ARCLK', 'BIST:ARDYZ', 'BIST:ARENA', 
        'BIST:ARMGD', 'BIST:ARSAN', 'BIST:ARTMS', 'BIST:ARZUM', 'BIST:ASGYO', 'BIST:ASELS', 'BIST:ASTOR', 
        'BIST:ATAGY', 'BIST:ATAKP', 'BIST:AGYO',  'BIST:ATLFA', 'BIST:ATSYH', 'BIST:ATLAS', 'BIST:ATATP', 
        'BIST:AVGYO', 'BIST:AVTUR', 'BIST:AVHOL', 'BIST:AVPGY', 'BIST:AYDEM', 'BIST:AYEN',  'BIST:AYES', 
        'BIST:AYGAZ', 'BIST:AZTEK', 'BIST:BAGFS', 'BIST:BAHKM', 'BIST:BAKAB', 'BIST:BALAT', 'BIST:BNTAS', 
        'BIST:BANVT', 'BIST:BARMA', 'BIST:BASGZ', 'BIST:BASCM', 'BIST:BEGYO', 'BIST:BTCIM', 'BIST:BSOKE', 
        'BIST:BYDNR', 'BIST:BAYRK', 'BIST:BERA',  'BIST:BRKT', ' BIST:BRKSN', 'BIST:BJKAS', 'BIST:BEYAZ', 
        'BIST:BIENY', 'BIST:BLCYT', 'BIST:BIMAS', 'BIST:BINBN', 'BIST:BIOEN', 'BIST:BRKVY', 'BIST:BRKO', 
        'BIST:BRLSM', 'BIST:BRMEN', 'BIST:BIZIM', 'BIST:BMSTL', 'BIST:BMSCH', 'BIST:BNPPI', 'BIST:BOBET', 
        'BIST:BORSK', 'BIST:BORLS', 'BIST:BRSAN', 'BIST:BRYAT', 'BIST:BFREN', 'BIST:BOSSA', 'BIST:BRISA', 
        'BIST:BURCE', 'BIST:BURVA', 'BIST:BUCIM', 'BIST:BVSAN', 'BIST:BIGCH', 'BIST:CRFSA', 'BIST:CASA', 
        'BIST:CEMZY', 'BIST:CEOEM', 'BIST:CCOLA', 'BIST:CONSE', 'BIST:COSMO', 'BIST:CRDFA', 'BIST:CVKMD', 
        'BIST:CWENE', 'BIST:GCAM',  'BIST:CAGFA', 'BIST:CLDNM', 'BIST:CANTE', 'BIST:CATES', 'BIST:CLEBI', 
        'BIST:CELHA', 'BIST:CLKMT', 'BIST:CEMAS', 'BIST:CEMTS', 'BIST:CMBTN', 'BIST:CMENT', 'BIST:CIMSA', 
        'BIST:CUSAN', 'BIST:DVRLK', 'BIST:DYBNK', 'BIST:DAGI',  'BIST:DAGHL', 'BIST:DAPGM', 'BIST:DARDL', 
        'BIST:DGATE', 'BIST:DCTTR', 'BIST:DGRVK', 'BIST:DMSAS', 'BIST:DENGE', 'BIST:DENFA', 'BIST:DNFIN', 
        'BIST:DZGYO', 'BIST:DERIM', 'BIST:DERHL', 'BIST:DESA',  'BIST:DESPC', 'BIST:DTBMK', 'BIST:DEVA', 
        'BIST:DNISI', 'BIST:DIRIT', 'BIST:DITAS', 'BIST:DMRGD', 'BIST:DOCO',  'BIST:DOFER', 'BIST:DOBUR', 
        'BIST:DOHOL', 'BIST:DTRND', 'BIST:DGNMO', 'BIST:ARASE', 'BIST:DOGUB', 'BIST:DGGYO', 'BIST:DOAS', 
        'BIST:DFKTR', 'BIST:DOKTA', 'BIST:DURDO', 'BIST:DURKN', 'BIST:DNYVA', 'BIST:DYOBY', 'BIST:EDATA', 
        'BIST:EBEBK', 'BIST:ECZYT', 'BIST:EDIP',  'BIST:EFORC', 'BIST:EGEEN', 'BIST:EGGUB', 'BIST:EGPRO', 
        'BIST:EGSER', 'BIST:EPLAS', 'BIST:ECILC', 'BIST:EKER',  'BIST:EKIZ',  'BIST:EKOFA', 'BIST:EKOS', 
        'BIST:EKOVR', 'BIST:EKSUN', 'BIST:ELITE', 'BIST:EMKEL', 'BIST:EMNIS', 'BIST:EMIRV', 'BIST:EKTVK', 
        'BIST:EKGYO', 'BIST:EMVAR', 'BIST:ENJSA', 'BIST:ENERY', 'BIST:ENKAI', 'BIST:ENSRI', 'BIST:ERBOS', 
        'BIST:ERCB',  'BIST:EREGL', 'BIST:ERGLI', 'BIST:KIMMR', 'BIST:ERSU',  'BIST:ESCAR', 'BIST:ESCOM', 
        'BIST:ESEN',  'BIST:ETILR', 'BIST:EUKYO', 'BIST:EUYO',  'BIST:ETYAT', 'BIST:EUHOL', 'BIST:TEZOL', 
        'BIST:EUREN', 'BIST:EUPWR', 'BIST:EYGYO', 'BIST:FADE',  'BIST:FSDAT', 'BIST:FMIZP', 'BIST:FENER', 
        'BIST:FLAP',  'BIST:FONET', 'BIST:FROTO', 'BIST:FORMT', 'BIST:FORTE', 'BIST:FRIGO', 'BIST:FZLGY', 
        'BIST:GWIND', 'BIST:GSRAY', 'BIST:GAPIN', 'BIST:GARFA', 'BIST:GRNYO', 'BIST:GEDIK', 'BIST:GEDZA', 
        'BIST:GLCVY', 'BIST:GENIL', 'BIST:GENTS', 'BIST:GEREL', 'BIST:GZNMI', 'BIST:GIPTA', 'BIST:GMTAS', 
        'BIST:GESAN', 'BIST:GLYHO', 'BIST:GGBVK', 'BIST:GSIPD', 'BIST:GOODY', 'BIST:GOKNR', 'BIST:GOLTS', 
        'BIST:GOZDE', 'BIST:GRTHO', 'BIST:GSDDE', 'BIST:GSDHO', 'BIST:GUBRF', 'BIST:GLRYH', 'BIST:GUNDG', 
        'BIST:GRSEL', 'BIST:SAHOL', 'BIST:HLGYO', 'BIST:HLVKS', 'BIST:HRKET', 'BIST:HATSN', 'BIST:HATEK', 
        'BIST:HDFFL', 'BIST:HDFGS', 'BIST:HEDEF', 'BIST:HDFVK', 'BIST:HEKTS', 'BIST:HEPFN', 'BIST:HKTM', 
        'BIST:HTTBT', 'BIST:HOROZ', 'BIST:HUBVC', 'BIST:HUNER', 'BIST:HUZFA', 'BIST:HURGZ', 'BIST:ENTRA', 
        'BIST:ICUGS', 'BIST:INGRM', 'BIST:INVEO', 'BIST:INVES', 'BIST:ISKPL', 'BIST:IEYHO', 'BIST:IDGYO', 
        'BIST:IHEVA', 'BIST:IHLGM', 'BIST:IHGZT', 'BIST:IHAAS', 'BIST:IHLAS', 'BIST:IHYAY', 'BIST:IMASM', 
        'BIST:INALR', 'BIST:INDES', 'BIST:INFO',  'BIST:INTEK', 'BIST:INTEM', 'BIST:IPEKE', 'BIST:ISDMR', 
        'BIST:ISTFK', 'BIST:ISFAK', 'BIST:ISFIN', 'BIST:ISGYO', 'BIST:ISGSY', 'BIST:ISYAT', 'BIST:ISBIR', 
        'BIST:ISSEN', 'BIST:IZINV', 'BIST:IZENR', 'BIST:IZMDC', 'BIST:IZFAS', 'BIST:JANTS', 'BIST:KFEIN', 
        'BIST:KLKIM', 'BIST:KLSER', 'BIST:KLVKS', 'BIST:KAPLM', 'BIST:KAREL', 'BIST:KARSN', 'BIST:KRTEK', 
        'BIST:KARYE', 'BIST:KARTN', 'BIST:KATVK', 'BIST:KTLEV', 'BIST:KATMR', 'BIST:KAYSE', 'BIST:KNTFA', 
        'BIST:KENT',  'BIST:KERVT', 'BIST:KRVGD', 'BIST:KERVN', 'BIST:TCKRC', 'BIST:KZBGY', 'BIST:KLGYO', 
        'BIST:KLRHO', 'BIST:KMPUR', 'BIST:KLMSN', 'BIST:KCAER'  'BIST:KFKTF', 'BIST:KOCFN', 'BIST:KCHOL', 
        'BIST:KOCMT', 'BIST:KLSYN', 'BIST:KNFRT', 'BIST:KONTR', 'BIST:KONYA', 'BIST:KONKA', 'BIST:KGYO', 
        'BIST:KORDS', 'BIST:KRPLS', 'BIST:KORTS', 'BIST:KOTON', 'BIST:KOZAL', 'BIST:KOZAA', 'BIST:KOPOL',  
        'BIST:KRGYO', 'BIST:KRSTL', 'BIST:KRONT', 'BIST:KTKVK', 'BIST:KTSVK', 'BIST:KSTUR', 'BIST:KUVVA', 
        'BIST:KUYAS', 'BIST:KBORU', 'BIST:KZGYO', 'BIST:KUTPO', 'BIST:KTSKR', 'BIST:LIDER', 'BIST:LVTVK', 
        'BIST:LIDFA', 'BIST:LILAK', 'BIST:LMKDC', 'BIST:LINK',  'BIST:LOGO',  'BIST:LKMNH', 'BIST:LRSHO', 
        'BIST:LUKSK', 'BIST:LYDHO', 'BIST:LYDYE', 'BIST:MACKO', 'BIST:MAKIM', 'BIST:MAKTK', 'BIST:MANAS', 
        'BIST:MRBAS', 'BIST:MAGEN', 'BIST:MRMAG', 'BIST:MARKA', 'BIST:MAALT', 'BIST:MRSHL', 'BIST:MRGYO', 
        'BIST:MARTI', 'BIST:MTRKS', 'BIST:MAVI',  'BIST:MZHLD' ,'BIST:MEDTR', 'BIST:MEGMT', 'BIST:MEGAP', 
        'BIST:MEKAG', 'BIST:MNDRS', 'BIST:MEPET', 'BIST:MERCN', 'BIST:MRBKF', 'BIST:MBFTR', 'BIST:MERIT', 
        'BIST:MERKO', 'BIST:METUR', 'BIST:METRO', 'BIST:MTRYO', 'BIST:MHRGY', 'BIST:MIATK', 'BIST:MGROS', 
        'BIST:MSGYO', 'BIST:MPARK', 'BIST:MMCAS', 'BIST:MOBTL', 'BIST:MOGAN', 'BIST:MNDTR', 'BIST:EGEPO', 
        'BIST:NATEN', 'BIST:NTGAZ', 'BIST:NTHOL', 'BIST:NETAS', 'BIST:NIBAS', 'BIST:NUHCM', 'BIST:NUGYO', 
        'BIST:NRHOL', 'BIST:NRLIN', 'BIST:NURVK', 'BIST:OBAMS', 'BIST:OBASE', 'BIST:ODAS',  'BIST:ODINE', 
        'BIST:OFSYM', 'BIST:ONCSM', 'BIST:ONRYT', 'BIST:OPET',  'BIST:ORCAY', 'BIST:ORFIN', 'BIST:ORGE', 
        'BIST:OSTIM', 'BIST:OTKAR', 'BIST:OTOKC', 'BIST:OTTO' , 'BIST:OYAKC', 'BIST:OYAYO', 'BIST:OYLUM', 
        'BIST:OZKGY', 'BIST:OZATD', 'BIST:OZGYO', 'BIST:OZRDN', 'BIST:OZSUB', 'BIST:OZYSR', 'BIST:PAMEL', 
        'BIST:PNLSN', 'BIST:PAGYO', 'BIST:PAPIL', 'BIST:PRFFK',' BIST:PRDGS', 'BIST:PRKME', 'BIST:PARSN',  
        'BIST:PASEU', 'BIST:PSGYO', 'BIST:PATEK', 'BIST:PCILT' ,'BIST:PGSUS', 'BIST:PEKGY', 'BIST:PENGD', 
        'BIST:PENTA', 'BIST:PEHOL', 'BIST:PSDTC', 'BIST:PETKM', 'BIST:PKENT', 'BIST:PETUN', 'BIST:PINSU', 
        'BIST:PNSUT', 'BIST:PKART', 'BIST:PLTUR', 'BIST:POLHO', 'BIST:POLTK', 'BIST:PRZMA', 'BIST:BIENF', 
        'BIST:QNBFF', 'BIST:QNBFK', 'BIST:QNBVK', 'BIST:QUAGR' ,'BIST:QUFIN', 'BIST:RNPOL', 'BIST:RALYH', 
        'BIST:RAYSG', 'BIST:REEDR', 'BIST:RYGYO', 'BIST:RYSAS', 'BIST:RODRG', 'BIST:ROYAL', 'BIST:RGYAS', 
        'BIST:RTALB', 'BIST:RUBNS', 'BIST:SAFKR', 'BIST:SANEL', 'BIST:SNICA', 'BIST:SANFM', 'BIST:SANKO', 
        'BIST:SAMAT', 'BIST:SARKY', 'BIST:SARTN', 'BIST:SASA' , 'BIST:SAYAS'  'BIST:SDTTR', 'BIST:SEGMN', 
        'BIST:SARTN', 'BIST:SASA',  'BIST:SAYAS', 'BIST:SDTTR', 'BIST:SEGMN', 'BIST:SEKUR', 'BIST:SELEC', 
        'BIST:SELGD', 'BIST:SELVA', 'BIST:SNKRN', 'BIST:SRVGY', 'BIST:SEYKM', 'BIST:SHTRP', 'BIST:SILVR', 
        'BIST:SNGYO', 'BIST:SKYLP', 'BIST:SMRTG', 'BIST:SMART', 'BIST:SODSN', 'BIST:SOKE',  'BIST:SKTAS', 
        'BIST:SONME', 'BIST:SNPAM', 'BIST:SUMAS', 'BIST:SUNTK', 'BIST:SURGY', 'BIST:SUWEN', 'BIST:SMRFA', 
        'BIST:SMRVA', 'BIST:SEKFA', 'BIST:SEKFK', 'BIST:SEGYO', 'BIST:SOKM',  'BIST:DRPHN', 'BIST:TOKI', 
        'BIST:TABGD', 'BIST:TAMFA', 'BIST:TNZTP', 'BIST:TARKM' ,'BIST:TATGD', 'BIST:TATEN', 'BIST:TAVHL', 
        'BIST:TEBFA', 'BIST:TEBCE', 'BIST:TEKTU', 'BIST:TKFEN', 'BIST:TKNSA', 'BIST:TMPOL', 'BIST:TRFFA', 
        'BIST:TFNVK', 'BIST:TGSAS', 'BIST:TIMUR', 'BIST:TRYKI', 'BIST:TOASO', 'BIST:TRGYO', 'BIST:TLMAN', 
        'BIST:TSPOR', 'BIST:TDGYO', 'BIST:TSGYO', 'BIST:TUCLK', 'BIST:TUKAS', 'BIST:TRCAS', 'BIST:TUREX', 
        'BIST:MARBL', 'BIST:TRKFN', 'BIST:TRILC', 'BIST:TCELL', 'BIST:TMSN',  'BIST:TUPRS', 'BIST:THYAO', 
        'BIST:PRKAB', 'BIST:TTKOM', 'BIST:TTRAK', 'BIST:TBORG', 'BIST:TURGG', 'BIST:GARAN', 'BIST:HALKB', 
        'BIST:SISE',  'BIST:UFUK',  'BIST:ULAS',  'BIST:ULUFA', 'BIST:ULUSE', 'BIST:ULUUN', 'BIST:UMPAS', 
        'BIST:USAK',  'BIST:ULKER', 'BIST:UNLU',  'BIST:VAKFN', 'BIST:VKGYO', 'BIST:VKFYO', 'BIST:VAKVK', 
        'BIST:VAKKO', 'BIST:VANGD', 'BIST:VBTYZ',' BIST:VDFLO', 'BIST:VRGYO', 'BIST:VERUS', 'BIST:VERTU', 
        'BIST:VESBE', 'BIST:VESTL', 'BIST:VKING', 'BIST:VDFAS', 'BIST:YKFKT', 'BIST:YKFIN', 'BIST:YAPRK', 
        'BIST:YYAPI', 'BIST:YESIL', 'BIST:YBTAS', 'BIST:YIGIT', 'BIST:YONGA', 'BIST:YKSLN', 'BIST:YUNSA', 
        'BIST:ZEDUR', 'BIST:ZEDUR', 'BIST:ZRGYO', 'BIST:ZKBVK', 'BIST:ZKBVR', 'BIST:ZOREN', 'BIST:ZORLF', 
        
    ]

    return tv, symbols



# Ana işlem fonksiyonu
def process_stocks():
    tv, symbols = get_symbols_and_data()

    # Raporlama için kullanılacak başlıklar
    Titles = ['Hisse Adı', 'Son Fiyat', 'Alım Sinyali']
    df_signals = pd.DataFrame(columns=Titles)

    # Her bir hisse için işlem yap
    for symbol in symbols:
        try:
            # Veriyi al (4 saatlik periyotta son 100 veri)
            data = tv.get_hist(symbol=symbol, exchange='BIST', interval=Interval.in_4_hour, n_bars=100)
            if data is None or data.empty:
                print(f"No data for {symbol}")
                continue

            data = data.reset_index()

            # Momentum, MFI ve WaveTrend sinyallerini kontrol et
            signals_df = momentum_mfi_wave_dip(data)
            signals_last = signals_df.tail(2).reset_index()

            # Alım sinyali kontrolü
            buy_signal = signals_last.loc[1, 'Buy_Signal']
            last_price = signals_last.loc[1, 'close']
            signal_row = [symbol, last_price, buy_signal]
            df_signals.loc[len(df_signals)] = signal_row
            print(signal_row)
        except Exception as e:
            print(f"Error processing {symbol}: {e}")

    # Alım Sinyali sütununu kontrol et ve bool türüne çevir
    df_signals['Alım Sinyali'] = df_signals['Alım Sinyali'].astype(bool)

    # Sadece True olanları al
    true_signals = df_signals[df_signals['Alım Sinyali'] == True]

    # Sonuçları yazdır (Sadece True olanları göster)
    print("\nAlım Sinyalleri (True):\n", true_signals)

    # Sonuçları CSV olarak kaydet (Sadece True olanları kaydet)
    true_signals.to_csv("Momentum_MFI_WaveTrend_Dip_Sinyalleri_True.csv", index=True)

    return true_signals  # Sadece True olanları döndürüyoruz

# Fonksiyonu çağır ve sonucu al
df_signals = process_stocks()
