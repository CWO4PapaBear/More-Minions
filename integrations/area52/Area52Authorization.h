#pragma once

#include <cstdint>
#include <string_view>

namespace MoreMinionsArea52
{
struct Mode
{
    bool enabled = false;
    bool coaEnabled = false;
    std::string_view classModel;
    std::string_view realmType;
};

constexpr bool Applies(Mode const& mode, std::uint8_t playerClass)
{
    return mode.enabled && mode.coaEnabled && mode.classModel == "hero" &&
        mode.realmType == "live" && playerClass == 10;
}

constexpr std::uint32_t ParentSpell(std::uint32_t bundle)
{
    switch (bundle)
    {
        case 23965200: return 965200;
        case 23091634: return 91634;
        case 23000890: return 890;
        case 23000891: return 891;
        case 23091606: return 91606;
        case 21954705: return 954705;
        default: return 0;
    }
}

template <class HasSpell>
bool Authorized(Mode const& mode, std::uint8_t playerClass, std::uint32_t bundle, HasSpell const& hasSpell)
{
    auto const spell = ParentSpell(bundle);
    return Applies(mode, playerClass) && spell != 0 && hasSpell(spell);
}
}
