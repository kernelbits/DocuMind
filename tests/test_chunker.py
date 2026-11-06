import pytest

from reader import TextChunker


def test_empty_text_produces_no_chunks():
    assert TextChunker().chunk("") == []


def test_short_text_is_a_single_chunk():
    assert TextChunker().chunk("hello world") == ["hello world"]


def test_default_size_and_overlap_are_600_and_50():
    text = "x" * 1500
    chunks = TextChunker().chunk(text)

    # Window starts at 0, 550, 1100 -> lengths 600, 600, 400.
    assert [len(c) for c in chunks] == [600, 600, 400]


def test_consecutive_chunks_share_the_overlap():
    text = "".join(str(i % 10) for i in range(2000))
    chunks = TextChunker().chunk(text)

    assert len(chunks) > 1
    for first, second in zip(chunks, chunks[1:]):
        assert first[-50:] == second[:50]


def test_chunks_cover_the_whole_text():
    text = "".join(chr(ord("a") + (i % 26)) for i in range(1234))
    chunks = TextChunker().chunk(text)

    assert chunks[0][0] == text[0]
    assert chunks[-1][-1] == text[-1]
    # Each window starts at a multiple of (size - overlap) = 550.
    for index, chunk in enumerate(chunks):
        assert chunk == text[index * 550 : index * 550 + 600]


def test_custom_size_and_overlap():
    chunks = TextChunker().chunk("abcdefghij", chunk_size=4, overlap=1)

    assert chunks == ["abcd", "defg", "ghij", "j"]


@pytest.mark.parametrize(
    "text, chunk_size, overlap",
    [
        (123, 600, 50),        # text must be a string
        ("abc", 0, 0),         # chunk size must be positive
        ("abc", -5, 0),        # chunk size must be positive
        ("abc", 600.0, 50),    # sizes must be integers
        ("abc", 600, 600),     # overlap must be smaller than chunk size
        ("abc", 600, -1),      # overlap cannot be negative
    ],
)
def test_invalid_arguments_raise_value_error(text, chunk_size, overlap):
    with pytest.raises(ValueError):
        TextChunker().chunk(text, chunk_size=chunk_size, overlap=overlap)
