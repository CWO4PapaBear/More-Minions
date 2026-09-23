"""Lua 5.1 bridge transport, selection, Beast-only happiness and cleanup tests."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path('work/regalia/libs').resolve()))
from lupa.lua51 import LuaRuntime
lua=LuaRuntime()
lua.execute(r'''
frames={};known=899;now=0;atStable=true;messages={};kind='Undead'
function widget(name)
 local w={name=name,scripts={},shown=true}
 return setmetatable(w,{__index=function(t,k)
  if k=='CreateFontString'or k=='CreateTexture'then return function()return widget()end end
  if k=='SetScript'or k=='HookScript'then return function(_,event,fn)t.scripts[event]=fn end end
  if k=='RegisterEvent'then return function(_,event)t[event]=true end end
  if k=='SetText'then return function(_,v)t.text=v end end
  if k=='GetFrameLevel'then return function()return 1 end end
  if k=='Show'then return function()t.shown=true end end
  if k=='Hide'then return function()t.shown=false end end
  if k=='IsShown'then return function()return t.shown end end
  if k=='Enable'then return function()t.enabled=true end end
  if k=='Disable'then return function()t.enabled=false end end
  return function()end
 end})
end
function CreateFrame(_,name,parent)local w=widget(name);frames[#frames+1]=w;return w end
function IsSpellKnown(id)return id==known end
function IsAtStableMaster()return atStable end
function UnitGUID(unit)return unit=='pet'and '0xF14000001A000006'or '0xF130000001000001'end
function InCombatLockdown()return false end
function UnitExists()return true end
function UnitName()return 'Abomination'end
function UnitCreatureType()return kind end
function GetPetHappiness()return 3 end
PET_HAPPINESS3='Happy'
function SetPortraitTexture()end
function GetTime()return now end
function GetMoney()return 100000 end
function GetCoinTextureString(n)return tostring(n)end
function SendChatMessage(m)messages[#messages+1]=m end
function ChatFrame_AddMessageEventFilter(_,fn)filter=fn end
DEFAULT_CHAT_FRAME=widget();GameTooltip=widget()
for _,name in ipairs({'PetStableFrame','PetStableCurrentPet','PetStableStabledPet1','PetStableStabledPet2','PetStableStabledPet3','PetStableStabledPet4','PetStablePurchaseButton','PetStableCostLabel','PetStableCostMoneyFrame','PetStableSlotText','PetStablePetInfo','PetStableLevelText','PetStableModel'})do _G[name]=widget(name)end
''')
lua.execute((Path(__file__).parent/'payload/MoreMinionsDemon/StableBridge.lua').read_text())
lua.execute(r'''
local events=frames[#frames]
local panel=frames[1]
local function event(e,m)events.scripts.OnEvent(events,e,m)end
local function receive(s)event('CHAT_MSG_SYSTEM',s)end
local function snapshot(id,slot,creatureKind)
 receive('MM_STABLE BEGIN '..id..' 1 5000')
 receive('MM_STABLE PET '..id..' '..slot..' 26 16247 75 '..creatureKind..' 41626f6d696e6174696f6e')
 receive('MM_STABLE END '..id)
end
event('PET_STABLE_SHOW');assert(#messages==1 and messages[1]:match('status'))
snapshot(99,0,6);assert(not panel.shown) -- stale response ignored
receive('MM_STABLE BEGIN 1 1 5000');assert(not panel.shown) -- incomplete not displayed
snapshot(1,0,6);assert(panel.shown and not PetStablePetInfo.shown)
assert(frames[2].enabled and not frames[3].enabled and frames[4].enabled)
frames[2].scripts.OnClick();assert(messages[2]:match('store .* 2 26$'))
frames[2].scripts.OnClick();assert(#messages==2) -- double-click suppressed
snapshot(2,1,6);assert(not frames[2].enabled)
frames[6].scripts.OnClick();assert(frames[3].enabled) -- stored slot selected
frames[3].scripts.OnClick();assert(messages[3]:match('retrieve .* 3 26$'))
snapshot(3,0,6)
frames[5].scripts.OnClick();assert(not PetStablePetInfo.shown)
frames[4].scripts.OnClick();snapshot(4,0,1);assert(PetStablePetInfo.shown and PetStablePetInfo.tooltip=='Happy')
event('PET_STABLE_CLOSED');assert(not panel.shown and PetStableCurrentPet.shown)
snapshot(4,0,6);assert(not panel.shown) -- late response cannot reopen
known=0;event('PET_STABLE_SHOW');assert(#messages==4 and PetStableCurrentPet.shown) -- stock path unchanged
for _,id in ipairs({899,896,93558,93569})do
 known=id;event('PET_STABLE_SHOW');assert(messages[#messages]:match('status'))
 event('PET_STABLE_CLOSED')
end
known=899;event('PET_STABLE_SHOW');now=9;events.scripts.OnUpdate();assert(not panel.shown)
assert(filter(nil,nil,'MM_STABLE BEGIN 1 1 5000') and not filter(nil,nil,'ordinary chat'))
''')
print('PASS: Lua 5.1 stable bridge lifecycle, all capture types, native cleanup, stale/partial responses, actions, timeout and Beast-only happiness.')
