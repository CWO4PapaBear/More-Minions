from pathlib import Path
import sys
sys.path.insert(0,str(Path('work/regalia/libs').resolve()))
from lupa.lua51 import LuaRuntime
lua=LuaRuntime()
lua.execute('''
known=899; exists=true; nativeHunter=false; petName='Abomination';listed=true
function IsSpellKnown(id)return id==known end
function UnitExists()return exists end
function UnitName()return petName end
function UnitLevel()return 75 end
function UnitCreatureFamily()return nil end
function GetPetTalentTree()return nil end
function HasPetUI()return true,nativeHunter end
originalHasPetUI=HasPetUI
function GetStablePetInfo(i)if i==0 and listed then return nil,petName,75,nil,nil end end
function GetStablePetFoodTypes()return ''end
function GetPetFoodTypes()return ''end
function GetSelectedStablePet()return 0 end
function GetNumStableSlots()return 0 end
function GetNumStablePets()return 1 end
function GetNextStableSlotCost()return 500 end
function GetMoney()return 10000 end
function IsAtStableMaster()return true end
function GetPetIcon()return nil end
function BuildListString()return ''end
function SetPetStablePaperdoll()end
function ClickStablePet()end
function SetPortraitTexture()end
function MoneyFrame_Update()end
function SetMoneyFrameColor()end
function SetItemButtonTexture(f,t)f.texture=t end
function ShowUIPanel(f)f:Show()end
function HideUIPanel(f)f:Hide()end
function ClosePetStables()end
format=string.format
STABLE_PET_INFO_TEXT='%s %d %s %s';STABLE_PET_INFO_TOOLTIP_TEXT='%d %s %s'
PET_DIET_TEMPLATE='%s';EMPTY_STABLE_SLOT='Empty'
function widget(name)
 local w={shown=true,name=name}
 return setmetatable(w,{__index=function(t,k)
  if k=='Show'then return function()t.shown=true end end
  if k=='Hide'then return function()t.shown=false end end
  if k=='IsShown'then return function()return t.shown end end
  if k=='IsOwned'then return function()return false end end
  if k=='GetName'then return function()return name end end
  return function()end
 end})
end
function CreateFrame()return widget('event')end
setmetatable(_G,{__index=function(t,k)if k:match('^PetStable')or k=='GameTooltip'then local w=widget(k);rawset(t,k,w);return w end end})
''')
reference=Path(sys.argv[1]) if len(sys.argv)>1 else Path('work/area52-review/mpq/ascension-live_Data_enUS_patch-enUS.MPQ/Interface/FrameXML/PetStable.lua')
lua.execute(reference.read_text())
lua.execute('PetStable_Update();assert(not PetStablePurchaseButton.shown)')
lua.execute((Path(__file__).parent/'payload/MoreMinionsDemon/StableCompatibility.lua').read_text())
lua.execute('''
for _,id in ipairs({899,896,93558,93569})do
 known=id;PetStable_Update()
 assert(PetStablePurchaseButton.shown and PetStableModel.shown)
 assert(PetStableCurrentPet.texture and PetStableCurrentPet.texture~='')
 assert(HasPetUI==originalHasPetUI);local _,hunter=HasPetUI();assert(not hunter)
end
known=0;PetStable_Update();assert(not PetStablePurchaseButton.shown)
known=93569;listed=false;PetStable_Update();assert(not PetStablePurchaseButton.shown)
listed=true;known=0;nativeHunter=true;PetStable_Update();assert(PetStablePurchaseButton.shown)
''')
print('PASS: native stable UI reproduces blank state; all four capture groups restore display/purchase; global APIs and ordinary non-Hunter exclusion preserved.')
