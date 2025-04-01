import base64
import zlib

from storage.poll_data import PollData


def compress_string(text: str) -> str:
    """
    TODO: compress using zlib
    base64 encode
    """
    compressed_data = zlib.compress(text.encode())
    encoded_data = base64.urlsafe_b64encode(compressed_data)
    return encoded_data.decode()


def decode_and_decompress(encoded_data: str) -> str:
    """
    Decode the Base64 data
    TODO: Decompress the data using zlib
    """
    string_data = base64.urlsafe_b64decode(encoded_data)
    serialized_data = zlib.decompress(string_data)

    return serialized_data.decode()


def compress_data(data: PollData) -> str:
    return compress_string(data.model_dump_json())


def decode_data(encoded_data: str) -> PollData:
    return PollData.model_validate_json(
        decode_and_decompress(encoded_data),
    )
