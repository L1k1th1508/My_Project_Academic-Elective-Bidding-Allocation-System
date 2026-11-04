# Issues Report

| Issue | Type | Line(s) | Description | Fix Approach |
| --- | --- | --- | --- | --- |
| Insecure Object Deserialization (`pickle`) | Security (Bandit B301, B403 - Medium Severity) | 2, 44, 49 | `pickle.dump()` and `pickle.load()` allow arbitrary code execution when restoring untrusted data files. | Replace `pickle` with `json` (`json.dump` / `json.load`) for safe file-based data persistence. |
| Bare `try-except-pass` Block | Security / Bug (Bandit B110, Flake8 E722 - Low Severity) | 24–25 | Catching all exceptions with a bare `except:` and `pass` silently suppresses error details and masks unexpected bugs. | Catch specific exceptions (e.g., `except KeyError:`) and handle or log invalid order lookups. |
| Unvalidated Order Status Assignment | Logic Bug | 21–25, 62 | `update_order_status` accepts invalid status values like `"teleported"`, ignoring the defined `VALID_STATUSES` list. | Validate that `status in VALID_STATUSES` before updating the order status dictionary. |
| Mutable Default Argument | Logic Bug / Code Quality | 11 | Using `order_history=[]` as a default argument retains list state across multiple function calls. | Change default parameter to `order_history=None` and initialize `if order_history is None: order_history = []` inside the function. |
| Unclosed File Handles | Code Quality | 30, 49 | Opening files directly using `open(...)` without context managers risks leaving file descriptors open if exceptions occur. | Refactor file operations to use context managers (`with open(...) as f:`). |
| PEP 8 Spacing and Naming Violations | Style (Flake8 E302, E305, E501) | 11, 21, 51, 70 | Missing double blank lines between functions, camelCase naming (`printQueue`), and line lengths exceeding 79 characters. | Add 2 blank lines between top-level functions, rename to `print_queue`, and format lines to under 79 characters. |
