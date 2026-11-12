import json
import os
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse

# Import your custom Python library here once you drop it into /api:
# from api import your_lib

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOANS_FILE = os.path.join(BASE_DIR, "loans.json")
HTML_FILE = os.path.join(BASE_DIR, "index.html")


def load_loans():
    with open(LOANS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/", response_class=HTMLResponse)
def serve_home():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/api/loans")
def get_loans(
    loan_type: str = Query("all"),
    amount: int = Query(100000),
    income: int = Query(15000),
    employment: str = Query("all"),
):
    loans = load_loans()
    filtered = []

    for loan in loans:
        if loan_type != "all" and loan["type"] != loan_type:
            continue
        if amount > loan["max_amount"]:
            continue
        if income < loan["min_income"]:
            continue
        if employment != "all" and employment not in loan["employment"]:
            continue
        filtered.append(loan)

    return {"count": len(filtered), "loans": filtered}


@app.get("/go/{offer_id}")
def track_and_redirect(offer_id: str):
    loans = load_loans()
    for loan in loans:
        if loan["id"] == offer_id:
            print(f"[AFFILIATE CLICK] offer_id={offer_id}")
            return RedirectResponse(url=loan["affiliate_url"], status_code=302)
    return JSONResponse(status_code=404, content={"error": "Offer not found"})
