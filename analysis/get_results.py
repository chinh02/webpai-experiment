#!/usr/bin/env python
"""
Get Results - Process evaluation results for a submission

Usage:
    python -m analysis.get_results evaluation/design2code/<submission>

This script:
1. Reads evaluation.json from the submission folder
2. Calculates aggregate statistics
3. Generates results breakdown by metric
4. Outputs summary to results/ folder
"""

import argparse
import json
import os
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Constants
METRICS = ["clip", "ssim", "text_similarity", "position_accuracy", "image_reproduction"]
METRIC_WEIGHTS = {
    "clip": 0.20,
    "ssim": 0.20,
    "text_similarity": 0.20,
    "position_accuracy": 0.20,
    "image_reproduction": 0.20
}
DELIMITER = "=" * 50


def load_evaluation(submission_path: str) -> Dict[str, Any]:
    """Load evaluation.json from submission folder."""
    eval_path = os.path.join(submission_path, "evaluation.json")
    if not os.path.exists(eval_path):
        raise FileNotFoundError(f"Evaluation file not found: {eval_path}")
    
    with open(eval_path, "r") as f:
        return json.load(f)


def load_metadata(submission_path: str) -> Dict[str, Any]:
    """Load metadata.yaml from submission folder."""
    for ext in ["yaml", "yml"]:
        meta_path = os.path.join(submission_path, f"metadata.{ext}")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                return yaml.safe_load(f)
    return {}


def calculate_overall_score(metrics: Dict[str, Dict]) -> float:
    """Calculate weighted overall score from individual metrics."""
    total_weight = 0
    weighted_sum = 0
    
    for metric, weight in METRIC_WEIGHTS.items():
        if metric in metrics and "average" in metrics[metric]:
            weighted_sum += metrics[metric]["average"] * weight
            total_weight += weight
    
    return weighted_sum / total_weight if total_weight > 0 else 0


def get_resolved_stats(instance_results: Dict[str, Dict]) -> Dict[str, Any]:
    """Calculate resolved/failed instance statistics."""
    total = len(instance_results)
    resolved = sum(1 for r in instance_results.values() if r.get("resolved", False))
    failed = total - resolved
    
    # Count errors by type
    error_counts = {}
    for result in instance_results.values():
        error = result.get("error")
        if error:
            error_counts[error] = error_counts.get(error, 0) + 1
    
    return {
        "total": total,
        "resolved": resolved,
        "failed": failed,
        "resolve_rate": resolved / total if total > 0 else 0,
        "error_breakdown": error_counts
    }


def generate_results(submission_path: str) -> Dict[str, Any]:
    """Generate comprehensive results for a submission."""
    evaluation = load_evaluation(submission_path)
    metadata = load_metadata(submission_path)
    
    # Extract submission info
    submission_name = os.path.basename(submission_path.rstrip('/'))
    date_str = submission_name.split('_')[0]
    
    # Calculate metrics
    metrics = evaluation.get("metrics", {})
    overall_score = calculate_overall_score(metrics)
    
    # Get instance statistics
    instance_results = evaluation.get("instance_results", {})
    resolved_stats = get_resolved_stats(instance_results)
    
    # Build results object
    results = {
        "submission": submission_name,
        "model": evaluation.get("model", "unknown"),
        "method": evaluation.get("method", "unknown"),
        "dataset": evaluation.get("dataset", "design2code"),
        "timestamp": evaluation.get("timestamp", datetime.now().isoformat()),
        "metrics": {
            metric: {
                "average": metrics.get(metric, {}).get("average", 0),
                "min": min(metrics.get(metric, {}).get("scores", {0: 0}).values()),
                "max": max(metrics.get(metric, {}).get("scores", {0: 0}).values()),
            }
            for metric in METRICS if metric in metrics
        },
        "overall_score": overall_score,
        "instance_stats": resolved_stats,
        "metadata": {
            "model_name": metadata.get("model", {}).get("name", "Unknown"),
            "provider": metadata.get("model", {}).get("provider", "Unknown"),
            "method_name": metadata.get("method", {}).get("name", "Unknown"),
            "tags": metadata.get("tags", []),
            "organization": metadata.get("submission", {}).get("organization", "Unknown")
        }
    }
    
    return results


def save_results(submission_path: str, results: Dict[str, Any]) -> None:
    """Save results to submission folder."""
    results_dir = os.path.join(submission_path, "results")
    os.makedirs(results_dir, exist_ok=True)
    
    # Save main results
    results_path = os.path.join(results_dir, "results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    
    # Save metrics breakdown
    metrics_path = os.path.join(results_dir, "metrics_breakdown.json")
    with open(metrics_path, "w") as f:
        json.dump(results["metrics"], f, indent=2)


def print_results(results: Dict[str, Any]) -> None:
    """Print formatted results to console."""
    print(f"\nSubmission summary for {results['submission']} on Design2Code")
    print(DELIMITER)
    
    # Overall score
    print(f"Overall Score: {results['overall_score'] * 100:.2f}%")
    print(DELIMITER)
    
    # Individual metrics
    print("Metrics Breakdown:")
    for metric, values in results["metrics"].items():
        avg = values["average"] * 100
        print(f"  - {metric}: {avg:.2f}%")
    
    print(DELIMITER)
    
    # Instance stats
    stats = results["instance_stats"]
    print(f"Instance Statistics:")
    print(f"  - Total: {stats['total']}")
    print(f"  - Resolved: {stats['resolved']} ({stats['resolve_rate'] * 100:.1f}%)")
    print(f"  - Failed: {stats['failed']}")
    
    if stats["error_breakdown"]:
        print("  - Errors:")
        for error, count in stats["error_breakdown"].items():
            print(f"      {error}: {count}")
    
    print(DELIMITER)
    
    # Metadata
    meta = results["metadata"]
    print(f"Model: {meta['model_name']} ({meta['provider']})")
    print(f"Method: {meta['method_name']}")
    print(f"Organization: {meta['organization']}")
    if meta["tags"]:
        print(f"Tags: {', '.join(meta['tags'])}")


def main(submission_path: str) -> None:
    """Main entry point."""
    # Validate path
    submission_path = submission_path.rstrip('/')
    if not os.path.exists(submission_path):
        raise ValueError(f"Submission path does not exist: {submission_path}")
    
    # Generate and save results
    print(f"Processing submission: {submission_path}")
    results = generate_results(submission_path)
    save_results(submission_path, results)
    print_results(results)
    
    print(f"\nResults saved to: {os.path.join(submission_path, 'results')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate results for a Design2Code submission"
    )
    parser.add_argument(
        "submission_path",
        type=str,
        help="Path to the submission folder (e.g., evaluation/design2code/20251229_gpt4o_direct)"
    )
    args = parser.parse_args()
    main(args.submission_path)
