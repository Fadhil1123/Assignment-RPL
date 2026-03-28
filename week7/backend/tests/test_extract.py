from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "Ship it!" in items


def test_extract_action_items_with_extended_patterns_and_deduplication():
    text = """
    Notes for the week
    1) Please update API docs before Friday
    2) Need to assign owner: Andi
    3) Follow up with QA team
    - todo: write tests
    - TODO: write tests
    random status update
    """.strip()

    items = extract_action_items(text)
    assert "Please update API docs before Friday" in items
    assert "Need to assign owner: Andi" in items
    assert "Follow up with QA team" in items
    assert "todo: write tests" in [item.lower() for item in items]
    assert len([item for item in items if "write tests" in item.lower()]) == 1


def test_extract_action_items_empty_input():
    assert extract_action_items("") == []
