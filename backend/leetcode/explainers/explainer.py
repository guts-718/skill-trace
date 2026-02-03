from config import USE_LLM_EXPLANATIONS
from leetcode.explainers.rule_explainer import explain as rule_explain
from leetcode.explainers.llm_explainer import explain as llm_explain

def explain(signals):
    if USE_LLM_EXPLANATIONS:
        res = llm_explain(signals)
        if res:
            return res

    return rule_explain(signals)
