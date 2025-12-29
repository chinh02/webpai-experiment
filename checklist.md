# Design2Code Experiments - Submission Checklist

This document outlines the requirements for submitting to the Design2Code leaderboard.

## 📋 Required Files

Your submission folder should be named: `YYYYMMDD_modelname_method`
(e.g., `20251229_gpt4o_direct`)

### 1. `evaluation.json` (Required)

Contains evaluation metrics for your submission:

```json
{
  "dataset": "design2code",
  "model": "model-name",
  "method": "method-name",
  "run_id": "unique_run_identifier",
  "timestamp": "2025-12-29T10:00:00Z",
  "metrics": {
    "clip": {
      "scores": {"0": 0.65, "1": 0.72, ...},
      "average": 0.68
    },
    "ssim": {
      "scores": {"0": 0.45, "1": 0.52, ...},
      "average": 0.48
    },
    "text_similarity": {
      "scores": {"0": 0.55, "1": 0.62, ...},
      "average": 0.58
    },
    "position_accuracy": {
      "scores": {"0": 0.52, "1": 0.58, ...},
      "average": 0.55
    },
    "image_reproduction": {
      "scores": {"0": 0.82, "1": 0.88, ...},
      "average": 0.85
    }
  },
  "instance_results": {
    "0": {"resolved": true, "error": null},
    "1": {"resolved": false, "error": "timeout"},
    ...
  }
}
```

### 2. `metadata.yaml` (Required)

Contains submission metadata:

```yaml
model:
  name: GPT-4o
  version: "2024-11-20"
  provider: OpenAI
  type: commercial  # or "open-source"

method:
  name: direct  # direct, cot, mark, etc.
  description: Direct prompting without chain-of-thought

submission:
  date: "2025-12-29"
  author: "Your Name"
  email: "your.email@example.com"
  organization: "Your Organization"

evaluation:
  dataset: design2code
  split: test
  num_instances: 20

hyperparameters:
  temperature: 0.0
  max_tokens: 4096
  top_p: 1.0

tags:
  - GPT
  - Multimodal
  - Commercial
  - Vision

notes: |
  Brief description of your approach and any special considerations.
```

### 3. `README.md` (Required)

A description of your submission including:

- Model information
- Approach/method description
- Results summary table
- Any notable findings
- Citation (if applicable)

### 4. `trajs/` (Recommended)

Reasoning traces for each instance (optional but encouraged):

```
trajs/
├── instance_0.json
├── instance_1.json
└── ...
```

### 5. `outputs/` (Recommended)

Generated HTML/CSS outputs:

```
outputs/
├── instance_0.html
├── instance_1.html
└── ...
```

---

## 📊 Metrics

Your submission will be evaluated on the following metrics:

| Metric | Description | Weight |
|--------|-------------|--------|
| CLIP | Visual similarity using CLIP embeddings | 20% |
| SSIM | Structural similarity index | 20% |
| Text Similarity | Text content matching accuracy | 20% |
| Position Accuracy | Element positioning accuracy | 20% |
| Image Reproduction | Image element reproduction quality | 20% |

**Overall Score** = Weighted average of all metrics

---

## ✅ Submission Checklist

Before submitting, ensure:

- [ ] Folder name follows format: `YYYYMMDD_modelname_method`
- [ ] `evaluation.json` contains all required metrics
- [ ] `metadata.yaml` contains all required fields
- [ ] `README.md` describes your approach
- [ ] All metric scores are between 0 and 1
- [ ] Instance results include all test instances
- [ ] No test set labels were used during generation
- [ ] Results are reproducible

---

## 🚀 How to Submit

1. **Fork** this repository
2. **Create** your submission folder under `evaluation/design2code/`
3. **Add** all required files
4. **Run** validation:
   ```bash
   python -m analysis.get_results evaluation/design2code/YOUR_SUBMISSION
   ```
5. **Create** a Pull Request

---

## ⚠️ Important Notes

- **Pass@1 Only**: Only single-attempt submissions are accepted
- **No Test Labels**: Do not use ground truth labels during generation
- **Reproducibility**: Provide sufficient details to reproduce results
- **One Submission Per PR**: Submit one model/method combination per PR

---

## 📞 Questions?

Create an issue in this repository or contact the maintainers.
