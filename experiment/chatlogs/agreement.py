#!/usr/bin/env python3
"""
My buddy Chat's script to compute inter-rater agreement from two Taguette
project exports.

Usage:
    python taguette_agreement.py coder_a.sqlite3 coder_b.sqlite3

Requirements:
    pip install pandas krippendorff
"""

import sys
import sqlite3
import pandas as pd
import krippendorff


# ----------------------------
# Load annotations from Taguette SQLite
# ----------------------------

def load_taguette_annotations(sqlite_path):
    """
    Return a DataFrame with columns:
        document, start_offset, end_offset, tag
    """
    conn = sqlite3.connect(sqlite_path)

    query = """
    SELECT
        d.name        AS document,
        h.start_offset,
        h.end_offset,
        t.path        AS tag
    FROM highlights h
    JOIN documents d
        ON h.document_id = d.id
    JOIN highlight_tags ht
        ON ht.highlight_id = h.id
    JOIN tags t
        ON ht.tag_id = t.id
    ORDER BY d.name, h.start_offset, h.end_offset, t.path
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# ----------------------------
# Align two coders by span
# ----------------------------

def align_two_coders(df_a, df_b):
    """
    Align annotations on (document, start_offset, end_offset).

    Returns DataFrame with:
        document, start_offset, end_offset, A, B
    """
    df_a = df_a.copy()
    df_b = df_b.copy()

    df_a["coder"] = "A"
    df_b["coder"] = "B"

    combined = pd.concat([df_a, df_b], ignore_index=True)

    aligned = combined.pivot_table(
        index=["document", "start_offset", "end_offset"],
        columns="coder",
        values="tag",
        aggfunc="first"
    )

    return aligned.reset_index()


# ----------------------------
# Krippendorff’s alpha
# ----------------------------

def krippendorff_alpha_nominal(aligned_df):
    """
    Compute Krippendorff’s alpha for nominal data.
    """
    data = [
        aligned_df["A"].tolist(),
        aligned_df["B"].tolist(),
    ]

    return krippendorff.alpha(
        reliability_data=data,
        level_of_measurement="nominal"
    )


# ----------------------------
# Main
# ----------------------------

def main():
    if len(sys.argv) != 3:
        print("Usage: python taguette_agreement.py coder_a.sqlite3 coder_b.sqlite3")
        sys.exit(1)

    path_a, path_b = sys.argv[1], sys.argv[2]

    print("Loading annotations...")
    coder_a = load_taguette_annotations(path_a)
    coder_b = load_taguette_annotations(path_b)

    print(f"  coder A annotations: {len(coder_a)}")
    print(f"  coder B annotations: {len(coder_b)}")

    print("\nAligning spans...")
    aligned = align_two_coders(coder_a, coder_b)
    print(f"  aligned spans: {len(aligned)}")

    print("\nSample aligned rows:")
    print(aligned.head(10))

    print("\nComputing Krippendorff’s α (nominal)...")
    alpha = krippendorff_alpha_nominal(aligned)
    print(f"\nKrippendorff’s α = {alpha:.4f}")

    # Optional per-tag alpha
    print("\nPer-tag α (where computable):")
    tags = sorted(
        set(aligned["A"].dropna()) | set(aligned["B"].dropna())
    )

    for tag in tags:
        subset = aligned[
            (aligned["A"] == tag) | (aligned["B"] == tag)
        ]
        if len(subset) >= 2:
            try:
                a = krippendorff_alpha_nominal(subset)
                print(f"  {tag}: {a:.4f}")
            except Exception:
                print(f"  {tag}: insufficient data")


if __name__ == "__main__":
    main()

