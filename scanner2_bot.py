# =====================================================
# 1️⃣ KURULUMLAR (COLAB)
# =====================================================
!pip install -q pandas numpy ta scikit-learn
!pip install -q git+https://github.com/rongardF/tvdatafeed

# =====================================================
# 2️⃣ IMPORTLAR
# =====================================================
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np

from tvDatafeed import TvDatafeed, Interval

from ta.momentum import RSIIndicator, ROCIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import EMAIndicator, SMAIndicator, MACD
from ta.volume import OnBalanceVolumeIndicator, MFIIndicator, ChaikinMoneyFlowIndicator
import ta







# =====================================================
# 3️⃣ TV DATAFEED
# =====================================================
# Eğer timeout olursa loginli kullan
# tv = TvDatafeed("kullanici", "sifre")
tv = TvDatafeed()

# =====================================================
# 4️⃣ BIST HİSSELER
# =====================================================
symbols = [
"BINHO","AVOD","A1CAP","ACSEL","ADEL","ADESE","ADGYO",
"AFYON","AGHOL","AGESA","AGROT","AHSGY","AHGAZ","AKBNK",
"AKCNS","AKYHO","AKENR","AKFGY","AKFYE","ATEKS","AKSGY",
"AKMGY","AKSA","AKSEN","AKGRT","AKSUE","ALCAR","ALGYO",
"ALARK","ALBRK","ALCTL","ALFAS","ALKIM","ALKA","AYCES",
"ALTNY","ALKLC","ALMAD","ALVES","ANSGR","AEFES","ANHYT",
"ASUZU","ANGEN","ANELE","ARCLK","ARDYZ","ARENA","ARMGD",
"ARSAN","ARTMS","ARZUM","ASGYO","ASELS","ASTOR","ATAGY",
"ATAKP","AGYO","ATSYH","ATLAS","ATATP","AVGYO","AVTUR",
"AVHOL","AVPGY","AYDEM","AYEN","AYES","AYGAZ","AZTEK",
"BAGFS","BAHKM","BAKAB","BALAT","BNTAS","BANVT","BARMA",
"BASGZ","BASCM","BEGYO","BTCIM","BSOKE","BYDNR","BAYRK",
"BERA","BRKSN","BJKAS","BEYAZ","BIENY","BLCYT","BIMAS",
"BINBN","BIOEN","BRKVY","BRKO","BRLSM","BRMEN","BIZIM",
"BMSTL","BMSCH","BOBET","BORSK","BORLS","BRSAN","BRYAT",
"BFREN","BOSSA","BRISA","BURCE","BURVA","BUCIM","BVSAN",
"BIGCH","CRFSA","CASA","CEMZY","CEOEM","CCOLA","CONSE",
"COSMO","CVKMD","CWENE","CANTE","CATES","CLEBI","CELHA",
"CEMAS","CEMTS","CIMSA","CUSAN","DAGI","DAGHL","DAPGM",
"DARDL","DGATE","DCTTR","DMSAS","DENGE","DZGYO","DERIM",
"DERHL","DESA","DEVA","DNISI","DIRIT","DITAS","DMRGD",
"DOCO","DOFER","DOBUR","DOHOL","DGNMO","ARASE","DOGUB",
"DOAS","DOKTA","DURDO","DURKN","DYOBY","EDATA","EBEBK",
"ECZYT","EDIP","EFORC","EGEEN","ECILC","EKIZ","EKOS",
"EKSUN","ELITE","EKGYO","ENJSA","ENERY","ENKAI","ENSRI",
"ERCB","EREGL","ERSU","ESCAR","ESCOM","ESEN","ETILR",
"EUKYO","EUYO","ETYAT","EUHOL","TEZOL","EUREN","EUPWR",
"EYGYO","FADE","FMIZP","FENER","FLAP","FONET","FROTO",
"FORMT","FORTE","FRIGO","FZLGY","GWIND","GSRAY","GARFA",
"GRNYO","GEDIK","GEDZA","GLCVY","GENIL","GENTS","GEREL",
"GZNMI","GIPTA","GMTAS","GESAN","GLYHO","GUBRF","GLRYH",
"GUNDG","GRSEL","SAHOL","HLGYO","HRKET","HATSN","HATEK",
"HDFGS","HEDEF","HEKTS","HKTM","HTTBT","HOROZ","HUBVC",
"HUNER","HURGZ","ENTRA","ICUGS","INGRM","INVEO","INVES",
"ISKPL","IEYHO","IDGYO","IHEVA","IHLGM","IHGZT","IHAAS",
"IHLAS","ICBCT"
]



EXCHANGE = "BIST"

# =====================================================
# 5️⃣ TIMEFRAMES
# =====================================================
TIMEFRAMES = {
    "4H": Interval.in_4_hour,
    "1D": Interval.in_daily,
    "1W": Interval.in_weekly
}

# =====================================================
# 6️⃣ DATA CACHE
# =====================================================
data_cache = {}

def get_data(symbol, tf_name, tf):
    key = (symbol, tf_name)

    try:
        data = tv.get_hist(symbol, EXCHANGE, tf, 300)
        data_cache[key] = data
        return data
    except:
        return None



# =====================================================
# 7️⃣ FEATURE ENGINE – ORTAK
# =====================================================
def build_features(df):
    df = df.copy()

    df["RSI"] = RSIIndicator(df["close"], 14).rsi()
    df["EMA20"] = EMAIndicator(df["close"], 20).ema_indicator()
    df["EMA21"] = EMAIndicator(df["close"], 21).ema_indicator()
    df["EMA50"] = EMAIndicator(df["close"], 50).ema_indicator()
    df["EMA200"] = EMAIndicator(df["close"], 200).ema_indicator()

    bb = BollingerBands(df["close"], 20, 2)
    df["BB_HIGH"] = bb.bollinger_hband()
    df["BB_LOW"] = bb.bollinger_lband()
    df["BB_WIDTH"] = df["BB_HIGH"] - df["BB_LOW"]

    df["ATR"] = AverageTrueRange(df["high"], df["low"], df["close"], 14).average_true_range()
    df["OBV"] = OnBalanceVolumeIndicator(df["close"], df["volume"]).on_balance_volume()
    df["MFI"] = MFIIndicator(df["high"], df["low"], df["close"], df["volume"], 14).money_flow_index()
    df["CMF"] = ChaikinMoneyFlowIndicator(df["high"], df["low"], df["close"], df["volume"], 20).chaikin_money_flow()

    df["VWAP"] = ta.volume.volume_weighted_average_price(
        df["high"], df["low"], df["close"], df["volume"]
    )

    df["VOL_MEAN"] = df["volume"].rolling(20).mean()
    df["VOLUME_RATIO"] = df["volume"] / df["VOL_MEAN"]
    df["ROC"] = ROCIndicator(df["close"]).roc()

    return df.dropna()

# =====================================================
# 8️⃣ STRATEJİLER
# =====================================================
def strat_squeeze(df):
    return df["BB_WIDTH"].iloc[-1] < df["BB_WIDTH"].rolling(20).mean().iloc[-1]

def strat_money_flat(df):
    return abs(df["EMA21"].iloc[-1] - df["EMA50"].iloc[-1]) / df["close"].iloc[-1] < 0.01

def strat_downtrend_break(df):
    return df["close"].iloc[-1] > df["EMA21"].iloc[-1] and \
           df["close"].iloc[-2] < df["EMA21"].iloc[-2]

def strat_accumulation(df):
    return df["MFI"].iloc[-1] < 40 and \
           df["OBV"].iloc[-1] > df["OBV"].iloc[-5]

def strat_tavan(df):
    return df["RSI"].iloc[-1] > 60 and \
           df["VOLUME_RATIO"].iloc[-1] > 2

def strat_pivot(df):
    low50 = df["low"].rolling(50).min().iloc[-1]
    return abs(df["close"].iloc[-1] - low50) / df["close"].iloc[-1] < 0.005

def strat_fake_break(df):
    return df["high"].iloc[-2] > df["BB_HIGH"].iloc[-2] and \
           df["close"].iloc[-1] < df["BB_HIGH"].iloc[-1]

# =====================================================
# CHATGPT QUANT ENGINE – STRATEJİ BLOĞU
# =====================================================

def strat_trend_pullback(df):
    return (
        (df["EMA20"].iloc[-1] > df["EMA50"].iloc[-1]) and
        (df["EMA50"].iloc[-1] > df["EMA200"].iloc[-1]) and
        (abs(df["close"].iloc[-1] - df["EMA20"].iloc[-1]) / df["close"].iloc[-1] < 0.01) and
        (df["RSI"].iloc[-1] > 40) and
        (df["RSI"].iloc[-1] < 55)
    )


def strat_macd_reversal(df):
    macd = MACD(df["close"])
    df["MACD_LINE"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    return (
        (df["MACD_LINE"].iloc[-1] > df["MACD_SIGNAL"].iloc[-1]) and
        (df["MACD_LINE"].iloc[-2] < df["MACD_SIGNAL"].iloc[-2]) and
        (df["RSI"].iloc[-1] > 35) and
        (df["RSI"].iloc[-1] < 55)
    )


def strat_volume_breakout(df):
    return (
        (df["VOLUME_RATIO"].iloc[-1] > 2) and
        (df["close"].iloc[-1] > df["EMA20"].iloc[-1]) and
        (df["CMF"].iloc[-1] > 0)
    )


STRATEGIES = {
    "SQUEEZE": strat_squeeze,
    "PARA_YATAY": strat_money_flat,
    "DUSEN_KIRILIM": strat_downtrend_break,
    "TAHTACI": strat_accumulation,
    "TAVAN": strat_tavan,
    "PIVOT": strat_pivot,
    "FAKE_BREAK": strat_fake_break,
    "CHATGPT_TREND": strat_trend_pullback,
    "CHATGPT_REVERSAL": strat_macd_reversal,
    "CHATGPT_VOLUME": strat_volume_breakout
}


# =====================================================
# 9️⃣ STRATEJİ HAM SONUÇ
# =====================================================
strategy_results = {name: [] for name in STRATEGIES}

for symbol in symbols:
    for tf_name, tf in TIMEFRAMES.items():

        df = get_data(symbol, tf_name, tf)
        if df is None or len(df) < 200:
            continue

        df = build_features(df)

        for strat_name, strat_func in STRATEGIES.items():
            try:
                if strat_func(df):
                    strategy_results[strat_name].append({
                        "SYMBOL": symbol,
                        "TIMEFRAME": tf_name,
                        "STRATEGY": strat_name,
                        "CLOSE": round(df["close"].iloc[-1], 2),
                        "RSI": round(df["RSI"].iloc[-1], 2),
                        "VWAP": round(df["VWAP"].iloc[-1], 2),
                        "EMA20": round(df["EMA20"].iloc[-1], 2),
                        "EMA50": round(df["EMA50"].iloc[-1], 2),
                        "VOLUME_RATIO": round(df["VOLUME_RATIO"].iloc[-1], 2)
                    })
            except:
                pass

# Ham çıktılar
for strat_name, data in strategy_results.items():
    print("\n"+"="*40)
    print(f"🔥 STRATEJİ HAM SONUÇ: {strat_name}")
    print("="*40)
    df_strat = pd.DataFrame(data)
    print(df_strat if not df_strat.empty else "SONUÇ YOK")

# =====================================================
# 🔟 TÜM SİNYALLERİ BİRLEŞTİR
# =====================================================
all_signals = pd.concat(
    [pd.DataFrame(v) for v in strategy_results.values()],
    ignore_index=True
)

if all_signals.empty:
    print("Hiç sinyal yok.")
else:

    # SIGNAL COUNT
    signal_count = all_signals.groupby("SYMBOL").size().reset_index(name="SIGNAL_COUNT")
    all_signals = all_signals.merge(signal_count, on="SYMBOL")

    # TF COUNT
    tf_count = all_signals.groupby("SYMBOL")["TIMEFRAME"].nunique().reset_index(name="TF_COUNT")
    all_signals = all_signals.merge(tf_count, on="SYMBOL")

    # VWAP + EMA BONUS
    all_signals["VWAP_EMA_BONUS"] = np.where(
        (all_signals["CLOSE"] > all_signals["VWAP"]) &
        (all_signals["EMA20"] > all_signals["EMA50"]),
        3,
        np.where((all_signals["CLOSE"] >= all_signals["VWAP"] * 0.99), 1, 0)
    )

    # POWER SCORE
    all_signals["POWER_SCORE"] = (
        all_signals["SIGNAL_COUNT"] * 2 +
        np.where(all_signals["RSI"].between(30,60), 2, 0) +
        np.where(all_signals["VOLUME_RATIO"] > 1, 1, 0) +
        all_signals["VWAP_EMA_BONUS"] +
        np.where(all_signals["TF_COUNT"] >= 2, 2, 0)
    )

    # AI SCORE
    all_signals["AI_SCORE"] = (
        (all_signals["POWER_SCORE"] / all_signals["POWER_SCORE"].max()) * 0.5 +
        (all_signals["RSI"] / 100) * 0.3 +
        (all_signals["VOLUME_RATIO"] / all_signals["VOLUME_RATIO"].max()) * 0.2
    )

    # KARAR
    all_signals["KARAR"] = np.where(
        (all_signals["SIGNAL_COUNT"] >= 2) &
        (all_signals["POWER_SCORE"] >= 5) &
        (all_signals["AI_SCORE"] >= 0.6),
        "DAL",
        "İZLE"
    )

    final_decision_df = (
        all_signals[all_signals["KARAR"] == "DAL"]
        .sort_values(by=["POWER_SCORE","TF_COUNT","SIGNAL_COUNT"], ascending=False)
        .drop_duplicates(subset="SYMBOL")
        .reset_index(drop=True)
    )

    print("\n🚀 CHATGPT QUANT ENGINE – SON DAL LİSTESİ 🚀")
    print(final_decision_df if not final_decision_df.empty else "DAL ÇIKMADI")


