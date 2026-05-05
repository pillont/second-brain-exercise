import logging
import time
from typing import Callable
from uuid import uuid4

from flask import Flask, Response, g, request

logger = logging.getLogger(__name__)


def _compute_duration_ms(start_time: float) -> float:
    return (time.monotonic() - start_time) * 1000


def _select_log_fn(duration_ms: float, slow_threshold_ms: int) -> Callable[..., None]:
    return logger.warning if duration_ms > slow_threshold_ms else logger.info


def _annotate_response(
    response: Response, start_time: float, slow_threshold_ms: int
) -> Response:
    request_id = g.get("request_id", "-")
    _log_duration(response, start_time, slow_threshold_ms, request_id)

    response.headers["X-Request-ID"] = request_id
    return response


def _log_duration(
    response: Response, start_time: float, slow_threshold_ms: int, request_id: str
) -> None:
    duration_ms = _compute_duration_ms(start_time)
    log_fn = _select_log_fn(duration_ms, slow_threshold_ms)

    log_fn(
        "%s %s → %d (%.1f ms) request_id=%s",
        request.method,
        request.path,
        response.status_code,
        duration_ms,
        request_id,
    )


def register_request_logger(app: Flask, slow_threshold_ms: int) -> None:
    @app.before_request
    def log_request() -> None:
        g.request_id = str(uuid4())
        g.request_start_time = time.monotonic()
        logger.info("%s %s request_id=%s", request.method, request.path, g.request_id)

    @app.after_request
    def log_response(response: Response) -> Response:
        return _annotate_response(response, g.request_start_time, slow_threshold_ms)
