from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

from primitives import DrumSound, NoteLength, Primitive
from src.utils import lse

LogProb = float

Production = Tuple[
    LogProb,
    Union[NoteLength, DrumSound],
]

Type = Union[NoteLength, DrumSound]


@dataclass
class LikelihoodSummary:
    """Tracks usage of primitives in a program"""

    # Count how many times each primitive is used
    uses: Dict[Primitive, int] = {}

    # Store normalizing constants
    normalizers: Dict[frozenset, float] = {}

    # Constant term in log likelihood
    constant: float = 0.0

    def record(self, actual: Primitive, possibles: List[Type]):
        """
        actual: The primitive that was actually used
        possibles: Set of all primitives that could have been used at this position
        """

        possibles = frozenset(sorted(possibles, key=hash))
        self.uses[actual] = self.uses.get(actual, 0) + 1
        self.normalizers[possibles] = self.normalizers.get(possibles, 0.0) + 1

    def logLikelihood(self, grammar):
        return (
            self.constant
            + sum(
                count * grammar.primitive_to_logprob[p]
                for p, count in self.uses.items()
            )
            - sum(
                count * lse([grammar.primitive_to_logprob[p] for p in ps])
                for ps, count in self.normalizers.items()
            )
        )


class Grammar:
    def __init__(self, productions: List[Production]):
        self.productions = productions
        self.primitive_to_logprob = {p: logprob for logprob, p in productions}

    @staticmethod
    def uniform(primitives: List[Primitive]) -> "Grammar":
        return Grammar([(0.0, p) for p in primitives])

    def get_candidates(self, request: Type) -> List[Production]:
        """Each position in program has a set of valid candidates depending on the position's type."""

        # if the type system was more complex, we would need to perform type unification here
        return [p for p in self.productions if isinstance(p[1], type(request))]

    def inside_outside(self) -> Production:
        pass

    def likelihood_summary(self, request: Type):
        candidates = self.get_candidates(request)
        possibles = set([type(p[1]) for p in candidates])
