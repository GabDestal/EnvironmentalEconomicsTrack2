"""Figures for section 4 of the paper.

Run after analysis.py, from the repository root:
    python scripts/figures.py

Every figure is drawn from load_analysis_data() or the CSVs in outputs/, with
periods and thresholds from config.py, so nothing here is typed by hand.
PNGs are written to outputs/figures/.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import COUNTRIES, EARLY, OUT_DIR, RECENT, ROBUSTNESS_START
from load_data import load_analysis_data

FIG_DIR = OUT_DIR / "figures"
NAMES = {"ESP": "Spain", "FRA": "France", "GER": "Germany", "SWE": "Sweden"}
# Two colours checked for colour-blind separation; early also drawn hollow/dashed.
C_EARLY, C_RECENT, C_INK, C_MUTED = "#3b6ea8", "#c2410c", "#222222", "#6b6b6b"
SOURCE = "Source: Copernicus Interactive Climate Atlas v2.5, ERA5-Land, accessed 29 Oct 2026."
EARLY_LBL = f"Early {EARLY[0]}–{EARLY[1]}"
RECENT_LBL = f"Recent {RECENT[0]}–{RECENT[1]}"

plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": C_MUTED, "axes.labelcolor": C_INK,
    "xtick.color": C_MUTED, "ytick.color": C_MUTED,
    "axes.grid": True, "grid.color": "#e6e6e6", "grid.linewidth": 0.6,
    "legend.frameon": False, "savefig.dpi": 200, "savefig.bbox": "tight",
})


def grid(title: str, note: str):
    fig, axes = plt.subplots(2, 2, figsize=(8, 5.6), sharex=True, sharey=True)
    fig.suptitle(title, x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.text(0.01, -0.01, f"{note} {SOURCE}", ha="left", va="top", fontsize=7.5,
             color=C_MUTED, wrap=True)
    return fig, dict(zip(COUNTRIES, axes.flat))


def fig_legend(fig, ax) -> None:
    h, l = ax.get_legend_handles_labels()
    fig.legend(h, l, loc="upper left", ncol=len(l), fontsize=8, bbox_to_anchor=(0.005, 0.955))


def save(fig, name: str) -> None:
    fig.tight_layout(rect=(0, 0.02, 1, 0.93))
    fig.savefig(FIG_DIR / f"{name}.png")
    plt.close(fig)
    print(f"wrote outputs/figures/{name}.png")


# Figure 1 ---------------------------------------------------------------
def fig1_timeseries(data: pd.DataFrame) -> None:
    txx = data[data["indicator"] == "TXx"]
    fig, ax = grid("Figure 1. Summer maximum temperature (TXx) anomaly, 1950–2025",
                   f"Dots: June, July and August values; line: their yearly mean. Anomaly in °C "
                   f"from the {EARLY[0]}–{EARLY[1]} mean of the same month. Shaded: the two compared "
                   f"periods. Dashed line: {ROBUSTNESS_START}, before which ERA5-Land may be less consistent.")
    for c, a in ax.items():
        d = txx[txx["country"] == c]
        a.axvspan(EARLY[0] - 0.5, EARLY[1] + 0.5, color=C_EARLY, alpha=0.08, lw=0)
        a.axvspan(RECENT[0] - 0.5, RECENT[1] + 0.5, color=C_RECENT, alpha=0.08, lw=0)
        a.axvline(ROBUSTNESS_START, color=C_MUTED, ls="--", lw=0.8)
        a.axhline(0, color=C_MUTED, lw=0.8)
        a.scatter(d["year"], d["analysis_value"], s=6, color=C_MUTED, alpha=0.45, lw=0)
        yearly = d.groupby("year")["analysis_value"].mean()
        a.plot(yearly.index, yearly.values, color=C_INK, lw=1.4)
        a.set_title(NAMES[c], loc="left")
    for c in ("ESP", "GER"):
        ax[c].set_ylabel("TXx anomaly (°C)")
    ax["ESP"].text(np.mean(EARLY), 0.97, "early", transform=ax["ESP"].get_xaxis_transform(),
                   ha="center", va="top", color=C_EARLY, fontsize=8)
    ax["ESP"].text(np.mean(RECENT), 0.97, "recent", transform=ax["ESP"].get_xaxis_transform(),
                   ha="center", va="top", color=C_RECENT, fontsize=8)
    save(fig, "fig1_txx_timeseries")


# Figure 2 ---------------------------------------------------------------
def fig2_distributions(data: pd.DataFrame) -> None:
    txx = data[(data["indicator"] == "TXx") & data["period"].notna()]
    bins = np.arange(np.floor(txx["analysis_value"].min()), np.ceil(txx["analysis_value"].max()) + 1, 1.0)
    fig, ax = grid("Figure 2. Distribution of summer TXx anomalies, early vs recent period",
                   f"Share of the 90 June–August values per period falling in each 1 °C bin. "
                   f"Vertical lines: period means. Anomaly from the {EARLY[0]}–{EARLY[1]} mean of the same month.")
    for c, a in ax.items():
        for per, col, lbl, ls in (("early", C_EARLY, EARLY_LBL, "--"), ("recent", C_RECENT, RECENT_LBL, "-")):
            v = txx[(txx["country"] == c) & (txx["period"] == per)]["analysis_value"]
            w = np.full(len(v), 100 / len(v))
            a.hist(v, bins=bins, weights=w, histtype="stepfilled", color=col, alpha=0.18)
            a.hist(v, bins=bins, weights=w, histtype="step", color=col, lw=1.4, ls=ls, label=lbl)
            a.axvline(v.mean(), color=col, lw=1.4, ls=ls)
        a.set_title(NAMES[c], loc="left")
    for c in ("ESP", "GER"):
        ax[c].set_ylabel("Share of observations (%)")
    for c in ("GER", "SWE"):
        ax[c].set_xlabel("TXx anomaly (°C)")
    fig_legend(fig, ax["ESP"])
    save(fig, "fig2_txx_distributions")


# Figure 3 ---------------------------------------------------------------
def fig3_shift_vs_shape(shift: pd.DataFrame) -> None:
    s = shift[shift["indicator"] == "TXx"]
    fig, ax = grid("Figure 3. Shift or change in shape? Change in TXx percentiles vs change in the mean",
                   f"Change from {EARLY[0]}–{EARLY[1]} to {RECENT[0]}–{RECENT[1]}, °C. Dots: change in each "
                   f"percentile; band: change in the mean. Bars and band: 95% intervals, bootstrap resampling "
                   f"whole summers. Under a pure shift every dot would lie on the dashed line, up to sampling noise. n: recent values above the "
                   f"recent percentile (distinct summers).")
    for c, a in ax.items():
        d = s[s["country"] == c].sort_values("tail_pct")
        m = d.iloc[0]
        x = np.arange(len(d))
        a.axhspan(m["d_mean_lo"], m["d_mean_hi"], color=C_EARLY, alpha=0.15, lw=0)
        a.axhline(m["d_mean"], color=C_EARLY, lw=1.4, ls="--", label="Change in the mean (95% band)")
        a.errorbar(x, d["d_q"], yerr=[d["d_q"] - d["d_q_lo"], d["d_q_hi"] - d["d_q"]], fmt="o",
                   color=C_RECENT, ms=6, capsize=3, lw=1.2, label="Change in percentile (95% interval)")
        for xi, (_, r) in zip(x, d.iterrows()):
            a.annotate(f"n={r['n_beyond_recent']} ({r['years_beyond_recent']})", (xi, r["d_q_hi"]),
                       textcoords="offset points", xytext=(0, 4), ha="center", fontsize=7, color=C_MUTED)
        a.set_xticks(x, [f"P{p}" for p in d["tail_pct"]])
        a.axhline(0, color=C_MUTED, lw=0.8)
        a.set_title(f"{NAMES[c]}  (mean {m['d_mean']:+.2f} °C)", loc="left")
        a.set_xlim(-0.5, len(d) - 0.5)
    for c in ("ESP", "GER"):
        ax[c].set_ylabel("Change, recent − early (°C)")
    for c in ("GER", "SWE"):
        ax[c].set_xlabel("Percentile of the TXx distribution")
    fig_legend(fig, ax["ESP"])
    save(fig, "fig3_txx_shift_vs_shape")


# Figure 4 ---------------------------------------------------------------
def fig4_thresholds(exc: pd.DataFrame) -> None:
    e = exc[exc["indicator"] == "TXx"]
    fig, ax = grid("Figure 4. How often are early-period extremes exceeded? Observed vs pure shift",
                   f"Share of June–August values above each threshold, an early-period ({EARLY[0]}–{EARLY[1]}) "
                   f"percentile of TXx. Pure shift: early values moved up by the change in the mean, with "
                   f"no change in shape. Labels: recent count out of 90. Log scale.")
    for c, a in ax.items():
        d = e[e["country"] == c].sort_values("threshold_pct")
        x = np.arange(len(d))
        a.plot(x, 100 * d["rate_early"], "o--", color=C_EARLY, mfc="white", lw=1.2, ms=6, label=EARLY_LBL)
        a.plot(x, 100 * d["rate_shift_only"], "s:", color=C_MUTED, lw=1.2, ms=5, label="Pure shift (benchmark)")
        a.plot(x, 100 * d["rate_recent"], "o-", color=C_RECENT, lw=1.6, ms=6, label=RECENT_LBL)
        for xi, (_, r) in zip(x, d.iterrows()):
            a.annotate(f"{r['k_recent']}", (xi, 100 * r["rate_recent"]), textcoords="offset points",
                       xytext=(0, 7), ha="center", va="bottom", fontsize=7, color=C_RECENT)
        a.set_yscale("log")
        a.set_ylim(0.5, 120)
        a.set_yticks([1, 2, 5, 10, 25, 50, 100], ["1", "2", "5", "10", "25", "50", "100"])
        a.set_xticks(x, [f"P{p}" for p in d["threshold_pct"]])
        a.set_title(NAMES[c], loc="left")
    for c in ("ESP", "GER"):
        ax[c].set_ylabel("Values above threshold (%)")
    for c in ("GER", "SWE"):
        ax[c].set_xlabel("Threshold: early-period percentile")
    fig_legend(fig, ax["ESP"])
    save(fig, "fig4_txx_thresholds")


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    data = load_analysis_data()
    shift = pd.read_csv(OUT_DIR / "shift_shape.csv")
    exc = pd.read_csv(OUT_DIR / "exceedance.csv")
    fig1_timeseries(data)
    fig2_distributions(data)
    fig3_shift_vs_shape(shift)
    fig4_thresholds(exc)


if __name__ == "__main__":
    main()
