from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).parent
compiler = shutil.which('g++') or shutil.which('clang++')
if not compiler:
    raise SystemExit('C++17 compiler required')
with tempfile.TemporaryDirectory(prefix='more-minions-area52-') as name:
    work = Path(name)
    (work / 'Config.h').write_text('''#pragma once
#include <string>
#include <type_traits>
struct ConfigMgr {
 bool enabled=false, coa=false;
 std::string model="coa", realm="live";
 template<class T> T GetOption(char const* key,T fallback) const {
  std::string k=key;
  if constexpr(std::is_same_v<T,bool>){
   if(k=="MoreMinions.Area52.Enable")return enabled;
   if(k=="CoA.Enable")return coa;
  }else{
   if(k=="CoA.ClassModel")return model;
   if(k=="CoA.RealmType")return realm;
  }
  return fallback;
 }
};
extern ConfigMgr* sConfigMgr;
''')
    (work / 'Player.h').write_text('''#pragma once
#include <set>
struct Player {
 unsigned char cls;std::set<unsigned> spells;
 unsigned char getClass()const{return cls;}
 bool HasSpell(unsigned id)const{return spells.count(id)!=0;}
};
''')
    executable = work / 'authorization-test'
    subprocess.run([compiler, '-std=c++17', '-Wall', '-Wextra', '-Werror', '-I', str(work),
                    '-I', str(root), str(root / 'Test-Authorization.cpp'), '-o', str(executable)], check=True)
    subprocess.run([str(executable)], check=True)
