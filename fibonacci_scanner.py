import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import time

tv = TvDatafeed()

hisseler = [    'BIST:BINHO', 'BIST:AVOD', 'BIST:A1CAP', 'BIST:ACSEL', 'BIST:ADEL', 'BIST:ADESE', 'BIST:ADGYO',
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
    'BIST:IHLAS']  # Listeyi kendin doldur

intervals = {
    '4H': Interval.in_4_hour,
    'Daily': Interval.in_daily,
    'Weekly': Interval.in_weekly
}

def fibonacci_levels(df, lookback=150):
    highestHigh = df['high'].rolling(window=lookback).max().iloc[-1]
    lowestLow = df['low'].rolling(window=lookback).min().iloc[-1]
    diff = highestHigh - lowestLow

    levels = {
        'fib_0': lowestLow,
        'fib_100': highestHigh,
        'fib_neg_38_2': lowestLow - diff * 0.382,
        'fib_neg_23_6': lowestLow - diff * 0.236,
        'fib_23_6': lowestLow + diff * 0.236,
        'fib_38_2': lowestLow + diff * 0.382,
        'fib_50': lowestLow + diff * 0.5,
        'fib_61_8': lowestLow + diff * 0.618,
        'fib_78_6': lowestLow + diff * 0.786,
        'fib_127_2': highestHigh + diff * 0.272,
        'fib_141_4': highestHigh + diff * 0.414,
        'fib_161_8': highestHigh + diff * 0.618
    }
    return levels

tolerance = 0.01  # %1 tolerans

# Periyotlara göre sonuçları tutacak dict
results_dict = {
    '4H': [],
    'Daily': [],
    'Weekly': []
}

for hisse in hisseler:
    for interval_name, interval_val in intervals.items():
        try:
            df = tv.get_hist(symbol=hisse, exchange='BIST', interval=interval_val, n_bars=200)
            if df is None or df.empty:
                continue

            fibs = fibonacci_levels(df, lookback=150)
            last_close = df['close'].iloc[-1]

            fib_0 = fibs['fib_0']
            alt = fib_0 * (1 - tolerance)
            ust = fib_0 * (1 + tolerance)

            if alt <= last_close <= ust:
                results_dict[interval_name].append({
                    'Hisse': hisse,
                    'Fibo Seviyesi': 'fib_0 (Dip)',
                    'Seviye Değeri': round(fib_0, 3),
                    'Son Kapanış': round(last_close, 3),
                    'Durum': 'Dip Fibo Teması'
                })

            time.sleep(3)  # API limitleri için bekle

        except Exception as e:
            print(f"{hisse} {interval_name} hata: {e}")
            continue

# Her periyot için ayrı DataFrame ve yazdırma
for period, data in results_dict.items():
    df_res = pd.DataFrame(data)
    print(f"\n===== {period} Periyot Fibonacci Teması =====")
    if not df_res.empty:
        print(df_res)
    else:
        print("Temas eden hisse yok.")
