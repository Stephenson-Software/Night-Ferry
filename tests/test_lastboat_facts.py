from nightferry import facts as firstFacts
from nightferry.lastboat import facts


def test_there_are_thirteen_and_none_shares_an_id_with_october():
    assert len(facts.FACTS) == 13
    assert not set(facts.FACTS) & set(firstFacts.FACTS)


def test_every_lead_points_at_a_fact_and_never_names_it():
    for factId in facts.FACTS:
        for target, line in facts.leads(factId):
            assert target in facts.FACTS, (factId, target)
            assert target != factId
            assert facts.title(target).lower() not in line.lower(), (factId, target)


def test_every_fact_is_reachable_from_the_first_through_the_web():
    seen, frontier = {facts.SIX_TONIGHT}, [facts.SIX_TONIGHT]
    while frontier:
        for target, _ in facts.leads(frontier.pop()):
            if target not in seen:
                seen.add(target)
                frontier.append(target)
    assert seen == set(facts.FACTS)


def test_the_trail_is_connected_by_leads():
    for earlier, later in zip(facts.TRAIL, facts.TRAIL[1:]):
        assert later in [t for t, _ in facts.leads(earlier)], (earlier, later)
    assert facts.TRAIL[-1] == facts.THE_ANSWER
