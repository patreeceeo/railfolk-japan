# Absolute Dictates

Consider the following for every code change.

1. YAGNI - Don't build it until you need it
2. DRY - Refactor after the second duplication
3. Delete aggressively - Less code means less bugs
4. KISS - Always choose the simpler option, all other things being equal
5. Fail fast - Early, explicit errors are better than late, subtle failures
6. Use explicit, self-documenting names. For example, a name like "wait-until-process-exits" is better than "wait"
7. Suppress agreeableness. In a partnership where the two partners always agree, one of them is unnecessary.
    * Use docstrings and comments for anything that still isn't obvious
8. Explicit dependencies. Add binary deps to flake.nix and Java/Clojure deps to the appropriate file.
9. Beware of null/nil/None, the "billion dollar mistake"! Favor monads like Result, and more descriptive monads like Artist = (Specified string | Unspecified) over generic ones like Maybe.
10. Focus. Never do more than one thing at a time. If it's not relevant to the task at hand, don't do it.