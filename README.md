# Design2Code Experiments

This repository contains records of submissions to the Design2Code leaderboard, similar to [SWE-bench/experiments](https://github.com/SWE-bench/experiments).

## 📁 Repository Structure

```
webpai-experiment/
├── evaluation/                    # Model submissions organized by dataset
│   └── design2code/               # Design2Code benchmark submissions
│       ├── 20251210_gpt4o_mark/
│       │   ├── evaluation.json    # Evaluation metrics
│       │   ├── metadata.yaml      # Submission metadata
│       │   ├── README.md          # Approach description
│       │   └── results/           # Generated results
│       └── ...
│
├── analysis/                      # Analysis scripts
│   ├── __init__.py
│   ├── get_results.py             # Process individual submission
│   ├── get_leaderboard.py         # Generate leaderboard data
│   ├── process_all.py             # Batch process all submissions
│   ├── compare.py                 # Compare submissions
│   └── api.py                     # API for website integration
│
├── data/                          # Generated leaderboard data
│   └── design2code-leaderboard.json
│
├── checklist.md                   # Submission requirements
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🔎 Viewing Results

### Get Results for a Submission

```bash
python -m analysis.get_results evaluation/design2code/<submission>

# Example
python -m analysis.get_results evaluation/design2code/20251210_gpt4o_mark
```

### Generate Leaderboard

```bash
python -m analysis.get_leaderboard

# With custom output
python -m analysis.get_leaderboard --output data/leaderboard.json
```

### Compare Submissions

```bash
python -m analysis.compare 20251210_gpt4o_mark 20251229_gpt4o_direct
```

### Process All Submissions

```bash
python -m analysis.process_all
```

## 🏆 Leaderboard Participation

To submit to the Design2Code leaderboard:

1. **Fork** this repository
2. **Create** a new folder under `evaluation/design2code/` with format: `YYYYMMDD_modelname_method`
3. **Add** required files:
   - `evaluation.json` - Evaluation metrics
   - `metadata.yaml` - Submission metadata
   - `README.md` - Approach description
4. **Run** validation:
   ```bash
   python -m analysis.get_results evaluation/design2code/YOUR_SUBMISSION
   ```
5. **Create** a Pull Request

See [checklist.md](checklist.md) for detailed submission requirements.

## 📊 Metrics

Submissions are evaluated on:

| Metric | Description |
|--------|-------------|
| **CLIP** | Visual similarity using CLIP embeddings |
| **SSIM** | Structural similarity index |
| **Text Similarity** | Text content matching accuracy |
| **Position Accuracy** | Element positioning accuracy |
| **Image Reproduction** | Image element reproduction quality |

**Overall Score** = Weighted average (20% each)

## 🔧 API Usage

For website integration:

```python
from analysis.api import get_leaderboard_data, get_submission_details

# Get leaderboard
leaderboard = get_leaderboard_data("design2code")

# Get submission details
details = get_submission_details("design2code", "20251210_gpt4o_mark")
```

## 📋 Example Submission Structure

```
evaluation/design2code/20251210_gpt4o_mark/
├── evaluation.json      # Required: Metrics data
├── metadata.yaml        # Required: Model/method info
├── README.md            # Required: Approach description
├── trajs/               # Optional: Reasoning traces
│   ├── instance_0.json
│   └── ...
└── outputs/             # Optional: Generated code
    ├── instance_0.html
    └── ...
```

## 📞 Contact

For questions, please create an issue in this repository.

## ✍️ Citation

If you use this repository, please cite:

```bibtex
@misc{design2code-experiments,
  title={Design2Code Experiments},
  year={2025},
  url={https://github.com/your-org/webpai-experiment}
}
```
