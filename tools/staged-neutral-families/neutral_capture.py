FILES={'modules/mod-more-minions/src/MoreMinions.cpp': [('&&p->IsHostileTo(c)&&p->IsValidAttackTarget(c)', '&&!p->IsFriendlyTo(c)&&p->IsValidAttackTarget(c)'), ('fail(!p->IsHostileTo(c),"target is not hostile to you");', 'fail(p->IsFriendlyTo(c),"target is friendly to you");')]}

def patch(source, changes):
 for before, after in changes:
  if source.count(before) != 1: raise ValueError("Live source differs from reviewed capture rules")
  source = source.replace(before, after)
 return source
