def compute_indicator_scores(results: dict, weights: dict) -> dict:
    """
    Computes FAIR principle scores (F, A, I, R) using evaluation results and weighting data.
    """

    scores = {}

    principles = ['F','A','I','R']

    # flatten results dict
    results_flattened= {key: value["result"] for key, value in results.items()}

    # get indicators assoicated with each principle
    for principle in principles:
        principle_indicators = [k for k in results_flattened.keys() if principle in k]

        # multiple result by weight
        for principle_indicator in principle_indicators:
            scores[principle_indicator] = results_flattened[principle_indicator] * weights[principle_indicator]
    
        # combine secondary indicators where needed
        if principle == 'F':
            scores['F1'] = weights['F1'] * (scores['F1_1'] + scores['F1_2'])
        elif principle == 'A':
            scores['A1'] = weights['A1'] * (scores['A1_1'] + scores['A1_2'])
        elif principle == 'R':
            scores['R1'] = weights['R1'] * (scores['R1_1'] + scores['R1_2'])

        # report overall principle score
        scores[principle] = sum(value for key, value in scores.items() if len(key)==2 and principle in key)

    return scores