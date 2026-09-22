FILES={'src/server/game/Entities/Pet/Pet.cpp': [('float Pet::GetNativeObjectScale() const\n{\n', 'float Pet::GetNativeObjectScale() const\n{\n    // Captured custom minions retain database creature sizing, not Hunter family growth.\n    if (getPetType() == HUNTER_PET && MoreMinionsTagged(GetUInt32Value(UNIT_CREATED_BY_SPELL)))\n        return Guardian::GetNativeObjectScale();\n\n')]}

def patch(source,changes):
 for before,after in changes:
  if after in source or source.count(before)!=1:raise ValueError("Unreviewed or already patched pet sizing source")
  source=source.replace(before,after)
 return source
