# --- Gerekli Kütüphaneler ---
!pip install git+https://github.com/rongardF/tvdatafeed --quiet
!pip install ta scikit-learn pandas numpy --quiet

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
import ta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

tv = TvDatafeed()

bist_hisseler = [    'BIST:BINHO', 'BIST:AVOD', 'BIST:A1CAP', 'BIST:ACSEL', 'BIST:ADEL', 'BIST:ADESE', 'BIST:ADGYO',
    'BIST:AFYON', 'BIST:AGHOL', 'BIST:AGESA', 'BIST:AGROT', 'BIST:AHSGY', 'BIST:AHGAZ', 'BIST:AKBNK', 
    'BIST:AKCNS', 'BIST:AKYHO', 'BIST:AKENR', 'BIST:AKFGY', 'BIST:AKFYE', 'BIST:ATEKS', 'BIST:AKSGY', 
    'BIST:AKMGY', 'BIST:AKSA', 'BIST:AKSEN', 'BIST:AKGRT', 'BIST:AKSUE', 'BIST:ALCAR', 'BIST:ALGYO', 
    'BIST:ALARK', 'BIST:ALBRK', 'BIST:ALCTL', 'BIST:ALFAS', 'BIST:ALKIM', 'BIST:ALKA', 'BIST:AYCES', 
    'BIST:ALTNY', 'BIST:ALKLC', 'BIST:ALMAD', 'BIST:ALVES', 'BIST:ANSGR', 'BIST:AEFES', 'BIST:ANHYT', 
    'BIST:ASUZU', 'BIST:ANGEN', 'BIST:ANELE', 'BIST:ARCLK', 'BIST:ARDYZ', 'BIST:ARENA', 'BIST:ARMGD', 
    'BIST:ARSAN', 'BIST:ARTMS', 'BIST:ARZUM', 'BIST:ASGYO', 'BIST:ASELS', 'BIST:ASTOR', 'BIST:ATAGY', 
    'BIST:ATAKP', 'BIST:AGYO', 'BIST:ATSYH', 'BIST:ATLAS', 'BIST:ATATP', 'BIST:AVGYO', 'BIST:AVTUR', 
    'BIST:AVHOL', 'BIST:AVPGY', 'BIST:AYDEM', 'BIST:AYEN', 'BIST:AYES', 'BIST:AYGAZ', 'BIST:AZTEK', 
    'BIST:BAGFS', 'BIST:BAHKM', 'BIST:BAKAB', 'BIST:BALAT', 'BIST:BNTAS', 'BIST:BANVT', 'BIST:BARMA', 
    'BIST:BASGZ', 'BIST:BASCM', 'BIST:BEGYO', 'BIST:BTCIM', 'BIST:BSOKE', 'BIST:BYDNR', 'BIST:BAYRK', 
    'BIST:BERA', 'BIST:BRKSN', 'BIST:BJKAS', 'BIST:BEYAZ', 'BIST:BIENY', 'BIST:BLCYT', 'BIST:BIMAS', 
    'BIST:BINBN', 'BIST:BIOEN', 'BIST:BRKVY', 'BIST:BRKO', 'BIST:BRLSM', 'BIST:BRMEN', 'BIST:BIZIM', 
    'BIST:BMSTL', 'BIST:BMSCH', 'BIST:BOBET', 'BIST:BORSK', 'BIST:BORLS', 'BIST:BRSAN', 'BIST:BRYAT', 
    'BIST:BFREN', 'BIST:BOSSA', 'BIST:BRISA', 'BIST:BURCE', 'BIST:BURVA', 'BIST:BUCIM', 'BIST:BVSAN', 
    'BIST:BIGCH', 'BIST:CRFSA', 'BIST:CASA', 'BIST:CEMZY', 'BIST:CEOEM', 'BIST:CCOLA', 'BIST:CONSE', 
    'BIST:COSMO', 'BIST:CVKMD', 'BIST:CWENE', 'BIST:CANTE', 'BIST:CATES', 'BIST:CLEBI', 'BIST:CELHA', 
    'BIST:CEMAS', 'BIST:CEMTS', 'BIST:CIMSA', 'BIST:CUSAN', 'BIST:DAGI', 'BIST:DAGHL', 'BIST:DAPGM', 
    'BIST:DARDL', 'BIST:DGATE', 'BIST:DCTTR', 'BIST:DMSAS', 'BIST:DENGE', 'BIST:DZGYO', 'BIST:DERIM', 
    'BIST:DERHL', 'BIST:DESA', 'BIST:DEVA', 'BIST:DNISI', 'BIST:DIRIT', 'BIST:DITAS', 'BIST:DMRGD', 
    'BIST:DOCO', 'BIST:DOFER', 'BIST:DOBUR', 'BIST:DOHOL', 'BIST:DGNMO', 'BIST:ARASE', 'BIST:DOGUB', 
    'BIST:DOAS', 'BIST:DOKTA', 'BIST:DURDO', 'BIST:DURKN', 'BIST:DYOBY', 'BIST:EDATA', 'BIST:EBEBK', 
    'BIST:ECZYT', 'BIST:EDIP', 'BIST:EFORC', 'BIST:EGEEN', 'BIST:ECILC', 'BIST:EKIZ', 'BIST:EKOS', 
    'BIST:EKSUN', 'BIST:ELITE', 'BIST:EKGYO', 'BIST:ENJSA', 'BIST:ENERY', 'BIST:ENKAI', 'BIST:ENSRI', 
    'BIST:ERCB', 'BIST:EREGL', 'BIST:ERSU', 'BIST:ESCAR', 'BIST:ESCOM', 'BIST:ESEN', 'BIST:ETILR', 
    'BIST:EUKYO', 'BIST:EUYO', 'BIST:ETYAT', 'BIST:EUHOL', 'BIST:TEZOL', 'BIST:EUREN', 'BIST:EUPWR', 
    'BIST:EYGYO', 'BIST:FADE', 'BIST:FMIZP', 'BIST:FENER', 'BIST:FLAP', 'BIST:FONET', 'BIST:FROTO', 
    'BIST:FORMT', 'BIST:FORTE', 'BIST:FRIGO', 'BIST:FZLGY', 'BIST:GWIND', 'BIST:GSRAY', 'BIST:GARFA', 
    'BIST:GRNYO', 'BIST:GEDIK', 'BIST:GEDZA', 'BIST:GLCVY', 'BIST:GENIL', 'BIST:GENTS', 'BIST:GEREL', 
    'BIST:GZNMI', 'BIST:GIPTA', 'BIST:GMTAS', 'BIST:GESAN', 'BIST:GLYHO', 'BIST:GUBRF', 'BIST:GLRYH', 
    'BIST:GUNDG', 'BIST:GRSEL', 'BIST:SAHOL', 'BIST:HLGYO', 'BIST:HRKET', 'BIST:HATSN', 'BIST:HATEK', 
    'BIST:HDFGS', 'BIST:HEDEF', 'BIST:HEKTS', 'BIST:HKTM', 'BIST:HTTBT', 'BIST:HOROZ', 'BIST:HUBVC', 
    'BIST:HUNER', 'BIST:HURGZ', 'BIST:ENTRA', 'BIST:ICUGS', 'BIST:INGRM', 'BIST:INVEO', 'BIST:INVES', 
    'BIST:ISKPL', 'BIST:IEYHO', 'BIST:IDGYO', 'BIST:IHEVA', 'BIST:IHLGM', 'BIST:IHGZT', 'BIST:IHAAS', 
    'BIST:IHLAS'
   
]

# Hareketli Ortalama Fonksiyonları
def ema(series, period=14):
    return series.ewm(span=period, adjust=False).mean()

def sma(series, period=14):
    return series.rolling(window=period).mean()

def wma(series, period=14):
    weights = np.arange(1, period + 1)
    return series.rolling(period).apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)

def hma(series, period=14):
    half = int(period / 2)
    sqrt = int(np.sqrt(period))
    wma_half = wma(series, half)
    wma_full = wma(series, period)
    return wma(2 * wma_half - wma_full, sqrt)

def zlsma(series, period=14):
    ema1 = ema(series, period)
    ema2 = ema(ema1, period)
    return 2 * ema1 - ema2

def dema(series, period=14):
    e = ema(series, period)
    return 2 * e - ema(e, period)

def tema(series, period=14):
    e1 = ema(series, period)
    e2 = ema(e1, period)
    e3 = ema(e2, period)
    return 3 * (e1 - e2) + e3

def hesapla_tum_indikatorler(df):
    # Hareketli Ortalamalar
    df['EMA5'] = ema(df['close'], 5)
    df['EMA20'] = ema(df['close'], 20)
    df['EMA50'] = ema(df['close'], 50)
    df['SMA20'] = sma(df['close'], 20)
    df['SMA50'] = sma(df['close'], 50)
    df['WMA20'] = wma(df['close'], 20)
    df['HMA20'] = hma(df['close'], 20)
    df['ZLSMA20'] = zlsma(df['close'], 20)
    df['DEMA20'] = dema(df['close'], 20)
    df['TEMA20'] = tema(df['close'], 20)

    # Momentum Göstergeleri
    df['RSI'] = ta.momentum.RSIIndicator(df['close'], 14).rsi()
    df['StochRSI'] = ta.momentum.StochRSIIndicator(df['close']).stochrsi()
    df['CCI'] = ta.trend.CCIIndicator(df['high'], df['low'], df['close'], 20).cci()
    df['Williams_%R'] = ta.momentum.WilliamsRIndicator(df['high'], df['low'], df['close'], 14).williams_r()
    df['ROC'] = ta.momentum.ROCIndicator(df['close'], 12).roc()

    # Hacim ve Para Akışı
    df['MFI'] = ta.volume.MFIIndicator(df['high'], df['low'], df['close'], df['volume'], 14).money_flow_index()
    df['OBV'] = ta.volume.OnBalanceVolumeIndicator(df['close'], df['volume']).on_balance_volume()
    df['CMF'] = ta.volume.ChaikinMoneyFlowIndicator(df['high'], df['low'], df['close'], df['volume'], 20).chaikin_money_flow()

    # KVO: Klinger Volume Oscillator (burada basit EMA farkı)
    df['KVO'] = df['volume'].ewm(span=34).mean() - df['volume'].ewm(span=55).mean()

    # Hacim ortalama ve spike
    df['Volume_MA20'] = df['volume'].rolling(20).mean()
    df['Volume_Spike'] = (df['volume'] > (df['Volume_MA20'] * 2)).astype(int)

    # Bollinger Bands ve Volatilite
    bb = ta.volatility.BollingerBands(df['close'], 20, 2)
    df['BB_Middle'] = bb.bollinger_mavg()
    df['BB_Upper'] = bb.bollinger_hband()
    df['BB_Lower'] = bb.bollinger_lband()
    df['BB_Squeeze'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Middle']

    df['ATR'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], 14).average_true_range()
    df['Donchian_High'] = df['high'].rolling(20).max()
    df['Donchian_Low'] = df['low'].rolling(20).min()
    df['SuperTrend'] = (df['high'] + df['low']) / 2 - (df['ATR'] * 3)

    # Trend ve Diğer
    df['TrendMagic'] = df['close'] - df['ATR']
    df['Fractals'] = ((df['high'].shift(2) < df['high']) & (df['low'].shift(2) > df['low'])).astype(int)

    ichi = ta.trend.IchimokuIndicator(df['high'], df['low'], 9, 26, 52)
    df['Ichimoku_A'] = ichi.ichimoku_a()
    df['Ichimoku_B'] = ichi.ichimoku_b()

    df['Pivot'] = (df['high'] + df['low'] + df['close']) / 3

    # Fisher Transform
    min9 = df['close'].rolling(9).min()
    max9 = df['close'].rolling(9).max()
    with np.errstate(divide='ignore', invalid='ignore'):
        val = (2 * (df['close'] - min9) / (max9 - min9)) - 1
        val = val.clip(-0.999, 0.999)
        df['Fisher'] = np.arctanh(val)

    # WaveTrend hesaplama
    esa = ta.trend.EMAIndicator(df['close'], 10).ema_indicator()
    d = ta.trend.EMAIndicator(abs(df['close'] - esa), 10).ema_indicator()
    ci = (df['close'] - esa) / (0.015 * d)
    wt1 = ta.trend.EMAIndicator(ci, 21).ema_indicator()
    wt2 = ta.trend.SMAIndicator(wt1, 4).sma_indicator()
    df['WaveTrend'] = wt1 - wt2

    return df

def veri_cek_bist(hisse, bar_sayisi=200):
    try:
        df = tv.get_hist(symbol=hisse, exchange='BIST', interval=Interval.in_4_hour, n_bars=bar_sayisi)
        df = df.reset_index()
        return df
    except Exception as e:
        print(f"⚠️ Veri çekilemedi: {hisse} | Hata: {e}")
        return None

def hacim_filtre(df):
    ort_hacim = df['volume'].rolling(20).mean().iloc[-1]
    son_hacim = df['volume'].iloc[-1]
    return son_hacim > ort_hacim * 1.0

def obv_pozitif_mi(df):
    return df['OBV'].iloc[-1] > df['OBV'].rolling(10).mean().iloc[-1]

def cmf_pozitif_mi(df):
    return df['CMF'].iloc[-1] > 0

def rsi_dipten_donuyor_mu(df):
    rsi_son = df['RSI'].iloc[-1]
    return 25 <= rsi_son <= 65

def ema_crossover(df):
    return df['close'].iloc[-1] > df['EMA20'].iloc[-1]

def atr_cikis(df):
    atr = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], 14).average_true_range()
    son_atr = atr.iloc[-1]
    ort_atr = atr.rolling(20).mean().iloc[-1]
    return son_atr < ort_atr * 1.1

def tahta_ai(df):
    df = hesapla_tum_indikatorler(df)
    df = df.dropna().reset_index(drop=True)

    df['future'] = df['close'].shift(-3)
    df['label'] = (df['future'] > df['close'] * 1.01).astype(int)
    df.dropna(inplace=True)

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    features = [col for col in numeric_cols if col not in ['future', 'label', 'open', 'high', 'low', 'close', 'volume']]

    X = df[features]
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

    X_train = X_train.replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill')
    y_train = y_train.replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill')

    valid_idx = X_train.notnull().all(axis=1) & y_train.notnull()
    X_train = X_train[valid_idx]
    y_train = y_train[valid_idx]

    model = RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    last_row = X.iloc[[-1]].replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill')
    prob = model.predict_proba(last_row)[0][1]

    if prob > 0.6:
        karar = "STRONG BUY"
    elif prob > 0.4:
        karar = "BUY"
    else:
        karar = "WATCH"

    print(f"TAHTACI AI Sinyal: {karar} - Tahmin Gücü: %{prob*100:.1f}")
    return karar, prob

def bist_tarama():
    sonuclar = []
    for hisse in bist_hisseler:
        print(f"\n📡 {hisse} verisi çekiliyor...")
        df = veri_cek_bist(hisse)
        if df is not None and len(df) > 100:
            df = hesapla_tum_indikatorler(df)

            print(f"{hisse} filtre durumu:")
            print(f" - Hacim filtre: {'✅' if hacim_filtre(df) else '❌'}")
            print(f" - OBV pozitif: {'✅' if obv_pozitif_mi(df) else '❌'}")
            print(f" - CMF pozitif: {'✅' if cmf_pozitif_mi(df) else '❌'}")
            print(f" - EMA crossover: {'✅' if ema_crossover(df) else '❌'}")
            print(f" - RSI 25-65 arası: {'✅' if rsi_dipten_donuyor_mu(df) else '❌'}")
            print(f" - ATR volatilite düşük: {'✅' if atr_cikis(df) else '❌'}")

            if (hacim_filtre(df) and obv_pozitif_mi(df) and cmf_pozitif_mi(df) and
                ema_crossover(df) and rsi_dipten_donuyor_mu(df) and atr_cikis(df)):

                karar, prob = tahta_ai(df)
                sonuclar.append((hisse, karar, prob))
            else:
                print(f"⏳ {hisse}: Sinyal güvenilir değil, elendi.")
        else:
            print(f"⏳ {hisse}: Veri yetersiz veya hata var.")

    df_sonuc = pd.DataFrame(sonuclar, columns=["Hisse", "Karar", "AI Skor"])
    print("\n--- TAHTACI AI Tarama Sonuçları (Gevşek Filtre) ---")
    print(df_sonuc.sort_values(by="AI Skor", ascending=False))

    super_buylar = df_sonuc[df_sonuc["AI Skor"] >= 0.6]
    print("\n--- %60 Üzeri AI Skorları (Strong ve Buy) ---")
    print(super_buylar.sort_values(by="AI Skor", ascending=False))
    return df_sonuc, super_buylar

if __name__ == "__main__":
    tum_sonuc, super_buylar = bist_tarama()
