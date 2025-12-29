# GPT-4o Direct Prompting - Design2Code

## Model Information
- **Model**: GPT-4o (2024-11-20)
- **Provider**: OpenAI
- **Method**: Direct Prompting

## Approach
This submission uses GPT-4o's vision capabilities with direct prompting to convert design images to HTML/CSS code.

### Prompt Template
```
Given the following design image, generate the corresponding HTML and CSS code that accurately reproduces the design.
```

## Results

| Metric | Score |
|--------|-------|
| CLIP | 61.22% |
| SSIM | 45.33% |
| Text Similarity | 46.44% |
| Position Accuracy | 54.11% |
| Image Reproduction | 82.77% |
| **Overall** | **60.55%** |

## Checklist
- [x] Pass@1 submission
- [x] Does not use test set labels
- [x] Reproducible results
- [ ] Open source code

## Citation
```bibtex
@article{openai2024gpt4o,
  title={GPT-4o Technical Report},
  author={OpenAI},
  year={2024}
}
```
