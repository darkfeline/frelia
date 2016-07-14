class ComposeTransforms:

    """Compose transformation functions."""

    def __init__(self, transforms=()):
        self.transforms = list(transforms)

    def __call__(self, iterable):
        """Apply all transformation functions to objects."""
        iterable = list(iterable)
        for transform in self.transforms:
            transform(iterable)
