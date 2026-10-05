#pragma once

#include "Area52Authorization.h"
#include "Config.h"
#include "Player.h"
#include <string>

extern void MoreMinionsSetAuthorization(bool (*fn)(Player const*, unsigned));

namespace MoreMinionsArea52
{
inline bool Enabled = false;
inline bool CoAEnabled = false;
inline std::string ClassModel;
inline std::string RealmType;

inline bool Authorize(Player const* player, unsigned bundle)
{
    return player && Authorized({Enabled, CoAEnabled, ClassModel, RealmType}, player->getClass(), bundle,
        [player](std::uint32_t spell) { return player->HasSpell(spell); });
}

inline void Configure()
{
    Enabled = sConfigMgr->GetOption<bool>("MoreMinions.Area52.Enable", false);
    if (!Enabled)
        return;

    CoAEnabled = sConfigMgr->GetOption<bool>("CoA.Enable", false);
    ClassModel = sConfigMgr->GetOption<std::string>("CoA.ClassModel", "coa");
    RealmType = sConfigMgr->GetOption<std::string>("CoA.RealmType", "live");
    MoreMinionsSetAuthorization(Authorize);
}
}
