from app.traps.injector import Injector


def test_injector_safe_mode_inert_payload():
    injector = Injector(safe_mode=True, seed="123")
    content = injector.inject("base")
    assert "base" in content
    assert "SAFE MODE" in content
