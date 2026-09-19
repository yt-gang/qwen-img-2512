from __future__ import annotations

import io

import pytest
import requests
from PIL import Image

from catline_worker import ContractError, upload_generated_image, validate_output_target


def output_target():
    return {
        "upload_url": "https://r2.example.test/signed?secret=redacted",
        "object_key": "projects/p/scenes/s/images/v1.webp",
        "content_type": "image/webp",
        "required_headers": {"Content-Type": "image/webp"},
    }


def test_uploads_exact_lossless_webp_contract():
    source = io.BytesIO()
    Image.new("RGB", (32, 32), "red").save(source, "PNG")
    captured = {}

    class Response:
        def raise_for_status(self):
            return None

    def put(url, *, data, headers, timeout):
        captured.update(url=url, data=data, headers=headers, timeout=timeout)
        return Response()

    asset = upload_generated_image(source.getvalue(), output_target(), request_put=put)
    with Image.open(io.BytesIO(captured["data"])) as result:
        assert result.format == "WEBP"
        assert result.size == (1080, 1920)
    assert asset["object_key"].endswith("v1.webp")
    assert asset["content_type"] == "image/webp"
    assert asset["size_bytes"] == len(captured["data"])


def test_output_target_rejects_wrong_key_or_transport():
    bad = output_target()
    bad["upload_url"] = "http://r2.example.test/object"
    with pytest.raises(ContractError):
        validate_output_target(bad)


def test_upload_error_does_not_expose_signed_url():
    source = io.BytesIO()
    Image.new("RGB", (2, 2), "red").save(source, "PNG")

    def fail(*args, **kwargs):
        raise requests.ConnectionError("https://r2.example.test/out?secret=do-not-log")

    with pytest.raises(RuntimeError, match="R2 output upload failed") as raised:
        upload_generated_image(source.getvalue(), output_target(), request_put=fail)
    assert "do-not-log" not in str(raised.value)
