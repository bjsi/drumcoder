from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

from primitives import DrumSound, NoteLength, Primitive, PrimitiveType
from utils import lse

LogProb = float

Production = Tuple[
    LogProb,
    Union[NoteLength, DrumSound],
]

Type = Union[NoteLength, DrumSound]


class LikelihoodSummary:
    """Tracks usage of primitives in a program"""

    # Count how many times each primitive is used
    uses: Dict[Primitive, int] = {}

    # Store normalizing constants
    normalizers: Dict[frozenset, float] = {}

    # Constant term in log likelihood
    constant: float = 0.0

    def __init__(self, constant: float):
        self.constant = constant

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


@dataclass
class Grammar:
    productions: List[Production]

    def __init__(self, productions: List[Production]):
        self.productions = productions
        self.primitive_to_logprob = {p: logprob for logprob, p in productions}

    def __hash__(self):
        return hash(tuple(self.productions))

    @staticmethod
    def uniform(primitives: List[Primitive]) -> "Grammar":
        return Grammar([(0.0, p) for p in primitives])

    def get_candidates(self, request: PrimitiveType) -> List[Production]:
        """Each position in program has a set of valid candidates depending on the position's type."""
        # if the type system was more complex, we would need to perform type unification here
        candidates = [p for p in self.productions if p[1].type == request]
        # normalize log probabilities
        z = lse([logProb for logProb, p in candidates])
        return [(logProb - z, p) for logProb, p in candidates]

    def inside_outside(self) -> Production:
        pass

    def likelihood_summary(self, request: PrimitiveType):
        candidates = self.get_candidates(request)
        possibles = set([p[1].type for p in candidates])

    def fill_holes(
        self,
        request: PrimitiveType,
        max_depth: int = 99,
        lower_bound: float = 0,
        upper_bound: float = 100,
        debug: bool = False,
    ):
        if upper_bound < 0 or max_depth == 1:
            return
        candidates = self.get_candidates(request)
        if debug:
            print(f"Candidates for filling hole of type {request}:")
            print("-" * 25)
            for logProb, p in candidates:
                print(f"{logProb} {p}")
        valid_candidates = []
        for logProb, p in candidates:
            mdl = -logProb
            if mdl > upper_bound:
                continue
            valid_candidates.append((mdl, p))
        return valid_candidates
