from unified_discovery import Chat, UnifiedDiscoveryEngine


def test_related_pair_beats_unrelated_pair():
    e = UnifiedDiscoveryEngine()
    chats = [
        Chat("A", "human communication puzzle and question generation for AI agents"),
        Chat("B", "question generation connects to agent memory and reasoning"),
        Chat("C", "recipe for mango chutney with spices"),
    ]
    rel = e.relate(chats)
    assert rel[0].a in {"A", "B"} and rel[0].b in {"A", "B"}
    assert rel[0].score > rel[-1].score


def test_graph_and_complementary_hypothesis():
    e = UnifiedDiscoveryEngine()
    chats = [
        Chat("A", "graph memory reasoning systems"),
        Chat("B", "memory graph agents deployment tooling"),
    ]
    graph = e.graph(chats)
    assert len(graph["relations"]) == 1
    hypotheses = e.hypotheses(chats)
    assert hypotheses and hypotheses[0]["pair"] == ["A", "B"]


def test_contradiction_baseline_is_explicit():
    e = UnifiedDiscoveryEngine()
    assert e.contradictions([Chat("A", "this is useful and strong")]) == []
