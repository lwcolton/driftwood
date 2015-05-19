import base64
import hashlib
import logging

from cryptography.hazmat.backends.openssl import backend as openssl_backend
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.serialization import load_ssh_public_key, load_pem_private_key

class EncryptedAdapter(logging.LoggerAdapter):
    """Used to notify a callback about changes in the loglevel of a program."""
    def __init__(self, logger, public_key=None, public_key_path=None, extra={}, plaintext_attrs=[], plaintext_static_messages=False):
        """
            :param plaintext_attrs list: List of extra attributes not to encrypt
            :param plaintext_stati_messages bool: Do message formatting inside the adapter,
                allowing messages with no format data to be plaintext
        """
        super().__init__(logger, extra)
        self.plaintext_static_messages = plaintext_static_messages
        self.plaintext_attrs = plaintext_attrs
        if public_key is None and public_key_path is None:
            raise ValueError("Must specify either public_key or public_key_path")
        if public_key_path is not None:
            with open(public_key_path, "rb") as key_file_handle:
                public_key = key_file_handle.read()
        self.public_key, self.fingerprint = self.load_key(public_key)

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
        encrypted_fields = []
        if "message" in force_encrypt:
            message = self.encrypt_message(plaintext_message, encrypted_fields)
        elif "message" in plaintext_attrs:
            message = plaintext_message
        elif self.plaintext_static_messages:
            if format_args or format_keywords:
                message = self.encrypt_message(plaintext_message, encrypted_fields)
            else:
                message = plaintext_message
        else:
            message = self.encrypt_message(plaintext_message, encrypted_fields)

        extra = self.extra.copy()
        extra.update(kwargs.get("extra", {}))
        for attr_key, attr_value in extra.items():
            if attr_key not in plaintext_attrs:
                extra[attr_key] = self.encrypt(attr_value)
                encrypted_fields.append(attr_key)

        extra["log_encryption_key"] = self.fingerprint
        extra["encrypted_fields"] = encrypted_fields
        
        kwargs["extra"] = extra
        return message, kwargs

    def load_key(self, key_data):
        public_key = load_ssh_public_key(key_data, openssl_backend)
        key_data_text = key_data.decode("utf-8").split(" ")[1]
        fp_plain = hashlib.md5(base64.b64decode(key_data_text)).hexdigest()
        fingerprint = ':'.join(a+b for a, b in zip(fp_plain[::2], fp_plain[1::2]))
        return public_key, fingerprint

    def encrypt_message(self, plaintext_message, encrypted_fields):
        encrypted_fields.append("message")
        return self.encrypt(plaintext_message)

    def encrypt(self, plaintext_data):
        if type(plaintext_data) != bytes:
            plaintext_data = str(plaintext_data).encode("utf-8")
        encrypted_bytes = self.public_key.encrypt(plaintext_data, self.padding)
        return base64.b64encode(encrypted_bytes).decode("utf-8")

class Decrypter:
    def __init__(self, private_rsa_key, password=None):
        self.private_key = load_pem_private_key(
            private_rsa_key,
            password=password,
            backend=openssl_backend
        )
        self.padding = OAEP(
            mgf=MGF1(algorithm=SHA1()),
            algorithm=SHA1(),
            label=None
        )
    
    def decrypt(self, log_record):
        for field_name in log_record["encrypted_fields"]:
            encrypted_value = base64.b64decode(log_record[field_name])
            decrypted_value = self.private_key.decrypt(encrypted_value, self.padding)
            log_record[field_name] = decrypted_value

