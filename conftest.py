"""Root conftest: mock the rips module before any imports."""

import sys
from unittest.mock import MagicMock

# Create a mock rips module so models/__init__.py can import it
mock_rips = MagicMock()
mock_rips.Instance = MagicMock
mock_rips.EclipseCase = MagicMock
mock_rips.View = MagicMock
mock_rips.WellPath = MagicMock
mock_rips.WellPathCollection = MagicMock

sys.modules["rips"] = mock_rips
