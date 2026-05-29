# --- GEREKLİ KÜTÜPHANELER ---
import pandas as pd
import numpy as np
import warnings
from tvDatafeed import TvDatafeed, Interval
import ta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

warnings.simplefilter(action='ignore')
tv = TvDatafeed()

# === İNDİKATÖR HESAPLAMA ===
def calculate_indicators(df):
    df['RSI'] = ta.momentum.RSIIndicator(df['close']).rsi()
    df['RSI_EMA'] = df['RSI'].ewm(span=7).mean()

    macd = ta.trend.MACD(df['close'])
    df['MACD_hist'] = macd.macd_diff()

    df['EMA5'] = df['close'].ewm(span=5).mean()
    df['EMA21'] = df['close'].ewm(span=21).mean()

    typical_price = (df['high'] + df['low'] + df['close']) / 3
    df['VWAP'] = (typical_price * df['volume']).cumsum() / df['volume'].cumsum()

    adx = ta.trend.ADXIndicator(df['high'], df['low'], df['close'])
    df['ADX'] = adx.adx()
    df['DI_plus'] = adx.adx_pos()
    df['DI_minus'] = adx.adx_neg()

    mfv = ((df['close'] - df['low']) - (df['high'] - df['close'])) / (df['high'] - df['low']).replace(0, np.nan)
    mfv = mfv.replace([np.inf, -np.inf], 0).fillna(0)
    df['CMF'] = (mfv * df['volume']).rolling(window=20).sum() / df['volume'].rolling(window=20).sum()

    obv = ta.volume.OnBalanceVolumeIndicator(df['close'], df['volume'])
    df['OBV'] = obv.on_balance_volume()
    df['OBV_SLOPE'] = df['OBV'].diff().rolling(window=3).mean()

    df['SQM'] = df['close'] - df['close'].rolling(window=20).mean()
    df['SQM'] = df['SQM'].fillna(0)

    ap = (df['high'] + df['low'] + df['close']) / 3
    esa = ap.ewm(span=10).mean()
    d = abs(ap - esa).ewm(span=10).mean()
    ci = (ap - esa) / (0.015 * d)
    df['WT1'] = ci.ewm(span=21).mean()
    df['WT2'] = df['WT1'].ewm(span=4).mean()

    stoch = ta.momentum.StochRSIIndicator(df['close'])
    df['STO_K'] = stoch.stochrsi_k()
    df['STO_D'] = stoch.stochrsi_d()

    df['VOL_AVG'] = df['volume'].rolling(window=20).mean()
    df['VOLUME_CHANGE'] = df['volume'].pct_change()

    df['ZLSMA'] = df['close'].rolling(window=20).mean()

    df['TRMAGIC'] = (df['low'] + df['high']) / 2 - ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()

    df['ATR'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
    df['ATR_SLOPE'] = df['ATR'].diff()

    ichi = ta.trend.IchimokuIndicator(df['high'], df['low'], window1=9, window2=26, window3=52)
    df['tenkan'] = ichi.ichimoku_conversion_line()
    df['kijun'] = ichi.ichimoku_base_line()
    df['senkou_a'] = ichi.ichimoku_a()
    df['senkou_b'] = ichi.ichimoku_b()

    return df

# === MAKİNE ÖĞRENMESİ İÇİN VERİ HAZIRLAMA ===
def prepare_ml_data(df):
    df['future_return'] = df['close'].pct_change(periods=3).shift(-3)  # 3 periyot sonrası getiri (~12 saat)
    df = df.dropna()

    features = ['RSI', 'RSI_EMA', 'MACD_hist', 'EMA5', 'EMA21', 'VWAP', 'ADX', 'DI_plus', 'DI_minus',
                'CMF', 'OBV', 'OBV_SLOPE', 'SQM', 'WT1', 'WT2', 'STO_K', 'STO_D', 'VOL_AVG', 'VOLUME_CHANGE',
                'ZLSMA', 'TRMAGIC', 'ATR', 'ATR_SLOPE', 'tenkan', 'kijun', 'senkou_a', 'senkou_b']

    X = df[features]
    y = (df['future_return'] > 0.01).astype(int)  # %1 üzerinde getiri = AL

    return X, y

# === MODEL EĞİTİMİ ===
def train_ml_model(df):
    X, y = prepare_ml_data(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print("ML Model Performans Raporu:")
    print(classification_report(y_test, preds))

    return model

# === SİNYAL İŞLEME VE ML ENTEGRASYONU ===
def get_signals_with_ml(symbol, model):
    df = tv.get_hist(symbol=symbol.split(":")[1], exchange=symbol.split(":")[0], interval=Interval.in_4_hour, n_bars=200)
    if df is None or df.empty:
        print(f"{symbol} için veri yok.")
        return None

    df = calculate_indicators(df)

    # KEŞİŞİM KONTROLLERİ (Sinyal sayısı)
    p, c = -2, -1
    sinyaller = {
        'RSI': df['RSI'].iloc[p] < df['RSI_EMA'].iloc[p] and df['RSI'].iloc[c] > df['RSI_EMA'].iloc[c],
        'MACD': df['MACD_hist'].iloc[p] < 0 and df['MACD_hist'].iloc[c] > 0,
        'EMA': df['EMA5'].iloc[p] < df['EMA21'].iloc[p] and df['EMA5'].iloc[c] > df['EMA21'].iloc[c],
        'VWAP': df['close'].iloc[p] < df['VWAP'].iloc[p] and df['close'].iloc[c] > df['VWAP'].iloc[c],
        'ADX': df['ADX'].iloc[p] < 25 and df['ADX'].iloc[c] > 25 and df['DI_plus'].iloc[c] > df['DI_minus'].iloc[c],
        'CMF': df['CMF'].iloc[p] < 0 and df['CMF'].iloc[c] > 0,
        'OBV': df['OBV_SLOPE'].iloc[c] > 0,
        'SQM': df['SQM'].iloc[p] < 0 and df['SQM'].iloc[c] > 0,
        'WaveTrend': df['WT1'].iloc[p] < df['WT2'].iloc[p] and df['WT1'].iloc[c] > df['WT2'].iloc[c],
        'StochRSI': df['STO_K'].iloc[p] < df['STO_D'].iloc[p] and df['STO_K'].iloc[c] > df['STO_D'].iloc[c],
        'VOLSpike': df['volume'].iloc[c] > 2 * df['VOL_AVG'].iloc[c],
        'TrendMagic': df['close'].iloc[p] < df['TRMAGIC'].iloc[p] and df['close'].iloc[c] > df['TRMAGIC'].iloc[c],
        'ZLSMA': df['close'].iloc[p] < df['ZLSMA'].iloc[p] and df['close'].iloc[c] > df['ZLSMA'].iloc[c],
        'ATR': df['ATR_SLOPE'].iloc[p] <= 0 and df['ATR_SLOPE'].iloc[c] > 0,
        'Ichimoku': df['tenkan'].iloc[p] < df['kijun'].iloc[p] and df['tenkan'].iloc[c] > df['kijun'].iloc[c] and df['close'].iloc[c] > df[['senkou_a', 'senkou_b']].iloc[c].max()
    }

    score = sum(sinyaller.values())

    # ONAY KRİTERLERİ
    onay_kriterleri = [
        df['volume'].iloc[c] > df['VOL_AVG'].iloc[c] and df['close'].iloc[c] > df['close'].iloc[p],  # bağlı hacim
        df['CMF'].iloc[c] > 0,  # para girişi
        df['MACD_hist'].iloc[c] > df['MACD_hist'].iloc[p],  # momentum artışı
        df['OBV_SLOPE'].iloc[c] > 0 or df['volume'].iloc[c] > 2 * df['VOL_AVG'].iloc[c],  # yüksek alım
        df['SQM'].iloc[p] < 0 and df['SQM'].iloc[c] > 0  # squeeze momentum çıkışı
    ]
    onay_skoru = sum(onay_kriterleri)

    # ML Tahmini
    features = ['RSI', 'RSI_EMA', 'MACD_hist', 'EMA5', 'EMA21', 'VWAP', 'ADX', 'DI_plus', 'DI_minus',
                'CMF', 'OBV', 'OBV_SLOPE', 'SQM', 'WT1', 'WT2', 'STO_K', 'STO_D', 'VOL_AVG', 'VOLUME_CHANGE',
                'ZLSMA', 'TRMAGIC', 'ATR', 'ATR_SLOPE', 'tenkan', 'kijun', 'senkou_a', 'senkou_b']
    X = df[features].iloc[c].values.reshape(1, -1)
    ml_pred = model.predict(X)[0]

    # Etiketleme
    if score >= 9 and onay_skoru >= 3 and ml_pred == 1:
        label = "🚀 STRONG BUY"
    elif score >= 6 and onay_skoru >= 2 and ml_pred == 1:
        label = "✅ BUY"
    elif score >= 4 and onay_skoru >= 1:
        label = "👀 WATCH"
    else:
        label = "❌ NO SIGNAL"

    if label != "❌ NO SIGNAL":
        print(f"\n{label} | {symbol} ({score}/15) Onay: {onay_skoru}/5 | ML Tahmini: {ml_pred}")
        aktifler = [k for k, v in sinyaller.items() if v]
        print("Sinyal Verenler:", ", ".join(aktifler))
    else:
        print(f"{label} | {symbol} ({score}/15) Onay: {onay_skoru}/5 | ML Tahmini: {ml_pred}")

# === MODELİ EĞİT ===
print("Model eğitimi başlıyor, sabır kanka...")
df_train = tv.get_hist(symbol='BIST:AKBNK', exchange='BIST', interval=Interval.in_4_hour, n_bars=500)
df_train = calculate_indicators(df_train)
model = train_ml_model(df_train)

# === HİSSELER ===
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

# === TARAYICI ÇALIŞTIR ===
for h in bist_hisseler:
    get_signals_with_ml(h, model)
