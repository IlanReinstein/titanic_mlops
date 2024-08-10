import pytest
import pandas as pd
from app import preprocessing


@pytest.fixture
def test_df():
    return pd.read_csv('tests/sample_test_data.csv', index_col=0)

def test_prepare_data(test_df):
    drop_cols = ['Ticket', 'Cabin', 'Name', 'Parch', 'SibSp', 'FamilySize']
    out_df = preprocessing.prepare_data(test_df)
    print(out_df.head())
    assert not set(drop_cols).issubset(out_df.columns)
    assert out_df.shape[1] == 9