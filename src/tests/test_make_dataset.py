# ---
# Import
# ---

import pandas as pd
import pytest

# Infrastructure Modules
import os
import warnings
from pathlib import Path
from datetime import datetime
import time

# Scripts
from src.data.make_dataset import get_data
from src.base import get_config

# ---
# Global Definitions
# ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ---
# Functions and classes
# ---

def test_get_data():
    config = get_config()
    portfolio = config.get("share_code_list")

    with pytest.raises(TypeError):
        get_data(portfolio[0])

    assert isinstance(get_data(portfolio[:2]), pd.DataFrame)

if __name__ == "__main__":
    config = get_config()
    portfolio = config.get("share_code_list")
    print(portfolio)
    test_get_data(portfolio[:2])