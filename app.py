from flask import Flask, render_template, request
from result_store import load_results
from scheduler import build_rankings

app = Flask(__name__)

@app.route("/")
def index():
    rankings = load_results()

    if not rankings:
        print("[app] no saved results, rebuilding...")
        rankings = build_rankings()

    model_filter = request.args.get("model", "").strip()
    issue_filter = request.args.get("issue", "").strip()
    min_profit = request.args.get("min_profit", "").strip()

    filtered = rankings

    if model_filter:
        filtered = [x for x in filtered if x.get("model") == model_filter]

    if issue_filter:
        filtered = [x for x in filtered if x.get("issue") == issue_filter]

    if min_profit:
        try:
            min_profit_value = int(min_profit)
            filtered = [x for x in filtered if int(x.get("profit", 0)) >= min_profit_value]
        except Exception:
            pass

    models = sorted(list({x.get("model", "") for x in rankings if x.get("model")}))
    issues = sorted(list({x.get("issue", "") for x in rankings if x.get("issue")}))

    print(f"[app] rankings count={len(rankings)} filtered count={len(filtered)}")

    return render_template(
        "index.html",
        rankings=filtered,
        all_models=models,
        all_issues=issues,
        model_filter=model_filter,
        issue_filter=issue_filter,
        min_profit=min_profit,
    )

@app.route("/refresh")
def refresh():
    rankings = build_rankings()
    return f"updated: {len(rankings)} items"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
