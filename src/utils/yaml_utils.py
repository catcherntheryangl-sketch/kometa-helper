"""
yaml_utils.py - Helpers for YAML editing, validation, and template generation
"""

import yaml
from typing import Any


KOMETA_CONFIG_TEMPLATE = {
    "plex": {
        "url": "",
        "token": "",
        "timeout": 60,
        "db_cache": None,
        "clean_bundles": False,
        "empty_trash": False,
        "optimize": False,
    },
    "tmdb": {
        "apikey": "",
        "language": "en",
        "region": "US",
        "cache_expiration": 60,
    },
    "settings": {
        "cache": True,
        "cache_expiration": 60,
        "asset_directory": ["config/assets"],
        "asset_folders": True,
        "asset_depth": 0,
        "create_asset_folders": False,
        "prioritize_assets": False,
        "dimensional_asset_rename": False,
        "download_url_assets": False,
        "show_missing_season_assets": False,
        "show_missing_episode_assets": False,
        "show_asset_not_needed": True,
        "sync_mode": "append",
        "default_collection_order": None,
        "minimum_items": 1,
        "delete_below_minimum": True,
        "delete_not_scheduled": False,
        "run_again_delay": 2,
        "missing_only_released": False,
        "only_filter_missing": False,
        "show_unmanaged_collections": True,
        "show_unconfigured_collections": True,
        "show_filtered": False,
        "show_options": False,
        "show_missing": True,
        "show_missing_assets": True,
        "save_report": False,
        "tvdb_language": "eng",
        "ignore_ids": None,
        "ignore_imdb_ids": None,
        "playlist_sync_to_users": "all",
        "playlist_exclude_users": None,
        "playlist_report": False,
        "custom_repo": None,
        "check_nightly": False,
        "show_missing_episode_collector": True,
    },
    "libraries": {},
}


COLLECTION_TEMPLATE = {
    "collections": {
        "My Collection": {
            "tmdb_popular": 10,
            "sort_title": "!010_My Collection",
            "sync_mode": "sync",
            "collection_order": "release",
            "summary": "A custom collection",
        }
    }
}


OVERLAY_TEMPLATE = {
    "overlays": {
        "Resolution": {
            "overlay": {
                "name": "resolution",
            }
        }
    }
}


LIBRARY_ENTRY_TEMPLATE = {
    "collection_files": [],
    "overlay_files": [],
    "operations": {
        "mass_genre_update": None,
        "mass_audience_rating_update": None,
        "mass_critic_rating_update": None,
        "mass_user_rating_update": None,
    },
}

DEFAULTS_COLLECTIONS = [
    "defaults/collections/audio_language",
    "defaults/collections/award",
    "defaults/collections/based_on",
    "defaults/collections/content_rating_cs",
    "defaults/collections/content_rating_uk",
    "defaults/collections/content_rating_us",
    "defaults/collections/country",
    "defaults/collections/decade",
    "defaults/collections/director",
    "defaults/collections/franchise",
    "defaults/collections/genre",
    "defaults/collections/network",
    "defaults/collections/producer",
    "defaults/collections/resolution",
    "defaults/collections/seasonal",
    "defaults/collections/separator_award",
    "defaults/collections/separator_chart",
    "defaults/collections/streaming",
    "defaults/collections/studio",
    "defaults/collections/subtitle_language",
    "defaults/collections/universe",
    "defaults/collections/writer",
    "defaults/collections/chart/anidb",
    "defaults/collections/chart/basic",
    "defaults/collections/chart/imdb",
    "defaults/collections/chart/myanimelist",
    "defaults/collections/chart/tautulli",
    "defaults/collections/chart/tmdb",
    "defaults/collections/chart/trakt",
]

DEFAULTS_OVERLAYS = [
    "defaults/overlays/audio_codec",
    "defaults/overlays/audio_language",
    "defaults/overlays/commonsense",
    "defaults/overlays/content_rating_cs",
    "defaults/overlays/content_rating_uk",
    "defaults/overlays/content_rating_us",
    "defaults/overlays/direct_play",
    "defaults/overlays/episode_info",
    "defaults/overlays/flixpatrol",
    "defaults/overlays/imdb_top_250",
    "defaults/overlays/mediastinger",
    "defaults/overlays/network",
    "defaults/overlays/personal_ratings",
    "defaults/overlays/ratings",
    "defaults/overlays/resolution",
    "defaults/overlays/rotten_tomatoes",
    "defaults/overlays/status",
    "defaults/overlays/streaming",
    "defaults/overlays/studio",
    "defaults/overlays/subtitle_language",
    "defaults/overlays/tautulli",
    "defaults/overlays/tmdb_top_rated",
    "defaults/overlays/trakt_top",
    "defaults/overlays/versions",
]


def yaml_to_string(data: Any, indent: int = 2) -> str:
    return yaml.dump(data, default_flow_style=False, allow_unicode=True,
                     sort_keys=False, indent=indent)


def string_to_yaml(text: str) -> tuple[Any, str]:
    """Returns (parsed_data, error_string). error_string is '' on success."""
    try:
        return yaml.safe_load(text), ""
    except yaml.YAMLError as e:
        return None, str(e)


def build_config_yml(
    plex_url: str,
    plex_token: str,
    tmdb_key: str,
    libraries: list[dict],
    extra: dict = None,
) -> dict:
    """Build a minimal valid config.yml from collected settings."""
    cfg = {
        "plex": {"url": plex_url, "token": plex_token},
        "tmdb": {"apikey": tmdb_key},
        "libraries": {},
    }
    for lib in libraries:
        name = lib.get("title", "Unknown")
        lib_entry = {}
        if lib.get("collection_files"):
            lib_entry["collection_files"] = [{"default": f} for f in lib["collection_files"]]
        if lib.get("overlay_files"):
            lib_entry["overlay_files"] = [{"default": f} for f in lib["overlay_files"]]
        cfg["libraries"][name] = lib_entry

    if extra:
        cfg.update(extra)
    return cfg


def get_friendly_yaml_error(error: str) -> str:
    """Convert a yaml.YAMLError string into a plain-English hint."""
    if "mapping values are not allowed here" in error:
        return "Indentation or colon error — check that your YAML keys are properly indented and that colons are followed by a space."
    if "could not find expected ':'" in error:
        return "Missing colon — every key needs a colon after it."
    if "found duplicate key" in error:
        return "Duplicate key — you have the same key name twice at the same level."
    if "found character '\\t'" in error:
        return "Tab character found — YAML requires spaces for indentation, not tabs."
    return f"YAML error: {error}"
