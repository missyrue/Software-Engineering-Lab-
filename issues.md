# Lab 5 Issue Table

The original locations below refer to the uncleaned `scholarship_system.py`
baseline and its initial Pylint, Bandit, and Flake8 reports. Final locations
refer to the cleaned `scholarship_system.py`; function names are used where
helpful so the references remain clear even when line numbers changed.

| Issue number | Tool | Original line number or function (baseline) | Issue description | Severity, where applicable | Fix applied (final source location) | Verification |
|---|---|---|---|---|---|---|
| 1 | Bandit B307 | `scholarship_system.py:12`, `calculate_merit_score` | `eval()` evaluated the user-configurable merit formula as unrestricted Python. | Medium | Replaced `eval()` with restricted AST validation and arithmetic evaluation in `_validate_expression`, `_parse_formula`, and `_evaluate_formula`; formulas with unsupported expressions or runtime errors are rejected. | Default and custom formulas passed focused checks; injected, unsupported, malformed, and divide-by-zero formulas were rejected. Final Bandit scan: no findings. |
| 2 | Bandit B110; Pylint W0702; Flake8 E722 | `scholarship_system.py:36-38`, `load_results` | A bare `except` swallowed every loading failure, and the file was read without a context manager or explicit encoding. | Low (Bandit B110); Pylint/Flake8 do not assign severity | `load_results` catches file, decoding, and JSON errors explicitly, reports them, validates that the JSON root is an object, and uses `with open(..., encoding="utf-8")`. | Missing, malformed, and wrong-shaped JSON inputs were tested; final Bandit scan: no findings. |
| 3 | Pylint W0102 | `scholarship_system.py:14`, `evaluate_applicant` | `logs=[]` shared a mutable list between calls. | Not assigned by Pylint | Changed the default to `None` and initializes a fresh list inside `evaluate_applicant`. | Repeated calls and the normal CLI run passed. |
| 4 | Pylint W0611; Flake8 F401 | `scholarship_system.py:2-3`, imports | `math` and `sys` were imported but unused. | Not assigned by these tools | Removed both unused imports. | Final Pylint report has no unused-import warning; final Flake8 report is empty. |
| 5 | Pylint C0103, W0622, C0121; Flake8 E712 | `scholarship_system.py:11,16,40,43`; `calculate_merit_score`, `evaluate_applicant`, `printShortlist` | `credits` shadowed a built-in name, `printShortlist` was not snake_case, and eligibility was compared to `True`. | Not assigned by these tools | Renamed the function to `print_shortlist`, updated its caller, renamed the local argument to `extracurricular_credits`, and used a truthiness check. | Final Pylint score: 9.90/10; final Flake8 report is empty; normal shortlist output was verified. |
| 6 | Pylint C0114/C0116 | Module and functions including `calculate_merit_score`, `evaluate_applicant`, `change_formula`, `persist_results`, `load_results`, `printShortlist`, and `main` | The module and functions lacked docstrings. | Not assigned by Pylint | Added a module docstring and concise function docstrings. | Final Pylint score: 9.90/10. |
| 7 | Pylint W1514/R1732 | `scholarship_system.py:29,36`, `persist_results` and `load_results` | File operations omitted an explicit encoding and did not consistently use context managers. | Not assigned by Pylint | Both JSON file operations now use context managers and UTF-8 encoding. | Normal persistence/load cycle passed; final Pylint has no encoding or resource-handling warning. |
| 8 | Pylint C0209 | `scholarship_system.py:21`, `evaluate_applicant` | Percent-style formatting could use an f-string. | Not assigned by Pylint | Replaced the formatting expression with an f-string. | Final Pylint report has no C0209 warning. |
| 9 | Flake8 E302/E305 | Baseline function boundaries at lines `11,14,24,28,33,40,46,59` | Function definitions and the end of the final function did not have the required blank-line spacing. | Flake8 does not assign severity | Corrected blank lines between top-level functions and after the final function. | The baseline report recorded these spacing violations; the final Flake8 report is empty. |
| 10 | Flake8 E501 | Formula helper lines `34,54,66,78` in the intermediate post-quality source before the final style commit | Four formula-helper lines exceeded the 79-character limit. These were found in the intermediate Flake8 run, not the initial baseline report. | Flake8 does not assign severity | Wrapped the conditions and error construction in the formula helpers. | Final Flake8 report is empty. |
| 11 | Pylint W0603 | Baseline `change_formula` and `load_results`; final `scholarship_system.py:108`, `change_formula` | Pylint flags the `global` statement used to update the configured formula. The `load_results` global was removed; the state-changing formula helper remains. | Not assigned by Pylint | Retained the existing formula-setting interface and behavior rather than adding an architectural change. | Final Pylint score is 9.90/10, above the 9.5 target; this one warning remains and is shown in `pylint_report.txt`. |

## Initial and final analysis results

| Tool | Initial baseline | Final |
|---|---|---|
| Pylint | 4.69/10 | 9.90/10 |
| Bandit | 2 findings: B307 (Medium) and B110 (Low) | 0 findings |
| Flake8 | 11 violations | 0 violations |
