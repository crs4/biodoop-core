# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import Array_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='NamedArrayCollection.proto',
  package='core_messages',
  serialized_pb='\n\x1aNamedArrayCollection.proto\x12\rcore_messages\x1a\x0b\x41rray.proto\"G\n\x14NamedArrayCollection\x12\n\n\x02id\x18\x01 \x02(\t\x12#\n\x05\x61rray\x18\x02 \x03(\x0b\x32\x14.core_messages.Array')




_NAMEDARRAYCOLLECTION = descriptor.Descriptor(
  name='NamedArrayCollection',
  full_name='core_messages.NamedArrayCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='core_messages.NamedArrayCollection.id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='array', full_name='core_messages.NamedArrayCollection.array', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=58,
  serialized_end=129,
)

_NAMEDARRAYCOLLECTION.fields_by_name['array'].message_type = Array_pb2._ARRAY
DESCRIPTOR.message_types_by_name['NamedArrayCollection'] = _NAMEDARRAYCOLLECTION

class NamedArrayCollection(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _NAMEDARRAYCOLLECTION
  
  # @@protoc_insertion_point(class_scope:core_messages.NamedArrayCollection)

# @@protoc_insertion_point(module_scope)
