"""
app/tools/rashi/api_routes.py

API routes for Rashi Tool (OSM Nominatim)

✅ Upgraded small-town search:
- India priority first
- Then fallback global
- More results
"""

from flask import Blueprint, request, jsonify
import requests

rashi_api_bp = Blueprint("rashi_api", __name__, url_prefix="/tools/rashi/api")


@rashi_api_bp.route("/places", methods=["GET"])
def search_places():
    query = request.args.get("q", "").strip()

    if not query or len(query) < 3:
        return jsonify([])

    url = "https://nominatim.openstreetmap.org/search"
    headers = {
        "User-Agent": "AppNest-RashiTool/2.0 (RealWorld Project)",
        "Accept-Language": "en",
    }

    def _call(params):
        res = requests.get(url, params=params, headers=headers, timeout=8)
        res.raise_for_status()
        data = res.json()

        cleaned = []
        seen = set()

        for item in data:
            display_name = item.get("display_name", "").strip()
            lat = item.get("lat", "")
            lon = item.get("lon", "")

            if not display_name or not lat or not lon:
                continue

            key = (display_name, lat, lon)
            if key in seen:
                continue
            seen.add(key)

            cleaned.append(
                {
                    "display_name": display_name,
                    "lat": lat,
                    "lon": lon,
                }
            )

        return cleaned

    try:
        # ✅ attempt 1 (India focus)
        params = {
            "format": "json",
            "q": query,
            "limit": 12,
            "addressdetails": 1,
            "countrycodes": "in",
            "dedupe": 1,
        }

        cleaned = _call(params)

        # ✅ attempt 2 (global fallback)
        if not cleaned:
            params.pop("countrycodes", None)
            cleaned = _call(params)

        return jsonify(cleaned)

    except Exception:
        return jsonify({"error": "Failed to fetch places"}), 500