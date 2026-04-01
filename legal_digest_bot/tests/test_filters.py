from legal_digest_bot.crawler import extract_bench_and_judges, match_acts, match_court, summarize_points


def test_match_court_and_acts():
    text = (
        "The Supreme Court held in a case under the Indian Contract Act and Constitution of India "
        "that relief could be granted."
    )
    assert match_court(text) == "Supreme Court of India"
    acts = match_acts(text)
    assert "indian contract act" in acts
    assert "constitution of india" in acts


def test_extract_bench_and_judges():
    text = "Coram: Justice A B Sharma and Justice C D Singh. The bench observed as follows."
    bench, judges = extract_bench_and_judges(text)
    assert "Justice A B Sharma" in bench
    assert "Justice A B Sharma" in judges[0]


def test_summarize_points_prioritizes_relevant_sentences():
    text = (
        "The bench discussed procedure. "
        "The Supreme Court observed that the Indian Evidence Act applies fully. "
        "The court held that the appeal should be allowed. "
        "A procedural history paragraph follows with less relevance."
    )
    points = summarize_points(text, ["indian evidence act"], "Supreme Court of India", max_points=2)
    assert len(points) == 2
