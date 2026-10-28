# Lab 5 Reflection

The repository README refers to four reflection questions in the lab handout,
but the exact questions and handout are not present in the available repository
files. The following are concise answers to the relevant reflection topics;
they are not presented as verbatim questions from the manual.

## What is the purpose of static code analysis?

Static analysis checks source code without requiring the program to run through
every possible input. It can identify suspicious patterns, likely defects,
maintainability problems, and style violations early. In this screener, the
tools identified unsafe formula evaluation, swallowed file errors, a shared
mutable default, unused imports, and inconsistent formatting.

## How do Pylint, Bandit, and Flake8 differ?

Bandit focuses on security-relevant Python patterns and reported the use of
`eval()` and a broad exception handler. Pylint checks a wider range of code
quality concerns, including missing docstrings, mutable defaults, naming,
unused imports, and file handling, and also provides a score. Flake8 reports
style and common static-check violations such as unused imports, blank-line
spacing, bare exceptions, and Boolean comparisons. Their overlap helps check
the same code from different perspectives.

## What did fixing the reported issues demonstrate?

Replacing `eval()` required preserving the configurable arithmetic formula
while restricting which expressions could execute. Focused checks confirmed
that the default and a representative custom formula still work and that
unsupported or invalid formulas are rejected. Explicit JSON error reporting
also made missing and malformed files visible without silently discarding
existing results. The final normal run retained the expected sample shortlist.

## What are the limitations of automated analysis?

Static-analysis findings need human review: tools can identify risky patterns
but do not know whether the scholarship criteria or applicant data are
appropriate. Passing the tools does not prove correctness for every input or
runtime environment. Tests and review are still needed to verify intended
behavior. Pylint also reports one remaining `global`-statement warning for the
formula-setting helper; retaining the existing interface keeps this small lab
change focused while the score remains above the target.
