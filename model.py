import datetime
import weakref
from typing import Optional, Iterable


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


class TrainingData:
    """A set of training and testing data with methods to load and test the samples."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.uploaded: Optional[datetime.datetime] = None
        self.tested: Optional[datetime.datetime] = None
        self.training: list[Sample] = []
        self.testing: list[Sample] = []
        self.tuning: list[Hyperparameter] = []

    def load(
            self,
            raw_data_source: Iterable[dict[str, str]]
    ) -> None:
        """Load and partition the raw data"""
        for n, row in enumerate(raw_data_source):
            # ... filter and extract subsets (See Chapter 6)
            # ... Create self.training and self.testing subsets
            pass

        self.uploaded = datetime.datetime.now(tz=datetime.timezone.utc)

    def test(
            self,
            parameter: Hyperparameter
    ) -> None:
        """Test this Hyperparameter value."""
        parameter.test()
        self.tuning.append(parameter)
        self.tested = datetime.datetime.now(tz=datetime.timezone.utc)

    def classify(
            self,
            parameter: Hyperparameter,
            sample: Sample
    ) -> Sample:
        """Classify a sample using the given Hyperparameter"""
        classification = parameter.classify(sample)
        sample.classify(classification)
        return sample
