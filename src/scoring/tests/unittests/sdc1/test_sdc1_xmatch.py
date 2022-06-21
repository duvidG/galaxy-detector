from astropy.coordinates import SkyCoord
from ska_sdc.sdc1.utils.sdc1_xmatch import Sdc1XMatch


class TestSdc1XMatch:
    def test_crossmatch_kdtree_core(self, sub_df_prep, truth_df_prep):
        # Test core position mode
        cand_match_df_core = Sdc1XMatch(
            cat_sub=sub_df_prep, cat_truth=truth_df_prep, mode=0
        ).execute(func_name="crossmatch_kdtree")

        # Should be 44 matches between the submission and truth test catalogues
        assert len(cand_match_df_core.index) == 44

        coord_arr_sub_core = SkyCoord(
            ra=cand_match_df_core["ra_core"].values,
            dec=cand_match_df_core["dec_core"].values,
            frame="fk5",
            unit="deg",
        )
        coord_arr_truth_core = SkyCoord(
            ra=cand_match_df_core["ra_core_t"].values,
            dec=cand_match_df_core["dec_core_t"].values,
            frame="fk5",
            unit="deg",
        )
        sep_arr_core = coord_arr_sub_core.separation(coord_arr_truth_core).arcsecond

        # Verify that match separations are all less than conv_size
        assert all(sep_arr_core < cand_match_df_core["conv_size"])

    def test_crossmatch_kdtree_cent(self, sub_df_prep, truth_df_prep):
        # Test centroid position mode
        cand_match_df_centr = Sdc1XMatch(
            cat_sub=sub_df_prep, cat_truth=truth_df_prep, mode=1
        ).execute(func_name="crossmatch_kdtree")

        # Should be 43 matches between the submission and truth test catalogues
        # (truth source 30996827 has a different centroid position that is further
        # than conv_size from sub source 80762)
        assert len(cand_match_df_centr.index) == 43

        coord_arr_sub_centr = SkyCoord(
            ra=cand_match_df_centr["ra_cent"].values,
            dec=cand_match_df_centr["dec_cent"].values,
            frame="fk5",
            unit="deg",
        )
        coord_arr_truth_centr = SkyCoord(
            ra=cand_match_df_centr["ra_cent_t"].values,
            dec=cand_match_df_centr["dec_cent_t"].values,
            frame="fk5",
            unit="deg",
        )
        sep_arr_centr = coord_arr_sub_centr.separation(coord_arr_truth_centr).arcsecond

        # Verify that match separations are all less than conv_size
        assert all(sep_arr_centr < cand_match_df_centr["conv_size"])
