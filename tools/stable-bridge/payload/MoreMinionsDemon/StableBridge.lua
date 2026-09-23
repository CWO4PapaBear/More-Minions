-- Native server transactions with a separate list for non-Beast primary pets.
local state,pending,serial,npc,selected,staging,dirty
local buttons={}
local panel=CreateFrame('Frame',nil,PetStableFrame)
panel:SetSize(340,145);panel:SetPoint('BOTTOMLEFT',16,35)
panel:SetFrameLevel(PetStableFrame:GetFrameLevel()+10)
panel:SetBackdrop({bgFile='Interface\\Tooltips\\UI-Tooltip-Background'})
panel:SetBackdropColor(.04,.04,.04,1);panel:Hide()
local label=panel:CreateFontString(nil,'OVERLAY','GameFontNormalSmall')
label:SetPoint('TOP',0,-3);label:SetText('Primary companion stable')
local status=panel:CreateFontString(nil,'OVERLAY','GameFontHighlightSmall')
status:SetPoint('TOP',0,-87);status:SetWidth(334)
local function eligible()
 for _,id in ipairs({899,896,93558,93569})do if IsSpellKnown(id)then return true end end
end
local function unhex(s)
 if s=='-'then return ''end
 return (s:gsub('%x%x',function(v)return string.char(tonumber(v,16))end))
end
local render,request
local nativeSlots={'PetStableCurrentPet','PetStableStabledPet1','PetStableStabledPet2','PetStableStabledPet3','PetStableStabledPet4'}
local function restore()
 for _,name in ipairs(nativeSlots)do if _G[name]then _G[name]:Show()end end
 state=nil;pending=nil;staging=nil;npc=nil;dirty=nil;panel:Hide()
end
local function actionButton(text,x,fn)
 local b=CreateFrame('Button',nil,panel,'UIPanelButtonTemplate')
 b:SetSize(106,22);b:SetPoint('BOTTOMLEFT',x,3);b:SetText(text);b:SetScript('OnClick',fn);return b
end
local store=actionButton('Store current',4,function()if state and state.pets[0]then request('store',state.pets[0].id)end end)
local retrieve=actionButton('Retrieve / swap',117,function()if state and selected and selected>0 and state.pets[selected]then request('retrieve',state.pets[selected].id)end end)
local buy=actionButton('Buy slot',230,function()request('buy')end)
local function enable(button,yes)if yes then button:Enable()else button:Disable()end end
for i=0,4 do
 local index=i
 local b=CreateFrame('Button',nil,panel)
 b:SetSize(44,44);b:SetPoint('TOPLEFT',14+i*66,-24)
 b.icon=b:CreateTexture(nil,'ARTWORK');b.icon:SetAllPoints()
 b:SetNormalTexture('Interface\\Buttons\\UI-Quickslot2')
 b:SetHighlightTexture('Interface\\Buttons\\ButtonHilight-Square','ADD')
 b.text=b:CreateFontString(nil,'OVERLAY','GameFontHighlightSmall');b.text:SetPoint('TOP',b,'BOTTOM',0,-2)
 b:SetScript('OnClick',function()selected=index;render()end)
 b:SetScript('OnEnter',function(self)
  if not state then return end
  local pet=state.pets[index];GameTooltip:SetOwner(self,'ANCHOR_RIGHT')
  GameTooltip:SetText(pet and pet.name or(index>state.slots and 'Locked slot'or 'Empty slot'))
  if pet then GameTooltip:AddLine('Level '..pet.level,1,1,1)end
  GameTooltip:Show()
 end)
 b:SetScript('OnLeave',function()GameTooltip:Hide()end)
 buttons[i]=b
end
render=function()
 if not state then return end
 panel:Show()
 -- Keep the native model/frame; hide controls relying on the empty native list.
 for _,name in ipairs({'PetStableCurrentPet','PetStableStabledPet1','PetStableStabledPet2','PetStableStabledPet3','PetStableStabledPet4','PetStablePurchaseButton','PetStableCostLabel','PetStableCostMoneyFrame','PetStableSlotText','PetStablePetInfo'})do
  if _G[name]then _G[name]:Hide()end
 end
 for i=0,4 do
  local b=buttons[i];local pet=state.pets[i]
  local icons={[1]='Ability_Hunter_BeastCall',[2]='Spell_Frost_SummonWaterElemental',[3]='INV_Misc_Head_Dragon_01',[4]='Spell_Shadow_SummonFelHunter',[6]='Spell_Shadow_AnimateDead'}
  b.icon:SetTexture(pet and ('Interface\\Icons\\'..(icons[pet.kind]or 'INV_Misc_QuestionMark'))or 'Interface\\Buttons\\UI-Quickslot')
  if pet and i==0 and UnitExists('pet')and UnitName('pet')==pet.name then SetPortraitTexture(b.icon,'pet')end
  b.text:SetText(i==0 and 'Current'or(i>state.slots and 'Locked'or('Slot '..i)))
  if i==selected then b:LockHighlight()else b:UnlockHighlight()end
 end
 local pet=state.pets[selected or 0]
 if pet then
  PetStableLevelText:SetText(pet.name..' - Level '..pet.level)
  if selected==0 and UnitExists('pet')then PetStableModel:SetUnit('pet')else PetStableModel:SetCreature(pet.entry)end
  PetStableModel:Show()
 else PetStableModel:Hide();PetStableLevelText:SetText('')end
 -- Only a live Beast has meaningful happiness. Never reuse a stale native tooltip.
 if pet and pet.kind==1 and selected==0 and UnitExists('pet')then
  local happiness=GetPetHappiness()
  local text=happiness and _G['PET_HAPPINESS'..happiness]
  if text and PetStablePetInfo then
   PetStablePetInfo.tooltip=text;PetStablePetInfo:Show()
  end
 end
 local free=false;for i=1,state.slots do if not state.pets[i]then free=true end end
 enable(store,not pending and state.pets[0]and free)
 enable(retrieve,not pending and selected and selected>0 and state.pets[selected])
 enable(buy,not pending and state.slots<4 and GetMoney()>=state.cost)
 status:SetText(pending and 'Waiting for the server...'or(state.slots<4 and ('Next slot: '..GetCoinTextureString(state.cost))or 'All stable slots purchased'))
end
request=function(action,number)
 if pending or not npc or not IsAtStableMaster()or InCombatLockdown()then return end
 serial=(serial or 0)+1;pending={id=serial,time=GetTime()};staging=nil
 SendChatMessage('.mmstable '..action..' '..npc..' '..serial..(number and (' '..number)or ''),'SAY')
 render()
end
local events=CreateFrame('Frame')
for _,event in ipairs({'PET_STABLE_SHOW','PET_STABLE_CLOSED','PET_STABLE_UPDATE','CHAT_MSG_SYSTEM','PLAYER_MONEY'})do events:RegisterEvent(event)end
events:SetScript('OnEvent',function(_,event,message)
 if event=='PET_STABLE_CLOSED'then restore();return end
 if event=='PET_STABLE_SHOW'then
  restore();selected=0
  if not eligible()then return end
  npc=UnitGUID('npc')or UnitGUID('target')
  if npc then request('status')end;return
 end
 if event=='PET_STABLE_UPDATE'or event=='PLAYER_MONEY'then dirty=true;return end
 if type(message)~='string'or not pending then return end
 local id,slots,cost=message:match('^MM_STABLE BEGIN (%d+) (%d+) (%d+)$')
 if id and tonumber(id)==pending.id then staging={id=tonumber(id),slots=math.min(4,tonumber(slots)),cost=tonumber(cost),pets={}};return end
 local req,slot,number,entry,level,origin,name=message:match('^MM_STABLE PET (%d+) (%d+) (%d+) (%d+) (%d+) (%d+) ([%x%-]+)$')
 if req and staging and tonumber(req)==pending.id and tonumber(slot)<=4 then
  staging.pets[tonumber(slot)]={id=tonumber(number),entry=tonumber(entry),level=tonumber(level),kind=tonumber(origin),name=unhex(name)};return
 end
 local done=message:match('^MM_STABLE END (%d+)$')
 if done and staging and tonumber(done)==pending.id then state=staging;pending=nil;staging=nil;render();return end
 local failed,reason=message:match('^MM_STABLE ERROR (%d+) (.+)$')
 if failed and tonumber(failed)==pending.id then pending=nil;staging=nil;render();DEFAULT_CHAT_FRAME:AddMessage('Stable request rejected: '..reason);return end
end)
events:SetScript('OnUpdate',function()
 if dirty then dirty=nil;render()end
 if pending and GetTime()-pending.time>8 then pending=nil;staging=nil;render();DEFAULT_CHAT_FRAME:AddMessage('No stable server response. Close and reopen the stable after checking the server package.')end
end)
-- Do not wrap PetStable_Update: StableCompatibility scopes that Lua function's environment.
PetStableFrame:HookScript('OnShow',function()dirty=true end)
ChatFrame_AddMessageEventFilter('CHAT_MSG_SYSTEM',function(_,_,message)return type(message)=='string'and message:match('^MM_STABLE ')~=nil end)
