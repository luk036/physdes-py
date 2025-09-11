# Gemini Code Assistant Context

## Project Overview

This is a Python project named `physdes-py`, designed for computational geometry tasks related to VLSI physical design. The core focus of the project is to provide a robust and efficient library for working with rectilinear polygons.

The project is structured using PyScaffold, a tool that helps in setting up a standard Python project structure. It includes a `src` directory for the source code, a `tests` directory for the tests, and a `docs` directory for the documentation.

The codebase is well-documented with docstrings and examples, which makes it easy to understand and use. The project also includes a comprehensive test suite using `pytest` and `hypothesis`.

## Building and Running

### Dependencies

The project's dependencies are listed in the `setup.cfg` file. The main dependencies are:

*   `importlib-metadata`
*   `typing_extensions`

The testing dependencies are:

*   `pytest`
*   `pytest-cov`
*   `hypothesis`
*   `typing_extensions`

### Installation

To install the project and its dependencies, you can use the following command:

```bash
pip install .
```

### Running Tests

The project uses `tox` to manage testing environments. To run the tests, you can use the following command:

```bash
tox
```

This will run the tests in a virtual environment, as defined in the `tox.ini` file.

## Development Conventions

### Code Style

The project uses `flake8` for linting, with a maximum line length of 188 characters. The configuration for `flake8` can be found in the `setup.cfg` file.

### Testing

The project uses `pytest` for testing. The tests are located in the `tests` directory. The project also uses `pytest-cov` to measure test coverage.

### Documentation

The project uses `Sphinx` to generate documentation. The documentation is located in the `docs` directory.

### Pre-commit Hooks

The project uses `pre-commit` to run checks before each commit. The configuration for `pre-commit` can be found in the `.pre-commit-config.yaml` file.
