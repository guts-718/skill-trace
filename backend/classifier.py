import yaml
import os

RULES_FILE = "rules.yaml"

rules = {
    "direct_domains": {},
    "domain_groups": {},
    "group_category": {},
    "path_keywords": {},
    "title_keywords": {}
}


def load_rules():
    global rules

    if not os.path.exists(RULES_FILE):
        print("rules.yaml not found")
        return

    with open(RULES_FILE, "r") as f:
        data = yaml.safe_load(f)
        if data is None:
            return

        rules["direct_domains"] = data.get("direct_domains", {})
        rules["domain_groups"] = data.get("domain_groups", {})
        rules["group_category"] = data.get("group_category", {})
        rules["path_keywords"] = data.get("path_keywords", {})
        rules["title_keywords"] = data.get("title_keywords", {})

    print("Rules v2 loaded")

def classify_session(session):
    scores = {}

    domain = (session.domain or "").lower()
    title = (session.title or "").lower()
    url = (session.url or "").lower()
    referrer = (session.referrer or "").lower()

    def add_score(cat, val):
        scores[cat] = scores.get(cat, 0) + val

    has_direct_match = False

    # 1) Direct domain
    for d, cat in rules["direct_domains"].items():
        if d in domain:
            add_score(cat, 3)
            has_direct_match = True

    # 2) Domain groups
    for group, domains in rules["domain_groups"].items():
        for d in domains:
            if d in domain:
                cat = rules["group_category"].get(group)
                if cat:
                    add_score(cat, 2)

    # 3) Path keywords
    for word, cat in rules["path_keywords"].items():
        if word in url:
            add_score(cat, 2)

    # 4) Title keywords
    for word, cat in rules["title_keywords"].items():
        if word in title:
            add_score(cat, 1)

    # 5) Referrer boost (only if no strong direct match)
    if not has_direct_match and referrer:
        for d, cat in rules["direct_domains"].items():
            if d in referrer:
                add_score(cat, 1)

        for group, domains in rules["domain_groups"].items():
            for d in domains:
                if d in referrer:
                    cat = rules["group_category"].get(group)
                    if cat:
                        add_score(cat, 1)

    if not scores:
        return "Other"

    return max(scores.items(), key=lambda x: x[1])[0]
