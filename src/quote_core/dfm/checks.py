from __future__ import annotations

import logging

from quote_core.domain.models import DFMResult

logger = logging.getLogger(__name__)


def run_dfm_checks() -> DFMResult:
    logger.info("Running DFM checks")
    return DFMResult()
