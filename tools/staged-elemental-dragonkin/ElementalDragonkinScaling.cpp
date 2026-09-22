// Staged first-wave handler. Requires guarded definition/binding installation.
#include "ScriptMgr.h"
#include "SpellScript.h"
#include "SpellInfo.h"
#include "Player.h"
#include "Pet.h"
#include <algorithm>
#include <cmath>

// The module bridge checks ownership, managed capture origin, current access,
// enabled mapping and membership of this spell in the creature's family profile.
extern Player* MoreMinionsScalingOwner(Unit*, unsigned);

namespace {
bool ReviewedSpell(unsigned id) {
    switch (id) {
    case 892102: case 892111: case 892121: case 892131:
    case 91755: case 91758: case 91759: case 91821:
    case 91768: case 91819: return true;
    default: return false;
    }
}
class DirectScaling : public SpellScript {
    PrepareSpellScript(DirectScaling);
    bool Validate(SpellInfo const* info) override {
        return ReviewedSpell(info->Id)
            && info->Effects[EFFECT_0].Effect == SPELL_EFFECT_SCHOOL_DAMAGE
            && !info->Effects[EFFECT_1].Effect && !info->Effects[EFFECT_2].Effect;
    }
    SpellCastResult Check() {
        return MoreMinionsScalingOwner(GetCaster(), GetSpellInfo()->Id)
            ? SPELL_CAST_OK : SPELL_FAILED_BAD_TARGETS;
    }
    void Scale(SpellEffIndex) {
        auto owner = MoreMinionsScalingOwner(GetCaster(), GetSpellInfo()->Id);
        if (!owner) { SetEffectValue(0); return; }
        double level = std::max(1u, std::min(80u, unsigned(owner->GetLevel())));
        double multiplier = 0.0267291844060354 + 0.0048541098014737 * level
            + 0.0001859597762293 * level * level;
        // Launch-target runs before native damage, armor/resistance and crit.
        // Use the calculated effect value to retain source dice, not stored BP.
        SetEffectValue(int32(std::lround(std::max(0, GetEffectValue()) * multiplier)));
    }
    void Register() override {
        OnCheckCast += SpellCheckCastFn(DirectScaling::Check);
        OnEffectLaunchTarget += SpellEffectFn(DirectScaling::Scale, EFFECT_0, SPELL_EFFECT_SCHOOL_DAMAGE);
    }
};
class ScalingLoader : public SpellScriptLoader {
public:
    ScalingLoader() : SpellScriptLoader("more_minions_elemental_dragonkin_direct") { }
    SpellScript* GetSpellScript() const override { return new DirectScaling(); }
};
}
void AddMoreMinionsElementalDragonkinScripts() { new ScalingLoader(); }
