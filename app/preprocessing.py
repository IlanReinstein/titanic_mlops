import pandas as pd
import numpy as np


def prepare_data(df):
    tmp_df = drop_unwanted(df)
    tmp_df = clean_passenger_title(tmp_df)
    tmp_df = clean_sex(tmp_df)
    tmp_df = clean_age(tmp_df)
    tmp_df = clean_family_size(tmp_df)
    tmp_df = clean_embarked(tmp_df)
    tmp_df = clean_fare(tmp_df)
    return tmp_df


def drop_unwanted(df) -> pd.DataFrame:
    return df.drop(columns=['Ticket', 'Cabin']).copy()


def clean_passenger_title(df) -> pd.DataFrame:
    df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)
    df['Title'] = df['Title'].replace(['Lady', 'Countess', 'Capt', 'Col',
                                       'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')

    df['Title'] = df['Title'].replace('Mlle', 'Miss')
    df['Title'] = df['Title'].replace('Ms', 'Miss')
    df['Title'] = df['Title'].replace('Mme', 'Mrs')

    title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
    df['Title'] = df['Title'].map(title_mapping)
    df['Title'] = df['Title'].fillna(0)

    return df.drop(columns=['Name']).copy()


def clean_sex(df) -> pd.DataFrame:
    df['Sex'] = df['Sex'].map({'female': 1, 'male': 0}).astype(int)
    return df.copy()


def clean_age(df) -> pd.DataFrame:
    """"
    Estimate median age and fill missing values
    Group/bin age groups after filling NAs
    """
    median_age = df['Age'][df.Age.notnull()].median()
    df['Age'] = df['Age'].fillna(median_age).astype(int)
    df.loc[df['Age'] <= 16, 'Age'] = 0
    df.loc[(df['Age'] > 16) & (df['Age'] <= 32), 'Age'] = 1
    df.loc[(df['Age'] > 32) & (df['Age'] <= 48), 'Age'] = 2
    df.loc[(df['Age'] > 48) & (df['Age'] <= 64), 'Age'] = 3
    df.loc[df['Age'] > 64, 'Age'] = 4
    df['Age*Class'] = df.Age * df.Pclass
    return df.copy()


def clean_family_size(df) -> pd.DataFrame:
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['IsAlone'] = np.where(df.FamilySize == 1, 1, 0)
    return df.drop(columns=['Parch', 'SibSp', 'FamilySize'])


def clean_embarked(df) -> pd.DataFrame:
    freq_port = 'S'  # from training data in the Kaggle notebook
    df['Embarked'] = df['Embarked'].fillna(freq_port)
    df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2}).astype(int)
    return df.copy()


def clean_fare(df) -> pd.DataFrame:
    df.loc[df['Fare'] <= 7.91, 'Fare'] = 0
    df.loc[(df['Fare'] > 7.91) & (df['Fare'] <= 14.454), 'Fare'] = 1
    df.loc[(df['Fare'] > 14.454) & (df['Fare'] <= 31), 'Fare'] = 2
    df.loc[df['Fare'] > 31, 'Fare'] = 3
    df['Fare'] = df['Fare'].astype(int)
    return df.copy()
