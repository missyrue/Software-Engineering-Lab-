# Lab 5 Deliverables

## Objective

Static analysis uses automated tools to identify security, correctness, and style issues early. This lab applies Bandit, Pylint, and Flake8 to improve the scholarship screener while preserving its scoring formula, criteria, sample applicants, and normal output.

## Issues and fixes

| Issue type/tool | Location | Description | Severity | Fix applied | Verification |
|---|---|---|---|---|---|
| Bandit B307 | `scholarship_system.py:12` (baseline) | `eval()` executed the configurable formula as unrestricted Python. | Medium | Replaced it with a restricted AST evaluator supporting only numeric constants, `gpa`, `credits`, and basic arithmetic; invalid formulas are reported and rejected. | Default and custom formulas passed; unsupported, injected, malformed, and divide-by-zero formulas were rejected. Final Bandit report has no findings. |
| Bandit B110 | `scholarship_system.py:37` (baseline) | A bare `except` swallowed JSON-loading errors. | Low | Catch file, decoding, and JSON errors explicitly and report them; reject non-object JSON without replacing current results. | Missing, malformed, and wrong-shaped JSON inputs were tested; final Bandit report has no findings. |
| Pylint W0102 | `scholarship_system.py:14` (baseline) | `logs=[]` shared a mutable list across calls. | — | Use `None` and create a fresh list inside `evaluate_applicant`. | Repeated calls and the normal CLI run passed. |
| Pylint C0114/C0116 | Module and functions (baseline) | Missing module and function documentation. | — | Added concise docstrings. | Final Pylint score is 9.90/10. |
| Pylint C0103/W0622/C0121 | `printShortlist`, `credits`, and `eligible == True` (baseline) | Non-snake-case naming, built-in-name shadowing, and Boolean equality. | — | Renamed the function and local parameter; updated call sites; test eligibility by truthiness. | Final Flake8 report is empty; normal shortlist output is unchanged. |
| Pylint W1514/R1732 | `scholarship_system.py:29,36` (baseline) | File operations omitted an encoding and did not consistently use context managers. | — | Use UTF-8 and `with` for reading and writing JSON. | Normal persistence/load cycle passed. |
| Flake8 E501 | Formula helper lines 34, 54, 66, 78 (before final style fix) | Four lines exceeded the configured 79-character limit. | — | Wrapped conditions and error construction without changing behavior. | Final Flake8 report is empty. |

## Reflection

The repository includes no exact handout reflection questions; these are original answers to relevant topics, not quoted prompts.

1. **Usefulness:** Static analysis quickly found problems that could be missed in a normal run, including unsafe formula evaluation, swallowed file errors, and a shared mutable default. Fixing them improved safety and maintainability.
2. **Tool differences:** Bandit focuses on security patterns, Pylint checks broader code quality and reports a score, and Flake8 enforces Python style and common static checks. Their overlap helped identify issues from different perspectives.
3. **Limitations:** Tools report patterns rather than understanding the full application intent. They cannot prove that the scholarship criteria are correct, and findings still need context and runtime checks.
4. **Application:** The restricted evaluator and focused invalid-input checks demonstrate why passing the tools alone is not enough. Normal CLI tests also confirmed the default and custom formulas preserve the expected behavior.

## Results

| Tool | Initial result | Final result |
|---|---|---|
| Pylint | 4.69/10 | 9.90/10 |
| Bandit | 2 findings: B307 (Medium) and B110 (Low) | 0 findings |
| Flake8 | 11 violations | 0 violations |

The final Pylint report retains one `W0603` warning for `change_formula` updating the configured formula. This preserves the existing state-changing helper and CLI behavior; the final score exceeds the lab target.

### Commits

1. `Fix Bandit security findings` — `6545303bc00e68312e51ac1d47be777287a50f5b`
2. `Improve Pylint code quality` — `31037bbc749de746d6659cb14f5746b5e49d0f15`
3. `Fix Flake8 style violations` — see git log -3 --oneline for the final commit hash.
