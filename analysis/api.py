#!/usr/bin/env python
"""
Leaderboard API - Utility functions for website integration

This module provides functions that can be imported and used by web frameworks
(Flask, FastAPI, etc.) to serve leaderboard data.

Usage:
    from analysis.api import get_leaderboard_data, get_submission_details
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import yaml


class LeaderboardAPI:
    """API class for accessing leaderboard and submission data."""
    
    def __init__(self, evaluation_dir: str = "evaluation"):
        self.evaluation_dir = Path(evaluation_dir)
        self._cache = {}
        self._cache_time = {}
        self.cache_ttl = 300  # 5 minutes
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cache is still valid."""
        if key not in self._cache_time:
            return False
        elapsed = (datetime.now() - self._cache_time[key]).seconds
        return elapsed < self.cache_ttl
    
    def get_datasets(self) -> List[str]:
        """Get list of available datasets."""
        if not self.evaluation_dir.exists():
            return []
        return [d.name for d in self.evaluation_dir.iterdir() if d.is_dir()]
    
    def get_submissions(self, dataset: str) -> List[Dict[str, Any]]:
        """Get list of submissions for a dataset."""
        cache_key = f"submissions_{dataset}"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        dataset_path = self.evaluation_dir / dataset
        if not dataset_path.exists():
            return []
        
        submissions = []
        for sub_dir in sorted(dataset_path.iterdir(), reverse=True):
            if not sub_dir.is_dir():
                continue
            
            eval_path = sub_dir / "evaluation.json"
            if not eval_path.exists():
                continue
            
            try:
                with open(eval_path) as f:
                    eval_data = json.load(f)
                
                # Parse date from folder name
                date_str = sub_dir.name.split('_')[0]
                try:
                    date = datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
                except ValueError:
                    date = "Unknown"
                
                submissions.append({
                    "id": sub_dir.name,
                    "model": eval_data.get("model", "Unknown"),
                    "method": eval_data.get("method", "Unknown"),
                    "date": date,
                    "path": str(sub_dir)
                })
            except Exception:
                continue
        
        self._cache[cache_key] = submissions
        self._cache_time[cache_key] = datetime.now()
        return submissions
    
    def get_submission_details(self, dataset: str, submission_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information for a specific submission."""
        sub_path = self.evaluation_dir / dataset / submission_id
        if not sub_path.exists():
            return None
        
        result = {
            "id": submission_id,
            "dataset": dataset,
            "evaluation": None,
            "metadata": None,
            "results": None,
            "readme": None
        }
        
        # Load evaluation.json
        eval_path = sub_path / "evaluation.json"
        if eval_path.exists():
            with open(eval_path) as f:
                result["evaluation"] = json.load(f)
        
        # Load metadata
        for ext in ["yaml", "yml"]:
            meta_path = sub_path / f"metadata.{ext}"
            if meta_path.exists():
                with open(meta_path) as f:
                    result["metadata"] = yaml.safe_load(f)
                break
        
        # Load results
        results_path = sub_path / "results" / "results.json"
        if results_path.exists():
            with open(results_path) as f:
                result["results"] = json.load(f)
        
        # Load README
        readme_path = sub_path / "README.md"
        if readme_path.exists():
            with open(readme_path) as f:
                result["readme"] = f.read()
        
        return result
    
    def get_leaderboard(self, dataset: str) -> Dict[str, Any]:
        """Get leaderboard data for a dataset."""
        cache_key = f"leaderboard_{dataset}"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        # Try to load from pre-generated file
        leaderboard_path = Path("data") / f"{dataset}-leaderboard.json"
        if leaderboard_path.exists():
            with open(leaderboard_path) as f:
                leaderboard = json.load(f)
                self._cache[cache_key] = leaderboard
                self._cache_time[cache_key] = datetime.now()
                return leaderboard
        
        # Generate on the fly
        from .get_leaderboard import generate_leaderboard
        leaderboard = generate_leaderboard(dataset, str(self.evaluation_dir))
        
        self._cache[cache_key] = leaderboard
        self._cache_time[cache_key] = datetime.now()
        return leaderboard
    
    def get_metrics_comparison(
        self,
        dataset: str,
        submission_ids: List[str]
    ) -> Dict[str, Any]:
        """Compare metrics across multiple submissions."""
        comparison = {
            "submissions": submission_ids,
            "metrics": {}
        }
        
        for sub_id in submission_ids:
            details = self.get_submission_details(dataset, sub_id)
            if not details or not details["evaluation"]:
                continue
            
            metrics = details["evaluation"].get("metrics", {})
            for metric, data in metrics.items():
                if metric not in comparison["metrics"]:
                    comparison["metrics"][metric] = {}
                comparison["metrics"][metric][sub_id] = data.get("average", 0)
        
        return comparison
    
    def search_submissions(
        self,
        dataset: str,
        query: Optional[str] = None,
        model: Optional[str] = None,
        method: Optional[str] = None,
        org: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Search submissions with filters."""
        submissions = self.get_submissions(dataset)
        results = []
        
        for sub in submissions:
            details = self.get_submission_details(dataset, sub["id"])
            if not details:
                continue
            
            # Apply filters
            if model and model.lower() not in sub["model"].lower():
                continue
            if method and method.lower() != sub["method"].lower():
                continue
            
            metadata = details.get("metadata", {})
            if org:
                sub_org = metadata.get("submission", {}).get("organization", "")
                if org.lower() not in sub_org.lower():
                    continue
            
            if tags:
                sub_tags = [t.lower() for t in metadata.get("tags", [])]
                if not all(t.lower() in sub_tags for t in tags):
                    continue
            
            if query:
                # Search in model name, method, org
                searchable = f"{sub['model']} {sub['method']} {metadata}"
                if query.lower() not in searchable.lower():
                    continue
            
            results.append(sub)
        
        return results


# Convenience functions for direct import
_api = None

def get_api() -> LeaderboardAPI:
    """Get or create the global API instance."""
    global _api
    if _api is None:
        _api = LeaderboardAPI()
    return _api


def get_leaderboard_data(dataset: str = "design2code") -> Dict[str, Any]:
    """Get leaderboard data for website."""
    return get_api().get_leaderboard(dataset)


def get_submission_details(dataset: str, submission_id: str) -> Optional[Dict[str, Any]]:
    """Get details for a specific submission."""
    return get_api().get_submission_details(dataset, submission_id)


def get_all_datasets() -> List[str]:
    """Get list of all available datasets."""
    return get_api().get_datasets()
