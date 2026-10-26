"""``config status`` / ``status`` / ``doctor`` parity with the server's store.

Regression coverage for the original mismatch: the server persisted
credentials under one key while the CLI built-ins read another, so a saved
credential was reported as "not configured". With hull, the server writes
``PerPluginStore("telegram")`` and ``build_cli(plugin_name="telegram")`` reads
the same blob. A pre-hull ``config.enc`` entry is migrated before a store
built-in runs, so an upgraded install is reported as configured without
starting the server first.

Everything runs against the real store and legacy file under the fake home of
the autouse ``_isolate_per_plugin_home`` fixture.
"""

from __future__ import annotations

import pytest
from hull_core.storage import PerPluginStore
from legacy_store import read_legacy_entry, write_legacy_store

from telegram import cli
from telegram.credential_state import (
    PLUGIN_NAME,
    _delete_single_user_config,
    _write_single_user_config,
)
from telegram.sessions import SERVER_NAME

FAKE_TOKEN = "123456:" + "S" * 35


def _run(capsys, *argv: str) -> tuple[int, str]:
    rc = cli.main(list(argv))
    captured = capsys.readouterr()
    assert FAKE_TOKEN not in captured.out + captured.err
    return rc, captured.out


@pytest.mark.parametrize("argv", [("config", "status"), ("status",)])
def test_builtins_report_configured_after_save(capsys, argv):
    _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN})
    rc, out = _run(capsys, *argv)
    assert rc == 0
    assert "not configured" not in out
    assert "configured" in out


@pytest.mark.parametrize("argv", [("config", "status"), ("status",)])
def test_builtins_report_not_configured_after_delete(capsys, argv):
    _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN})
    _delete_single_user_config()
    rc, out = _run(capsys, *argv)
    assert rc == 0
    assert "not configured" in out


@pytest.mark.parametrize("argv", [("config", "status"), ("status",)])
def test_legacy_only_install_reports_configured(capsys, argv):
    """An upgraded install is configured before the server ever starts."""
    write_legacy_store({SERVER_NAME: {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}})
    rc, out = _run(capsys, *argv)
    assert rc == 0
    assert "not configured" not in out
    assert PerPluginStore(PLUGIN_NAME).load() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}
    assert read_legacy_entry(SERVER_NAME) is None


def test_non_store_subcommands_do_not_migrate(capsys):
    write_legacy_store({SERVER_NAME: {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}})
    rc, _ = _run(capsys, "--version")
    assert rc == 0
    assert PerPluginStore(PLUGIN_NAME).load() is None
    assert read_legacy_entry(SERVER_NAME) == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}


def test_config_delete_clears_migrated_legacy_entry(capsys):
    write_legacy_store({SERVER_NAME: {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}})
    rc, _ = _run(capsys, "config", "delete", "--yes")
    assert rc == 0
    assert PerPluginStore(PLUGIN_NAME).load() is None
    assert read_legacy_entry(SERVER_NAME) is None


def test_failed_migration_still_runs_builtin(capsys, monkeypatch):
    import telegram.credential_state as cs

    def _boom(*_a, **_k):
        raise OSError("unreadable")

    monkeypatch.setattr(cs, "_read_single_user_config", _boom)
    rc = cli.main(["status"])
    captured = capsys.readouterr()
    assert rc == 0
    assert "not configured" in captured.out
    assert "legacy credential migration skipped (OSError)" in captured.err
