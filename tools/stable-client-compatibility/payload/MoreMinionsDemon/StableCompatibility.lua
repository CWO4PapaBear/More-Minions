-- Scope compatibility to the native stable UI. Never replace global pet APIs.
local captures={899,896,93558,93569} -- Undead, Dragonkin, Elemental, Demon
local installed={}
local function access()
 for _,id in ipairs(captures)do if IsSpellKnown and IsSpellKnown(id)then return true end end
 return false
end
local function current()
 if not access()or not UnitExists('pet')then return false end
 local _,name=GetStablePetInfo(0)
 return name and name~=''and name==UnitName('pet')
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
