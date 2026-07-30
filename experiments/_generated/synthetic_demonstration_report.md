# Synthetic demonstration report

**Label:** synthetic_demonstration
**Human participants executed:** no
**SLAPA validated:** no

```json
{
  "EXP-01": {
    "study_label": "synthetic_demonstration",
    "experiment_id": "EXP-01",
    "participants": {
      "SYN-CODER-A": {
        "n_cases": 26,
        "exact_match_to_reference": 26,
        "exact_match_rate": 1.0,
        "reference_label": "REFERENCE_ADJUDICATION",
        "not_ground_truth": true
      },
      "SYN-CODER-B": {
        "n_cases": 26,
        "exact_match_to_reference": 22,
        "exact_match_rate": 0.8461538461538461,
        "reference_label": "REFERENCE_ADJUDICATION",
        "not_ground_truth": true
      }
    },
    "pairwise_unit_count_agreement": 0.8461538461538461
  },
  "EXP-02_independent_demo": {
    "study_label": "synthetic_demonstration",
    "experiment_id": "EXP-02",
    "empirical_intercoder_reliability": "NOT_COMPUTED_DEMO_ONLY_RAW_AGREEMENT",
    "reliability_blocked_reason": null,
    "participants": {
      "SYN-CODER-A": {
        "n": 32,
        "rung_agreement_vs_reference": 1.0,
        "pass_type": "independent_human"
      },
      "SYN-CODER-B": {
        "n": 32,
        "rung_agreement_vs_reference": 0.875,
        "pass_type": "independent_human"
      }
    },
    "raw_rung_agreement": 0.875,
    "note": "Full alpha reserved for genuinely independent coder studies."
  },
  "EXP-02_procedural_block_demo": {
    "study_label": "synthetic_demonstration",
    "experiment_id": "EXP-02",
    "empirical_intercoder_reliability": "NOT_COMPUTED",
    "reliability_blocked_reason": "Metadata include simulated_procedural_second_pass; empirical Krippendorff's alpha must not be reported.",
    "participants": {
      "SYN-CODER-A": {
        "n": 32,
        "rung_agreement_vs_reference": 1.0,
        "pass_type": "independent_human"
      },
      "SYN-PROC": {
        "n": 32,
        "rung_agreement_vs_reference": 0.875,
        "pass_type": "simulated_procedural_second_pass"
      }
    }
  },
  "EXP-03": {
    "study_label": "synthetic_demonstration",
    "experiment_id": "EXP-03",
    "item_means": {
      "US-01": 3.5,
      "US-02": 3.5,
      "US-03": 3.5,
      "US-04": 3.5,
      "US-05": 3.5,
      "US-06": 2.0,
      "US-07": 3.5,
      "US-08": 3.5,
      "US-09": 3.5,
      "US-10": 3.5,
      "US-11": 3.5,
      "US-12": 3.5,
      "US-13": 3.5,
      "US-14": 45.0
    },
    "psychometric_validation_claimed": false,
    "n_response_rows": 32
  },
  "EXP-04": {
    "study_label": "synthetic_demonstration",
    "experiment_id": "EXP-04",
    "participants": {
      "SYN-RATER-1": {
        "accuracy": 1.0,
        "n": 18
      },
      "SYN-RATER-2": {
        "accuracy": 0.7777777777777778,
        "n": 18
      }
    },
    "confusion_counts": {
      "1->1": 4,
      "2->2": 7,
      "3->3": 8,
      "4->4": 9,
      "5->5": 4,
      "2->3": 3,
      "4->5": 1
    }
  },
  "EXP-05": {
    "study_label": "synthetic_demonstration",
    "experiment_id": "EXP-05",
    "i_cvi_relevance": {
      "A": 1.0,
      "B": 1.0,
      "C": 1.0,
      "D": 1.0,
      "E": 1.0,
      "F": 1.0,
      "G": 1.0,
      "H": 1.0
    },
    "s_cvi_ave": 1.0,
    "slapa_validated": false,
    "note": "Synthetic CVI demonstration only; not content validation evidence."
  },
  "EXP-06": {
    "study_label": "synthetic_demonstration",
    "experiment_id": "EXP-06",
    "n_domain_judgements": 48,
    "missing_information_frequency": 1.0,
    "unsupported_inference_prompt_frequency": 1.0,
    "total_score_emitted": false,
    "slapa_validated": false
  },
  "claims": {
    "experiments_executed_with_humans": false,
    "slapa_validated": false,
    "empirical_alpha_from_procedural_pass": false
  }
}
```
