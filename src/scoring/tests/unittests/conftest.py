import configparser

import pytest
from ska_sdc.common.utils.cat_io import load_dataframe
from ska_sdc.data.data_resources import SDC2_CONFIG_PATH
from ska_sdc.sdc1.dc_defns import CAT_COLUMNS
from ska_sdc.sdc1.utils.prep import prepare_data


# SDC 1 fixtures
#
@pytest.fixture
def sub_path():
    return "./tests/testdata/sdc1/submission_sample/submission_sample.txt"


@pytest.fixture
def truth_path():
    return "./tests/testdata/sdc1/truth_sample/truth_sample.txt"


@pytest.fixture
def sub_path_errors():
    return "./tests/testdata/sdc1/submission_sample/submission_with_errors.txt"


@pytest.fixture
def data_cat_paths(sub_path, truth_path, sub_path_errors):
    return [sub_path, truth_path, sub_path_errors]


@pytest.fixture
def sub_df(sub_path):
    return load_dataframe(sub_path, columns=CAT_COLUMNS, skip_n=1)


@pytest.fixture
def truth_df(truth_path):
    return load_dataframe(truth_path, columns=CAT_COLUMNS)


@pytest.fixture
def sub_df_prep(sub_df):
    return prepare_data(sub_df, 1400, train=False)


@pytest.fixture
def truth_df_prep(truth_df):
    return prepare_data(truth_df, 1400, train=False)


# SDC2 fixtures
#
@pytest.fixture
def sdc2_config():
    config = configparser.ConfigParser()
    config.read(SDC2_CONFIG_PATH)
    return config


@pytest.fixture
def sub_path_sdc2():
    return "./tests/testdata/sdc2/submission_sample/submission_sample.txt"


@pytest.fixture
def truth_path_sdc2():
    return "./tests/testdata/sdc2/truth_sample/truth_sample.txt"


@pytest.fixture
def sub_path_sdc2_nohead():
    return "./tests/testdata/sdc2/submission_sample/submission_nohead.txt"


@pytest.fixture
def truth_path_sdc2_nohead():
    return "./tests/testdata/sdc2/truth_sample/truth_nohead.txt"


@pytest.fixture
def cat_columns(sdc2_config):
    return sdc2_config["general"]["sub_cat_column_names"].split(",")


@pytest.fixture
def sub_cat_sdc2(cat_columns, sub_path_sdc2):
    return load_dataframe(sub_path_sdc2, columns=cat_columns, skip_n=1)


@pytest.fixture
def truth_cat_sdc2(cat_columns, truth_path_sdc2):
    return load_dataframe(truth_path_sdc2, columns=cat_columns, skip_n=1)
