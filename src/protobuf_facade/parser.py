import logging
from typing import TypeVar, ClassVar, Generic, Optional
from google.protobuf.json_format import ParseDict, MessageToDict
from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message import DecodeError, Message

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Message)


class ProtobufParser(Generic[T]):
    """
    A generic parser for Protocol Buffer (Protobuf) messages, using a class-level
    `message_type`. This class is intended to be subclassed, with the subclass
    specifying which Protobuf message type should be used.

    Subclasses should define:
        message_type: ClassVar[Type[T]]
    where `T` is a concrete subclass of `google.protobuf.message.Message`.

    Once defined, the subclass's parser methods will automatically parse/serialize
    messages of that type from/to bytes and Python dictionaries.
    """

    # Must be overridden in subclasses, e.g.:
    #     class MyMessageParser(ProtobufParser[MyMessage]):
    #         message_type = MyMessage
    message_type: ClassVar[type[T]]

    def parse_bytes_to_protobuf(self, data: bytes) -> T:
        """
        Deserialize raw bytes into an instance of the subclass's `message_type`.

        Args:
            data (bytes): Serialized Protobuf bytes.

        Returns:
            T: A Protobuf message instance of type `message_type`.
        """
        logger.debug("Parsing bytes into Protobuf message.")
        payload = self.message_type()
        try:
            payload.ParseFromString(data)
            logger.debug("Successfully parsed bytes into Protobuf message.")
        except DecodeError as e:
            logger.error(f"Error decoding Protobuf message: {e}", exc_info=True)
        return payload

    def parse_protobuf_to_bytes(self, protobuf: Message) -> bytes | None:
        """
        Serialize a Protobuf message instance to raw bytes.

        Args:
            protobuf (Message): A Protobuf message instance to serialize.

        Returns:
            bytes: The serialized bytes, or None if an error occurs.
        """
        logger.debug("Serializing Protobuf message to bytes.")
        if not isinstance(protobuf, self.message_type):
            logger.error(
                f"Invalid message type: {type(protobuf)} (expected {self.message_type})"
            )
            return
        try:
            return protobuf.SerializeToString()
        except Exception as e:
            logger.error(f"Error serializing Protobuf message: {e}", exc_info=True)
            return None

    def parse_dict_to_protobuf(
        self,
        data: dict,
        ignore_unknown_fields: bool = False,
        descriptor_pool: Optional[DescriptorPool] = None,
    ) -> T:
        """
        Convert a Python dictionary to an instance of the subclass's `message_type`,
        using the official Protobuf JSON-to-message conversion.

        Args:
            data (dict): A dictionary representing fields for the Protobuf message.
            ignore_unknown_fields (bool): If True, ignore any fields not recognized
                by the `message_type`. Defaults to False.
            descriptor_pool (DescriptorPool, optional): A descriptor pool used
                to resolve field information during parsing. Defaults to None.

        Returns:
            T: A Protobuf message instance of type `message_type`.
        """
        logger.debug("Converting dict to Protobuf message.")
        payload = self.message_type()
        try:
            ParseDict(
                js_dict=data,
                message=payload,
                ignore_unknown_fields=ignore_unknown_fields,
                descriptor_pool=descriptor_pool,
            )
            logger.debug("Dictionary successfully converted to Protobuf message.")
        except Exception as e:
            logger.error(f"Error parsing dict into Protobuf: {e}", exc_info=True)
        return payload

    def parse_dict_to_bytes(
        self,
        data: dict,
        ignore_unknown_fields: bool = False,
        descriptor_pool: Optional[DescriptorPool] = None,
    ) -> bytes:
        """
        Convert a Python dictionary to an instance of the subclass's `message_type`,
        then serialize it to bytes.

        Args:
            data (dict): A dictionary representing fields for the Protobuf message.
            ignore_unknown_fields (bool): If True, ignore fields not recognized
                by the `message_type`. Defaults to False.
            descriptor_pool (DescriptorPool, optional): A descriptor pool used
                to resolve field information. Defaults to None.

        Returns:
            bytes: The serialized Protobuf message as raw bytes.
        """
        logger.debug("Converting dict to bytes via Protobuf message.")
        protobuf_msg = self.parse_dict_to_protobuf(
            data,
            ignore_unknown_fields=ignore_unknown_fields,
            descriptor_pool=descriptor_pool,
        )
        return self.parse_protobuf_to_bytes(protobuf_msg)

    def parse_bytes_to_dict(
        self,
        data: bytes,
        always_print_fields_with_no_presence: bool = False,
        preserving_proto_field_name: bool = True,
        use_integers_for_enums: bool = False,
        descriptor_pool: Optional[DescriptorPool] = None,
        float_precision: Optional[float] = None,
    ) -> dict | None:
        """
        Deserialize raw bytes into an instance of the subclass's `message_type`,
        then convert it into a Python dictionary.

        Args:
            data (bytes): Serialized Protobuf bytes.
            always_print_fields_with_no_presence (bool): If True, include fields
                in the output even if they have no presence. Defaults to False.
            preserving_proto_field_name (bool): If True, keep the original field
                names defined in the .proto file. Defaults to True.
            use_integers_for_enums (bool): If True, enum fields are returned as
                integers instead of strings. Defaults to False.
            descriptor_pool (DescriptorPool, optional): A descriptor pool used
                for resolving field information. Defaults to None.
            float_precision (Optional[float]): If set, the output for floating point
                fields is rounded to this precision. Defaults to None.

        Returns:
            dict: A dictionary representation of the Protobuf message, or None
                  if an error occurs.
        """
        logger.debug("Converting bytes to dict via Protobuf message.")
        payload = self.parse_bytes_to_protobuf(data)
        try:
            return MessageToDict(
                message=payload,
                always_print_fields_with_no_presence=always_print_fields_with_no_presence,
                preserving_proto_field_name=preserving_proto_field_name,
                use_integers_for_enums=use_integers_for_enums,
                descriptor_pool=descriptor_pool,
                float_precision=float_precision,
            )
        except Exception as e:
            logger.error(
                f"Error converting Protobuf message to dict: {e}", exc_info=True
            )
            return None

    def parse_protobuf_to_dict(self, protobuf: Message) -> dict | None:
        """
        Convert a Protobuf message instance to a Python dictionary.

        Args:
            protobuf (Message): A Protobuf message instance to convert.

        Returns:
            dict: A dictionary representation of the Protobuf message, or None
                  if an error occurs.
        """
        logger.debug("Converting Protobuf message to dict.")
        try:
            return MessageToDict(protobuf)
        except Exception as e:
            logger.error(
                f"Error converting Protobuf message to dict: {e}", exc_info=True
            )
            return None
