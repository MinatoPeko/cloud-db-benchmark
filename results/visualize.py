#!/usr/bin/env python3
"""
results/visualize.py
Đọc CSV kết quả từ results/data/, vẽ 4 loại biểu đồ và lưu vào results/charts/.

Sử dụng:
    python results/visualize.py
    python results/visualize.py --file results/data/results_small_20261024_120000.csv
"""

import argparse
import glob
import os

import matplotlib
matplotlib.use("Agg")   # non-interactive backend (Codespaces / headless)
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")
DATA_DIR   = os.path.join(os.path.dirname(__file__), "data")

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
DB_PALETTE = {"PostgreSQL": "#336791", "MongoDB": "#4DB33D", "Neo4j": "#008CC1"}


def load_latest(data_dir: str) -> pd.DataFrame:
    files = sorted(glob.glob(os.path.join(data_dir, "results_*.csv")), key=os.path.getmtime)
    if not files:
        raise FileNotFoundError(f"Không có file kết quả nào trong {data_dir}")
    path = files[-1]
    print(f"📂 Đọc file: {path}")
    return pd.read_csv(path), path


def _save(fig, name):
    os.makedirs(CHARTS_DIR, exist_ok=True)
    path = os.path.join(CHARTS_DIR, name)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  💾 {path}")


# ── Chart 1: Mean Latency per UC per DB (grouped bar) ─────────────────────────
def chart_latency_bar(df: pd.DataFrame, suffix: str):
    fig, ax = plt.subplots(figsize=(13, 6))
    ucs = df["uc_id"].unique()
    x = range(len(ucs))
    width = 0.25
    dbs = df["db"].unique()
    for i, db in enumerate(dbs):
        sub = df[df["db"] == db].set_index("uc_id")
        vals = [sub.loc[uc, "mean_ms"] if uc in sub.index else 0 for uc in ucs]
        ax.bar([p + i * width for p in x], vals, width,
               label=db, color=DB_PALETTE.get(db))
    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(ucs, rotation=20)
    ax.set_ylabel("Latency trung bình (ms)")
    ax.set_title("So sánh Latency trung bình theo Use Case và CSDL")
    ax.legend()
    _save(fig, f"01_latency_bar_{suffix}.png")


# ── Chart 2: p99 Latency heatmap ──────────────────────────────────────────────
def chart_p99_heatmap(df: pd.DataFrame, suffix: str):
    pivot = df.pivot_table(index="db", columns="uc_id", values="p99_ms", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax,
                linewidths=0.5, cbar_kws={"label": "p99 Latency (ms)"})
    ax.set_title("Heatmap p99 Latency (ms) — thấp hơn = tốt hơn")
    ax.set_xlabel("Use Case"); ax.set_ylabel("CSDL")
    _save(fig, f"02_p99_heatmap_{suffix}.png")


# ── Chart 3: QPS per UC per DB (horizontal bar) ───────────────────────────────
def chart_qps(df: pd.DataFrame, suffix: str):
    fig, ax = plt.subplots(figsize=(10, 7))
    ucs = df["uc_id"].unique()
    y = range(len(ucs))
    height = 0.25
    dbs = df["db"].unique()
    for i, db in enumerate(dbs):
        sub = df[df["db"] == db].set_index("uc_id")
        vals = [sub.loc[uc, "qps"] if uc in sub.index else 0 for uc in ucs]
        ax.barh([p + i * height for p in y], vals, height,
                label=db, color=DB_PALETTE.get(db))
    ax.set_yticks([p + height for p in y])
    ax.set_yticklabels(ucs)
    ax.set_xlabel("Throughput (Queries / giây)")
    ax.set_title("So sánh Throughput (QPS) theo Use Case và CSDL")
    ax.legend()
    _save(fig, f"03_qps_bar_{suffix}.png")


# ── Chart 4: RAM usage bar ────────────────────────────────────────────────────
def chart_ram(df: pd.DataFrame, suffix: str):
    if "ram_mean_mb" not in df.columns:
        print("  ⚠️  Không có cột ram_mean_mb, bỏ qua chart RAM.")
        return
    ram_df = df.groupby(["db", "uc_id"])["ram_mean_mb"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(13, 6))
    ucs = ram_df["uc_id"].unique()
    x = range(len(ucs))
    width = 0.25
    dbs = ram_df["db"].unique()
    for i, db in enumerate(dbs):
        sub = ram_df[ram_df["db"] == db].set_index("uc_id")
        vals = [sub.loc[uc, "ram_mean_mb"] if uc in sub.index else 0 for uc in ucs]
        ax.bar([p + i * width for p in x], vals, width,
               label=db, color=DB_PALETTE.get(db))
    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(ucs, rotation=20)
    ax.set_ylabel("RAM trung bình (MB)")
    ax.set_title("So sánh mức tiêu thụ RAM theo Use Case và CSDL")
    ax.legend()
    _save(fig, f"04_ram_bar_{suffix}.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default=None, help="Đường dẫn file CSV cụ thể (mặc định: file mới nhất)")
    args = parser.parse_args()

    if args.file:
        df = pd.read_csv(args.file)
        path = args.file
    else:
        df, path = load_latest(DATA_DIR)

    suffix = os.path.splitext(os.path.basename(path))[0].replace("results_", "")
    print(f"  📊 {len(df)} dòng kết quả / {df['db'].nunique()} CSDL / {df['uc_id'].nunique()} Use Cases\n")

    print("Vẽ biểu đồ...")
    chart_latency_bar(df, suffix)
    chart_p99_heatmap(df, suffix)
    chart_qps(df, suffix)
    chart_ram(df, suffix)

    print(f"\n✅ Đã xuất 4 biểu đồ vào {CHARTS_DIR}")


if __name__ == "__main__":
    main()
