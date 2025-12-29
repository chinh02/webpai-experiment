#!/usr/bin/env python
"""
Process All Submissions - Batch process all submissions to generate results

Usage:
    python -m analysis.process_all
    python -m analysis.process_all --dataset design2code

This script iterates through all submissions and generates results for each.
"""

import argparse
import os
from pathlib import Path
from typing import List

from .get_results import main as process_submission


def get_all_submissions(dataset: str = "design2code", evaluation_dir: str = "evaluation") -> List[Path]:
    """Get all submission directories for a dataset."""
    dataset_path = Path(evaluation_dir) / dataset
    if not dataset_path.exists():
        raise ValueError(f"Dataset path does not exist: {dataset_path}")
    
    submissions = []
    for item in sorted(dataset_path.iterdir()):
        if item.is_dir() and (item / "evaluation.json").exists():
            submissions.append(item)
    
    return submissions


def main(dataset: str = "design2code", evaluation_dir: str = "evaluation") -> None:
    """Process all submissions for a dataset."""
    submissions = get_all_submissions(dataset, evaluation_dir)
    
    print(f"Found {len(submissions)} submissions to process")
    print("=" * 50)
    
    for i, submission in enumerate(submissions, 1):
        print(f"\n[{i}/{len(submissions)}] Processing: {submission.name}")
        try:
            process_submission(str(submission))
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 50)
    print(f"Processed {len(submissions)} submissions")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process all Design2Code submissions"
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
    main(args.dataset, args.evaluation_dir)
