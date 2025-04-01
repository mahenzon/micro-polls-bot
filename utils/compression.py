import base64


def compress_string(text: str) -> str:
    """
    TODO: compress using zlib
    base64 encode
    """
    encoded_data = base64.urlsafe_b64encode(text.encode())
    return encoded_data.decode()


def decode_and_decompress(encoded_data: str) -> str:
    """
    Decode the Base64 data
    TODO: Decompress the data using zlib
    """
    string_data = base64.urlsafe_b64decode(encoded_data)

    return string_data.decode()
