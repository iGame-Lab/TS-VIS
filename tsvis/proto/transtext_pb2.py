# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tsvis/proto/transtext.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tsvis.proto import tensor_pb2 as tsvis_dot_proto_dot_tensor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1btsvis/proto/transtext.proto\x12\x05tsvis\x1a\x18tsvis/proto/tensor.proto\"\x83\x01\n\rAttentionItem\x12\x0b\n\x03tag\x18\x01 \x01(\t\x12 \n\x04\x61ttn\x18\x02 \x01(\x0b\x32\x12.tsvis.TensorProto\x12 \n\x04left\x18\x03 \x01(\x0b\x32\x12.tsvis.TensorProto\x12!\n\x05right\x18\x04 \x01(\x0b\x32\x12.tsvis.TensorProtob\x06proto3')



_ATTENTIONITEM = DESCRIPTOR.message_types_by_name['AttentionItem']
AttentionItem = _reflection.GeneratedProtocolMessageType('AttentionItem', (_message.Message,), {
  'DESCRIPTOR' : _ATTENTIONITEM,
  '__module__' : 'tsvis.proto.transtext_pb2'
  # @@protoc_insertion_point(class_scope:tsvis.AttentionItem)
  })
_sym_db.RegisterMessage(AttentionItem)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ATTENTIONITEM._serialized_start=65
  _ATTENTIONITEM._serialized_end=196
# @@protoc_insertion_point(module_scope)
