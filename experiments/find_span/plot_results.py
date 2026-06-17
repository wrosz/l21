import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path
BASE = r"experiments\find_span\detailed_results"
NS   = [5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 100, 120, 150, 200, 250]
frames = {}
for n in NS:
    path = Path(BASE) / f"barabasi_albert_{n}.csv"
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df["time"]    = df["Time taken (seconds)"].astype(float)
    df["timeout"] = df["Timeout happened"].astype(str).str.strip() == "True"
    df["sat"]     = df["Satisfiable"].astype(str).str.strip()
    df["k"]       = df["k"].astype(int)
    frames[n] = df.sort_values("k", ascending=False).reset_index(drop=True)
def find_span(df):
    sat_rows = df[(df["sat"] == "True") & (~df["timeout"])]
    return sat_rows["k"].min() if not sat_rows.empty else None
ncols = 3
nrows = -(-len(NS) // ncols)
fig, axes = plt.subplots(nrows, ncols, figsize=(14, nrows * 3.2))
axes = axes.flatten()
for i, n in enumerate(NS):
    ax   = axes[i]
    df   = frames[n]
    span = find_span(df)
    colors = []
    for _, row in df.iterrows():
        if row["timeout"]:
            colors.append("#f0a500")
        elif row["sat"] == "True":
            colors.append("#2171b5")
        else:
            colors.append("#74c476")
    ax.plot(df["k"], df["time"], color="#2171b5", linewidth=1)
    ax.scatter(df["k"], df["time"], color=colors, zorder=3, s=25)

    # oś X: tylko liczby całkowite
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    # oś X: malejąca
    ax.invert_xaxis()

    ax.tick_params(axis="x", labelsize=7)
    # oś Y: przytnij do przedostatniej największej wartości jeśli jest timeout
    if df["timeout"].any():
        non_timeout_times = df.loc[~df["timeout"], "time"]
        if not non_timeout_times.empty:
            sorted_times = non_timeout_times.sort_values(ascending=False)
            ymax = sorted_times.iloc[0] if len(sorted_times) == 1 else sorted_times.iloc[1]
            ax.set_ylim(0, ymax * 1.15)
    if span is not None:
        # znajdź pozycję x odpowiadającą span
        ax.axvline(span, color="black", linewidth=1.2, linestyle="--", label=f"span={span}")
        ax.legend(fontsize=7, loc="lower left")
    ax.set_title(f"n={n}", fontsize=10)
    ax.set_xlabel("k", fontsize=8)
    ax.set_ylabel("czas (s)", fontsize=8)
    ax.tick_params(axis="y", labelsize=7)
for j in range(len(NS), len(axes)):
    axes[j].set_visible(False)
legend_handles = [
    mpatches.Patch(color="#2171b5", label="SAT (spełnialna)"),
    mpatches.Patch(color="#74c476", label="UNSAT (niespełnialna)"),
    mpatches.Patch(color="#f0a500",  label="timeout"),
]
fig.legend(handles=legend_handles, loc="lower right", fontsize=9,
           bbox_to_anchor=(0.98, 0.01))
fig.suptitle("Wyznaczanie spanu grafów Barabási–Albert — przebieg obliczeń", fontsize=13, y=1.01)
fig.tight_layout()
fig.savefig(r"experiments\find_span\span_results.pdf", bbox_inches="tight")
print("Zapisano: experiments\\find_span\\span_results.pdf")