from dataclasses import dataclass
from tasty import Corpus, CellComponent, encode, pipe


@dataclass
class TastyPair(CellComponent):
    foo: str
    bar: int

    @property
    def serialized(self):
        return self._serialize(
            self.foo | pipe | encode,
            self.bar | pipe | str
        )


@dataclass
class Quux:
    value: str


@dataclass
class TastyTriple(CellComponent):
    baz: str
    qux: int
    quux: Quux

    @property
    def serialized(self):
        return self._serialize(
            self.baz | pipe | encode,
            self.qux | pipe | str,
            self.quux.value | pipe | encode
        )


written_corpus = Corpus(
    (
        (
            (
                (TastyPair('one', 1), ),
                (TastyTriple('two', 2, Quux('three')), TastyTriple('two', 2, Quux('three')))
            ),
            (
                (TastyPair('three', 3), ),
                (TastyTriple('four', 4, Quux('five')), )
            )
        ),
        (
            (
                (TastyPair('six', 6), ),
                (TastyTriple('seven', 7, Quux('eight')), )
            ),
        )
    )
).write('corpus.txt', header = ('pair', 'triple'))

read_corpus = Corpus.read('corpus.txt', parsers = (TastyPair, TastyTriple))

assert read_corpus.data == written_corpus.data
