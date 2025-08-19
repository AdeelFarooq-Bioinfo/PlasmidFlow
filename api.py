import io
import json
import base64
import tempfile
import datetime as dt
from flask import Blueprint, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
from db import db, Dataset, StyleProfile
from utils import parse_csv_file, validate_dataframe, filter_by_traits, dataframe_preview
from viz import build_sankey, build_network, build_heatmap

import plotly.io as pio

api_bp = Blueprint("api", __name__)

ALLOWED_EXTENSIONS = {"csv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route("/upload", methods=["POST"])
def upload():
    """Upload CSV, validate, persist into DB, return dataset_id and preview."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Only CSV files are allowed"}), 400

    filename = secure_filename(file.filename)
    try:
        df = parse_csv_file(file.stream)
        ok, message = validate_dataframe(df)
        if not ok:
            return jsonify({"error": message}), 400
        # Persist dataset (store as JSON records for simplicity)
        ds = Dataset(
            name=filename,
            filename=filename,
            data_json=df.to_json(orient="records"),
            owner_sid=session.get("sid"),
        )
        db.session.add(ds)
        db.session.commit()
        return jsonify({
            "dataset_id": ds.id,
            "preview": dataframe_preview(df, 5),
            "message": "Upload successful"
        })
    except Exception as e:
        return jsonify({"error": f"Failed to parse CSV: {str(e)}"}), 400

@api_bp.route("/dataset/<int:dataset_id>", methods=["GET"])
def get_dataset(dataset_id):
    ds = db.session.get(Dataset, dataset_id)
    if not ds:
        return jsonify({"error": "Dataset not found"}), 404
    if ds.owner_sid and ds.owner_sid != session.get("sid"):
        # Simple access control per session
        return jsonify({"error": "Not authorized"}), 403
    return jsonify({
        "dataset_id": ds.id,
        "name": ds.name,
        "filename": ds.filename,
        "records": json.loads(ds.data_json)
    })

def _get_df(dataset_id):
    ds = db.session.get(Dataset, dataset_id)
    if not ds:
        return None, ("Dataset not found", 404)
    if ds.owner_sid and ds.owner_sid != session.get("sid"):
        return None, ("Not authorized", 403)
    import pandas as pd
    return pd.DataFrame(json.loads(ds.data_json)), None

@api_bp.route("/figure/<string:ftype>", methods=["POST"])
def figure(ftype):
    """Build a figure JSON for sankey|network|heatmap given dataset_id and options."""
    payload = request.get_json(silent=True) or {}
    dataset_id = payload.get("dataset_id")
    env_filter = payload.get("env_filter", "").strip()
    traits = payload.get("traits", [])
    style = payload.get("style", {})
    scale = payload.get("scale", "Blues")

    df, err = _get_df(dataset_id)
    if err:
        msg, code = err
        return jsonify({"error": msg}), code

    # Apply environment filter
    if env_filter:
        df = df[df["Environment"].str.contains(env_filter, case=False, na=False)]

    # Apply trait filter (keep rows where selected traits are present != "no")
    if traits:
        df = filter_by_traits(df.copy(), traits)

    # Build figure
    if ftype == "sankey":
        fig = build_sankey(df, style)
    elif ftype == "network":
        fig = build_network(df, style)
    elif ftype == "heatmap":
        fig = build_heatmap(df, scale, style)
    else:
        return jsonify({"error": "Unknown figure type"}), 400

    return jsonify(fig.to_dict())

@api_bp.route("/export", methods=["POST"])
def export():
    """Export a given Plotly figure (JSON) to PNG/SVG/PDF via Kaleido."""
    payload = request.get_json(silent=True) or {}
    fig_dict = payload.get("figure")
    fmt = payload.get("format", "png")
    width = int(payload.get("width", 1200))
    height = int(payload.get("height", 800))
    scale = int(payload.get("scale", 2))

    if not fig_dict:
        return jsonify({"error": "Missing figure JSON"}), 400

    import plotly.graph_objects as go
    fig = go.Figure(fig_dict)

    try:
        import kaleido  # noqa: F401
        tmp = tempfile.NamedTemporaryFile(suffix=f".{fmt}", delete=False)
        tmp.close()
        pio.write_image(fig, tmp.name, format=fmt, width=width, height=height, scale=scale)
        return send_file(tmp.name, as_attachment=True, download_name=f"plasmidflow.{fmt}")
    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

@api_bp.route("/style/save", methods=["POST"])
def style_save():
    """Persist a style JSON profile for the current session; return style_id."""
    payload = request.get_json(silent=True) or {}
    name = payload.get("name") or f"style-{dt.datetime.utcnow().isoformat()}"
    style = payload.get("style", {})
    sp = StyleProfile(name=name, style_json=json.dumps(style), owner_sid=session.get("sid"))
    db.session.add(sp)
    db.session.commit()
    return jsonify({"style_id": sp.id, "name": sp.name})

@api_bp.route("/style/<int:style_id>", methods=["GET"])
def style_get(style_id):
    sp = db.session.get(StyleProfile, style_id)
    if not sp:
        return jsonify({"error": "Style not found"}), 404
    if sp.owner_sid and sp.owner_sid != session.get("sid"):
        return jsonify({"error": "Not authorized"}), 403
    return jsonify({"style_id": sp.id, "name": sp.name, "style": json.loads(sp.style_json)})