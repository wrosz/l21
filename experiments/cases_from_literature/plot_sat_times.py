import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

BASE = r"experiments\cases_from_literature"

# ── helpers ───────────────────────────────────────────────────────────────────
PALETTE = {
    "cycle":             "#6baed6",
    "hypercube":         "#4292c6",
    "path":              "#2171b5",
    "projective_plane":  "#084594",
    "random_regular":    "#74c476",
    "random_tree":       "#238b45",
}

def enrich(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    df["name"]  = df["File"].str.replace(".dimacs", "", regex=False)
    df["class"] = df["name"].str.extract(r"^([a-z_]+?)(?=_\d)")
    df["label"] = df["name"].apply(make_label)
    return df

def make_label(name):
    parts = name.rsplit("_", 2)
    if len(parts) == 3:
        cls, size, k = parts
        return f"{cls}  n={size}  k={k}"
    return name

def get_color(cls, timeout=False):
    return "#CC0000" if timeout else PALETTE.get(cls, "#888888")

def apply_timeout_style(bar, is_timeout):
    if is_timeout:
        bar.set_hatch("///")
        bar.set_edgecolor("#8B0000")
        bar.set_linewidth(2.5)

def build_legend(classes, has_timeout):
    handles = [mpatches.Patch(color=PALETTE[c], label=c)
               for c in sorted(classes) if c in PALETTE]
    if has_timeout:
        handles.append(mpatches.Patch(
            facecolor="#CC0000", edgecolor="#8B0000", linewidth=2,
            hatch="///", label="timeout / nieweryfikowalna"))
    return handles

def plot_chart(df_sub, title, outfile, log_scale=False, timeout_col="timeout"):
    fig, ax = plt.subplots(figsize=(11, max(8, len(df_sub) * 0.28)))
    bar_colors = [get_color(row["class"], row[timeout_col]) for _, row in df_sub.iterrows()]
    bars = ax.barh(df_sub["label"], df_sub["time"], color=bar_colors)
    for bar, (_, row) in zip(bars, df_sub.iterrows()):
        apply_timeout_style(bar, row[timeout_col])
    ax.invert_yaxis()
    ax.set_xlabel("Czas (s)" + (" — skala logarytmiczna" if log_scale else ""))
    ax.set_title(title)
    if log_scale:
        ax.set_xscale("log")
    ax.legend(handles=build_legend(df_sub["class"].unique(), df_sub[timeout_col].any()),
              loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(outfile, dpi=150, bbox_inches="tight")

# ── dane: satisfiability ──────────────────────────────────────────────────────
df = enrich(pd.read_csv(f"{BASE}\\satisfiability_results.csv"))
df["time"]    = df["Time taken (seconds)"].astype(float)
df["timeout"] = df["Satisfiable"].astype(str).str.strip() == "None"

should = df["Should be Satisfiable"].astype(str).str.strip()
sat    = df[should == "True"].sort_values(["class", "time"]).reset_index(drop=True)
unsat  = df[should == "False"].sort_values(["class", "time"]).reset_index(drop=True)

plot_chart(sat,   "Formuły spełnialne (SAT) — czasy sprawdzania",      f"{BASE}\\plots\\sat_times.png")
plot_chart(unsat, "Formuły niespełnialne (UNSAT) — czasy sprawdzania", f"{BASE}\\plots\\unsat_times.png", log_scale=True)

# ── dane: drat-trim ───────────────────────────────────────────────────────────
# kolumny: File, Proof Verified, Time taken (seconds), Did time out
drat = enrich(pd.read_csv(f"{BASE}\\proof_verification_results.csv"))
drat["time_drat"]    = drat["Time taken (seconds)"].astype(float)
drat["unverified"]   = drat["Proof Verified"].astype(str).str.strip() == "False"

# dołącz czas generacji formuły z unsat
drat = drat.merge(
    unsat[["name", "time"]].rename(columns={"time": "time_sat"}),
    on="name", how="left"
)
drat = drat[~drat["unverified"]].sort_values(["class", "time_drat"]).reset_index(drop=True)

# ── wykres drat-trim: grouped bar ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, max(8, len(drat) * 0.5)))

y      = np.arange(len(drat))
height = 0.38

bars_sat  = ax.barh(y + height/2, drat["time_sat"],  height, label="generacja formuły (UNSAT solver)",
                    color=[PALETTE.get(c, "#888") for c in drat["class"]], alpha=0.55)
bars_drat = ax.barh(y - height/2, drat["time_drat"], height, label="weryfikacja dowodu (drat-trim)",
                    color=[PALETTE.get(c, "#888") for c in drat["class"]], alpha=1.0)

for bar, (_, row) in zip(bars_drat, drat.iterrows()):
    apply_timeout_style(bar, row["unverified"])

ax.set_yticks(y)
ax.set_yticklabels(drat["label"], fontsize=8)
ax.invert_yaxis()
ax.set_xscale("log")
ax.set_xlabel("Czas (s) — skala logarytmiczna")
ax.set_title("Weryfikacja drat-trim vs czas generacji formuły (UNSAT)")

class_handles = [mpatches.Patch(color=PALETTE[c], label=c)
                 for c in sorted(drat["class"].unique()) if c in PALETTE]
style_handles = [
    mpatches.Patch(facecolor="#aaa", alpha=0.55, label="generacja formuły"),
    mpatches.Patch(facecolor="#aaa", alpha=1.0,  label="weryfikacja drat-trim"),
]


ax.legend(handles=class_handles + style_handles, loc="lower right", fontsize=8)
fig.tight_layout()
fig.savefig(f"{BASE}\\plots\\drat_times.png", dpi=150, bbox_inches="tight")
