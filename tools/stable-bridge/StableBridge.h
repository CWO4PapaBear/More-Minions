#pragma once
#include "ScriptMgr.h"
#include "Chat.h"
#include "ChatCommand.h"
#include "WorldSession.h"
#include "WorldPacket.h"
#include "Opcodes.h"
#include "DBCStores.h"
#include <cctype>

namespace MoreMinionsStable {
inline std::string Hex(std::string const& value){
 static char const* digits="0123456789abcdef";std::string out;
 for(unsigned char c:value){out+=digits[c>>4];out+=digits[c&15];}
 return out.empty()?"-":out;
}
inline bool Guid(std::string const& text,uint64& value){
 if(text.size()!=18||text.substr(0,2)!="0x")return false;
 value=0;
 for(size_t i=2;i<text.size();++i){unsigned char c=text[i];unsigned n;
  if(c>='0'&&c<='9')n=c-'0';else if(c>='a'&&c<='f')n=c-'a'+10;else if(c>='A'&&c<='F')n=c-'A'+10;else return false;
  value=(value<<4)|n;
 }
 return value!=0;
}
inline void State(ChatHandler* h,uint32 request){
 auto p=h->GetSession()->GetPlayer();auto stable=p->GetPetStable();
 unsigned slots=stable?stable->MaxStabledPets:0,cost=0;
 if(slots<MAX_PET_STABLES){auto price=sStableSlotPricesStore.LookupEntry(slots+1);if(price)cost=price->Price;}
 h->SendSysMessage("MM_STABLE BEGIN "+std::to_string(request)+" "+std::to_string(slots)+" "+std::to_string(cost));
 auto row=[&](unsigned slot,PetStable::PetInfo const& pet){
  // Summoned guardians are never included in the primary-pet list.
  if(pet.Type!=HUNTER_PET)return;
  auto creature=sObjectMgr->GetCreatureTemplate(pet.CreatureId);
  h->SendSysMessage("MM_STABLE PET "+std::to_string(request)+" "+std::to_string(slot)+" "+std::to_string(pet.PetNumber)+" "+std::to_string(pet.CreatureId)+" "+std::to_string(pet.Level)+" "+std::to_string(creature?creature->type:0)+" "+Hex(pet.Name));
 };
 if(stable){
  if(stable->CurrentPet)row(0,*stable->CurrentPet);
  else if(auto pet=stable->GetUnslottedHunterPet())row(0,*pet);
  for(unsigned i=0;i<stable->StabledPets.size();++i)if(stable->StabledPets[i])row(i+1,*stable->StabledPets[i]);
 }
 h->SendSysMessage("MM_STABLE END "+std::to_string(request));
}
class Commands final:public CommandScript {
public:Commands():CommandScript("MoreMinionsStableBridge"){}
 static bool Control(ChatHandler* h,std::string action,std::string npc,uint32 request,Optional<uint32> number){
  auto session=h->GetSession();auto p=session->GetPlayer();
  auto error=[&](char const* reason){h->SendSysMessage("MM_STABLE ERROR "+std::to_string(request)+" "+reason);return true;};
  if(!MoreMinionsHasAccess(p))return error("ACCESS");
  uint64 raw=0;if(!Guid(npc,raw))return error("NPC");
  ObjectGuid guid(raw);
  if(!p->IsAlive()||p->IsInCombat()||p->IsMounted()||p->IsInFlight()||!p->GetNPCIfCanInteractWith(guid,UNIT_NPC_FLAG_STABLEMASTER))return error("INTERACTION");
  if(action=="status"){State(h,request);return true;}
  if(action!="buy"&&action!="store"&&action!="retrieve")return error("ACTION");
  auto stable=p->GetPetStable();
  if(action=="store"){
   auto pet=stable?(stable->CurrentPet?&stable->CurrentPet.value():stable->GetUnslottedHunterPet()):nullptr;
   if(!number||!pet||pet->Type!=HUNTER_PET||pet->PetNumber!=*number)return error("STALE_PET");
   WorldPacket packet(CMSG_STABLE_PET,8);packet<<guid;session->HandleStablePet(packet);
  }else if(action=="retrieve"){
   bool owned=false;if(stable&&number)for(auto const& slot:stable->StabledPets)if(slot&&slot->Type==HUNTER_PET&&slot->PetNumber==*number)owned=true;
   if(!owned)return error("STALE_PET");
   WorldPacket packet(CMSG_UNSTABLE_PET,12);packet<<guid<<uint32(*number);session->HandleUnstablePet(packet);
  }else{
   unsigned slots=stable?stable->MaxStabledPets:0;
   if(slots>=MAX_PET_STABLES||!sStableSlotPricesStore.LookupEntry(slots+1))return error("SLOTS");
   WorldPacket packet(CMSG_BUY_STABLE_SLOT,8);packet<<guid;session->HandleBuyStableSlot(packet);
  }
  // Persist purchased slots and money using the normal character save path.
  p->SaveToDB(false,false);State(h,request);return true;
 }
 Acore::ChatCommands::ChatCommandTable GetCommands()const override{return {{"mmstable",Control,SEC_PLAYER,Acore::ChatCommands::Console::No}};}
};
}
