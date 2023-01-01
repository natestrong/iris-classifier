import weakref
from typing import Optional


class Sample:
    def __init__(
            self,
            sepal_length: float,
            sepal_width: float,
            petal_length: float,
            petal_width: float,
            species: Optional[str] = None
    ) -> None:
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.species = species
        self.classification: Optional[str] = None

    def classify(self, classification: str) -> None:
        self.classification = classification

    def matches(self) -> bool:
        return self.species == self.classification

    def __repr__(self):
        known_unknown = "KnownSample" if self.species else "UnknownSample"
        classification = f", classification={self.classification!r}" if self.classification else ""
        return (
                f"{known_unknown}(" +
                f"sepal_length={self.sepal_length}, " +
                f"sepal_width={self.sepal_width}, " +
                f"petal_length={self.petal_length}, " +
                f"petal_width={self.petal_width}, " +
                f"species={self.species!r}" +
                f"{classification}" +
                f")"
        )


class Hyperparameter:
    """Holds k-value and the quality of the classification"""

    def __init__(self, k: int, training: "TrainingData") -> None:
        self.k = k
        self.data: weakref.ReferenceType["TrainingData"] = weakref.ref(training)
        self.quality: Optional[float] = None

    def test(self) -> None:
        """Test the quality of the classification"""
        training_data: Optional["TrainingData"] = self.data()
        if not training_data:
            raise ValueError("Broken Weak Reference")

        pass_count, fail_count = 0, 0
        for sample in training_data.testing:
            sample.classification = self.classify(sample)
            if sample.matches():
                pass_count += 1
            else:
                fail_count += 1
            self.quality = pass_count / (pass_count + fail_count)
