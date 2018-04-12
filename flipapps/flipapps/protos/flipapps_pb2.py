# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flipapps/protos/flipapps.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='flipapps/protos/flipapps.proto',
  package='flipapps',
  syntax='proto3',
  serialized_pb=_b('\n\x1e\x66lipapps/protos/flipapps.proto\x12\x08\x66lipapps\x1a\x1bgoogle/protobuf/empty.proto\")\n\x0bTextRequest\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x0c\n\x04\x66ont\x18\x02 \x01(\t\"5\n\x0eWeatherRequest\x12\x10\n\x08latitude\x18\x01 \x01(\x02\x12\x11\n\tlongitude\x18\x02 \x01(\x02\"\x0e\n\x0c\x43lockRequest\"\x11\n\x0f\x46lipAppResponse\"!\n\x0f\x44isplayResponse\x12\x0e\n\x06pixels\x18\x01 \x03(\x08\x32\x89\x02\n\x08\x46lipApps\x12:\n\x04Text\x12\x15.flipapps.TextRequest\x1a\x19.flipapps.FlipAppResponse\"\x00\x12@\n\x07Weather\x12\x18.flipapps.WeatherRequest\x1a\x19.flipapps.FlipAppResponse\"\x00\x12<\n\x05\x43lock\x12\x16.flipapps.ClockRequest\x1a\x19.flipapps.FlipAppResponse\"\x00\x12\x41\n\nGetDisplay\x12\x16.google.protobuf.Empty\x1a\x19.flipapps.DisplayResponse\"\x00\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_TEXTREQUEST = _descriptor.Descriptor(
  name='TextRequest',
  full_name='flipapps.TextRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='flipapps.TextRequest.text', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='font', full_name='flipapps.TextRequest.font', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=73,
  serialized_end=114,
)


_WEATHERREQUEST = _descriptor.Descriptor(
  name='WeatherRequest',
  full_name='flipapps.WeatherRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='latitude', full_name='flipapps.WeatherRequest.latitude', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='longitude', full_name='flipapps.WeatherRequest.longitude', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=116,
  serialized_end=169,
)


_CLOCKREQUEST = _descriptor.Descriptor(
  name='ClockRequest',
  full_name='flipapps.ClockRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=171,
  serialized_end=185,
)


_FLIPAPPRESPONSE = _descriptor.Descriptor(
  name='FlipAppResponse',
  full_name='flipapps.FlipAppResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=187,
  serialized_end=204,
)


_DISPLAYRESPONSE = _descriptor.Descriptor(
  name='DisplayResponse',
  full_name='flipapps.DisplayResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pixels', full_name='flipapps.DisplayResponse.pixels', index=0,
      number=1, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=206,
  serialized_end=239,
)

DESCRIPTOR.message_types_by_name['TextRequest'] = _TEXTREQUEST
DESCRIPTOR.message_types_by_name['WeatherRequest'] = _WEATHERREQUEST
DESCRIPTOR.message_types_by_name['ClockRequest'] = _CLOCKREQUEST
DESCRIPTOR.message_types_by_name['FlipAppResponse'] = _FLIPAPPRESPONSE
DESCRIPTOR.message_types_by_name['DisplayResponse'] = _DISPLAYRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TextRequest = _reflection.GeneratedProtocolMessageType('TextRequest', (_message.Message,), dict(
  DESCRIPTOR = _TEXTREQUEST,
  __module__ = 'flipapps.protos.flipapps_pb2'
  # @@protoc_insertion_point(class_scope:flipapps.TextRequest)
  ))
_sym_db.RegisterMessage(TextRequest)

WeatherRequest = _reflection.GeneratedProtocolMessageType('WeatherRequest', (_message.Message,), dict(
  DESCRIPTOR = _WEATHERREQUEST,
  __module__ = 'flipapps.protos.flipapps_pb2'
  # @@protoc_insertion_point(class_scope:flipapps.WeatherRequest)
  ))
_sym_db.RegisterMessage(WeatherRequest)

ClockRequest = _reflection.GeneratedProtocolMessageType('ClockRequest', (_message.Message,), dict(
  DESCRIPTOR = _CLOCKREQUEST,
  __module__ = 'flipapps.protos.flipapps_pb2'
  # @@protoc_insertion_point(class_scope:flipapps.ClockRequest)
  ))
_sym_db.RegisterMessage(ClockRequest)

FlipAppResponse = _reflection.GeneratedProtocolMessageType('FlipAppResponse', (_message.Message,), dict(
  DESCRIPTOR = _FLIPAPPRESPONSE,
  __module__ = 'flipapps.protos.flipapps_pb2'
  # @@protoc_insertion_point(class_scope:flipapps.FlipAppResponse)
  ))
_sym_db.RegisterMessage(FlipAppResponse)

DisplayResponse = _reflection.GeneratedProtocolMessageType('DisplayResponse', (_message.Message,), dict(
  DESCRIPTOR = _DISPLAYRESPONSE,
  __module__ = 'flipapps.protos.flipapps_pb2'
  # @@protoc_insertion_point(class_scope:flipapps.DisplayResponse)
  ))
_sym_db.RegisterMessage(DisplayResponse)



_FLIPAPPS = _descriptor.ServiceDescriptor(
  name='FlipApps',
  full_name='flipapps.FlipApps',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=242,
  serialized_end=507,
  methods=[
  _descriptor.MethodDescriptor(
    name='Text',
    full_name='flipapps.FlipApps.Text',
    index=0,
    containing_service=None,
    input_type=_TEXTREQUEST,
    output_type=_FLIPAPPRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Weather',
    full_name='flipapps.FlipApps.Weather',
    index=1,
    containing_service=None,
    input_type=_WEATHERREQUEST,
    output_type=_FLIPAPPRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Clock',
    full_name='flipapps.FlipApps.Clock',
    index=2,
    containing_service=None,
    input_type=_CLOCKREQUEST,
    output_type=_FLIPAPPRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetDisplay',
    full_name='flipapps.FlipApps.GetDisplay',
    index=3,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_DISPLAYRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_FLIPAPPS)

DESCRIPTOR.services_by_name['FlipApps'] = _FLIPAPPS

# @@protoc_insertion_point(module_scope)
