import os
import yaml
from .config import *
from .musescore_conversion import musescore_conversion
from .produce_msq import produce_msq
from .slice_system_pngs import slice_system_pngs


def build(slice_index: int, slice_count: int):
    # load and filter corpus scores
    with open(os.path.join(LIEDER_CORPUS_PATH, "data/scores.yaml")) as f:
        corpus_scores = yaml.load(f, Loader=yaml.FullLoader)
    for score_id in IGNORED_SCORE_IDS:
        del corpus_scores[score_id]
    
    # slice score IDs
    assert slice_index >= 0
    assert slice_index < slice_count
    score_ids = list(corpus_scores.keys())
    slice_size = len(score_ids) // slice_count
    slice_score_ids = score_ids[
        (slice_index * slice_size) : ((slice_index + 1) * slice_size)
    ]
    if slice_index == slice_count - 1:
        slice_score_ids = score_ids[(slice_index * slice_size):]
    slice_scores = {
        score_id: score
        for score_id, score in corpus_scores.items()
        if score_id in set(slice_score_ids)
    }

    # run MuseScore conversions
    musescore_conversion(
        scores=slice_scores,
        slice_index=slice_index,
        slice_count=slice_count
    )

    # split xml files into systems and convert to sequences
    produce_msq(
        score_ids=slice_score_ids,
        slice_index=slice_index,
        slice_count=slice_count
    )

    # slice up full-page PNGs to system-level PNGs
    slice_system_pngs(score_ids=slice_score_ids)
    