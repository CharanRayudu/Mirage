from app.traps.labyrinth import labyrinth


def test_labyrinth_generates_deterministic_path():
    path_a = labyrinth.generate_next_step("foo/bar.txt")
    path_b = labyrinth.generate_next_step("foo/bar.txt")
    assert path_a == path_b
    assert "hidden" in path_a
