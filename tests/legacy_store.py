"""Write a pre-hull mcp-core ``config.enc`` for the migration tests.

mcp-core is no longer a dependency, so the file is produced here in its
current on-disk format (``[16-byte salt][12-byte IV][AES-GCM ciphertext]``,
key ``PBKDF2-HMAC-SHA256("<machine_id>:<username>", salt, 600_000)``), the
format hull's read-only ``legacy_config_file`` decrypts. The path is the fake
one installed by the autouse ``_isolate_per_plugin_home`` fixture.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

import hull_core.storage.legacy_config_file as legacy_config_file
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def legacy_path() -> Path:
    return legacy_config_file.default_legacy_config_path()


def write_legacy_store(servers: dict[str, dict[str, Any]]) -> Path:
    salt = os.urandom(16)
    material = f"{legacy_config_file.machine_id()}:{legacy_config_file.username()}"
    key = hashlib.pbkdf2_hmac(
        "sha256",
        material.encode(),
        salt,
        legacy_config_file.PBKDF2_ITERATIONS,
        dklen=32,
    )
    iv = os.urandom(12)
    plaintext = json.dumps({"version": 1, "servers": servers}).encode("utf-8")
    path = legacy_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(salt + iv + AESGCM(key).encrypt(iv, plaintext, None))
    return path


def read_legacy_entry(server_name: str) -> dict[str, Any] | None:
    return legacy_config_file.read_legacy_config(server_name)
