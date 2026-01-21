# Towncrier changelog fragments

This directory contains changelog entries managed by towncrier.

Fragments are named: `<ISSUE_NUMBER>.<TYPE>.rst`

Types:
- `feature`: New features
- `bugfix`: Bug fixes
- `doc`: Documentation changes
- `removal`: Deprecations and removals
- `misc`: Misc changes (internal, refactoring, etc.)

Example:
```
changelog/123.feature.rst
```

Content:
```rst
Add automated changelog management (#123)
```

These fragments are automatically collected and compiled into CHANGELOG.rst
when making a new release using `towncrier build`.
