// Contract tests use narrow stand-ins; the full PTR build remains required.
#include <array>
#include <cassert>
#include <cstdint>
#include <optional>
#include <string>
#include <vector>
using uint64=uint64_t;using uint32=uint32_t;
template<class T>using Optional=std::optional<T>;
constexpr unsigned MAX_PET_STABLES=4,HUNTER_PET=1,UNIT_NPC_FLAG_STABLEMASTER=1;
constexpr unsigned CMSG_STABLE_PET=1,CMSG_UNSTABLE_PET=2,CMSG_BUY_STABLE_SLOT=3;
struct ObjectGuid{uint64 value;explicit ObjectGuid(uint64 v):value(v){}};
struct WorldPacket{unsigned opcode;uint64 guid=0;uint32 pet=0;WorldPacket(unsigned o,unsigned):opcode(o){};WorldPacket& operator<<(ObjectGuid g){guid=g.value;return *this;}WorldPacket& operator<<(uint32 p){pet=p;return *this;}};
struct PetStable{
 struct PetInfo{unsigned Type=HUNTER_PET,PetNumber=26,CreatureId=16247,Level=75,CreatedBySpellId=885;std::string Name="Abomination";};
 unsigned MaxStabledPets=1;Optional<PetInfo>CurrentPet;std::array<Optional<PetInfo>,4>StabledPets;Optional<PetInfo>unslotted;
 PetInfo const* GetUnslottedHunterPet()const{return unslotted?&*unslotted:nullptr;}
};
struct Player{
 PetStable stable;bool access=true,alive=true,combat=false,mounted=false,flight=false,near=true;int saves=0;
 PetStable* GetPetStable(){return &stable;}bool IsAlive(){return alive;}bool IsInCombat(){return combat;}bool IsMounted(){return mounted;}bool IsInFlight(){return flight;}
 bool GetNPCIfCanInteractWith(ObjectGuid g,unsigned){return near&&g.value==0xF130000001000001;}void SaveToDB(){++saves;}
};
bool MoreMinionsHasAccess(Player* p){return p->access;}
struct CreatureTemplate{unsigned type=6;};
struct ObjectMgr{CreatureTemplate creature;CreatureTemplate* GetCreatureTemplate(unsigned){return &creature;}}objects;
auto sObjectMgr=&objects;
struct Price{unsigned Price=5000;};
struct Prices{bool available=true;struct Price price;struct Price* LookupEntry(unsigned){return available?&price:nullptr;}}sStableSlotPricesStore;
struct WorldSession{
 Player player;unsigned called=0,pet=0;Player* GetPlayer(){return &player;}
 void HandleStablePet(WorldPacket& p){called=p.opcode;assert(p.guid==0xF130000001000001);}
 void HandleUnstablePet(WorldPacket& p){called=p.opcode;pet=p.pet;}
 void HandleBuyStableSlot(WorldPacket& p){called=p.opcode;}
};
struct ChatHandler{WorldSession session;std::vector<std::string>messages;WorldSession* GetSession(){return &session;}void SendSysMessage(std::string s){messages.push_back(s);}};
constexpr unsigned SEC_PLAYER=0;
namespace Acore::ChatCommands {
enum class Console{No};
struct Command{template<class F>Command(char const*,F,unsigned,Console){}};using ChatCommandTable=std::vector<Command>;
}
struct CommandScript{explicit CommandScript(char const*){}virtual Acore::ChatCommands::ChatCommandTable GetCommands()const=0;};
#include "StableBridge.h"
int main(){
 using MoreMinionsStable::Commands;
 ChatHandler h;auto& p=h.session.player;auto& s=p.stable;
 s.CurrentPet=PetStable::PetInfo{};s.StabledPets[0]=PetStable::PetInfo{};s.StabledPets[0]->PetNumber=27;
 auto request=[&](std::string action,Optional<uint32> number={}){h.session.called=0;h.messages.clear();Commands::Control(&h,action,"0xF130000001000001",7,number);};
 request("status");assert(h.session.called==0&&h.messages.size()==4&&h.messages.front()=="MM_STABLE BEGIN 7 1 5000");
 assert(h.messages[1].find(" 26 16247 75 6 41626f6d696e6174696f6e")!=std::string::npos);
 request("store",26);assert(h.session.called==CMSG_STABLE_PET&&p.saves==1);
 request("retrieve",27);assert(h.session.called==CMSG_UNSTABLE_PET&&h.session.pet==27);
 request("buy");assert(h.session.called==CMSG_BUY_STABLE_SLOT);
 request("store",999);assert(h.session.called==0&&h.messages.back().find("STALE_PET")!=std::string::npos);
 request("retrieve",26);assert(h.session.called==0);
 s.CurrentPet->Type=0;request("store",26);assert(h.session.called==0);request("status");assert(h.messages.size()==3);s.CurrentPet->Type=HUNTER_PET;
 for(bool* flag:{&p.combat,&p.mounted,&p.flight}){*flag=true;request("buy");assert(h.session.called==0);*flag=false;}
 for(bool* flag:{&p.access,&p.alive,&p.near}){*flag=false;request("store",26);assert(h.session.called==0);*flag=true;}
 s.MaxStabledPets=4;request("buy");assert(h.session.called==0);s.MaxStabledPets=1;
 sStableSlotPricesStore.available=false;request("buy");assert(h.session.called==0);
 uint64 guid=0;assert(!MoreMinionsStable::Guid("123",guid)&&!MoreMinionsStable::Guid("0x0000000000000000",guid)&&!MoreMinionsStable::Guid("0xF13000000100000z",guid));
 assert(MoreMinionsStable::Hex("\xc3\xa9")=="c3a9");
}
