from nightferry import endings, facts, premise
from nightferry.state import State


def test_there_are_sixteen_facts():
    assert len(facts.FACTS) == 16


def test_every_lead_points_at_a_fact_and_never_names_it():
    for factId in facts.FACTS:
        for target, line in facts.leads(factId):
            assert target in facts.FACTS, (factId, target)
            assert target != factId
            assert facts.title(target).lower() not in line.lower(), (factId, target)


def test_every_fact_but_the_first_is_led_to():
    ledTo = {target for f in facts.FACTS for target, _ in facts.leads(f)}
    for factId in facts.FACTS:
        if factId == facts.CABIN_SIX:
            continue
        assert factId in ledTo, factId


def test_every_fact_is_reachable_from_the_first_through_the_web():
    seen, frontier = {facts.CABIN_SIX}, [facts.CABIN_SIX]
    while frontier:
        for target, _ in facts.leads(frontier.pop()):
            if target not in seen:
                seen.add(target)
                frontier.append(target)
    assert seen == set(facts.FACTS)


def test_the_trail_is_connected_by_leads():
    for earlier, later in zip(facts.TRAIL, facts.TRAIL[1:]):
        assert later in [t for t, _ in facts.leads(earlier)], (earlier, later)
    assert facts.TRAIL[-1] == facts.THE_CAPTAIN


def test_the_premise_page_grows_with_what_is_known_and_says_the_ending():
    state = State()
    empty = premise.text(state)
    assert "WHERE YOU ARE" in empty
    assert "WHAT IS HAPPENING TO YOU" not in empty
    state.learn(facts.CABIN_SIX)
    assert "WHAT IS HAPPENING TO YOU. Cabin 6 was booked" in premise.text(state)
    for factId in facts.FACTS:
        state.learn(factId)
    state.ending = endings.KEPT_CROSSING
    full = premise.text(state)
    assert "THE ANSWER. Cabin 6 was for Maren Sollid." in full
    assert "HOW IT ENDED. You kept the captain's secret" in full
    assert "HOW IT ENDED. Off the light" not in full
    parts = len(premise.PARAGRAPHS) - len(endings.ENDINGS) + 1
    assert "(%d of %d parts" % (parts, parts) in full


def test_every_fact_is_needed_by_some_premise_paragraph():
    needed = {f for needs, _, _ in premise.PARAGRAPHS for f in needs}
    assert needed == set(facts.FACTS)


def test_every_ending_has_a_premise_paragraph():
    named = {ending for _, ending, _ in premise.PARAGRAPHS if ending}
    assert named == set(endings.ENDINGS)
