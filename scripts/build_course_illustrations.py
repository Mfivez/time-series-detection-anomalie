#!/usr/bin/env python3
"""Génère les illustrations PNG statiques des jours 2 et 3."""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from prophet import Prophet
from sklearn.ensemble import IsolationForest

from build_day1_illustrations import (
    BG,
    BLUE,
    GREEN,
    GRID,
    INK,
    MUTED,
    ORANGE,
    PURPLE,
    RED,
    ROOT,
    TEAL,
    rounded_box,
    save,
    style_axis,
)


DAY_2 = ROOT / "assets" / "jour_02"
DAY_3 = ROOT / "assets" / "jour_03"
CLEAN_DATASET = ROOT / "datasets" / "prepared" / "iot_hvac_clean.csv"
LABELED_DATASET = ROOT / "datasets" / "prepared" / "iot_hvac_labeled.csv"


def save2(fig: plt.Figure, filename: str) -> None:
    save(fig, filename, DAY_2)


def save3(fig: plt.Figure, filename: str) -> None:
    save(fig, filename, DAY_3)


def arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float], color: str = MUTED) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=2.2,
            color=color,
        )
    )


def load_clean_hourly() -> pd.DataFrame:
    df = pd.read_csv(CLEAN_DATASET)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df.set_index("timestamp").select_dtypes("number").resample("1h").mean()


def load_labeled() -> pd.DataFrame:
    df = pd.read_csv(LABELED_DATASET)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df.set_index("timestamp").sort_index()


# ---------------------------------------------------------------------------
# Jour 2 — forecasting


def day2_baseline_concept() -> None:
    hours = np.arange(72)
    actual = 2.4 + 1.1 * np.sin(2 * np.pi * (hours - 7) / 24) + 0.15 * np.sin(2 * np.pi * hours / 8)
    split = 48
    persistence = np.full(24, actual[split - 1])
    seasonal = actual[24:48]

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.6), sharey=True)
    fig.suptitle("Une baseline est une règle simple à battre", fontsize=23, weight="bold")
    for ax in axes:
        ax.plot(hours[:split], actual[:split], color=INK, linewidth=2, label="passé connu")
        ax.plot(hours[split:], actual[split:], color="#94A3B8", linewidth=2.5, label="réel futur")
        ax.axvline(split - 0.5, color=MUTED, linestyle="--", linewidth=2)
        ax.axvspan(split - 0.5, 71.5, color="#FFF7E6", alpha=0.7)
        ax.set_xlabel("Temps")
        ax.set_ylabel("Puissance (kW)")
        style_axis(ax)
    axes[0].plot(hours[split:], persistence, color=RED, linewidth=3, label="persistance")
    axes[0].set_title("Persistance : garder la dernière valeur", weight="bold")
    axes[1].plot(hours[split:], seasonal, color=BLUE, linewidth=3, label="motif de la veille")
    axes[1].set_title("Saisonnier : répéter le dernier motif", weight="bold")
    for ax in axes:
        ax.legend(loc="upper left")
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    save2(fig, "01_baseline_persistance_saisonniere.png")


def day2_mae_rmse() -> None:
    labels = ["erreur 1", "erreur 2", "erreur 3", "grande erreur"]
    errors = np.array([0.5, 0.5, 0.5, 3.0])
    mae = errors.mean()
    mse = np.mean(errors**2)
    rmse = np.sqrt(mse)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8))
    fig.suptitle("MAE et RMSE ne réagissent pas pareil aux grandes erreurs", fontsize=22, weight="bold")
    axes[0].bar(labels, errors, color=[BLUE, BLUE, BLUE, ORANGE])
    axes[0].axhline(mae, color=TEAL, linestyle="--", linewidth=3, label=f"MAE = {mae:.2f}")
    axes[0].set_title("MAE : chaque écart garde sa taille", weight="bold")
    axes[0].set_ylabel("Erreur absolue")
    axes[0].legend()

    axes[1].bar(labels, errors**2, color=[BLUE, BLUE, BLUE, RED])
    axes[1].axhline(
        mse,
        color=PURPLE,
        linestyle="--",
        linewidth=3,
        label=f"MSE = {mse:.2f} → RMSE = {rmse:.2f}",
    )
    axes[1].set_title("RMSE : la grande erreur est davantage pénalisée", weight="bold")
    axes[1].set_ylabel("Erreur mise au carré")
    axes[1].legend()
    for ax in axes:
        ax.tick_params(axis="x", rotation=18)
        style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    save2(fig, "01_mae_et_rmse.png")


def day2_real_baselines(hourly: pd.DataFrame) -> None:
    power = hourly["power_kw"]
    cutoff = power.index.max() - pd.DateOffset(days=7)
    train = power.loc[power.index <= cutoff]
    test = power.loc[power.index > cutoff]
    persistence = pd.Series(train.iloc[-1], index=test.index)
    seasonal = pd.Series(np.resize(train.iloc[-168:].to_numpy(), len(test)), index=test.index)

    fig, ax = plt.subplots(figsize=(14, 6))
    fig.suptitle("Deux baselines confrontées au même futur", fontsize=22, weight="bold")
    ax.plot(test.index, test, color=INK, linewidth=2.5, label="réel")
    ax.plot(test.index, persistence, color=RED, linewidth=2, label="persistance")
    ax.plot(test.index, seasonal, color=BLUE, linewidth=2, alpha=0.9, label="semaine précédente")
    ax.set_ylabel("Puissance (kW)")
    ax.set_xlabel("Période de test")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.legend(ncol=3)
    style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    save2(fig, "01_baselines_sur_donnees_reelles.png")


def day2_prophet_format() -> None:
    fig, ax = plt.subplots(figsize=(15, 6.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.suptitle("Prophet attend une date ds et une valeur y", fontsize=23, weight="bold")

    input_rows = [["10:00", "2.1"], ["11:00", "2.4"], ["12:00", "3.5"], ["13:00", "3.4"]]
    output_rows = [["14:00", "3.2"], ["15:00", "3.0"], ["16:00", "2.8"]]
    table_in = ax.table(cellText=input_rows, colLabels=["ds", "y"], cellLoc="center", bbox=[0.03, 0.18, 0.27, 0.58])
    table_out = ax.table(cellText=output_rows, colLabels=["ds", "yhat"], cellLoc="center", bbox=[0.70, 0.23, 0.27, 0.48])
    for table, color in [(table_in, BLUE), (table_out, ORANGE)]:
        table.auto_set_font_size(False)
        table.set_fontsize(13)
        for (row, _column), cell in table.get_celld().items():
            cell.set_edgecolor("white")
            cell.set_facecolor(color if row == 0 else ("#F1F5F9" if row % 2 else "white"))
            if row == 0:
                cell.set_text_props(color="white", weight="bold")
    rounded_box(ax, 0.40, 0.30, 0.20, 0.32, "PROPHET", "tendance +\nsaisonnalités", PURPLE)
    arrow(ax, (0.31, 0.47), (0.39, 0.47))
    arrow(ax, (0.61, 0.47), (0.69, 0.47))
    ax.text(0.165, 0.82, "Passé pour apprendre", ha="center", weight="bold", color=BLUE, fontsize=14)
    ax.text(0.835, 0.77, "Dates futures à prévoir", ha="center", weight="bold", color=ORANGE, fontsize=14)
    ax.text(0.5, 0.12, "yhat est la valeur prévue ; elle devra ensuite être comparée à la vraie valeur.", ha="center", fontsize=13)
    save2(fig, "02_format_prophet_ds_y.png")


def day2_prophet_components() -> None:
    x = np.linspace(0, 14, 14 * 8)
    trend = 2.0 + 0.025 * x
    daily = 0.75 * np.sin(2 * np.pi * (x - 0.3))
    weekly = 0.25 * np.sin(2 * np.pi * x / 7)
    total = trend + daily + weekly
    fig, axes = plt.subplots(4, 1, figsize=(14, 8), sharex=True)
    fig.suptitle("Intuition : Prophet additionne plusieurs composantes", fontsize=22, weight="bold")
    items = [
        (trend, "Tendance : évolution lente", BLUE),
        (daily, "Saisonnalité journalière : motif au sein d'une journée", TEAL),
        (weekly, "Saisonnalité hebdomadaire : différences selon les jours", PURPLE),
        (total, "Prévision = tendance + saisonnalités", ORANGE),
    ]
    for ax, (values, title, color) in zip(axes, items):
        ax.plot(x, values, color=color, linewidth=2.4)
        ax.set_title(title, loc="left", weight="bold", fontsize=14)
        style_axis(ax)
    axes[-1].set_xlabel("Temps (jours)")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    save2(fig, "02_composantes_prophet.png")


def prepare_prophet(hourly: pd.DataFrame) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    power = hourly["power_kw"]
    cutoff = power.index.max() - pd.DateOffset(days=7)
    train = power.loc[power.index <= cutoff]
    test = power.loc[power.index > cutoff]
    prophet_train = train.rename_axis("ds").rename("y").reset_index()
    prophet_train["ds"] = prophet_train["ds"].dt.tz_localize(None)
    logging.getLogger("cmdstanpy").setLevel(logging.WARNING)
    model = Prophet(daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=False, uncertainty_samples=0)
    model.fit(prophet_train)
    all_dates = pd.DataFrame({"ds": power.index.tz_localize(None)})
    prediction = model.predict(all_dates)["yhat"].to_numpy()
    predicted_all = pd.Series(prediction, index=power.index)
    return train, test, predicted_all.loc[train.index], predicted_all.loc[test.index]


def day2_prophet_forecast(train: pd.Series, test: pd.Series, predicted: pd.Series) -> None:
    view_train = train.loc[train.index >= train.index.max() - pd.DateOffset(days=3)]
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.suptitle("Le test simule les valeurs futures que Prophet n'a pas vues", fontsize=22, weight="bold")
    ax.plot(view_train.index, view_train, color=MUTED, linewidth=2, label="passé d'entraînement")
    ax.plot(test.index, test, color=INK, linewidth=2.4, label="réel futur")
    ax.plot(predicted.index, predicted, color=BLUE, linewidth=2.4, label="prévision Prophet")
    ax.axvline(test.index.min(), color=ORANGE, linestyle="--", linewidth=2.5, label="frontière")
    ax.axvspan(test.index.min(), test.index.max(), color="#FFF7E6", alpha=0.45)
    ax.set_ylabel("Puissance (kW)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.legend(ncol=2)
    style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    save2(fig, "02_prevision_prophet.png")


def day2_residual(test: pd.Series, predicted: pd.Series) -> None:
    real = test.iloc[:48]
    forecast = predicted.reindex(real.index)
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.suptitle("Le résidu est l'écart entre l'observation et la prévision", fontsize=22, weight="bold")
    ax.plot(real.index, real, color=INK, linewidth=2.5, marker="o", markersize=3, label="observé")
    ax.plot(forecast.index, forecast, color=BLUE, linewidth=2.5, label="prévu")
    selected = np.arange(3, len(real), 8)
    for index in selected:
        ax.vlines(real.index[index], forecast.iloc[index], real.iloc[index], color=RED, linewidth=2.5)
    ax.text(0.02, 0.08, "traits rouges = résidus", transform=ax.transAxes, color=RED, weight="bold", fontsize=13)
    ax.set_ylabel("Puissance (kW)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m\n%Hh"))
    ax.legend()
    style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    save2(fig, "03_residu_observe_prevu.png")


def day2_error_threshold(train: pd.Series, train_pred: pd.Series, test: pd.Series, test_pred: pd.Series) -> None:
    train_errors = (train - train_pred).abs()
    threshold = train_errors.quantile(0.99)
    errors = (test - test_pred).abs()
    flags = errors > threshold
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.suptitle("Une grande erreur devient une alerte lorsqu'elle dépasse le seuil", fontsize=22, weight="bold")
    ax.plot(errors.index, errors, color=BLUE, linewidth=1.8, label="erreur absolue")
    ax.axhline(threshold, color=ORANGE, linestyle="--", linewidth=3, label="seuil appris sur le passé")
    ax.scatter(errors.index[flags], errors.loc[flags], color=RED, s=35, zorder=4, label="alertes")
    ax.fill_between(errors.index, threshold, errors.max() * 1.05, color="#FEE2E2", alpha=0.45)
    ax.set_ylabel("Erreur absolue (kW)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.legend(ncol=3)
    style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    save2(fig, "03_erreur_seuil_alerte.png")


def day2_precision_recall() -> None:
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.suptitle("Précision et rappel répondent à deux questions différentes", fontsize=22, weight="bold")
    columns = [(0.31, "ALERTE"), (0.65, "PAS D'ALERTE")]
    rows = [(0.57, "ANOMALIE RÉELLE"), (0.27, "COMPORTEMENT NORMAL")]
    for x, label in columns:
        ax.text(x + 0.13, 0.82, label, ha="center", weight="bold", fontsize=14)
    for y, label in rows:
        ax.text(0.16, y + 0.11, label, ha="center", va="center", weight="bold", fontsize=12)
    cells = [
        (0.31, 0.57, "VRAI POSITIF", "bonne alerte", GREEN),
        (0.65, 0.57, "FAUX NÉGATIF", "anomalie manquée", RED),
        (0.31, 0.27, "FAUX POSITIF", "fausse alerte", ORANGE),
        (0.65, 0.27, "VRAI NÉGATIF", "silence correct", BLUE),
    ]
    for x, y, title, detail, color in cells:
        rounded_box(ax, x, y, 0.26, 0.22, title, detail, color)
    ax.text(0.44, 0.12, "PRÉCISION : parmi les alertes, combien sont justes ?", ha="center", color=ORANGE, weight="bold", fontsize=13)
    ax.text(0.44, 0.055, "RAPPEL : parmi les anomalies, combien sont détectées ?", ha="center", color=RED, weight="bold", fontsize=13)
    save2(fig, "03_precision_et_rappel.png")


def day2_challenge_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.suptitle("Le protocole complet du forecasting", fontsize=23, weight="bold")
    steps = [
        ("1 · DÉCOUPER", "passé / futur", BLUE),
        ("2 · BASELINE", "règle à battre", TEAL),
        ("3 · PROPHET", "apprendre les motifs", PURPLE),
        ("4 · MESURER", "MAE et RMSE", ORANGE),
        ("5 · EXPLIQUER", "grandes erreurs", GREEN),
    ]
    xs = np.linspace(0.03, 0.81, len(steps))
    for index, ((title, detail, color), x) in enumerate(zip(steps, xs)):
        rounded_box(ax, x, 0.34, 0.16, 0.32, title, detail, color)
        if index < len(steps) - 1:
            arrow(ax, (x + 0.162, 0.50), (xs[index + 1] - 0.008, 0.50))
    ax.text(0.5, 0.20, "Même période de test, mêmes métriques : la comparaison devient honnête.", ha="center", fontsize=14, weight="bold")
    save2(fig, "04_pipeline_forecasting.png")


# ---------------------------------------------------------------------------
# Jour 3 — anomalies et maintenance prédictive


def day3_anomaly_types() -> None:
    rng = np.random.default_rng(3)
    x = np.arange(80)
    base = 1.0 + 0.06 * np.sin(x / 5) + rng.normal(0, 0.025, len(x))
    point = base.copy()
    point[45] = 2.1
    contextual = base.copy()
    contextual[15:22] += 0.7
    drift = base.copy()
    drift[40:] += np.linspace(0, 1.0, 40)

    fig, axes = plt.subplots(2, 2, figsize=(14, 8), sharex=True)
    fig.suptitle("Une anomalie peut prendre plusieurs formes", fontsize=23, weight="bold")
    items = [
        (base, "Comportement habituel", GREEN, None),
        (point, "Pic ponctuel", RED, 45),
        (contextual, "Valeur inhabituelle dans ce contexte", ORANGE, slice(15, 22)),
        (drift, "Dérive progressive", PURPLE, slice(40, 80)),
    ]
    for ax, (values, title, color, highlight) in zip(axes.flat, items):
        ax.plot(x, values, color=BLUE, linewidth=2)
        if isinstance(highlight, int):
            ax.scatter([highlight], [values[highlight]], color=color, s=90, zorder=3)
        elif isinstance(highlight, slice):
            ax.plot(x[highlight], values[highlight], color=color, linewidth=3)
            ax.axvspan(highlight.start, highlight.stop - 1, color=f"{color}18")
        ax.set_title(title, color=color, weight="bold")
        ax.set_ylabel("Signal")
        style_axis(ax)
    axes[1, 0].set_xlabel("Temps")
    axes[1, 1].set_xlabel("Temps")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    save3(fig, "01_formes_anomalies.png")


def day3_threshold_and_zscore() -> None:
    rng = np.random.default_rng(8)
    x = np.arange(70)
    signal = 1.0 + 0.12 * np.sin(x / 7) + rng.normal(0, 0.04, len(x))
    signal[55] = 1.75
    rolling = pd.Series(signal).shift(1).rolling(20, min_periods=8)
    mean = rolling.mean()
    std = rolling.std()

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.8))
    fig.suptitle("Deux références : une limite métier ou le comportement récent", fontsize=22, weight="bold")
    axes[0].plot(x, signal, color=BLUE, linewidth=2)
    axes[0].axhline(1.5, color=RED, linestyle="--", linewidth=3, label="seuil métier")
    axes[0].scatter([55], [signal[55]], color=RED, s=90, zorder=3)
    axes[0].set_title("Seuil fixe : la limite est connue", weight="bold")
    axes[0].legend()

    axes[1].plot(x, signal, color=BLUE, linewidth=2, label="mesure")
    axes[1].plot(x, mean, color=TEAL, linewidth=2.5, label="moyenne du passé")
    axes[1].fill_between(x, mean - 3 * std, mean + 3 * std, color="#CCFBF1", alpha=0.8, label="zone habituelle")
    axes[1].scatter([55], [signal[55]], color=RED, s=90, zorder=3)
    axes[1].set_title("Z-score mobile : la référence évolue", weight="bold")
    axes[1].legend()
    for ax in axes:
        ax.set_xlabel("Temps")
        ax.set_ylabel("Vibration")
        style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    save3(fig, "01_seuil_metier_et_zscore.png")


def day3_isolation_forest_intuition() -> None:
    rng = np.random.default_rng(42)
    normal = rng.normal([21.5, 1.0], [0.8, 0.12], size=(170, 2))
    anomalies = np.array([[25.0, 2.0], [18.4, 1.8], [24.6, 0.55], [19.0, 2.25], [26.0, 1.45]])
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.suptitle("Isolation Forest cherche les points faciles à isoler", fontsize=22, weight="bold")
    ax.scatter(normal[:, 0], normal[:, 1], color=BLUE, alpha=0.6, s=35, label="comportements fréquents")
    ax.scatter(anomalies[:, 0], anomalies[:, 1], color=RED, edgecolor="white", linewidth=1.5, s=110, label="combinaisons isolées")
    ax.axvline(24.0, color=ORANGE, linestyle="--", linewidth=2)
    ax.axhline(1.55, color=ORANGE, linestyle="--", linewidth=2)
    ax.text(24.1, 0.7, "quelques coupures\nsuffisent à isoler\nces points", color=RED, weight="bold", fontsize=13)
    ax.set_xlabel("Température (°C)")
    ax.set_ylabel("Vibration (mm/s)")
    ax.legend()
    style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    save3(fig, "02_isolation_forest_intuition.png")


def prepare_iforest(df: pd.DataFrame) -> pd.DataFrame:
    features = ["temperature_c", "humidity_pct", "power_kw", "pressure_bar", "vibration_mm_s"]
    train_end = df.index.min() + pd.DateOffset(days=28)
    normal_train = df.loc[(df.index < train_end) & (df["is_anomaly"] == 0), features]
    detector = IsolationForest(n_estimators=200, contamination=0.02, random_state=42, n_jobs=1)
    detector.fit(normal_train)
    result = df.copy()
    result["anomaly_score"] = -detector.decision_function(result[features])
    result["iforest_flag"] = (detector.predict(result[features]) == -1).astype(int)
    return result.loc[result.index >= train_end]


def day3_iforest_score(test: pd.DataFrame) -> None:
    start = test.index.max() - pd.DateOffset(days=14)
    view = test.loc[test.index >= start]
    flagged = view["iforest_flag"] == 1
    fig, axes = plt.subplots(2, 1, figsize=(14, 7), sharex=True)
    fig.suptitle("Le score multivarié devient une alerte après seuillage", fontsize=22, weight="bold")
    axes[0].plot(view.index, view["vibration_mm_s"], color=BLUE, linewidth=1.6)
    axes[0].scatter(view.index[flagged], view.loc[flagged, "vibration_mm_s"], color=RED, s=22, label="alertes")
    axes[0].set_ylabel("Vibration")
    axes[0].set_title("Signal physique", loc="left", weight="bold")
    axes[0].legend()
    axes[1].plot(view.index, view["anomaly_score"], color=PURPLE, linewidth=1.5)
    axes[1].scatter(view.index[flagged], view.loc[flagged, "anomaly_score"], color=RED, s=22)
    axes[1].axhline(0, color=ORANGE, linestyle="--", linewidth=2, label="frontière de décision")
    axes[1].set_ylabel("Score d'étrangeté")
    axes[1].set_title("Score produit par Isolation Forest", loc="left", weight="bold")
    axes[1].legend()
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    for ax in axes:
        style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    save3(fig, "02_score_isolation_forest.png")


def day3_maintenance_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.suptitle("Une anomalie utile doit devenir une action contextualisée", fontsize=22, weight="bold")
    steps = [
        ("SCORE", "degré d'étrangeté", PURPLE),
        ("REGROUPER", "éviter les doublons", BLUE),
        ("CONTEXTE", "machine, durée, capteurs", TEAL),
        ("SÉVÉRITÉ", "à surveiller → critique", ORANGE),
        ("ACTION", "inspection planifiée", GREEN),
    ]
    xs = np.linspace(0.03, 0.81, len(steps))
    for index, ((title, detail, color), x) in enumerate(zip(steps, xs)):
        rounded_box(ax, x, 0.36, 0.16, 0.30, title, detail, color)
        if index < len(steps) - 1:
            arrow(ax, (x + 0.162, 0.51), (xs[index + 1] - 0.008, 0.51))
    ax.text(0.5, 0.21, "Le technicien confirme le diagnostic et enrichit le retour terrain.", ha="center", fontsize=14, weight="bold")
    save3(fig, "02_anomalie_vers_maintenance.png")


def day3_neuron_learning() -> None:
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.suptitle("Le minimum du Deep Learning : ajuster des poids pour réduire une erreur", fontsize=21, weight="bold")
    inputs = [(0.10, 0.68, "température"), (0.10, 0.50, "puissance"), (0.10, 0.32, "vibration")]
    for x, y, label in inputs:
        circle = Circle((x, y), 0.06, facecolor="#EAF2FF", edgecolor=BLUE, linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, label, ha="center", va="center", fontsize=10.5)
        arrow(ax, (x + 0.065, y), (0.40, 0.50), BLUE)
    neuron = Circle((0.48, 0.50), 0.11, facecolor="#F3E8FF", edgecolor=PURPLE, linewidth=3)
    ax.add_patch(neuron)
    ax.text(0.48, 0.50, "combinaison\npondérée +\nactivation", ha="center", va="center", weight="bold", fontsize=11)
    arrow(ax, (0.595, 0.50), (0.73, 0.50), PURPLE)
    rounded_box(ax, 0.74, 0.39, 0.18, 0.22, "SORTIE", "prédiction", ORANGE)
    ax.text(0.50, 0.18, "LOSS : écart entre la sortie et la valeur attendue", ha="center", color=RED, fontsize=14, weight="bold")
    ax.plot([0.83, 0.83, 0.48], [0.38, 0.24, 0.24], color=RED, linewidth=2.5)
    arrow(ax, (0.48, 0.24), (0.48, 0.38), RED)
    ax.text(0.66, 0.275, "l'optimiseur corrige les poids", ha="center", color=RED, fontsize=11)
    save3(fig, "03_neurone_poids_loss.png")


def day3_autoencoder_architecture() -> None:
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.suptitle("L'autoencoder apprend à reconstruire un comportement normal", fontsize=22, weight="bold")
    layers = [
        (0.08, 5, "MESURES", BLUE),
        (0.29, 3, "ENCODER", TEAL),
        (0.50, 2, "BOTTLENECK", PURPLE),
        (0.71, 3, "DECODER", TEAL),
        (0.92, 5, "RECONSTRUCTION", ORANGE),
    ]
    coordinates: list[list[tuple[float, float]]] = []
    for x, count, title, color in layers:
        ys = np.linspace(0.30, 0.72, count)
        layer_points = []
        for y in ys:
            ax.add_patch(Circle((x, y), 0.025, facecolor=f"{color}25", edgecolor=color, linewidth=2))
            layer_points.append((x, y))
        coordinates.append(layer_points)
        ax.text(x, 0.82, title, ha="center", color=color, weight="bold", fontsize=12)
    for left, right in zip(coordinates, coordinates[1:]):
        for start in left:
            for end in right:
                ax.plot([start[0] + 0.025, end[0] - 0.025], [start[1], end[1]], color="#CBD5E1", linewidth=0.7, alpha=0.8)
    ax.text(0.50, 0.20, "compression", ha="center", color=PURPLE, weight="bold")
    arrow(ax, (0.15, 0.20), (0.45, 0.20), PURPLE)
    ax.text(0.68, 0.20, "reconstruction", ha="center", color=ORANGE, weight="bold")
    arrow(ax, (0.55, 0.20), (0.85, 0.20), ORANGE)
    ax.text(0.5, 0.08, "Si entrée et reconstruction diffèrent beaucoup → erreur élevée → anomalie possible", ha="center", fontsize=13, weight="bold")
    save3(fig, "03_architecture_autoencoder.png")


def day3_reconstruction_threshold() -> None:
    rng = np.random.default_rng(12)
    normal = rng.lognormal(mean=-3.0, sigma=0.42, size=450)
    anomalies = rng.lognormal(mean=-1.2, sigma=0.55, size=55)
    threshold = np.quantile(normal, 0.99)
    fig, axes = plt.subplots(1, 2, figsize=(15, 5.8))
    fig.suptitle("L'erreur de reconstruction devient un score d'anomalie", fontsize=22, weight="bold")

    features = ["temp.", "humid.", "puiss.", "pression", "vibration"]
    original = np.array([0.2, -0.1, 0.4, 0.1, 2.1])
    reconstructed = np.array([0.1, 0.0, 0.2, 0.1, 0.6])
    x = np.arange(len(features))
    axes[0].bar(x - 0.18, original, width=0.36, color=BLUE, label="entrée")
    axes[0].bar(x + 0.18, reconstructed, width=0.36, color=ORANGE, label="reconstruction")
    axes[0].set_xticks(x, features, rotation=20)
    axes[0].set_title("Une variable mal reconstruite augmente l'erreur", weight="bold")
    axes[0].legend()

    bins = np.linspace(0, np.quantile(anomalies, 0.98), 35)
    axes[1].hist(normal, bins=bins, color=BLUE, alpha=0.7, label="normal appris")
    axes[1].hist(anomalies, bins=bins, color=RED, alpha=0.65, label="comportements inhabituels")
    axes[1].axvline(threshold, color=ORANGE, linestyle="--", linewidth=3, label="seuil 99 %")
    axes[1].set_title("Le seuil est appris sur les erreurs normales", weight="bold")
    axes[1].set_xlabel("Erreur de reconstruction")
    axes[1].legend()
    for ax in axes:
        style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    save3(fig, "03_erreur_reconstruction_seuil.png")


def day3_compare_methods() -> None:
    fig, ax = plt.subplots(figsize=(15, 6.8))
    ax.axis("off")
    fig.suptitle("Trois détecteurs, trois compromis", fontsize=23, weight="bold")
    rows = [
        ["Seuil / Z-score", "très forte", "faible", "écart d'un signal", "premier niveau explicable"],
        ["Isolation Forest", "moyenne", "moyenne", "combinaison\ninhabituelle", "plusieurs capteurs"],
        ["Autoencoder", "plus faible", "forte", "reconstruction\ndifficile", "motifs multivariés\ncomplexes"],
    ]
    columns = ["Méthode", "Explicabilité", "Complexité", "Force", "Bon usage"]
    table = ax.table(cellText=rows, colLabels=columns, cellLoc="center", colLoc="center", bbox=[0.03, 0.18, 0.94, 0.64])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    colors = [BLUE, TEAL, PURPLE]
    for (row, column), cell in table.get_celld().items():
        cell.set_edgecolor("white")
        if row == 0:
            cell.set_facecolor(INK)
            cell.set_text_props(color="white", weight="bold")
        else:
            cell.set_facecolor(f"{colors[row - 1]}14" if column else colors[row - 1])
            if column == 0:
                cell.set_text_props(color="white", weight="bold")
    ax.text(0.5, 0.08, "La méthode gagnante est celle dont les erreurs et le coût sont acceptables en production.", ha="center", fontsize=14, weight="bold")
    save3(fig, "04_comparer_les_methodes.png")


def day3_vote_priority() -> None:
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.suptitle("Faire voter plusieurs détecteurs pour prioriser les alertes", fontsize=22, weight="bold")
    detectors = [(0.05, 0.70, "Z-SCORE", BLUE), (0.05, 0.46, "ISOLATION\nFOREST", TEAL), (0.05, 0.22, "AUTOENCODER", PURPLE)]
    for x, y, title, color in detectors:
        rounded_box(ax, x, y, 0.18, 0.16, title, "0 ou 1", color)
        arrow(ax, (x + 0.185, y + 0.08), (0.39, 0.50), color)
    rounded_box(ax, 0.40, 0.37, 0.18, 0.25, "VOTE", "au moins 2\nméthodes d'accord", ORANGE)
    arrow(ax, (0.585, 0.50), (0.69, 0.50), ORANGE)
    rounded_box(ax, 0.70, 0.37, 0.23, 0.25, "FILE D'INTERVENTION", "sévérité + contexte\n+ action recommandée", GREEN)
    ax.text(0.5, 0.10, "Le vote réduit les alertes isolées, mais il doit rester évalué et surveillé.", ha="center", fontsize=14, weight="bold")
    save3(fig, "04_vote_et_priorisation.png")


def day3_production_architecture() -> None:
    fig, ax = plt.subplots(figsize=(16, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.suptitle("Du prototype au détecteur exploitable", fontsize=23, weight="bold")
    steps = [
        ("DONNÉES", "qualité surveillée", BLUE),
        ("VARIABLES", "même préparation", TEAL),
        ("ARTEFACTS", "scaler + modèle\nversionnés ensemble", PURPLE),
        ("SCORE + SEUIL", "paramètres tracés", ORANGE),
        ("ALERTES", "historique + tableau\nde bord", RED),
        ("TECHNICIEN", "action + retour", GREEN),
    ]
    xs = np.linspace(0.02, 0.835, len(steps))
    for index, ((title, detail, color), x) in enumerate(zip(steps, xs)):
        rounded_box(ax, x, 0.40, 0.14, 0.30, title, detail, color)
        if index < len(steps) - 1:
            arrow(ax, (x + 0.142, 0.55), (xs[index + 1] - 0.006, 0.55))
    ax.plot([0.905, 0.905, 0.50], [0.39, 0.25, 0.25], color=GREEN, linewidth=2.5)
    arrow(ax, (0.50, 0.25), (0.50, 0.39), GREEN)
    ax.text(0.70, 0.27, "retour terrain et amélioration", ha="center", color=GREEN, weight="bold", fontsize=13)
    ax.text(0.5, 0.10, "Surveiller aussi l'absence de données, la dérive des scores et le volume d'alertes.", ha="center", fontsize=14, weight="bold")
    save3(fig, "04_architecture_production.png")


def main() -> None:
    hourly = load_clean_hourly()
    day2_baseline_concept()
    day2_mae_rmse()
    day2_real_baselines(hourly)
    day2_prophet_format()
    day2_prophet_components()
    train, test, train_pred, test_pred = prepare_prophet(hourly)
    day2_prophet_forecast(train, test, test_pred)
    day2_residual(test, test_pred)
    day2_error_threshold(train, train_pred, test, test_pred)
    day2_precision_recall()
    day2_challenge_pipeline()

    labeled = load_labeled()
    day3_anomaly_types()
    day3_threshold_and_zscore()
    day3_isolation_forest_intuition()
    iforest_test = prepare_iforest(labeled)
    day3_iforest_score(iforest_test)
    day3_maintenance_pipeline()
    day3_neuron_learning()
    day3_autoencoder_architecture()
    day3_reconstruction_threshold()
    day3_compare_methods()
    day3_vote_priority()
    day3_production_architecture()
    print(f"10 illustrations générées dans {DAY_2}")
    print(f"11 illustrations générées dans {DAY_3}")


if __name__ == "__main__":
    main()
