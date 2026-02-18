## Large Numbers

This package provides utilities and reference implementations for working with very large and transfinite numbers, including aleph (cardinality) numbers and hyperoperations (tetration and beyond).

**Contents**
- `aleph_number.py`: utilities and classes for representing aleph numbers (e.g. $\\aleph_0$, $\\aleph_{n}$).
- `hyperoperation.py`: implementations and helpers for hyperoperations such as tetration ($x\\uparrow\\uparrow y$) and higher.

**Overview**
An aleph number ($\\aleph$) denotes the cardinality of infinite sets. For example, $\\aleph_0$ is the cardinality of the set of natural numbers. Higher alephs ($\\aleph_{n+1}$) describe larger well-ordered infinite cardinalities.

Hyperoperations form a hierarchy of operations that extend addition, multiplication, and exponentiation. Tetration is the next level after exponentiation and is often written as $x\\uparrow\\uparrow y$ or as an iterated power $^y x$; these grow extremely rapidly even for small inputs.

**Examples**
The modules in this folder are intended for exploration and education rather than arbitrary-precision arithmetic in production.

Basic usage (illustrative):

```python
# Import the module(s) you need
from large_numbers import aleph_number, hyperoperation

# Example: inspect or construct an aleph symbol (API depends on module)
# aleph = aleph_number.Aleph(0)  # represents $\\aleph_0$

# Example: compute a small hyperoperation/tetration (API depends on module)
# result = hyperoperation.tetration(3, 2)  # represents 3 \\uparrow\\uparrow 2
```

Refer to the module docstrings and the unit tests for precise usage examples and expected behavior.

**Installation**
- Install requirements from the repository root:

```bash
pip install -r requirements.txt
```

**Running tests**
- Run the test suite (from the repository root):

```bash
pytest tests/large_numbers
```

**Contributing**
- Contributions and improvements are welcome. Please open a pull request with a clear description and include tests for new behaviors.

**References & Notes**
- Aleph numbers and cardinalities: standard set theory texts.
- Hyperoperations and tetration: see literature on large-number notation and combinatorial number theory.

**License**
- See the repository LICENSE or project root documentation for license details.