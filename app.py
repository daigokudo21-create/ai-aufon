from flask import Flask, render_template, request
from scheduler import start_scheduler
from result_store import load_results

app = Flask(__name__)

start_scheduler()

@app.route("/")
def index():
    selected_model = request.args.get("model", "")
    selected_damage = request.args.get("damage", "")
    profit_filter = request.args.get("profit", "")

    results = load_results()

    if selected_model:
        results = [r for r in results if r["model"] == selected_model]

    if selected_damage:
        results = [r for r in results if r["damage"] == selected_damage]

    if profit_filter == "plus":
        results = [r for r in results if r["profit"] > 0]
    elif profit_filter == "5000":
        results = [r for r in results if r["profit"] >= 5000]
    elif profit_filter == "10000":
        results = [r for r in results if r["profit"] >= 10000]

    results = sorted(results, key=lambda x: x["profit"], reverse=True)

    return render_template(
        "index.html",
        results=results,
        selected_model=selected_model,
        selected_damage=selected_damage,
        profit_filter=profit_filter
    )

@app.route("/healthz")
def healthz():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
