import os
import argparse
from typing import Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def detect_zscore(series: pd.Series, thresh: float = 3.0) -> pd.Series:
    z = np.abs(stats.zscore(series.ffill()))
    return pd.Series(z > thresh, index=series.index)


def detect_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    return (series < lower) | (series > upper)


def detect_percent_of_max(series: pd.Series, pct: float = 0.9) -> pd.Series:
    # Marks points above pct * max as anomalies
    return series > (series.max() * pct)


def detect_mad(series: pd.Series, thresh: float = 3.5) -> pd.Series:
    # Median Absolute Deviation based detection (robust)
    med = series.median()
    mad = np.median(np.abs(series - med))
    if mad == 0:
        return pd.Series(False, index=series.index)
    modified_z = 0.6745 * (series - med) / mad
    return np.abs(modified_z) > thresh


def plot_series_with_anomalies(series: pd.Series, anomalies: pd.Series, title: str, out_path: str):
    plt.figure(figsize=(14, 5))
    sns.lineplot(x=series.index, y=series.values, label=title)
    if anomalies.any():
        sns.scatterplot(x=series.index[anomalies], y=series[anomalies], color='red', label='Anomalies')
    plt.xlabel('Time')
    plt.ylabel(title)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def analyze_server_data(file_path: str, output_dir: str = 'output') -> None:
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(file_path)
    df['Time'] = pd.to_datetime(df['Time'])
    df.set_index('Time', inplace=True)

    metrics = ['CPU_Usage', 'Memory_Usage', 'Network_Usage', 'Temperature']

    desc = df[metrics].describe()
    print("Statistiques descriptives :")
    print(desc)

    results = {}

    for metric in metrics:
        series = df[metric].copy()

        # Apply detectors
        z_anom = detect_zscore(series)
        iqr_anom = detect_iqr(series)
        pct_anom = detect_percent_of_max(series, pct=0.95)
        mad_anom = detect_mad(series)

        # Combine: mark as anomaly if any detector triggers
        combined = z_anom | iqr_anom | pct_anom | mad_anom

        results[metric] = {
            'count': int(combined.sum()),
            'percent': float(combined.sum()) / len(series) * 100.0,
            'z_count': int(z_anom.sum()),
            'iqr_count': int(iqr_anom.sum()),
            'pct_count': int(pct_anom.sum()),
            'mad_count': int(mad_anom.sum()),
        }

        # Plot time series and anomalies
        out_file = os.path.join(output_dir, f'{metric}.png')
        plot_series_with_anomalies(series, combined, metric, out_file)

        # Also save a histogram with anomaly overlay
        plt.figure(figsize=(8, 4))
        sns.histplot(series, bins=50, kde=True)
        if combined.any():
            sns.rugplot(series[combined], color='red')
        plt.title(f'Histogramme de {metric}')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'{metric}_hist.png'))
        plt.close()

    # Print summary report
    print('\nRésumé détection d\'anomalies :')
    for m, r in results.items():
        print(f"- {m}: {r['count']} anomalies ({r['percent']:.2f}%). Détails: z={r['z_count']}, iqr={r['iqr_count']}, pct={r['pct_count']}, mad={r['mad_count']}")


def main():
    parser = argparse.ArgumentParser(description='Analyse et détection d\'anomalies sur server_usage_data.csv')
    parser.add_argument('--file', '-f', default='dataset/server_usage_data.csv', help='Chemin vers le fichier CSV')
    parser.add_argument('--out', '-o', default='output', help='Dossier de sortie pour les graphiques')
    args = parser.parse_args()

    analyze_server_data(args.file, args.out)


if __name__ == '__main__':
    main()
