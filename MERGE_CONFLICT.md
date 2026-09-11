# Merge Conflict Explanation

## What happened
Two feature branches were created independently from `develop`, and both
modified the same line in `app.py`:

- **`feature/version-bump`** changed `APP_VERSION` from `"1.0.0"` to `"1.1.0"`
  to reflect a new release.
- **`feature/version-format`** changed `APP_VERSION` from `"1.0.0"` to
  `"v1.0.0-stable"` to adopt a `v`-prefixed naming convention.

`feature/version-bump` was merged into `develop` first without issue.
When `feature/version-format` was then merged, Git could not automatically
reconcile the two changes to the same line and raised:

```
CONFLICT (content): Merge conflict in app.py
```

## How it was resolved
Both changes had valid intent — one updated the actual version number, the
other introduced a naming convention. The conflict was resolved manually by
combining both: keeping the bumped version number (`1.1.0`) while adopting
the `v`-prefix convention, resulting in:

```python
APP_VERSION = "v1.1.0"
```

After resolving the conflict in `app.py`, the existing test asserting the
old version string (`"1.0.0"`) was updated to expect `"v1.1.0"`, and the
full test suite was re-run to confirm all 4 tests still passed before the
merge was finalized.

## Why this matters
This reflects a realistic scenario: two engineers working in parallel on
related but distinct improvements to the same piece of code. Resolving it
required understanding the intent of both changes rather than blindly
picking one side, and verifying downstream tests still held after the fix.