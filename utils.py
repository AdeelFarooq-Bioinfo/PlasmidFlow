import io
import pandas as pd

REQUIRED_COLUMNS = {"Plasmid_ID", "Host_Genome", "Environment", "ARGs", "Virulence", "T4SS", "MGEs"}

def parse_csv_file(stream) -> pd.DataFrame:
    """Read CSV from a file-like object using pandas with UTF-8 fallback."""
    raw = stream.read()
    try:
        txt = raw.decode("utf-8")
    except Exception:
        txt = raw.decode("latin-1")
    return pd.read_csv(io.StringIO(txt))

def validate_dataframe(df: pd.DataFrame):
    """Ensure required columns exist and dataframe not empty."""
    if df is None or df.empty:
        return False, "Uploaded file is empty."
    missing = REQUIRED_COLUMNS.difference(set(df.columns))
    if missing:
        return False, f"Missing required columns: {', '.join(sorted(missing))}"
    return True, "ok"

def filter_by_traits(df: pd.DataFrame, traits):
    """Filter rows where selected traits are present (not equal to 'no' case-insensitive)."""
    for t in traits or []:
        if t in df.columns:
            df = df[df[t].astype(str).str.lower() != "no"]
    return df

def dataframe_preview(df: pd.DataFrame, n=5):
    """Return a simple preview (columns + first n rows) for the front end."""
    return {
        "columns": list(df.columns),
        "rows": df.head(n).to_dict(orient="records"),
        "n_total": int(df.shape[0])
    }