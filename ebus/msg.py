import collections

Msg = collections.namedtuple('Msg', 'circuit msgdef fields')
Field = collections.namedtuple('Field', 'fielddef value')
Error = collections.namedtuple('Error', 'msg')
