#include "Area52Adapter.h"
#include <cassert>
#include <iostream>
#include <set>

bool (*registered)(Player const*, unsigned) = nullptr;
void MoreMinionsSetAuthorization(bool (*fn)(Player const*, unsigned)) { registered = fn; }
ConfigMgr config;
ConfigMgr* sConfigMgr = &config;

int main()
{
    using namespace MoreMinionsArea52;
    Mode mode{true, true, "hero", "live"};
    std::set<unsigned> learned;
    auto knows = [&](unsigned spell) { return learned.count(spell) != 0; };
    for (unsigned bundle : {23965200u, 23091634u, 23000890u, 23000891u, 23091606u, 21954705u})
    {
        learned.clear();
        assert(!Authorized(mode, 10, bundle, knows));
        learned.insert(ParentSpell(bundle));
        assert(Authorized(mode, 10, bundle, knows));
        for (unsigned cls : {1u, 3u, 9u, 11u, 12u, 32u})
            assert(!Authorized(mode, cls, bundle, knows));
        assert(!Authorized({false, true, "hero", "live"}, 10, bundle, knows));
        assert(!Authorized({true, false, "hero", "live"}, 10, bundle, knows));
        assert(!Authorized({true, true, "coa", "live"}, 10, bundle, knows));
        assert(!Authorized({true, true, "hero", "seasonal"}, 10, bundle, knows));
        assert(!Authorized({true, true, "wildcard", "live"}, 10, bundle, knows));
        assert(!Authorized({true, true, "unexpected", "live"}, 10, bundle, knows));
        learned.clear();
        assert(!Authorized(mode, 10, bundle, knows));
    }
    learned = {899, 896, 688, 920000};
    assert(!Authorized(mode, 10, 23000891, knows));
    assert(!Authorized(mode, 10, 21954705, knows));
    assert(!Authorized(mode, 10, 23920000, knows));
    assert(!Authorized(mode, 10, 500009183, knows));
    assert(!Authorized(mode, 10, 0, knows));
    Configure();
    assert(registered == nullptr);
    config.enabled = true;
    config.coa = true;
    config.model = "hero";
    Configure();
    Player player{10, {891}};
    assert(registered && registered(&player, 23000891));
    assert(!registered(nullptr, 23000891));
    player.spells.clear();
    assert(!registered(&player, 23000891));
    config.model = "coa";
    Configure();
    player.spells.insert(891);
    assert(!registered(&player, 23000891));
    std::cout << "PASS: six parent-spell authorizations, mode/class isolation, refund revocation, unknown-ID rejection, adapter registration\n";
}
