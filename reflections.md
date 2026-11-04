# Software Engineering Lab Reflections: Food Delivery System

## 1. Insights from Static Analysis Tools
* **Pylint & Flake8:** Running these tools highlighted the importance of adhering to standard Python coding conventions (PEP 8). Issues such as missing double blank lines between top-level functions (`E302`), lines exceeding 79 characters (`E501`), non-standard camelCase naming (`printQueue`), and unclosed file handlers were instantly brought to light. Consistent formatting significantly improves readability and team collaboration.
* **Bandit:** Using Bandit demonstrated how easy it is for high-severity security vulnerabilities to hide in working code. Specifically, identifying `pickle` deserialization issues (`B301`, `B403`) underscored why untrusted data serialization must be handled with secure formats like JSON.

## 2. Key Refactoring & Security Fixes
* **Replacing `pickle` with `json`:** Replaced insecure `pickle.dump()` and `pickle.load()` methods with standard JSON serialization (`json.dump` and `json.load`). This eliminates the risk of arbitrary code execution when loading backup order state.
* **Eliminating Bare Exceptions:** Replaced the generic `except:` block in `update_order_status()` with specific exception handling (`except KeyError:`). Silently ignoring all errors using `try-except-pass` hides critical runtime bugs and masks invalid operations.
* **Enforcing Context Managers:** Switched raw `open()` file operations to Python context managers (`with open(...) as f:`), guaranteeing that file descriptors are safely closed even if exceptions occur.

## 3. Challenges & Lessons Learned
* **Distinguishing Syntax Bugs from Logical Vulnerabilities:** Code can run without throwing runtime errors—such as assigning the invalid status `"teleported"` or silently defaulting missing menu item prices to `99`—while still being logically broken or insecure.
* **Automated Code Quality in CI/CD:** Integrating static analysis tools (`pylint`, `flake8`, `bandit`) early in the development lifecycle saves significant effort by catching formatting flaws and security vulnerabilities before code reaches production or code review.

## 4. Conclusion
Through this exercise, I learned that write-once execution is insufficient for production-grade software. Enforcing strict linting rules, proactively resolving security warnings, and documenting issues in `ISSUES.md` and `reflections.md` ensures that code remains secure, maintainable, and readable for team projects.
