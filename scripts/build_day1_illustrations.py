#!/usr/bin/env python3
"""Génère les illustrations PNG statiques utilisées dans les notebooks du jour 1."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "jour_01"
DATASET = ROOT / "datasets" / "prepared" / "iot_hvac_clean.csv"

BLUE = "#2563EB"
TEAL = "#0F9D8A"
ORANGE = "#F59E0B"
RED = "#DC2626"
PURPLE = "#7C3AED"
INK = "#172033"
MUTED = "#64748B"
GRID = "#D9E2F0"
BG = "#F7FAFC"
GREEN = "#16A34A"


plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 12,
        "axes.titlesize": 18,
        "axes.labelsize": 13,
        "axes.edgecolor": "#B8C4D6",
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "text.color": INK,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)


def save(fig: plt.Figure, filename: str, output_dir: Path = OUTPUT_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / filename, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def style_axis(ax: plt.Axes) -> None:
    ax.grid(True, color=GRID, linewidth=0.8, alpha=0.8)
    ax.spines[["top", "right"]].set_visible(False)


def rounded_box(
    ax: plt.Axes,
    x: float,
    y: float,
    width: float,
    height: float,
    title: str,
    detail: str,
    color: str,
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.035",
        linewidth=2,
        edgecolor=color,
        facecolor=f"{color}12",
    )
    ax.add_patch(patch)
    title_size = 13 if len(title) >= 12 else 15
    ax.text(x + width / 2, y + height * 0.62, title, ha="center", va="center", weight="bold", fontsize=title_size)
    ax.text(x + width / 2, y + height * 0.30, detail, ha="center", va="center", color=MUTED, fontsize=10.5)


def illustration_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(14, 6.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.suptitle("Du capteur à une décision de maintenance", fontsize=24, weight="bold", y=0.96)
    ax.text(
        0.5,
        0.87,
        "Une série temporelle n'est qu'une étape d'une chaîne IoT complète",
        ha="center",
        color=MUTED,
        fontsize=14,
    )

    items = [
        ("CAPTEURS", "température\nvibration\npuissance", BLUE),
        ("DONNÉES", "timestamp +\nmesures", TEAL),
        ("COMPORTEMENT", "motifs et\nprévision", PURPLE),
        ("ALERTE", "écart assez\ninhabituel", ORANGE),
        ("DÉCISION", "inspection et\nretour terrain", GREEN),
    ]
    xs = np.linspace(0.035, 0.805, len(items))
    for index, ((title, detail, color), x) in enumerate(zip(items, xs)):
        rounded_box(ax, x, 0.34, 0.16, 0.30, title, detail, color)
        if index < len(items) - 1:
            ax.add_patch(
                FancyArrowPatch(
                    (x + 0.162, 0.49),
                    (xs[index + 1] - 0.008, 0.49),
                    arrowstyle="-|>",
                    mutation_scale=18,
                    linewidth=2,
                    color=MUTED,
                )
            )
    ax.text(
        0.5,
        0.19,
        "Une alerte aide à décider ; elle ne remplace ni le contexte métier ni le technicien.",
        ha="center",
        fontsize=13,
        weight="bold",
    )
    save(fig, "00_chaine_iot_maintenance.png")


def illustration_architecture_around_model() -> None:
    fig, ax = plt.subplots(figsize=(16, 8.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.suptitle("Ce qu'il y a autour du modèle", fontsize=25, weight="bold", y=0.97)
    ax.text(
        0.5,
        0.90,
        "Une chaîne IoT opérationnelle, du signal physique au retour terrain",
        ha="center",
        color=MUTED,
        fontsize=15,
    )

    top = [
        (0.03, "CAPTEUR", "mesures\nphysiques", BLUE),
        (0.28, "PASSERELLE", "collecte\nlocale", TEAL),
        (0.53, "BROKER", "transport des\nmessages", PURPLE),
        (0.78, "STOCKAGE", "historique\nhorodaté", ORANGE),
    ]
    bottom = [
        (0.78, "DONNÉES\nPRÉPARÉES", "nettoyage et\nvariables", ORANGE),
        (0.53, "DÉTECTEUR", "règle ou\nmodèle", PURPLE),
        (0.28, "SERVICE\nD'ALERTES", "score, seuil,\npriorité", TEAL),
        (0.03, "TECHNICIEN", "contexte et\naction", GREEN),
    ]
    width = 0.18
    height = 0.18

    for x, title, detail, color in top:
        rounded_box(ax, x, 0.64, width, height, title, detail, color)
    for x, title, detail, color in bottom:
        rounded_box(ax, x, 0.36, width, height, title, detail, color)

    for left, right in zip(top, top[1:]):
        ax.add_patch(
            FancyArrowPatch(
                (left[0] + width + 0.006, 0.73),
                (right[0] - 0.006, 0.73),
                arrowstyle="-|>",
                mutation_scale=18,
                linewidth=2.2,
                color=MUTED,
            )
        )
    ax.add_patch(
        FancyArrowPatch(
            (0.87, 0.63),
            (0.87, 0.55),
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=2.2,
            color=MUTED,
        )
    )
    for left, right in zip(bottom, bottom[1:]):
        ax.add_patch(
            FancyArrowPatch(
                (left[0] - 0.006, 0.45),
                (right[0] + width + 0.006, 0.45),
                arrowstyle="-|>",
                mutation_scale=18,
                linewidth=2.2,
                color=MUTED,
            )
        )

    ax.plot([0.12, 0.12, 0.62], [0.35, 0.27, 0.27], color=GREEN, linewidth=2.5)
    ax.add_patch(
        FancyArrowPatch(
            (0.62, 0.27),
            (0.62, 0.35),
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=2.5,
            color=GREEN,
        )
    )
    ax.text(
        0.37,
        0.285,
        "retour terrain → amélioration des règles et modèles",
        ha="center",
        va="bottom",
        color=GREEN,
        fontsize=12,
        weight="bold",
    )

    governance = [
        (0.04, "SURVEILLER", "absence ou retard de données", BLUE),
        (0.37, "CONSERVER", "historique des alertes", TEAL),
        (0.70, "VERSIONNER", "modèle et paramètres", PURPLE),
    ]
    for x, title, detail, color in governance:
        patch = FancyBboxPatch(
            (x, 0.05),
            0.26,
            0.11,
            boxstyle="round,pad=0.015,rounding_size=0.025",
            linewidth=1.8,
            edgecolor=color,
            facecolor=f"{color}10",
        )
        ax.add_patch(patch)
        ax.text(x + 0.13, 0.118, title, ha="center", va="center", color=color, weight="bold", fontsize=12)
        ax.text(x + 0.13, 0.077, detail, ha="center", va="center", color=MUTED, fontsize=10.5)

    save(fig, "00_architecture_autour_modele.png")


def illustration_timeseries_table_and_chart() -> None:
    times = ["10:00", "10:15", "10:30", "10:45", "11:00", "11:15"]
    temperature = [20.8, 21.0, 21.5, 21.2, 21.8, 22.1]

    fig, (ax_table, ax_plot) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [0.9, 1.5]})
    fig.suptitle("Une série temporelle : des valeurs reliées à des instants ordonnés", fontsize=22, weight="bold")

    ax_table.axis("off")
    table = ax_table.table(
        cellText=[[t, f"{v:.1f} °C"] for t, v in zip(times, temperature)],
        colLabels=["timestamp", "température"],
        cellLoc="center",
        colLoc="center",
        bbox=[0.08, 0.05, 0.84, 0.82],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    for (row, _column), cell in table.get_celld().items():
        cell.set_edgecolor("white")
        if row == 0:
            cell.set_facecolor(BLUE)
            cell.set_text_props(color="white", weight="bold")
        elif row % 2:
            cell.set_facecolor("#EAF2FF")
        else:
            cell.set_facecolor(BG)
    ax_table.set_title("Le tableau", pad=16, weight="bold")

    x = np.arange(len(times))
    ax_plot.plot(x, temperature, color=BLUE, marker="o", markersize=9, linewidth=3)
    for position, value in zip(x, temperature):
        ax_plot.annotate(f"{value:.1f}", (position, value), xytext=(0, 12), textcoords="offset points", ha="center")
    ax_plot.set_xticks(x, times)
    ax_plot.set_xlabel("Le temps avance de gauche à droite")
    ax_plot.set_ylabel("Température (°C)")
    ax_plot.set_ylim(20.4, 22.5)
    ax_plot.set_title("La même information sous forme de courbe", pad=16, weight="bold")
    style_axis(ax_plot)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    save(fig, "01_serie_temporelle_table_et_courbe.png")


def illustration_order_matters() -> None:
    chronological_times = np.array([0, 1, 2, 3, 4, 5])
    values = np.array([20.8, 21.0, 21.5, 21.2, 21.8, 22.1])
    file_order = np.array([3, 0, 5, 2, 1, 4])

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.7), sharey=True)
    fig.suptitle("Pourquoi faut-il trier une série temporelle ?", fontsize=22, weight="bold")

    axes[0].plot(np.arange(6), values[file_order], marker="o", linewidth=3, color=RED)
    axes[0].set_xticks(np.arange(6), ["10:45", "10:00", "11:15", "10:30", "10:15", "11:00"], rotation=35)
    axes[0].set_title("Ordre d'arrivée du fichier  ✕", color=RED, weight="bold")
    axes[0].set_xlabel("Les lignes sautent dans le temps")
    axes[0].set_ylabel("Température (°C)")

    axes[1].plot(chronological_times, values, marker="o", linewidth=3, color=GREEN)
    axes[1].set_xticks(chronological_times, ["10:00", "10:15", "10:30", "10:45", "11:00", "11:15"], rotation=35)
    axes[1].set_title("Ordre chronologique  ✓", color=GREEN, weight="bold")
    axes[1].set_xlabel("On retrouve l'histoire réelle du signal")

    for ax in axes:
        ax.set_ylim(20.4, 22.5)
        style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    save(fig, "01_ordre_temporel.png")


def illustration_quality_problems() -> None:
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Quatre défauts de qualité temporelle à distinguer", fontsize=22, weight="bold")

    panels = [
        ("Lignes désordonnées", ["10:30", "10:00", "10:15"], [21.5, 20.8, 21.0], "Le temps recule dans le fichier", ORANGE),
        ("Timestamp dupliqué", ["10:00", "10:15", "10:15"], [20.8, 21.0, 21.2], "Deux lignes revendiquent 10:15", RED),
        ("Valeur absente", ["10:00", "10:15", "10:30"], ["20.8", "NaN", "21.5"], "La ligne existe, une case est vide", PURPLE),
        ("Message absent", ["10:00", "10:15", "10:45"], [20.8, 21.0, 21.8], "La ligne de 10:30 n'existe pas", BLUE),
    ]
    for ax, (title, times, vals, caption, color) in zip(axes.flat, panels):
        ax.axis("off")
        ax.set_title(title, color=color, weight="bold", fontsize=17, pad=12)
        rows = [[time, str(value)] for time, value in zip(times, vals)]
        table = ax.table(cellText=rows, colLabels=["timestamp", "température"], cellLoc="center", bbox=[0.14, 0.24, 0.72, 0.63])
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        for (row, _column), cell in table.get_celld().items():
            cell.set_edgecolor("white")
            cell.set_facecolor(color if row == 0 else ("#F1F5F9" if row % 2 else "white"))
            if row == 0:
                cell.set_text_props(color="white", weight="bold")
        ax.text(0.5, 0.10, caption, ha="center", va="center", transform=ax.transAxes, color=MUTED, fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    save(fig, "02_quatre_problemes_qualite.png")


def illustration_asfreq() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Créer la grille attendue rend le message absent visible", fontsize=22, weight="bold")

    before = [["10:00", "21.2"], ["10:15", "21.4"], ["10:45", "21.8"]]
    after = [["10:00", "21.2"], ["10:15", "21.4"], ["10:30", "NaN"], ["10:45", "21.8"]]
    for ax, title, rows, color in [
        (axes[0], "Avant : la ligne manque", before, ORANGE),
        (axes[1], "Après asfreq() : le trou apparaît", after, BLUE),
    ]:
        ax.axis("off")
        ax.set_title(title, color=color, weight="bold", fontsize=17)
        table = ax.table(cellText=rows, colLabels=["timestamp", "température (°C)"], cellLoc="center", bbox=[0.18, 0.12, 0.64, 0.72])
        table.auto_set_font_size(False)
        table.set_fontsize(14)
        for (row, _column), cell in table.get_celld().items():
            cell.set_edgecolor("white")
            cell.set_facecolor(color if row == 0 else ("#F1F5F9" if row % 2 else "white"))
            if row == 0:
                cell.set_text_props(color="white", weight="bold")
            elif cell.get_text().get_text() == "NaN":
                cell.set_facecolor("#FEE2E2")
                cell.set_text_props(color=RED, weight="bold")
    axes[0].annotate("", xy=(1.07, 0.5), xytext=(0.94, 0.5), xycoords="axes fraction", arrowprops={"arrowstyle": "-|>", "color": MUTED, "lw": 3})
    fig.text(0.5, 0.05, "La grille ajoute un emplacement vide ; elle n'invente encore aucune mesure.", ha="center", fontsize=13, weight="bold")
    fig.tight_layout(rect=(0, 0.08, 1, 0.90))
    save(fig, "02_asfreq_grille_temporelle.png")


def illustration_interpolation() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8), sharey=True)
    fig.suptitle("Interpolation : utile pour un petit trou, risquée pour une longue absence", fontsize=21, weight="bold")

    x_short = np.arange(5)
    y_short = np.array([20.0, 20.5, np.nan, 21.5, 22.0])
    y_short_filled = pd.Series(y_short).interpolate().to_numpy()
    axes[0].plot(x_short, y_short_filled, color=TEAL, linewidth=3)
    axes[0].scatter(x_short[[0, 1, 3, 4]], y_short_filled[[0, 1, 3, 4]], s=90, color=BLUE, label="mesuré", zorder=3)
    axes[0].scatter([2], [y_short_filled[2]], s=130, facecolors="white", edgecolors=ORANGE, linewidth=3, label="estimé", zorder=4)
    axes[0].set_title("Petit trou : estimation plausible  ✓", color=GREEN, weight="bold")
    axes[0].legend()

    x_long = np.arange(9)
    known_x = np.array([0, 1, 7, 8])
    known_y = np.array([20.0, 20.4, 23.0, 23.2])
    axes[1].scatter(known_x, known_y, s=90, color=BLUE, label="mesuré", zorder=3)
    axes[1].plot(known_x, known_y, linestyle="--", linewidth=3, color=RED, alpha=0.8, label="ligne inventée")
    axes[1].axvspan(1, 7, color="#FEE2E2", alpha=0.75)
    axes[1].text(4, 21.2, "Que s'est-il passé\nici ?", ha="center", color=RED, fontsize=14, weight="bold")
    axes[1].set_title("Long trou : ne pas masquer l'absence  ✕", color=RED, weight="bold")
    axes[1].legend()

    for ax in axes:
        ax.set_xticks([])
        ax.set_xlabel("Temps")
        ax.set_ylabel("Température (°C)")
        style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    save(fig, "02_interpolation_courte_longue.png")


def illustration_aggregation() -> None:
    values = np.array([0.8, 0.9, 3.2, 0.8, 0.9, 1.0, 0.8, 0.9])
    x = np.arange(len(values))
    means = [values[:4].mean(), values[4:].mean()]
    maxima = [values[:4].max(), values[4:].max()]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))
    fig.suptitle("Rééchantillonner : la règle choisie change l'information conservée", fontsize=21, weight="bold")
    axes[0].bar(x, values, color=[ORANGE if value > 2 else BLUE for value in values])
    axes[0].axvline(3.5, color=MUTED, linestyle="--")
    axes[0].set_title("Mesures toutes les 15 min")
    axes[0].set_xlabel("Deux heures")
    axes[0].set_ylabel("Vibration (mm/s)")

    axes[1].bar(["Heure 1", "Heure 2"], means, color=TEAL)
    axes[1].set_title("Moyenne horaire")
    axes[1].text(0, means[0] + 0.08, "Le pic est dilué", ha="center", color=MUTED)

    axes[2].bar(["Heure 1", "Heure 2"], maxima, color=ORANGE)
    axes[2].set_title("Maximum horaire")
    axes[2].text(0, maxima[0] + 0.08, "Le pic est conservé", ha="center", color=RED, weight="bold")

    for ax in axes:
        ax.set_ylim(0, 3.8)
        style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    save(fig, "02_moyenne_ou_maximum.png")


def illustration_signal_components() -> None:
    rng = np.random.default_rng(7)
    x = np.linspace(0, 14, 14 * 8)
    trend = 20 + 0.10 * x
    seasonality = 1.5 * np.sin(2 * np.pi * x)
    noise = rng.normal(0, 0.28, len(x))
    observed = trend + seasonality + noise

    fig, axes = plt.subplots(4, 1, figsize=(14, 8), sharex=True)
    fig.suptitle("Une grille de lecture simple du signal", fontsize=22, weight="bold")
    series = [
        (trend, "Tendance : le niveau évolue lentement", BLUE),
        (seasonality, "Saisonnalité : un motif revient chaque jour", TEAL),
        (noise, "Bruit : de petites variations rapides", MUTED),
        (observed, "Signal observé : les effets se superposent", ORANGE),
    ]
    for ax, (y, title, color) in zip(axes, series):
        ax.plot(x, y, color=color, linewidth=2.2)
        ax.set_title(title, loc="left", fontsize=14, weight="bold")
        style_axis(ax)
    axes[-1].set_xlabel("Temps (jours)")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    save(fig, "03_tendance_saisonnalite_bruit.png")


def load_hourly() -> pd.DataFrame:
    df = pd.read_csv(DATASET)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df.set_index("timestamp").select_dtypes("number").resample("1h").mean()


def illustration_moving_averages(hourly: pd.DataFrame) -> None:
    temperature = hourly["temperature_c"]
    start = temperature.index.max() - pd.DateOffset(days=21)
    view = temperature.loc[temperature.index >= start]
    smooth_24h = temperature.rolling(24, center=True, min_periods=12).mean().reindex(view.index)
    smooth_7d = temperature.rolling(24 * 7, center=True, min_periods=24).mean().reindex(view.index)

    fig, ax = plt.subplots(figsize=(14, 6))
    fig.suptitle("Plus la fenêtre est longue, plus la courbe est lissée", fontsize=22, weight="bold")
    ax.plot(view.index, view, color="#94A3B8", alpha=0.55, linewidth=1.2, label="mesure horaire")
    ax.plot(view.index, smooth_24h, color=TEAL, linewidth=2.5, label="moyenne mobile 24 h")
    ax.plot(view.index, smooth_7d, color=PURPLE, linewidth=3.3, label="moyenne mobile 7 jours")
    ax.set_ylabel("Température (°C)")
    ax.set_xlabel("Date")
    ax.legend(ncol=3, loc="upper left")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    save(fig, "03_moyennes_mobiles.png")


def illustration_daily_profile(hourly: pd.DataFrame) -> None:
    profile = hourly.groupby(hourly.index.hour)[["temperature_c", "power_kw"]].mean()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.7))
    fig.suptitle("Le profil journalier moyen révèle un motif qui se répète", fontsize=22, weight="bold")
    axes[0].plot(profile.index, profile["temperature_c"], marker="o", color=ORANGE, linewidth=2.8)
    axes[0].set_title("Température moyenne selon l'heure")
    axes[0].set_ylabel("Température (°C)")
    axes[1].plot(profile.index, profile["power_kw"], marker="o", color=BLUE, linewidth=2.8)
    axes[1].axvspan(7, 19, color="#DBEAFE", alpha=0.6, label="plage d'activité")
    axes[1].set_title("Puissance moyenne selon l'heure")
    axes[1].set_ylabel("Puissance (kW)")
    axes[1].legend()
    for ax in axes:
        ax.set_xlabel("Heure de la journée (UTC)")
        ax.set_xticks(np.arange(0, 24, 3))
        style_axis(ax)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    save(fig, "03_profil_journalier.png")


def illustration_temporal_split() -> None:
    fig, axes = plt.subplots(2, 1, figsize=(14, 6.5), gridspec_kw={"height_ratios": [1, 1.25]})
    fig.suptitle("Évaluer une série temporelle sans laisser le futur fuiter", fontsize=22, weight="bold")

    axes[0].axis("off")
    axes[0].set_xlim(0, 100)
    axes[0].set_ylim(0, 1)
    axes[0].barh(0.5, 80, left=0, height=0.28, color=BLUE)
    axes[0].barh(0.5, 20, left=80, height=0.28, color=ORANGE)
    axes[0].text(40, 0.5, "ENTRAÎNEMENT\npassé connu", color="white", ha="center", va="center", weight="bold")
    axes[0].text(90, 0.5, "TEST\nfutur simulé", color="white", ha="center", va="center", weight="bold")
    axes[0].axvline(80, ymin=0.15, ymax=0.85, color=INK, linewidth=2, linestyle="--")
    axes[0].text(80, 0.88, "frontière", ha="center", weight="bold")
    axes[0].text(50, 0.08, "Découpage chronologique  ✓", ha="center", color=GREEN, fontsize=15, weight="bold")

    axes[1].axis("off")
    axes[1].set_xlim(0, 100)
    axes[1].set_ylim(0, 1)
    for index, left in enumerate(range(0, 100, 10)):
        color = BLUE if index % 3 else ORANGE
        axes[1].barh(0.56, 9, left=left, height=0.24, color=color)
    axes[1].text(50, 0.90, "Mélange aléatoire : des morceaux du futur entrent dans l'entraînement", ha="center", color=RED, fontsize=14, weight="bold")
    axes[1].add_patch(FancyArrowPatch((88, 0.33), (28, 0.43), arrowstyle="-|>", mutation_scale=20, color=RED, linewidth=3, connectionstyle="arc3,rad=-0.12"))
    axes[1].text(58, 0.20, "information future utilisée dans le passé = fuite  ✕", ha="center", color=RED, fontsize=14, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    save(fig, "03_decoupage_train_test.png")


def illustration_challenge_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.suptitle("Le mini-challenge assemble les gestes du jour 1", fontsize=23, weight="bold")
    steps = [
        ("1", "INSPECTER", "forme, types,\nvaleurs absentes", BLUE),
        ("2", "ORDONNER", "convertir et\ntrier le temps", TEAL),
        ("3", "NETTOYER", "doublons, grille,\npetits trous", PURPLE),
        ("4", "COMPRENDRE", "agréger, lisser,\nvisualiser", ORANGE),
        ("5", "ÉVALUER", "séparer passé\net futur", GREEN),
    ]
    xs = np.linspace(0.03, 0.81, len(steps))
    for index, ((number, title, detail, color), x) in enumerate(zip(steps, xs)):
        rounded_box(ax, x, 0.31, 0.16, 0.36, f"{number} · {title}", detail, color)
        if index < len(steps) - 1:
            ax.add_patch(FancyArrowPatch((x + 0.162, 0.49), (xs[index + 1] - 0.008, 0.49), arrowstyle="-|>", mutation_scale=18, linewidth=2, color=MUTED))
    ax.text(0.5, 0.16, "À chaque étape : expliquer le choix, exécuter, puis contrôler le résultat.", ha="center", fontsize=14, weight="bold")
    save(fig, "04_pipeline_challenge.png")


def main() -> None:
    illustration_pipeline()
    illustration_architecture_around_model()
    illustration_timeseries_table_and_chart()
    illustration_order_matters()
    illustration_quality_problems()
    illustration_asfreq()
    illustration_interpolation()
    illustration_aggregation()
    illustration_signal_components()
    hourly = load_hourly()
    illustration_moving_averages(hourly)
    illustration_daily_profile(hourly)
    illustration_temporal_split()
    illustration_challenge_pipeline()
    print(f"13 illustrations générées dans {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
