class BackendError(Exception):
    """Base exception for backend failures."""


class ConfigurationError(BackendError):
    """Raised when backend configuration is invalid."""


class ModelLoadError(BackendError):
    """Raised when a model artifact cannot be loaded."""
