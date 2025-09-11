import subprocess
import sys

import pytest

from physdes.skeleton import fib, main

__author__ = "Wai-Shing Luk"
__copyright__ = "Wai-Shing Luk"
__license__ = "MIT"


def test_fib():
    """API Tests"""
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["7"])
    captured = capsys.readouterr()
    assert "The 7-th Fibonacci number is 13" in captured.out


def test_main_run_as_script():
    """CLI Tests"""
    result = subprocess.run(
        [sys.executable, "-m", "physdes.skeleton", "7"], capture_output=True, text=True
    )
    assert "The 7-th Fibonacci number is 13" in result.stdout
