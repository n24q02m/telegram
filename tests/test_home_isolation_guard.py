"""Guard: the autouse ``_isolate_per_plugin_home`` fixture must stay in place.

The fixture in conftest.py is defense-in-depth -- no test leaks into the real
home today. These tests exist so that if someone deletes the fixture, the
suite goes red immediately instead of silently starting to write into the
developer's (or the CI runner's) real ~/.telegram/.

``test_single_user_write_stays_out_of_the_real_store`` is the load-bearing
one. It drives the production path that can genuinely write there:
``credential_state._write_single_user_config`` -> hull ``PerPluginStore("telegram")``
-> ``backend_from_env()`` -> ``LocalFsBackend`` -> ``~/.telegram/config.json``
plus the ``.secret`` machine key.

Note the asserts compare against the real *store* directory, not the real
home. On Windows pytest's tmp_path lives under ``~\\AppData\\Local\\Temp``,
so "is not under the real home" is false for a correctly isolated path.
"""

from __future__ import annotations

import os
from pathlib import Path

import hull_core.storage.legacy_config_file as legacy_config_file
from hull_core.storage import PerPluginStore

from telegram.credential_state import PLUGIN_NAME, _write_single_user_config

# Captured at import time: collection runs before any fixture, so this is the
# genuine home directory, whatever the fixture later redirects Path.home() to.
_REAL_HOME = Path(os.path.expanduser("~")).resolve()
_REAL_STORE_DIR = _REAL_HOME / ".telegram"
_REAL_LEGACY_PATH = legacy_config_file.default_legacy_config_path().resolve()

FAKE_TOKEN = "123456:" + "G" * 35


def _snapshot(directory: Path) -> set[tuple[str, int, int]]:
    """Identify every file under directory by path, size and mtime.

    Works whether or not the directory exists, so this never assumes the
    developer has no real ~/.telegram/ of their own.
    """
    if not directory.exists():
        return set()
    return {
        (str(path), path.stat().st_size, path.stat().st_mtime_ns)
        for path in directory.rglob("*")
        if path.is_file()
    }


def test_home_is_redirected_away_from_the_real_home():
    assert Path.home().resolve() != _REAL_HOME


def test_legacy_config_path_is_redirected():
    assert legacy_config_file.default_legacy_config_path().resolve() != (
        _REAL_LEGACY_PATH
    )


def test_per_plugin_store_path_is_not_in_the_real_store_dir():
    cred_path = PerPluginStore(PLUGIN_NAME).cred_path
    assert cred_path is not None
    cred_path = cred_path.resolve()
    assert _REAL_STORE_DIR != cred_path
    assert _REAL_STORE_DIR not in cred_path.parents


def test_single_user_write_stays_out_of_the_real_store():
    """Drive the production write path that can reach the real home."""
    # Resolve where the write would land BEFORE performing it. A guard that
    # pollutes the real store when it fires is self-defeating: on a developer
    # machine _write_single_user_config would overwrite real credentials.
    cred_path = PerPluginStore(PLUGIN_NAME).cred_path
    assert cred_path is not None
    assert _REAL_STORE_DIR not in cred_path.resolve().parents, (
        f"refusing to run the write probe: it would land in {cred_path}. "
        "Restore _isolate_per_plugin_home in tests/conftest.py."
    )

    before = _snapshot(_REAL_STORE_DIR)
    _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN})

    written = sorted(Path.home().glob(".telegram/*"))
    assert written, "expected the LocalFsBackend write to land in the tmp home"
    for path in written:
        assert _REAL_STORE_DIR not in path.resolve().parents
    assert _snapshot(_REAL_STORE_DIR) == before
