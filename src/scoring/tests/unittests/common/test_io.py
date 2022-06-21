import pandas as pd
from ska_sdc.common.utils.cat_io import load_dataframe
from ska_sdc.sdc1.dc_defns import CAT_COLUMNS


class TestIo:
    def test_load_dataframe(self, data_cat_paths):
        for data_cat_path in data_cat_paths:
            cat_df = load_dataframe(data_cat_path, columns=CAT_COLUMNS)
            assert isinstance(cat_df, pd.DataFrame)
            assert cat_df.isna().sum().sum() == 0
