from hull_core.auth import AuthContext, reset_current_user, set_current_user

import telegram.server as srv


def test_not_ready_response_unconfigured():
    """Unconfigured default namespace: CLI setup hints plus env var names."""
    old_unconfigured = srv._unconfigured
    try:
        srv._unconfigured = True
        data = srv._not_ready_response()
        assert data["error"] == "Not configured"
        setup = data["setup"]
        assert set(setup) == {"bot_mode", "user_mode"}
        assert setup["bot_mode"]["command"] == "telegram auth --bot-token <token>"
        assert setup["bot_mode"]["env_var"] == "TELEGRAM_BOT_TOKEN"
        assert setup["user_mode"]["command"] == "telegram auth --phone <+number>"
        assert setup["user_mode"]["env_vars"] == ["TELEGRAM_PHONE"]
    finally:
        srv._unconfigured = old_unconfigured


def test_not_ready_response_unconfigured_namespace():
    """A non-default namespace gets ``--user`` hints and no env var hints."""
    token = set_current_user(AuthContext(uid="a", namespace="a", mode="multi"))
    try:
        data = srv._not_ready_response()
    finally:
        reset_current_user(token)
    setup = data["setup"]
    assert setup["bot_mode"]["command"].endswith("--user a")
    assert setup["user_mode"]["command"].endswith("--user a")
    assert "env_var" not in setup["bot_mode"]
    assert "env_vars" not in setup["user_mode"]


def test_not_ready_response_authenticated_error():
    """Test _not_ready_response when _unconfigured is False."""
    old_unconfigured = srv._unconfigured
    try:
        srv._unconfigured = False
        data = srv._not_ready_response()
        assert "error" in data
        assert "not authenticated" in data["error"].lower()
    finally:
        srv._unconfigured = old_unconfigured
