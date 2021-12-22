"""Define view name consts, so we don't type strings everywhere.
This is defined in a file other then views.py to avoid circular imports when
importing from e.g. models.py
"""

from typing import Final

SUMBISSION_VIEW: Final[str] = "submission"
