# L6_L7_11 — Amusement Park Ride Access

Lab 7: Fuzz Testing with Hypothesis

## About

A set of property-based fuzz tests targeting rider height/fastpass specifications, dispatch throughput calculations, and safety restraint codes to expose edge-case bugs.

## Completed work

- `processor.py` validates malformed and unexpected inputs without uncaught exceptions.
- `test_processor.py` uses Hypothesis to fuzz all three public functions with arbitrary text and `None`.
- `Lab_7_FuzzTesting_Report_PES2UG24CS013.pdf` documents the discovered failures, fixes, and before/after command output.
- `reports/` contains the evidence images and raw command logs.

Invalid rider specifications return `Invalid rider specification`; invalid throughput input returns `None`; unknown restraint zones return `Unknown ride zone`. Valid input behavior is unchanged.

To reproduce the final test result, install `hypothesis` and `pytest`, then run `python -m pytest -q test_processor.py` from this folder.

## Files

| File | Description |
|------|-------------|
| `processor.py` | The module under test (buggy starter code) |
| `test_processor.py` | Starter test file to complete using Hypothesis |

Keep all your Lab 7 work in this `LAB7` folder.

Refer to the lab handout for instructions.
