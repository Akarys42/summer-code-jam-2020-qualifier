"""
Use this file to write your solution for the Summer Code Jam 2020 Qualifier.

Important notes for submission:

- Do not change the names of the two classes included below. The test suite we
  will use to test your submission relies on existence these two classes.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the
  advanced requirements.

- Do not include "debug"-code in your submission. This means that you should
  remove all debug prints and other debug statements before you submit your
  solution.
"""
import datetime
import functools
import itertools
import typing
import re
from operator import itemgetter

VALID_CUTS = (' ', '\n')
WORDS_RE = re.compile("[^a-zA-Z]")


class ArticleField:
    """The `ArticleField` class for the Advanced Requirements."""

    def __init__(self, field_type: typing.Type[typing.Any]):
        pass


@functools.total_ordering  # Let's take it the lazy way
class Article:
    """The *sexy* `Article` class you need to write for the qualifier."""
    id_counter = itertools.count()

    def __init__(self, title: str, author: str, publication_date: datetime.datetime, content: str) -> None:
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self._content = content

        self.id = next(self.id_counter)
        self.last_edited = None

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        self.last_edited = datetime.datetime.now()
        self._content = value

    def short_introduction(self, n_characters: int) -> typing.Optional[str]:
        cuts = []

        for i, c in enumerate(self.content):
            if i < n_characters and c in VALID_CUTS:
                cuts.append(i)

        return self.content[:cuts[-1]]

    def most_common_words(self, n_words: int) -> typing.Dict[str, int]:
        d = {}

        for word in WORDS_RE.split(self.content):
            if word:  # The regex can sometimes output an empty string
                d[word.lower()] = d.get(word.lower(), 0) + 1

        return {k: v for k, v in sorted(d.items(), key=itemgetter(1), reverse=True)[:n_words]}

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} title={repr(self.title)} author={repr(self.author)} " 
            f"publication_date={repr(self.publication_date.isoformat())}>"
        )

    def __len__(self) -> int:
        return len(self.content)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        
        return self.publication_date < other.publication_date

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.publication_date == other.publication_date
