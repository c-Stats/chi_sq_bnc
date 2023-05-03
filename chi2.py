from itertools import repeat
from scipy.stats import chi2

categories = ["A", "B", "C", "D", "E", "A", "B", "C", "D"]
count = [9000, 7000, 6000, 5000, 35, 900, 670, 580, 475]
source = ["HIST", "HIST", "HIST", "HIST", "HIST", "NOW", "NOW", "NOW", "NOW"]

results = [{"CATEGORY": a, "COUNT": b, "SOURCE": c} for (a,b,c) in zip(categories, count, source)]
results


def chi_sq_test(results, alpha = 0.05):
    multinom_classes = list(set([res["CATEGORY"] for res in results]))
    multinom_classes.sort()
    n_classes = len(multinom_classes)
    
    integer_mapping = {}
    for i, cl in enumerate(multinom_classes):
        integer_mapping[cl] = i
    
    vectors = {"HIST": list(repeat(0, n_classes)), "NOW": list(repeat(0, n_classes))}    
    for res in results:
        vectors[res["SOURCE"]][integer_mapping[res["CATEGORY"]]] = res["COUNT"]
        
    scaling_factor = sum(vectors["NOW"]) / sum(vectors["HIST"])
    vectors["HIST"] = [scaling_factor * c for c in vectors["HIST"]]
    
    ssq = sum((x - m)**2 / m for (x, m) in zip(vectors["NOW"], vectors["HIST"]))
    cdf_val = chi2.cdf(ssq, n_classes - 1)
    pval = 2*min([1 - cdf_val, cdf_val])
    
    outcome = "PASS" if pval > alpha else "FAIL"
    
    vectors["HIST"] = [round(c) for c in vectors["HIST"]]
    ssq = round(ssq, 2)
    pval = round(pval, 4)
    
    info = []
    for (hist, now, ct) in zip(vectors["HIST"], vectors["NOW"], multinom_classes):
        info.append({"Category": ct, "Expected": hist, "Observed": now, "Delta": now - hist})
    
    return {"result": pval, "outcome": outcome, "info": info}
    
    chi_sq_test(results)
