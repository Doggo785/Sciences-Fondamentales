
import csv
import os
from statistics import mean, median, stdev
import math

def quantiles(data):
    data = sorted(data)
    n = len(data)
    def q(p):
        idx = p * (n - 1)
        i, f = int(idx), idx - int(idx)
        if i + 1 < n:
            return data[i] + f * (data[i+1] - data[i])
        return data[i]
    return q(0.25), q(0.5), q(0.75)

def boxplot_stats(data):
    q1, med, q3 = quantiles(data)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = [x for x in data if x < lower or x > upper]
    return {
        'Q1': q1,
        'Median': med,
        'Q3': q3,
        'IQR': iqr,
        'Min': min(data),
        'Max': max(data),
        'Lower whisker': min([x for x in data if x >= lower]),
        'Upper whisker': max([x for x in data if x <= upper]),
        'Outliers': outliers
    }

def pearson_corr(x, y):
    n = len(x)
    if n < 2:
        return float('nan')
    mx, my = mean(x), mean(y)
    num = sum((a-mx)*(b-my) for a, b in zip(x, y))
    den = math.sqrt(sum((a-mx)**2 for a in x) * sum((b-my)**2 for b in y))
    return num / den if den else float('nan')

def normality_test(data):
    # Test visuel : rapport écart-type/moyenne, symétrie, kurtosis
    m = mean(data)
    s = stdev(data)
    med = median(data)
    q1, _, q3 = quantiles(data)
    skew = (m - med) / s if s else 0
    kurt = sum((x-m)**4 for x in data) / (len(data)*s**4) if s else 0
    return {
        'mean': m,
        'stdev': s,
        'skewness': skew,
        'kurtosis': kurt,
        'symmetry': abs(skew) < 0.5,
        'bell-shaped': kurt > 2 and kurt < 4
    }

def select_best_days(csv_path, top_n=10):
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        days = []
        for row in reader:
            cnt = int(row['cnt'])
            weathersit = int(row['weathersit'])
            workingday = int(row['workingday'])
            temp = float(row['temp'])
            atemp = float(row['atemp'])
            hum = float(row['hum'])
            windspeed = float(row['windspeed'])
            dteday = row['dteday']
            score = cnt
            if weathersit == 1:
                score += 500
            if workingday == 0:
                score += 300
            days.append({
                'date': dteday,
                'cnt': cnt,
                'weathersit': weathersit,
                'workingday': workingday,
                'temp': temp,
                'atemp': atemp,
                'hum': hum,
                'windspeed': windspeed,
                'score': score
            })

    best_days = sorted(days, key=lambda x: x['score'], reverse=True)[:top_n]
    print("\n" + "="*60)
    print(f"  TOP {top_n} JOURS OPTIMAUX POUR OUVRIR BIKESURFING")
    print("="*60)
    print(f"{'Rang':<5} {'Date':<12} {'Locations':<10} {'Météo':<8} {'Week-end/férié':<15}")
    print("-"*60)
    for i, day in enumerate(best_days, 1):
        meteo = {1: 'Beau', 2: 'Nuageux', 3: 'Pluie/Neige'}.get(day['weathersit'], str(day['weathersit']))
        wknd = 'Oui' if day['workingday']==0 else 'Non'
        print(f"{i:<5} {day['date']:<12} {day['cnt']:<10} {meteo:<8} {wknd:<15}")
    print("-"*60)
    print("Critères : score = locations + bonus météo + bonus week-end/férié")
    print("(Météo: 1=beau, 2=nuageux, 3=pluie/neige)")

    cnts = [d['cnt'] for d in days]
    print("\n" + "="*60)
    print("  STATISTIQUES GLOBALES SUR LES LOCATIONS/JOUR")
    print("="*60)
    print(f"{'Moyenne':<15}: {mean(cnts):.2f}")
    print(f"{'Médiane':<15}: {median(cnts):.2f}")
    print(f"{'Écart-type':<15}: {stdev(cnts):.2f}")
    q1, med, q3 = quantiles(cnts)
    print(f"{'Quantile Q1':<15}: {q1:.2f}")
    print(f"{'Quantile Q3':<15}: {q3:.2f}")
    print(f"{'Étendue':<15}: {min(cnts)} à {max(cnts)}")

    box = boxplot_stats(cnts)
    print("\n" + "="*60)
    print("  BOÎTE À MOUSTACHE (locations/jour)")
    print("="*60)
    for k, v in box.items():
        if isinstance(v, float):
            print(f"{k:<15}: {v:.2f}")
        else:
            print(f"{k:<15}: {v}")

    print("\n" + "="*60)
    print("  CORRÉLATION LINÉAIRE AVEC LES VARIABLES")
    print("="*60)
    for var in ['temp', 'atemp', 'hum', 'windspeed', 'weathersit', 'workingday']:
        vals = [d[var] for d in days]
        corr = pearson_corr(cnts, vals)
        print(f"cnt vs {var:<10}: {corr:.3f}")

    print("\n" + "="*60)
    print("  TEST DE NORMALITÉ (locations/jour)")
    print("="*60)
    norm = normality_test(cnts)
    for k, v in norm.items():
        print(f"{k:<15}: {v}")

if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), 'dataset', 'day.csv')
    select_best_days(base, top_n=10)
