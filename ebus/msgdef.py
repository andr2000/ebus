import collections

MsgDef = collections.namedtuple("MsgDef", "circuit name read prio write update fields")
FieldDef = collections.namedtuple("FieldDef", "uname name types dividervalues unit")
