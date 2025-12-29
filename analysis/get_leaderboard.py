#!/usr/bin/env python
"""
Get Leaderboard - Generate leaderboard data from all submissions

Usage:
    python -m analysis.get_leaderboard
    python -m analysis.get_leaderboard --output data/leaderboard.json
    python -m analysis.get_leaderboard --dataset design2code

This script:
1. Scans all submissions in evaluation/<dataset>/
2. Reads evaluation.json and metadata.yaml for each
3. Calculates rankings based on overall score
4. Outputs leaderboard.json for website consumption
"""

import argparse
import json
import os
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from tqdm import tqdm

# Metric weights for overall score calculation
METRIC_WEIGHTS = {
    "clip": 0.20,
    "ssim": 0.20,
    "text_similarity": 0.20,
    "position_accuracy": 0.20,
    "image_reproduction": 0.20
}

# Metric display names
METRIC_DISPLAY = {
    "clip": "CLIP",
    "ssim": "SSIM",
    "text_similarity": "Text",
    "position_accuracy": "Position",
    "image_reproduction": "IR"
}


def calculate_overall_score(metrics: Dict[str, Dict]) -> float:
    """Calculate weighted overall score from individual metrics."""
    total_weight = 0
    weighted_sum = 0
    
    for metric, weight in METRIC_WEIGHTS.items():
        if metric in metrics and "average" in metrics[metric]:
            weighted_sum += metrics[metric]["average"] * weight
            total_weight += weight
    
    return weighted_sum / total_weight if total_weight > 0 else 0


def load_submission(submission_path: Path) -> Optional[Dict[str, Any]]:
    """Load and parse a single submission."""
    eval_path = submission_path / "evaluation.json"
    if not eval_path.exists():
        return None
    
    try:
        with open(eval_path, "r") as f:
            evaluation = json.load(f)
        
        # Load metadata
        metadata = {}
        for ext in ["yaml", "yml"]:
            meta_path = submission_path / f"metadata.{ext}"
            if meta_path.exists():
                with open(meta_path, "r") as f:
                    metadata = yaml.safe_load(f)
                break
        
        # Extract date from folder name
        folder_name = submission_path.name
        date_str = folder_name.split('_')[0]
        try:
            date = datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Calculate metrics
        metrics = evaluation.get("metrics", {})
        overall_score = calculate_overall_score(metrics)
        
        # Build model display name
        model_name = metadata.get("model", {}).get("name", evaluation.get("model", "Unknown"))
        method_name = metadata.get("method", {}).get("name", evaluation.get("method", "Unknown"))
        display_name = f"{model_name} ({method_name.capitalize()})"
        
        return {
            "submission_id": folder_name,
            "model": display_name,
            "model_name": model_name,
            "method": method_name,
            "clip": metrics.get("clip", {}).get("average", 0),
            "ssim": metrics.get("ssim", {}).get("average", 0),
            "text": metrics.get("text_similarity", {}).get("average", 0),
            "position": metrics.get("position_accuracy", {}).get("average", 0),
            "ir": metrics.get("image_reproduction", {}).get("average", 0),
            "overall": overall_score,
            "date": date,
            "org": metadata.get("submission", {}).get("organization", 
                   metadata.get("model", {}).get("provider", "Unknown")),
            "tags": metadata.get("tags", []),
            "num_instances": len(evaluation.get("instance_results", {})),
        }
    except Exception as e:
        print(f"Error loading {submission_path}: {e}")
        return None


def format_percentage(value: float) -> str:
    """Format a decimal value as percentage string."""
    return f"{value * 100:.2f}%"


def generate_leaderboard(
    dataset: str = "design2code",
    evaluation_dir: str = "evaluation"
) -> Dict[str, Any]:
    """Generate leaderboard data from all submissions."""
    
    dataset_path = Path(evaluation_dir) / dataset
    if not dataset_path.exists():
        raise ValueError(f"Dataset path does not exist: {dataset_path}")
    
    # Collect all submissions
    submissions = []
    submission_dirs = sorted(dataset_path.iterdir())
    
    print(f"Scanning submissions in {dataset_path}...")
    for submission_dir in tqdm(submission_dirs):
        if not submission_dir.is_dir():
            continue
        
        submission = load_submission(submission_dir)
        if submission:
            submissions.append(submission)
    
    # Sort by overall score (descending)
    submissions.sort(key=lambda x: x["overall"], reverse=True)
    
    # Assign ranks
    results = []
    for rank, submission in enumerate(submissions, 1):
        results.append({
            "rank": rank,
            "model": submission["model"],
            "clip": format_percentage(submission["clip"]),
            "ssim": format_percentage(submission["ssim"]),
            "text": format_percentage(submission["text"]),
            "position": format_percentage(submission["position"]),
            "ir": format_percentage(submission["ir"]),
            "overall": format_percentage(submission["overall"]),
            "date": submission["date"],
            "org": submission["org"],
            "tags": submission["tags"],
        })
    
    # Build leaderboard object
    leaderboard = {
        "name": dataset,
        "lastUpdated": datetime.now().isoformat() + "Z",
        "totalSubmissions": len(results),
        "metrics": list(METRIC_DISPLAY.values()),
        "results": results
    }
    
    return leaderboard


def save_leaderboard(leaderboard: Dict[str, Any], output_path: str) -> None:
    """Save leaderboard to JSON file."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(leaderboard, f, indent=2)
    print(f"Leaderboard saved to: {output_path}")


def print_leaderboard(leaderboard: Dict[str, Any]) -> None:
    """Print formatted leaderboard to console."""
    print(f"\n{'='*80}")
    print(f"Design2Code Leaderboard - {leaderboard['name']}")
    print(f"Last Updated: {leaderboard['lastUpdated']}")
    print(f"Total Submissions: {leaderboard['totalSubmissions']}")
    print(f"{'='*80}\n")
    
    # Header
    header = f"{'Rank':<6} {'Model':<35} {'CLIP':<10} {'SSIM':<10} {'Text':<10} {'Pos':<10} {'IR':<10} {'Overall':<10}"
    print(header)
    print("-" * len(header))
    
    # Rows
    for entry in leaderboard["results"]:
        row = (
            f"{entry['rank']:<6} "
            f"{entry['model'][:33]:<35} "
            f"{entry['clip']:<10} "
            f"{entry['ssim']:<10} "
            f"{entry['text']:<10} "
            f"{entry['position']:<10} "
            f"{entry['ir']:<10} "
            f"{entry['overall']:<10}"
        )
        print(row)


def main(
    dataset: str = "design2code",
    output: Optional[str] = None,
    evaluation_dir: str = "evaluation"
) -> None:
    """Main entry point."""
    leaderboard = generate_leaderboard(dataset, evaluation_dir)
    
    # Print to console
    print_leaderboard(leaderboard)
    
    # Save to file
    if output:
        save_leaderboard(leaderboard, output)
    else:
        # Default output path
        default_output = f"data/{dataset}-leaderboard.json"
        save_leaderboard(leaderboard, default_output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate leaderboard from Design2Code submissions"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="design2code",
        help="Dataset name (folder under evaluation/)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output path for leaderboard JSON"
    )
    parser.add_argument(
        "--evaluation-dir",
        type=str,
        default="evaluation",
        help="Base evaluation directory"
    )
    args = parser.parse_args()
    main(args.dataset, args.output, args.evaluation_dir)
