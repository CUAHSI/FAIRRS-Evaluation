"""
Convert HydroShare Model Program metadata (JSON) to CodeMeta v3.

This CLI mirrors the structure of the provided `csdms2codemeta.py` tool and
expects input files that look like the HydroShare model program JSON shown in
your extract (one JSON per research software object).

Usage
-----
# Single file
python hydroshare2codemeta.py -f path/to/model-program.json -o out_dir

# Directory of files (\*.json)
python hydroshare2codemeta.py -d path/to/dir -o out_dir

Notes
-----
- We map HydroShare fields to CodeMeta where there is a clear correspondence.
- Unknown or missing values are omitted rather than filled with placeholders.
- "downloadUrl" is taken from HydroShare `file_types` entries that represent
  software or engines. We ignore documentation entries for this field.
- "license" is taken from `rights.url` when present, otherwise we fall back to
  embedding the `rights.statement` as a CreativeWork name.
"""

from __future__ import annotations

import json
import logging
from datetime import date, datetime
from glob import glob
from pathlib import Path
from typing import Any, Iterable, List, Optional

import typer
from pydantic.v1 import HttpUrl
from pydantic2_schemaorg.Person import Person
from pydantic2_schemaorg.Organization import Organization
from pydantic2_schemaorg.CreativeWork import CreativeWork
from codemeticulous.codemeta.models import CodeMetaV3, VersionedLanguage


app = typer.Typer(help="Convert HydroShare Model Program JSON to CodeMeta v3")


@app.command()
def encode(
    file: Path | None = typer.Option(
        None,
        "--file",
        "-f",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="path to a single HydroShare JSON file",
    ),
    directory: Path | None = typer.Option(
        None,
        "--directory",
        "-d",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        help="path to a directory containing HydroShare JSON files",
    ),
    output_directory: Path = typer.Option(
        ...,  # required
        "--output_directory",
        "-o",
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        help="directory to write CodeMeta JSON output",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="verbose logging"),
) -> None:
    """Main entry point for converting one file or a directory of files."""

    # Ensure exactly one of file or directory was provided
    if (file is None and directory is None) or (file is not None and directory is not None):
        typer.echo("Error: provide exactly one of --file or --directory", err=True)
        raise typer.Exit(code=1)

    logging.basicConfig(level=logging.INFO if verbose else logging.ERROR, format="%(message)s")

    if file:
        _process_one(file, output_directory, verbose)
    else:
        files = sorted(Path(directory).glob("*.json"))
        total = len(files)
        for i, f in enumerate(files, start=1):
            logging.info(f"Processing file [{i} of {total}]: {f}")
            _process_one(f, output_directory, verbose)


def _process_one(file: Path, output_directory: Path, verbose: bool) -> None:
    cm = build_codemeta(file)

    # Pretty-print using json library (codemeticulous' .json() may not indent)
    json_data = json.loads(cm.json())
    out_path = output_directory / f"{file.stem}.json"
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(json_data, fh, indent=4, ensure_ascii=False)

    if verbose:
        logging.info(json.dumps(json_data, indent=4, ensure_ascii=False))


# -------------------------------
# Core converter
# -------------------------------

def build_codemeta(json_file: Path) -> CodeMetaV3:
    """Read one HydroShare JSON file and emit a CodeMetaV3 model.

    Parameters
    ----------
    json_file : Path
        Path to a HydroShare model program JSON file.
    """
    with json_file.open("r", encoding="utf-8") as fh:
        hs = json.load(fh)

    # -----------------
    # Basic properties
    # -----------------
    name: Optional[str] = hs.get("title") or _basename_fallback(json_file)

    # Keywords
    subjects = _as_list(hs.get("subjects")) or None

    # Programming languages -> List[VersionedLanguage]
    plangs_raw = _as_list(hs.get("programming_languages"))
    programmingLanguage = [VersionedLanguage(name=p) for p in plangs_raw] if plangs_raw else None

    # Operating systems
    operatingSystem = _as_list(hs.get("operating_systems")) or None

    # Version
    softwareVersion = hs.get("version") or None

    # Dates
    datePublished = _parse_datetime(hs.get("published"))  # HydroShare timestamp -> date

    # Web presence
    website = hs.get("website")
    codeRepository = hs.get("code_repository")

    # Choose url: prefer website; else HydroShare landing page; else aggregation URL
    url = None
    if website:
        url = _as_http_url(website)
    else:
        rid = hs.get("resource_id")
        agg_url = hs.get("url")
        if rid:
            url = _as_http_url(f"https://www.hydroshare.org/resource/{rid}")
        elif agg_url:
            url = _as_http_url(agg_url)

    # License -> from rights block
    license_obj = None
    rights = hs.get("rights") or {}
    rights_url = rights.get("url")
    rights_stmt = rights.get("statement")
    if rights_url or rights_stmt:
        license_obj = CreativeWork(name=rights_stmt,url=_as_http_url(rights_url))

    # downloadUrl(s) from file_types entries that indicate software/engine/executable
    downloadUrl = _extract_download_urls(hs.get("file_types")) or None

    # Authors
    author = _authors_from_creators(hs.get("creators") or []) or None

    # Identifier (resource_id)
    identifier = hs.get("resource_id")

    # applicationCategory: we use first subject if nothing else
    applicationCategory = None
    if subjects:
        applicationCategory = subjects[0]

    # Build CodeMeta object
    meta = CodeMetaV3(
        name=name,
        author=author,
        description=None,  # HydroShare Model Program JSON rarely includes a rich description field
        keywords=subjects,
        programmingLanguage=programmingLanguage,
        operatingSystem=operatingSystem,
        softwareVersion=softwareVersion,
        codeRepository=_as_http_url(codeRepository) if codeRepository else None,
        url=url,
        datePublished=datePublished,
        downloadUrl=downloadUrl,
        applicationCategory=applicationCategory,
        identifier=identifier,
    )

    # Skip validation for license via attribute assignment (pattern used in reference script)
    meta.license = license_obj

    return meta


# -------------------------------
# Helpers
# -------------------------------

def _as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [v for v in value if v is not None]
    return [value]


def _basename_fallback(path: Path) -> str:
    return path.stem.replace("-model-program", "")


def _parse_datetime(ts: Optional[str]) -> Optional[date]:
    if not ts:
        return None
    # HydroShare example: "2021-11-04 16:36:44.150474+00:00"
    try:
        # Try multiple formats robustly
        for fmt in (
            "%Y-%m-%d %H:%M:%S.%f%z",
            "%Y-%m-%d %H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ):
            try:
                dt = datetime.strptime(ts, fmt)
                return dt.date()
            except ValueError:
                continue
    except Exception:
        return None
    return None


def _as_http_url(url_str: str | None) -> Optional[HttpUrl]:
    if not url_str:
        return None
    try:
        scheme = url_str.split(":")[0]
        return HttpUrl(scheme=scheme, url=url_str)
    except Exception:
        return None


_SOFTWARE_LIKE_TYPES = {
    "https://www.hydroshare.org/terms/modelSoftware",
    "https://www.hydroshare.org/terms/modelEngine",
    "https://www.hydroshare.org/terms/modelProgramSoftware",
}


def _extract_download_urls(file_types: Optional[Iterable[dict]]) -> Optional[list[HttpUrl]]:
    if not file_types:
        return None
    urls: list[HttpUrl] = []
    for ft in file_types:
        t = (ft or {}).get("type")
        u = (ft or {}).get("url")
        if not u:
            continue
        if (t in _SOFTWARE_LIKE_TYPES) or (t and ("Software" in t or "Engine" in t)):
            http_u = _as_http_url(u)
            if http_u:
                urls.append(http_u)
    return urls or None


def _authors_from_creators(creators: list[dict[str, Any]]) -> list[Person]:
    people: list[Person] = []
    for c in creators:
        name = (c or {}).get("name")
        # Try to parse given/family from a "Last, First" or "First Last" name if possible
        given, family = _split_name(name)
        email = (c or {}).get("email")
        org = (c or {}).get("organization")
        address_bits = []
        if (c or {}).get("address"):
            address_bits.append(c.get("address"))
        # Build affiliation if we have organization
        affiliation = None
        if org:
            affiliation = Organization(name=org, address=", ".join(address_bits) if address_bits else None)
        person = Person(givenName=given, familyName=family, email=email, affiliation=affiliation)
        people.append(person)
    return people


def _split_name(name: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    if not name:
        return None, None
    name = name.strip()
    # Comma style: "Last, First M."
    if "," in name:
        last, first = [part.strip() for part in name.split(",", 1)]
        return first or None, last or None
    # Space style: take last token as family
    parts = name.split()
    if len(parts) == 1:
        return None, parts[0]
    return " ".join(parts[:-1]), parts[-1]


if __name__ == "__main__":
    app()