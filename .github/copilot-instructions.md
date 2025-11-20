# Copilot instructions for this repository

This repository contains small, self-contained implementations of Lipschitz-aware global optimization algorithms (DOO variants and a simple zooming routine). The guidance below highlights repository-specific APIs, conventions, and quick run/debug steps so an AI coding agent can be productive immediately.

**Project Purpose**: Implement and experiment with deterministic optimistic optimization (DOO) and related 1D discrete/zooming routines for Lipschitz-continuous functions. Key files: `doo_opt.py`, `doo_discrete.py`, `zooming_opt.py`.

**Structure / Big Picture**:
- `doo_opt.py`: Continuous-space DOO implementation. Main class `DOO` encapsulates algorithm state, evaluation history, and priority queue of cells.
- `doo_discrete.py`: Integer / 1D discrete variant. Class `DiscreteDOO` exposes the same high-level `optimize()` API but expects scalar integer inputs.
- `zooming_opt.py`: A small, experimental zooming-style routine (`zooming` function) used in the included Jupyter notebook examples.

**Important API patterns & types (copyable examples)**
- Continuous DOO (multi-dim):
  ```python
  from doo_opt import DOO
  import numpy as np

  def f(x: np.ndarray):
      return -np.sum(x**2)

  bounds = [[-1.0, 1.0], [0.0, 2.0]]  # shape (dim, 2)
  opt = DOO(f, k=1.0, bounds=bounds, max_evals=200)
  best_point, best_value = opt.optimize()
  ```
- Discrete DOO (1D integer):
  ```python
  from doo_discrete import DiscreteDOO
  def f_int(x: int):
      return float(x % 10)

  opt = DiscreteDOO(f_int, k=0.01, low=1, high=999, max_evals=100)
  best_x, best_val = opt.optimize()
  ```
- Zooming helper: `zooming(n, f_real, L, low, high, N)` — used in `test.ipynb` where `f_real` is a Python list of sampled values.

**Conventions & patterns to preserve**
- `DOO` expects `bounds` as a list/array of shape `(dim, 2)` and `f` to accept a NumPy array of length `dim`.
- `DiscreteDOO.f` expects a scalar (integer), callers should `int()` or clip inputs as done in the implementation.
- The DOO implementations use a heap of tuples `(-upper_bound, counter, node)` (negative upper bound so heapq acts as max-heap). Preserve the 3-tuple format when modifying queue logic.
- Many inline comments and docstrings are in Chinese — keep language/terminology consistent when editing.

**Developer workflows**
- Install dependencies (recommended):
  ```powershell
  python -m pip install --user numpy matplotlib
  ```
- Run the simple notebook example: open `test.ipynb` in VS Code or Jupyter; it imports `DiscreteDOO` and `zooming` and contains runnable examples.
- Quick script run (1-file example):
  ```powershell
  python -c "from doo_discrete import DiscreteDOO; import numpy as np; print('See docs in .github/copilot-instructions.md')"
  ```

**Integration & external deps**
- Minimal external dependencies: `numpy` and `matplotlib` (only used for plotting in the notebook/experiments). There are no external web services or databases.

**Where to look when changing algorithm logic**
- `doo_opt.py`: splitting logic is in `_split_node`, diameter in `_diameter`, evaluation bookkeeping in `_evaluate`. Tests (if added) should assert `best_value` and `best_point` invariants.
- `doo_discrete.py`: `_evaluate` caches values in `self.evaluated`; rely on that cache to avoid re-evaluating expensive functions.
- `zooming_opt.py` and `test.ipynb`: examples demonstrating index-based usage and data layout for `f_real`.

**Safety / Do not change**
- Do not change the heap tuple ordering or remove the `cell/ node counter` used to break ties — this preserves deterministic behavior.
- Avoid changing public method signatures: `DOO.__init__(f,k,bounds,max_evals)` and `optimize()`; `DiscreteDOO.__init__(f,k,low,high,max_evals)` and `optimize()`.

If anything in these instructions is unclear or you want more examples (e.g., unit-test scaffolding or a small runner script), tell me which part and I will iterate.
