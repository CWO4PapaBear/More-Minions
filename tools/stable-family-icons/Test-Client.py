from pathlib import Path
import sys
sys.path.insert(0,str(Path('work/regalia/libs').resolve()))
from lupa.lua51 import LuaRuntime
lua=LuaRuntime()
lua.execute(r'''
frames={};known=899;now=0;messages={};nativeCalls=0;mouse=nil
function widget(name)
 local w={name=name,scripts={},shown=true}
 return setmetatable(w,{__index=function(t,k)
  if k=='SetScript'or k=='HookScript'then return function(_,event,fn)t.scripts[event]=fn end end
  if k=='GetScript'then return function(_,event)return t.scripts[event]end end
  if k=='GetName'then return function()return name end end
  if k=='SetText'then return function(_,v)t.text=v end end
  if k=='SetChecked'then return function(_,v)t.checked=v end end
  if k=='SetCreature'then return function(_,v)t.creature=v end end
  if k=='Show'then return function()t.shown=true end end
  if k=='Hide'then return function()t.shown=false end end
  if k=='IsShown'then return function()return t.shown end end
  if k=='Enable'then return function()t.enabled=true end end
  if k=='Disable'then return function()t.enabled=false end end
  if k=='SetPoint'or k=='SetSize'or k=='ClearAllPoints'then return function()error('Native layout must remain unchanged')end end
  return function()end
 end})
end
function CreateFrame(_,name,parent)assert(not parent,'No replacement interface');local w=widget(name);frames[#frames+1]=w;return w end
function IsSpellKnown(id)return id==known end
function IsAtStableMaster()return true end
function UnitGUID()return '0xF130000001000001'end
function InCombatLockdown()return false end
function UnitExists()return true end
function GetPetHappiness()return 3 end
PET_HAPPINESS3='Happy';EMPTY_STABLE_SLOT='Empty';LEVEL='Level'
function GetTime()return now end
function GetMoney()return 100000 end
function SetItemButtonTexture(b,icon)b.texture=icon end
function MoneyFrame_Update(_,cost)lastCost=cost end
function SetMoneyFrameColor()end
function SendChatMessage(m)messages[#messages+1]=m end
function ChatFrame_AddMessageEventFilter(_,fn)filter=fn end
function SetCursor(v)cursor=v end
function ResetCursor()cursor=nil end
function MouseIsOver(button)return mouse==button end
DEFAULT_CHAT_FRAME=widget();GameTooltip=widget()
for _,name in ipairs({'PetStableFrame','PetStableCurrentPet','PetStableStabledPet1','PetStableStabledPet2','PetStableStabledPet3','PetStableStabledPet4','PetStablePurchaseButton','PetStableCostLabel','PetStableCostMoneyFrame','PetStableSlotText','PetStablePetInfo','PetStableLevelText','PetStableModel'})do
 _G[name]=widget(name);_G[name..'Background']=widget();_G[name..'IconTexture']=widget()
 for _,script in ipairs({'OnClick','OnDragStart','OnReceiveDrag','OnDragStop'})do _G[name].scripts[script]=function()nativeCalls=nativeCalls+1 end end
end
''')
lua.execute((Path(__file__).parent/'payload/MoreMinionsDemon/StableBridge.lua').read_text())
lua.execute(r'''
assert(#frames==1) -- event listener only; original frames retained
local events=frames[1]
local function event(e,m)events.scripts.OnEvent(events,e,m)end
local function receive(s)event('CHAT_MSG_SYSTEM',s)end
local function act(button,script)button.scripts[script](button)end
local function snapshot(id,slot,kind,slots)
 receive('MM_STABLE BEGIN '..id..' '..(slots or 1)..' 5000')
 receive('MM_STABLE PET '..id..' '..slot..' 26 16247 75 '..kind..' 41626f6d696e6174696f6e')
 receive('MM_STABLE END '..id)
end
act(PetStableCurrentPet,'OnClick');assert(nativeCalls==1)
event('PET_STABLE_SHOW');assert(messages[1]:match('status'))
snapshot(99,0,6);assert(rawget(PetStableCurrentPet,'texture')==nil)
snapshot(1,0,6);assert(not PetStablePetInfo.shown and PetStableCurrentPet.enabled and PetStablePurchaseButton.enabled)
local icon=PetStableCurrentPet.texture
act(PetStableCurrentPet,'OnDragStart');mouse=PetStableStabledPet1
act(PetStableCurrentPet,'OnDragStop');assert(messages[2]:match('store .* 2 26$')and not cursor)
act(PetStablePurchaseButton,'OnClick');assert(#messages==2) -- pending mutation blocks duplicates
snapshot(2,1,6);assert(PetStableStabledPet1.texture==icon and PetStableStabledPet1.checked)
assert(PetStableModel.creature==16247 and PetStableModel.shown)
act(PetStableStabledPet1,'OnDragStart');mouse=PetStableCurrentPet
act(PetStableStabledPet1,'OnDragStop');assert(messages[3]:match('retrieve .* 3 26$'))
snapshot(3,0,6);act(PetStableCurrentPet,'OnClick')
act(PetStableStabledPet1,'OnClick');assert(messages[4]:match('store .* 4 26$'))
snapshot(4,1,6);act(PetStableCurrentPet,'OnClick');assert(messages[5]:match('retrieve .* 5 26$'))
snapshot(5,0,6);act(PetStablePurchaseButton,'OnClick');assert(messages[6]:match('buy .* 6$'))
snapshot(6,0,1,4);assert(not PetStablePurchaseButton.shown and PetStablePetInfo.shown and PetStablePetInfo.tooltip=='Happy')
event('PET_STABLE_CLOSED');snapshot(6,1,6)
known=0;event('PET_STABLE_SHOW');act(PetStablePurchaseButton,'OnClick');assert(nativeCalls==2)
for _,id in ipairs({899,896,93558,93569})do known=id;event('PET_STABLE_SHOW');assert(messages[#messages]:match('status'));event('PET_STABLE_CLOSED')end
known=899;event('PET_STABLE_SHOW');now=9;events.scripts.OnUpdate()
act(PetStableCurrentPet,'OnClick');assert(nativeCalls==3)
assert(filter(nil,nil,'MM_STABLE BEGIN 1 1 5000')and not filter(nil,nil,'normal chat'))
''')
lua.execute(r'''
function GetStablePetInfo()return nil end
function UnitCreatureFamily()return 'Wolf'end
function GetPetIcon()return 'Interface\\Icons\\Ability_Hunter_Pet_Wolf'end
local event=frames[1].scripts.OnEvent
event(frames[1],'PET_STABLE_CLOSED');known=899;event(frames[1],'PET_STABLE_SHOW')
local req=messages[#messages]:match(' (%d+)$')
local function wolf(id,slot)
 event(frames[1],'CHAT_MSG_SYSTEM','MM_STABLE BEGIN '..id..' 1 5000')
 event(frames[1],'CHAT_MSG_SYSTEM','MM_STABLE PET '..id..' '..slot..' 50 30 10 1 576f6c66')
 event(frames[1],'CHAT_MSG_SYSTEM','MM_STABLE END '..id)
end
wolf(req,0);local icon=PetStableCurrentPet.texture
assert(icon:match('FamilyIcons')and not icon:match('QuestionMark'))
PetStableStabledPet1.scripts.OnClick(PetStableStabledPet1)
req=messages[#messages]:match(' (%d+) 50$');wolf(req,1)
assert(PetStableStabledPet1.texture==icon)
''')
print('PASS: classic controls/actions, family icons, Beast current/stored cache, happiness, stale replies and native fallback.')
