# SWE-bench Experiments Repository Summary

## Overview

The **[SWE-bench/experiments](https://github.com/SWE-bench/experiments)** repository is the official archive for submissions to the [SWE-bench](https://swe-bench.github.io/) leaderboard. It contains open-sourced predictions, execution logs, reasoning trajectories, and evaluation results from various AI models and agents attempting to solve real-world software engineering tasks.

**Repository Stats:**
- ⭐ 232 stars | 👁️ 9 watchers | 🍴 278 forks
- 👥 123+ contributors
- Languages: Shell (89%), Python (11%)

---

## What is SWE-bench?

SWE-bench is a benchmark for evaluating AI systems on their ability to solve real-world GitHub issues. It tests whether AI models/agents can:
- Understand issue descriptions and codebase context
- Generate correct code patches to fix bugs or implement features
- Produce patches that pass the project's test suite

---

## Repository Structure

```
experiments/
├── evaluation/                    # Model submissions organized by benchmark split
│   ├── lite/                      # SWE-bench Lite (300 instances)
│   ├── verified/                  # SWE-bench Verified (500 instances)
│   ├── test/                      # SWE-bench Full Test (2294 instances)
│   ├── multimodal/                # SWE-bench Multimodal (517 instances)
│   └── bash-only/                 # Bash-only submissions
│
├── analysis/                      # Scripts for analyzing submissions
│   ├── get_results.py             # Generate submission results & statistics
│   ├── download_logs.py           # Download logs/trajectories from S3
│   ├── get_leaderboard.py         # Generate leaderboard data
│   ├── detect_similarity.py       # Detect similar submissions
│   └── pre_v2/                    # Legacy analysis scripts
│
├── validation/                    # Validation logs for dev/test splits
│   ├── dev/
│   └── test/
│
├── README.md                      # Main documentation
└── checklist.md                   # Submission checklist guidelines
```

---

## Benchmark Splits

| Split | # Instances | Description |
|-------|-------------|-------------|
| **Lite** | 300 | Curated subset of easier, well-defined tasks |
| **Verified** | 500 | Human-verified subset for reliable evaluation |
| **Multilingual** | 300 | Multi-language tasks |
| **Test** | 2,294 | Full test benchmark |
| **Multimodal** | 517 | Tasks requiring multimodal understanding |

---

## Submission Format

Each submission folder (`evaluation/<split>/<YYYYMMDD_model_name>/`) contains:

| File/Folder | Description |
|-------------|-------------|
| `all_preds.jsonl` or `preds.json` | Model predictions for each instance |
| `metadata.yaml` | Submission metadata (model info, hyperparameters, etc.) |
| `README.md` | Description of the approach/method |
| `trajs/` | Reasoning traces showing how the system solved each task |
| `logs/` | Execution logs with evaluation artifacts |
| `results/` | Generated results (resolved counts, breakdowns by repo/time) |

### Logs Folder Structure
Each instance in `logs/` contains:
- `patch.diff` - The generated code patch
- `test_output.txt` - Test execution output
- `report.json` - Evaluation outcome summary

---

## Key Analysis Tools

### 1. Get Results
```bash
python -m analysis.get_results evaluation/<split>/<submission>
```
Generates statistics including:
- Total resolved instances (% resolved)
- Breakdown by repository
- Breakdown by issue creation year

### 2. Download Logs & Trajectories
```bash
python -m analysis.download_logs evaluation/<split>/<submission>
```
Downloads logs and reasoning traces from the public S3 bucket (`swe-bench-experiments`).

### 3. Generate Leaderboard Data
```bash
python -m analysis.get_leaderboard
```
Produces JSON data for the official leaderboard website.

---

## How to Submit to the Leaderboard

### For SWE-bench Lite, Verified, Multilingual:

1. **Fork** this repository
2. **Create a folder** under the appropriate split:
   - Format: `evaluation/<split>/<YYYYMMDD_model_name>/`
   - Example: `evaluation/lite/20240415_sweagent_gpt4/`
3. **Add required files**: predictions, metadata, README, trajectories, logs
4. **Run** `python -m analysis.get_results evaluation/<split>/<submission>`
5. **Create a Pull Request**

### For SWE-bench Multimodal:
- Use the [sb-cli](https://github.com/swe-bench/sb-cli/) tool
- Follow instructions at [swebench.com](https://www.swebench.com/sb-cli/submit-to-leaderboard/)

---

## Submission Policy (as of Nov 2025)

> **Important:** SWE-bench Verified and Multilingual now **only accepts submissions from academic teams and research institutions** with:
> - Open source methods
> - Peer-reviewed publications

---

## Result Verification

To receive a "verified" checkmark on your submission:
1. Create an issue in the repository
2. Provide instructions on how to run your model
3. The team will run your model on a random subset to verify results

---

## Reasoning Traces Requirement

Since July 2024, submissions **must include reasoning traces** (`trajs/` folder) showing:
- How the system analyzed the problem
- The decision-making process
- Actions taken to generate the patch

This provides transparency into cutting-edge methods without requiring full code release.

---

## Example Submissions

Notable submissions in the repository include:
- **SWE-agent** (with various LLM backends: GPT-4, Claude, etc.)
- **Agentless** / Agentless-Lite
- **Amazon Q Developer Agent**
- **Lingma Agent**
- **OpenHands**
- **Harness AI**
- **Various research prototypes** from academic institutions

---

## Contact

- **Issues**: [GitHub Issues](https://github.com/SWE-bench/experiments/issues)
- **Email**: johnby@stanford.edu, carlosej@princeton.edu

---

## Citation

If using this repository for academic purposes, cite the main [SWE-bench paper](https://github.com/SWE-bench/SWE-bench?tab=readme-ov-file#%EF%B8%8F-citation).

---

## Related Resources

- **Main SWE-bench Repository**: [github.com/swe-bench/SWE-bench](https://github.com/swe-bench/SWE-bench)
- **SWE-bench CLI Tool**: [github.com/swe-bench/sb-cli](https://github.com/swe-bench/sb-cli)
- **Leaderboard Website**: [swe-bench.github.io](https://swe-bench.github.io/)
