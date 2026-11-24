from chain.graph import build_graph


def test_boucle_s_arrete_apres_deux_tentatives():
    graph = build_graph()
    etat_final = graph.invoke({"task": "fizzbuzz", "attempts": 0})
    assert etat_final["attempts"] == 2


def test_ordre_execution_noeuds():
    graph = build_graph()
    noeuds_executes = [nom for etape in graph.stream({"task": "fizzbuzz", "attempts": 0}) for nom in etape]
    assert noeuds_executes == ["spec", "coder", "fake_runner", "coder", "fake_runner"]
