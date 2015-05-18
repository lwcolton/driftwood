from base64 import b64encode
import logging

from cryptography.hazmat.backends.openssl import backend as openssl_backend
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.serialization import load_ssh_public_key

class EncryptedAdapter(logging.LoggerAdapter):
    """Used to notify a callback about changes in the loglevel of a program."""
    def __init__(self, logger, public_key_file, extra={}, plaintext_attrs=[], plaintext_static_messages=False):
        """
            :param plaintext_attrs list: List of extra attributes not to encrypt
            :param plaintext_stati_messages bool: Do message formatting inside the adapter,
                allowing messages with no format data to be plaintext
        """
        super().__init__(logger, extra)
        self.plaintext_static_messages = plaintext_static_messages
        self.plaintext_attrs = plaintext_attrs
        with open(public_key_file, "rb") as key_file_handle:
            raw_public_key = key_file_handle.read()
        self.public_key = load_ssh_public_key(raw_public_key, openssl_backend)
        self.padding = OAEP(
            mgf=MGF1(algorithm=SHA1()),
            algorithm=SHA1(),
            label=None
        )

    def process(self, plaintext_message, kwargs):
        add_plaintext = kwargs.pop("add_plaintext", [])
        plaintext_attrs = kwargs.pop("plaintext_attrs", self.plaintext_attrs)
        plaintext_attrs = set(plaintext_attrs) | set(add_plaintext)
        force_encrypt = kwargs.pop("force_encrypt", [])
        format_args = kwargs.pop("format_args", [])
        format_keywords = kwargs.pop("format_keywords", {})
        if "message" in force_encrypt:
            message = self.encrypt(plaintext_message)
        elif "message" in plaintext_attrs:
            message = plaintext_message
        elif self.plaintext_static_messages:
            if format_args or format_keywords:
                message = self.encrypt(plaintext_message)
            else:
                message = plaintext_message
        else:
            message = self.encrypt(plaintext_message)

        extra = self.extra.copy()
        extra.update(kwargs.get("extra", {}))
        for attr_key, attr_value in extra.items():
            if attr_key not in plaintext_attrs:
                extra[attr_key] = self.encrypt(attr_value)
        kwargs["extra"] = extra
        return message, kwargs

        
    def encrypt(self, plaintext_data):
        prepared_data = str(plaintext_data).encode("utf-8")
        encrypted_bytes = self.public_key.encrypt(prepared_data, self.padding)
        return b64encode(encrypted_bytes)
         
