from pathlib import Path
import argparse
import hashlib
import json

here = Path(__file__).parent

def patch(text):
    if 'MoreMinionsArea52::Configure' in text or 'Area52Adapter.h' in text:
        raise ValueError('Area 52 adapter is already present')
    include = '#include "MinionRules.h"'
    startup = ' void OnStartup()override{'
    if text.count(include) != 1 or text.count(startup) != 1:
        raise ValueError('Unrecognized More Minions source layout')
    if 'void MoreMinionsSetAuthorization(bool(*fn)(Player const*,unsigned))' not in text:
        raise ValueError('Required authoritative adapter entry point is absent')
    text = text.replace(include, include + '\n#include "Area52Adapter.h"', 1)
    return text.replace(startup, startup + '\n  MoreMinionsArea52::Configure();', 1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stage the Area 52 authorization adapter without modifying PTR source.')
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.output.resolve() == args.source.parent.resolve():
        parser.error('Output must be a new, separate directory')
    raw = args.source.read_bytes()
    candidate = patch(raw.decode())
    args.output.mkdir(parents=True)
    (args.output / 'MoreMinions.cpp').write_text(candidate)
    for name in ['Area52Adapter.h', 'Area52Authorization.h']:
        (args.output / name).write_bytes((here / name).read_bytes())
    (args.output / 'provenance.json').write_text(json.dumps({
        'source': str(args.source), 'sha256': hashlib.sha256(raw).hexdigest(),
        'status': 'authorization adapter staged only; core hooks, data and full build remain required'
    }, indent=2))
    print('Area 52 adapter staged; supplied source unchanged.')
