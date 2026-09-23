-- Populate the original Wrath stable controls; retain the verified server transport.
local state,pending,staging,npc,selected,dirty,dragged
local serial=0
local buttons={[0]=PetStableCurrentPet}
for i=1,4 do buttons[i]=_G['PetStableStabledPet'..i]end
local icons={[1]='Ability_Hunter_BeastCall',[2]='Spell_Frost_SummonWaterElemental',[3]='INV_Misc_Head_Dragon_01',[4]='Spell_Shadow_SummonFelHunter',[6]='Spell_Shadow_AnimateDead'}
local function eligible()
 for _,id in ipairs({899,896,93558,93569})do if IsSpellKnown(id)then return true end end
end
local function unhex(s)
 if s=='-'then return ''end
 return(s:gsub('%x%x',function(v)return string.char(tonumber(v,16))end))
end
local function icon(pet)
 -- A stable family icon is used in BOTH locations. A live portrait cannot survive
 -- disappearance of its unit and was the cause of the previous icon change.
 return 'Interface\\Icons\\'..(icons[pet.kind]or 'INV_Misc_QuestionMark')
end
local function enable(control,yes)if yes then control:Enable()else control:Disable()end end
local function clearDrag()if dragged then dragged=nil;ResetCursor()end end
local function reset()
 clearDrag();state=nil;pending=nil;staging=nil;npc=nil;selected=nil;dirty=nil
end
local render,request
render=function()
 if not state or not PetStableFrame:IsShown()then return end
 local pet=selected and state.pets[selected]
 if not pet then
  selected=nil
  for i=0,4 do if state.pets[i]then selected=i;pet=state.pets[i];break end end
 end
 for i=0,4 do
  local b=buttons[i];local row=state.pets[i]
  b:Show();enable(b,not pending and(i==0 or i<=state.slots))
  SetItemButtonTexture(b,row and icon(row)or '')
  local texture=_G[b:GetName()..'IconTexture'];if texture then texture:SetTexCoord(0,1,0,1)end
  b:SetChecked(row and selected==i)
  b.tooltip=row and row.name or EMPTY_STABLE_SLOT
  b.tooltipSubtext=row and ((LEVEL or 'Level')..' '..row.level)or ''
  local bg=_G[b:GetName()..'Background']
  if bg then if i==0 or i<=state.slots then bg:SetVertexColor(1,1,1)else bg:SetVertexColor(1,.1,.1)end end
 end
 PetStablePetInfo:Hide();PetStablePetInfo.tooltip=nil
 if pet then
  PetStableLevelText:SetText(pet.name..' - '..(LEVEL or 'Level')..' '..pet.level)
  if selected==0 and UnitExists('pet')then PetStableModel:SetUnit('pet')else PetStableModel:SetCreature(pet.entry)end
  PetStableModel:Show()
  if selected==0 and pet.kind==1 and UnitExists('pet')then
   local happiness=GetPetHappiness();local text=happiness and _G['PET_HAPPINESS'..happiness]
   if text then PetStablePetInfo.tooltip=text;PetStablePetInfo:Show()end
  end
 else PetStableModel:Hide();PetStableLevelText:SetText('')end
 local purchase=state.slots<4 and IsAtStableMaster()
 for _,name in ipairs({'PetStablePurchaseButton','PetStableCostLabel','PetStableCostMoneyFrame','PetStableSlotText'})do
  if purchase then _G[name]:Show()else _G[name]:Hide()end
 end
 MoneyFrame_Update('PetStableCostMoneyFrame',state.cost)
 enable(PetStablePurchaseButton,purchase and not pending and GetMoney()>=state.cost)
 SetMoneyFrameColor('PetStableCostMoneyFrame',GetMoney()>=state.cost and 'white'or 'red')
end
request=function(action,number)
 if pending or not npc or not IsAtStableMaster()or InCombatLockdown()then return end
 serial=serial+1;pending={id=serial,time=GetTime()};staging=nil;clearDrag()
 SendChatMessage('.mmstable '..action..' '..npc..' '..serial..(number and(' '..number)or ''),'SAY')
 render()
end
local function transfer(from,to)
 if not state or pending or from==to or to>state.slots then return end
 local pet=state.pets[from];if not pet then return end
 if from==0 and to>0 then
  local other=state.pets[to]
  if other then request('retrieve',other.id)else request('store',pet.id)end
 elseif from>0 and to==0 then request('retrieve',pet.id)
 end
end
for i=0,4 do
 local index=i;local b=buttons[i]
 for _,script in ipairs({'OnClick','OnDragStart','OnReceiveDrag','OnDragStop'})do
  local old=b:GetScript(script)
  b:SetScript(script,function(self,...)
   if not state then if old then return old(self,...)end;return end
   if pending then return end
   if script=='OnDragStart'then
    if state.pets[index]then dragged={slot=index,id=state.pets[index].id};selected=index;SetCursor('CAST_CURSOR');render()end
   elseif script=='OnDragStop'then
    local source=dragged
    if source and state.pets[source.slot]and state.pets[source.slot].id==source.id then
     for target=0,4 do if MouseIsOver(buttons[target])then transfer(source.slot,target);break end end
    end
    clearDrag()
   elseif dragged then
    local source=dragged;clearDrag()
    if state.pets[source.slot]and state.pets[source.slot].id==source.id then transfer(source.slot,index)end
   elseif script=='OnClick'then
    if state.pets[index]then selected=index
    elseif selected and state.pets[selected]then transfer(selected,index)end
   end
   render()
  end)
 end
end
local nativeBuy=PetStablePurchaseButton:GetScript('OnClick')
PetStablePurchaseButton:SetScript('OnClick',function(self,...)
 if state then request('buy')elseif nativeBuy then return nativeBuy(self,...)end
end)
local events=CreateFrame('Frame')
for _,event in ipairs({'PET_STABLE_SHOW','PET_STABLE_CLOSED','PET_STABLE_UPDATE','PET_STABLE_UPDATE_PAPERDOLL','UNIT_PET','UNIT_NAME_UPDATE','UNIT_HAPPINESS','CHAT_MSG_SYSTEM','PLAYER_MONEY'})do events:RegisterEvent(event)end
events:SetScript('OnEvent',function(_,event,message)
 if event=='PET_STABLE_CLOSED'then reset();return end
 if event=='PET_STABLE_SHOW'then
  reset();if not eligible()then return end
  npc=UnitGUID('npc')or UnitGUID('target');if npc then request('status')end;return
 end
 if event~='CHAT_MSG_SYSTEM'then dirty=true;return end
 if type(message)~='string'or not pending then return end
 local id,slots,cost=message:match('^MM_STABLE BEGIN (%d+) (%d+) (%d+)$')
 if id and tonumber(id)==pending.id then staging={slots=math.min(4,tonumber(slots)),cost=tonumber(cost),pets={}};return end
 local req,slot,number,entry,level,kind,name=message:match('^MM_STABLE PET (%d+) (%d+) (%d+) (%d+) (%d+) (%d+) ([%x%-]+)$')
 if req and staging and tonumber(req)==pending.id and tonumber(slot)<=4 then
  staging.pets[tonumber(slot)]={id=tonumber(number),entry=tonumber(entry),level=tonumber(level),kind=tonumber(kind),name=unhex(name)};return
 end
 local done=message:match('^MM_STABLE END (%d+)$')
 if done and staging and tonumber(done)==pending.id then
  clearDrag();state=staging;pending=nil;staging=nil;render();return
 end
 local failed,reason=message:match('^MM_STABLE ERROR (%d+) (.+)$')
 if failed and tonumber(failed)==pending.id then pending=nil;staging=nil;render();DEFAULT_CHAT_FRAME:AddMessage('Stable request rejected: '..reason)end
end)
events:SetScript('OnUpdate',function()
 if dirty then dirty=nil;render()end
 if pending and GetTime()-pending.time>8 then
  pending=nil;staging=nil;render();DEFAULT_CHAT_FRAME:AddMessage('No stable server response. Close and reopen the stable.')
 end
end)
PetStableFrame:HookScript('OnHide',reset)
PetStableFrame:HookScript('OnShow',function()dirty=true end)
ChatFrame_AddMessageEventFilter('CHAT_MSG_SYSTEM',function(_,_,message)return type(message)=='string'and message:match('^MM_STABLE ')~=nil end)
