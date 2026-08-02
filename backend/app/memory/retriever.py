"""Memory retrieval interface for locating relevant context."""


class MemoryRetriever:
    """Defines the contract for retrieving contextually relevant memories."""

    def retrieve(self):
        """Retrieve memories relevant to a query or context."""
        raise NotImplementedError()
