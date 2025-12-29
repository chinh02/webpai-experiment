#!/usr/bin/env python
"""
Compare Submissions - Compare metrics between two or more submissions

Usage:
    python -m analysis.compare submission1 submission2
    python -m analysis.compare 20251210_gpt4o_mark 20251229_gpt4o_direct --dataset design2code

This script generates a side-by-side comparison of submissions.
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from tabulate import tabulate


METRICS = ["clip", "ssim", "text_similarity", "position_accuracy", "image_reproduction"]


def load_evaluation(submission_path: Path) -> Dict[str, Any]:
    """Load evaluation.json from submission folder."""
    eval_path = submission_path / "evaluation.json"
    if not eval_path.exists():
        raise FileNotFoundError(f"Evaluation file not found: {eval_path}")
    
    with open(eval_path, "r") as f:
        return json.load(f)


def compare_submissions(
    submissions: List[str],
    dataset: str = "design2code",
    evaluation_dir: str = "evaluation"
) -> None:
    """Compare multiple submissions side by side."""
    
    # Load all submissions
    data = {}
    for sub in submissions:
        sub_path = Path(evaluation_dir) / dataset / sub
        if not sub_path.exists():
            print(f"Warning: Submission not found: {sub}")
            continue
        
        try:
            data[sub] = load_evaluation(sub_path)
        except Exception as e:
            print(f"Error loading {sub}: {e}")
    
    if len(data) < 2:
        print("Need at least 2 valid submissions to compare")
        return
    
    # Build comparison table
    headers = ["Metric"] + list(data.keys())
    rows = []
    
    for metric in METRICS:
        row = [metric]
        for sub, eval_data in data.items():
            avg = eval_data.get("metrics", {}).get(metric, {}).get("average", 0)
            row.append(f"{avg * 100:.2f}%")
        rows.append(row)
    
    # Add overall score
    row = ["Overall"]
    for sub, eval_data in data.items():
        metrics = eval_data.get("metrics", {})
        overall = sum(
            metrics.get(m, {}).get("average", 0) for m in METRICS
        ) / len(METRICS)
        row.append(f"{overall * 100:.2f}%")
    rows.append(row)
    
    print("\nSubmission Comparison")
    print("=" * 60)
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    # Show winner for each metric
    print("\nBest per Metric:")
    for metric in METRICS:
        best_sub = None
        best_val = -1
        for sub, eval_data in data.items():
            avg = eval_data.get("metrics", {}).get(metric, {}).get("average", 0)
            if avg > best_val:
                best_val = avg
                best_sub = sub
        print(f"  {metric}: {best_sub} ({best_val * 100:.2f}%)")


def main():
    parser = argparse.ArgumentParser(
        description="Compare Design2Code submissions"
    )
    parser.add_argument(
        "submissions",
        nargs="+",
        help="Submission folder names to compare"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="design2code",
        help="Dataset name"
    )
    parser.add_argument(
        "--evaluation-dir",
        type=str,
        default="evaluation",
        help="Base evaluation directory"
    )
    args = parser.parse_args()
    compare_submissions(args.submissions, args.dataset, args.evaluation_dir)


if __name__ == "__main__":
    main()
