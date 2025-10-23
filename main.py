import json
import os

from flask import (
	abort,
	Flask,
	jsonify,
)
from flask_cors import CORS
from pathlib import Path
from typing import Optional


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

app = Flask(__name__)
CORS(app, resources={r"/reports/*": {"origins": "http://localhost:4200"}})


@app.get("/reports/<person_id>")
def get_report(person_id: str):
	report_file = _locate_report_file(person_id)
	if report_file is None:
		abort(404, description=f"No report found for id {person_id}")

	with report_file.open("r", encoding="utf-8") as handle:
		payload = json.load(handle)

	return jsonify(payload)

def _locate_report_file(person_id: str) -> Optional[Path]:
	"""Return the first matching report file for a given person id."""

	direct_match = DATA_DIR / f"datacredito_{person_id}.json"
	if direct_match.is_file():
		return direct_match

	# Fall back to the first file that starts with the id so suffixes still work.
	for candidate in sorted(DATA_DIR.glob(f"datacredito_{person_id}_*.json")):
		return candidate

	return None


if __name__ == "__main__":
	port = int(os.environ.get("PORT", "5000"))
	app.run(host="0.0.0.0", port=port, debug=True)
