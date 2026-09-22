"""Staged managed-pet learning gates; no NPC spell-record changes."""
BEFORE='if(!info||info->SpellLevel>level)continue;'
AFTER='if(!info||info->SpellLevel>level||(id==880743&&level<30)||(id==50335&&level<40))continue;'
def patch(source):
 if source.count(BEFORE)!=1 or AFTER in source:raise ValueError('Unreviewed or already patched ProfileSkills source')
 return source.replace(BEFORE,AFTER)
