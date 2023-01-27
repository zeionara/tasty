# Tasty

Tasty - **ta**b **s**eparated **t**ables - a human-readable format for nested data serialization. The module allows to represent lists of objects with variable length in the following format:

```sh
pair	triple
one 1	two 2 three two 2 three
three 3	four 4 five

six 6	seven 7 eight
```

Which corresponds to the following data (see `examples/main.py` for more details):

```py
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
```

## Installation

The module doesn't require any additional dependencies. To install from pypi, run the following command:

```sh
pip install tasty
```

## Usage

Default methods for dataset serialization and deserialization are implemented, so the module can be used as follows (see the `main.py` script in the `examples` folder):

```py
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
```
