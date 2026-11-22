import importlib.util
import os
import tempfile
import unittest
from unittest.mock import Mock, patch
from io import StringIO
from contextlib import redirect_stdout


ROOT = os.path.dirname(__file__)
SPEC = importlib.util.spec_from_file_location(
    "whatsapp_osint",
    os.path.join(ROOT, "whatsapp-osint.py"),
)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class WhatsAppOsintTests(unittest.TestCase):
    def test_sanitizes_and_validates_requested_number(self):
        phone = module.sanitize_phone("12345678901")
        self.assertEqual(phone, "12345678901")
        self.assertTrue(module.is_valid_phone(phone))

    def test_rejects_short_or_non_numeric_number(self):
        self.assertFalse(module.is_valid_phone("123"))
        self.assertFalse(module.is_valid_phone("1234567890abc"))

    def test_saves_plain_and_data_uri_base64(self):
        encoded = "aGVsbG8="
        with tempfile.TemporaryDirectory() as directory:
            plain_path = os.path.join(directory, "plain.jpg")
            uri_path = os.path.join(directory, "uri.jpg")
            self.assertTrue(module.save_b64(encoded, plain_path))
            self.assertTrue(module.save_b64("data:image/jpeg;base64," + encoded, uri_path))
            with open(plain_path, "rb") as file:
                self.assertEqual(file.read(), b"hello")

    def test_get_request_uses_phone_query(self):
        response = object()
        with patch.object(module.requests, "get", return_value=response) as get:
            result = module.fetch_endpoint("12345678901", "test-key", "/about")
        self.assertIs(result, response)
        get.assert_called_once()
        self.assertEqual(get.call_args.kwargs["params"], {"phone": "12345678901"})

    def test_business_response_dict_is_supported(self):
        response = Mock()
        response.status_code = 200
        response.text = "{}"
        response.json.return_value = {
            "is_business": True,
            "business_name": "Test Business",
            "verification_status": "verified",
            "business_category": "Retail",
        }
        output = StringIO()
        with patch.object(module.requests, "post", return_value=response):
            with redirect_stdout(output):
                module.process_business_verification("12345678901", "test-key")
        text = output.getvalue()
        self.assertIn("Is WhatsApp Business: True", text)
        self.assertIn("Test Business", text)


if __name__ == "__main__":
    unittest.main()
