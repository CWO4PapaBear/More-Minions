-- Scope compatibility to the native stable UI. Never replace global pet APIs.
local captures={899,896,93558,93569} -- Undead, Dragonkin, Elemental, Demon
local installed={}
local function access()
 for _,id in ipairs(captures)do if IsSpellKnown and IsSpellKnown(id)then return true end end
 return false
end
local function current()
 if not access()or not UnitExists('pet')then return false end
 local guid=UnitGUID('pet')
 -- Permanent primary pet GUID; independent guardians are not this unit.
 return type(guid)=='string'and guid:sub(1,6):upper()=='0XF140'
end
local function install()
 for _,name in ipairs({'PetStable_Update','PetStable_OnEvent'})do
  local fn=_G[name]
  if type(fn)=='function'and not installed[fn]then
   local base=getfenv(fn)
   local env=setmetatable({}, {__index=base,__newindex=base})
   rawset(env,'HasPetUI',function()
    local has,hunter=base.HasPetUI()
    if not hunter and current()then return true,true end
    return has,hunter
   end)
   rawset(env,'GetPetIcon',function()
    return base.GetPetIcon()or(current()and 'Interface\\Icons\\Ability_Hunter_BeastCall')or nil
   end)
   rawset(env,'UnitCreatureFamily',function(unit)
    return base.UnitCreatureFamily(unit)or(unit=='pet'and current()and (base.UnitCreatureType(unit)or 'Companion'))or nil
   end)
   rawset(env,'GetStablePetInfo',function(index)
    local icon,petName,level,family,talent=base.GetStablePetInfo(index)
    if access()and petName and petName~=''then
     return icon or 'Interface\\Icons\\Ability_Hunter_BeastCall',petName,level or 1,family or '',talent or ''
    end
    return icon,petName,level,family,talent
   end)
   setfenv(fn,env);installed[fn]=true
  end
 end
end
local frame=CreateFrame('Frame')
frame:RegisterEvent('PLAYER_LOGIN');frame:RegisterEvent('ADDON_LOADED')
frame:SetScript('OnEvent',install)
install()

-- Read-only live evidence: retain it in the addon's existing per-character settings.
SLASH_MOREMINIONSSTABLE1='/mmstable'
SlashCmdList.MOREMINIONSSTABLE=function()
 local lines={}
 local function values(...)
  local out={};for i=1,select('#',...)do out[#out+1]=tostring(select(i,...))end
  return table.concat(out,' / ')
 end
 local function record(label,fn)
  local ok,result=pcall(fn)
  local text=label..': '..(ok and result or ('ERROR '..tostring(result)))
  lines[#lines+1]=text;DEFAULT_CHAT_FRAME:AddMessage('MM Stable '..text)
 end
 record('v3 known',function()return values(IsSpellKnown and IsSpellKnown(899),IsSpellKnown and IsSpellKnown(896),IsSpellKnown and IsSpellKnown(93558),IsSpellKnown and IsSpellKnown(93569))end)
 record('pet',function()return values(UnitExists('pet'),UnitName('pet'),UnitGUID('pet'),HasPetUI())end)
 record('stable',function()return values(IsAtStableMaster(),GetNumStableSlots(),GetNumStablePets(),GetSelectedStablePet(),GetNextStableSlotCost())end)
 for i=0,4 do record('slot '..i,function()return values(GetStablePetInfo(i))end)end
 record('hooks',function()return values(installed[PetStable_Update],installed[PetStable_OnEvent],current())end)
 record('scoped pet UI',function()return values(getfenv(PetStable_Update).HasPetUI())end)
 MoreMinionsBarSettings=MoreMinionsBarSettings or {}
 MoreMinionsBarSettings.stableDiagnostic={version=3,character=UnitName('player'),lines=lines}
end
