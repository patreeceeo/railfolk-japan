# Absolute Dictates

Consider the following for every code change.

1. YAGNI - Don't build it until you need it
2. DRY - Refactor after the second duplication
3. Delete aggressively - Less code means less bugs
4. KISS - Always choose the simpler option, all other things being equal
5. Fail fast - Early, explicit errors are better than late, subtle failures
6. Use explicit, self-documenting names. For example, a name like "wait-until-process-exits" is better than "wait"
    * Use docstrings and comments for anything that still isn't obvious
8. Suppress agreeableness. In a partnership where the two partners always agree, one of them is unnecessary.
9. Keep dependencies explicit, preferably as code.
10. Beware of null/nil/None, the "billion dollar mistake"! Favor monads like Result, and more descriptive monads like Artist = (Specified string | Unspecified) over generic ones like Maybe.
11. Focus. Never do more than one thing at a time. If it's not relevant to the task at hand, don't do it.
