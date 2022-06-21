import numpy as np
import pandas as pd
from src.scoring.ska_sdc.common.utils.score_helper import (
    count_match_cat_rej,
    get_acc_series,
    get_match_cat_acc,
)
from src.scoring.ska_sdc.sdc1.dc_defns import core_thr, flux_thr, multid_thr, size_thr
from src.scoring.ska_sdc.sdc1.models.sdc1_score import Sdc1Score
from src.scoring.ska_sdc.sdc1.utils.score_helper import (
    SCORE_MAX,
    get_b_min_scores,
    get_class_acc_series,
    get_core_frac_acc_series,
    get_pa_acc_series,
    get_pa_scores,
    get_pos_acc_series,
    get_position_scores,
    get_size_acc_series,
)


def create_sdc_score(sieved_sub_df, freq, n_det, mode, train, detail):
    """
    Complete the scoring pipeline using the data generated by the previous steps.
    This requires the (sieved) candidate match catalogue created from the crossmatch
    step.

    Args:
        sieved_sub_df (:obj:`pandas.DataFrame`): The processed and sieved candidate
            match catalogue between submission and truth.
        freq (:obj:`int`): The current frequency value.
        n_det (:obj:`int`): Total number of detected sources.
        mode (:obj:`int`): 0 or 1 to use core or centroid positions for scoring
        train (:obj:`bool`): Whether the score is determined based on training area only
        detail (:obj:`bool`): If True, will include the detailed score and match data
            with the returned Sdc1Score object.

    Returns:
        :class:`ska_sdc.sdc1.models.sdc1_score.Sdc1Score`: The calculated SDC1 score
            object
    """
    # Instantiate Score object:
    sdc_score = Sdc1Score(mode, train, detail)

    # Reject matches from cross matched catalogues that lie above the multid_thr.
    # Count them for the report.
    match_sub_df = get_match_cat_acc(sieved_sub_df, multid_thr)
    n_rej = count_match_cat_rej(sieved_sub_df, multid_thr)

    # Add the match_df to the sdc_score for detailed feedback
    sdc_score.match_df = match_sub_df

    # Compute final score
    sdc_score = compute_score_value(sdc_score, match_sub_df, freq, n_det, n_rej)

    return sdc_score


def compute_score_value(sdc_score, match_sub_df, freq, n_det, n_rej):
    """
    Compute the per-match accuracy and generate the final score report.

    Args:
        submission_metadata (SubmissionMetadata): Identifies the submission catalogue
            location and metadata
        n_det (int): The total number of detected sources in the submission
        match_sub_df (pd.DataFrame): The sieved matches that are below the multi_d
            threshold
        beam_size (float): The beam_size, used to calculate the positional accuracy
        n_rej (int): Number of candidate matches rejected on the basis of multi_d
    """
    # Create required variables
    beam_size = 0.25 / freq * 1400.0

    # Number of matches below multi_d_err threshold
    n_match = len(match_sub_df.index)

    if n_match == 0:
        # No matches found; nothing else to do
        sdc_score.value = 0.0
        sdc_score.n_det = n_det
        sdc_score.n_bad = n_rej
        sdc_score.n_match = n_match
        sdc_score.n_false = n_det - n_match
        sdc_score.score_det = 0.0
        sdc_score.acc_pc = 0.0
        sdc_score.scores_df = None
        return sdc_score

    # Compute accuracy for position (core)
    core_acc_series = get_pos_acc_series(
        match_sub_df["ra_core"],
        match_sub_df["dec_core"],
        match_sub_df["ra_core_t"],
        match_sub_df["dec_core_t"],
        match_sub_df["b_maj_t"],
        match_sub_df["b_min_t"],
        beam_size,
    )

    # Compute accuracy for position (centroid)
    cent_acc_series = get_pos_acc_series(
        match_sub_df["ra_cent"],
        match_sub_df["dec_cent"],
        match_sub_df["ra_cent_t"],
        match_sub_df["dec_cent_t"],
        match_sub_df["b_maj_t"],
        match_sub_df["b_min_t"],
        beam_size,
    )

    # Compute accuracy of total flux measurement
    flux_acc_series = get_acc_series(
        match_sub_df["flux"], match_sub_df["flux_t"], match_sub_df["flux_t"]
    )

    # Compute accuracy of size estimate (B_maj)
    b_maj_acc_series = get_size_acc_series(
        match_sub_df["b_maj"],
        match_sub_df["b_maj_t"],
        match_sub_df["size_id"],
        match_sub_df["size_id_t"],
    )

    # Compute accuracy of size estimate (B_min)
    b_min_acc_series = get_size_acc_series(
        match_sub_df["b_min"],
        match_sub_df["b_min_t"],
        match_sub_df["size_id"],
        match_sub_df["size_id_t"],
    )

    # Compute accuracy of position angle
    pa_acc_series = get_pa_acc_series(match_sub_df["pa"], match_sub_df["pa_t"])

    # Compute accuracy of core fraction
    core_frac_acc_series = get_core_frac_acc_series(
        match_sub_df["core_frac"], match_sub_df["core_frac_t"]
    )

    # Compute accuracy of class determination
    class_acc_series = get_class_acc_series(
        match_sub_df["class"], match_sub_df["class_t"]
    )

    # Log per-source scores in a new DataFrame
    scores_df = pd.DataFrame()

    # Position scores
    scores_df["position"] = get_position_scores(core_acc_series, cent_acc_series)

    # Flux scores
    flux_acc_frac_series = (SCORE_MAX / flux_acc_series) * flux_thr
    scores_df["flux"] = np.minimum(SCORE_MAX, flux_acc_frac_series)

    # Major axis size scores
    b_maj_acc_frac_series = (SCORE_MAX / b_maj_acc_series) * size_thr
    scores_df["b_maj"] = np.minimum(SCORE_MAX, b_maj_acc_frac_series)

    # Minor axis size scores
    scores_df["b_min"] = get_b_min_scores(b_min_acc_series, match_sub_df["size_id_t"])

    # Position angle scores
    scores_df["pa"] = get_pa_scores(pa_acc_series, match_sub_df["size_id_t"])

    # Core fraction scores
    core_frac_acc_frac_series = (SCORE_MAX / core_frac_acc_series) * core_thr
    scores_df["core_frac"] = np.minimum(SCORE_MAX, core_frac_acc_frac_series)

    # Class scores
    scores_df["class"] = class_acc_series * SCORE_MAX

    # Weight scores so maximum score per source is SCORE_MAX
    weight = SCORE_MAX / len(scores_df.columns)
    scores_df_weighted = scores_df.multiply(weight)

    score_sum = scores_df_weighted.sum().sum()
    score_final = score_sum - float(n_det - n_match)

    # Add ID column to scores_df to provide detailed feedback
    scores_df.insert(0, "id", match_sub_df["id"])

    # Write data to sdc_score
    sdc_score.value = score_final
    sdc_score.n_det = n_det
    sdc_score.n_bad = n_rej
    sdc_score.n_match = n_match
    sdc_score.n_false = n_det - n_match
    sdc_score.score_det = score_sum
    sdc_score.acc_pc = score_sum / float(n_match) * 100.0
    sdc_score.scores_df = scores_df

    return sdc_score