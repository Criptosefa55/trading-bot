# =====================================================
# 1️⃣ KURULUM
# =====================================================
!pip install -q pandas numpy ta scikit-learn git+https://github.com/rongardF/tvdatafeed

# =====================================================
# 2️⃣ IMPORT
# =====================================================
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import EMAIndicator
from ta.volume import ChaikinMoneyFlowIndicator
from concurrent.futures import ThreadPoolExecutor, as_completed

tv = TvDatafeed()

# =====================================================
# 3️⃣ BIST HİSSELER
# =====================================================
symbols =  [
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
# 4️⃣ TIMEFRAME
# =====================================================
TIMEFRAMES = {
"4H": Interval.in_4_hour,
"1D": Interval.in_daily,
"1W": Interval.in_weekly
}

# =====================================================
# 5️⃣ DATA
# =====================================================
def get_data(symbol, tf):

    try:
        df = tv.get_hist(symbol, EXCHANGE, tf, 500)
        if df is None or len(df) < 200:
            return None
        return df
    except:
        return None

# =====================================================
# 6️⃣ FEATURE ENGINEERING
# =====================================================
def build_features(df):

    df = df.copy()

    df["RSI"] = RSIIndicator(df["close"],14).rsi()

    df["EMA20"] = EMAIndicator(df["close"],20).ema_indicator()
    df["EMA50"] = EMAIndicator(df["close"],50).ema_indicator()
    df["EMA200"] = EMAIndicator(df["close"],200).ema_indicator()

    bb = BollingerBands(df["close"],20,2)
    df["BB_HIGH"] = bb.bollinger_hband()
    df["BB_LOW"] = bb.bollinger_lband()
    df["BB_WIDTH"] = df["BB_HIGH"] - df["BB_LOW"]

    df["ATR"] = AverageTrueRange(
        df["high"],df["low"],df["close"],14
    ).average_true_range()

    df["VOL_MEAN"] = df["volume"].rolling(20).mean()
    df["VOLUME_RATIO"] = df["volume"] / df["VOL_MEAN"]

    df["CMF"] = ChaikinMoneyFlowIndicator(
        df["high"],df["low"],df["close"],df["volume"],20
    ).chaikin_money_flow()

    df = df.dropna()

    return df

# =====================================================
# 7️⃣ STRATEJİLER
# =====================================================

# 1️⃣ SQUEEZE PATLAMA
def strat_squeeze(df):

    cond1 = df["BB_WIDTH"].iloc[-1] < df["BB_WIDTH"].rolling(20).mean().iloc[-1]
    cond2 = df["RSI"].iloc[-1] > 50
    cond3 = df["VOLUME_RATIO"].iloc[-1] > 1

    return cond1 and cond2 and cond3


# 2️⃣ LOT TOPLAMA
def strat_lot_toplama(df):

    band = df["high"].rolling(30).max().iloc[-1] - df["low"].rolling(30).min().iloc[-1]

    cond1 = band / df["close"].iloc[-1] < 0.05
    cond2 = df["VOLUME_RATIO"].iloc[-1] < 1.2
    cond3 = df["RSI"].iloc[-1] > 45

    return cond1 and cond2 and cond3


# 3️⃣ HACİM PATLAMASI
def strat_volume(df):

    cond1 = df["VOLUME_RATIO"].iloc[-1] > 2
    cond2 = df["RSI"].iloc[-1] > 60
    cond3 = df["CMF"].iloc[-1] > 0

    return cond1 and cond2 and cond3


# 4️⃣ TREND DEVAMI
def strat_trend(df):

    cond1 = df["EMA50"].iloc[-1] > df["EMA200"].iloc[-1]
    cond2 = df["close"].iloc[-1] > df["EMA20"].iloc[-1]
    cond3 = df["RSI"].iloc[-1] > 50

    return cond1 and cond2 and cond3


# 5️⃣ TAVAN ADAYI
def strat_tavan(df):

    cond1 = df["BB_WIDTH"].iloc[-1] < df["BB_WIDTH"].rolling(30).mean().iloc[-1]
    cond2 = df["VOLUME_RATIO"].iloc[-1] > 2
    cond3 = df["RSI"].iloc[-1] > 55
    cond4 = df["close"].iloc[-1] > df["EMA20"].iloc[-1]

    return cond1 and cond2 and cond3 and cond4


STRATEGIES = {
"SQUEEZE": strat_squeeze,
"LOT_TOPLAMA": strat_lot_toplama,
"HACIM_PATLAMASI": strat_volume,
"TREND_DEVAMI": strat_trend,
"TAVAN_ADAYI": strat_tavan
}

# =====================================================
# 8️⃣ TARAMA
# =====================================================
def process_symbol(symbol):

    results = []

    for tf_name, tf in TIMEFRAMES.items():

        df = get_data(symbol, tf)

        if df is None:
            continue

        df = build_features(df)

        for strat_name, strat_func in STRATEGIES.items():

            try:

                if strat_func(df):

                    results.append({
                        "SYMBOL":symbol,
                        "TIMEFRAME":tf_name,
                        "STRATEGY":strat_name,
                        "CLOSE":round(df["close"].iloc[-1],2),
                        "RSI":round(df["RSI"].iloc[-1],2),
                        "VOLUME_RATIO":round(df["VOLUME_RATIO"].iloc[-1],2)
                    })

            except:
                pass

    return results

strategy_results = {name: [] for name in STRATEGIES}

with ThreadPoolExecutor(max_workers=20) as executor:

    futures = {executor.submit(process_symbol, sym): sym for sym in symbols}

    for future in as_completed(futures):

        res = future.result()

        for r in res:
            strategy_results[r["STRATEGY"]].append(r)

# =====================================================
# 9️⃣ STRATEJİ SONUÇLARI
# =====================================================
for strat, data in strategy_results.items():

    df = pd.DataFrame(data)

    print("\n"+"="*60)
    print(f"🔥 {strat} SONUÇ")
    print("="*60)

    if df.empty:
        print("Sonuç yok")
    else:
        print(df)

# =====================================================
# 🔟 MEGA HİSSELER
# =====================================================

all_df = pd.concat([pd.DataFrame(v) for v in strategy_results.values()],ignore_index=True)

if not all_df.empty:

    mega = all_df.groupby("SYMBOL").size().reset_index(name="COUNT")

    mega = mega.sort_values("COUNT",ascending=False)

    print("\n"+"="*60)
    print("🚀 MEGA HİSSELER (Birden fazla strateji)")
    print("="*60)

    print(mega.head(10))