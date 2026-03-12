"""English locale pack for UI and battle text output."""

from __future__ import annotations

WINDOW_TITLE = "TBS Prototype"

MAIN_MENU_TITLE = "TBS Prototype"
MAIN_MENU_START = "Start Game"
MAIN_MENU_QUIT = "Quit"

LEVEL_SELECT_TITLE = "Level Select"
LEVEL_SELECT_SCENARIO = "Scenario 1 (level_1)"
LEVEL_SELECT_DEPLOYMENT = "Deployment"
LEVEL_SELECT_PROGRESSION = "Progression"
LEVEL_SELECT_BACK = "Back to Main Menu"

DEPLOYMENT_TITLE = "Deployment"
DEPLOYMENT_TIPS = "Click a unit on the left, then click a blue deployment tile."
DEPLOYMENT_START = "Start Battle"
DEPLOYMENT_READY = "All units deployed. Ready to battle."
DEPLOYMENT_NOT_READY = "Deploy all units first."
DEPLOYMENT_UNPLACED = "Unplaced"

PROGRESSION_TITLE = "Progression"
PROGRESSION_SELECT_TITLE = "Select Character"
PROGRESSION_SELECT_HELP = "Click a character to enter progression   Wheel/Left/Right: scroll   ESC: back"
PROGRESSION_PROFESSION_LABEL = "Class"
PROGRESSION_PROFESSION_UNKNOWN = "Unassigned"
PROGRESSION_SUMMARY_TITLE = "Character Info"
PROGRESSION_EQUIPMENT_HEADER = "Equipped Items"
PROGRESSION_PANEL_UNITS = "Units"
PROGRESSION_PANEL_STATS = "Stats"
PROGRESSION_PANEL_SKILLS = "Progression Modes"
PROGRESSION_TAB_STATS = "Stats"
PROGRESSION_TAB_SKILLS = "Skills"
PROGRESSION_TAB_EQUIPMENT = "Equipment"
PROGRESSION_SKILL_SECTION = "Skills"
PROGRESSION_EQUIPMENT_SECTION = "Equipment"
PROGRESSION_EQUIPMENT_SLOTS = "Equipment Slots"
PROGRESSION_NO_SKILLS = "No skills available"
PROGRESSION_NO_EQUIPMENT = "No equipment for this slot"
PROGRESSION_HELP = "Mouse: select/add/learn/equip gear   Wheel: scroll   ESC: back"
PROGRESSION_BUTTON_LEARN = "Learn"
PROGRESSION_BUTTON_EQUIP = "Equip"
PROGRESSION_BUTTON_UNEQUIP = "Unequip"
PROGRESSION_BUTTON_BACK = "Back"
PROGRESSION_SKILL_STATE_EQUIPPED = "Equipped"
PROGRESSION_SKILL_STATE_LEARNED = "Learned"
PROGRESSION_SKILL_STATE_LOCKED = "Locked"
PROGRESSION_EQUIP_STATE_EQUIPPED = "Equipped"
PROGRESSION_EQUIP_STATE_AVAILABLE = "Available"
PROGRESSION_EQUIP_STATE_EMPTY = "Empty"
PROGRESSION_STATS_HEADER = "Allocated Stats:"
PROGRESSION_LEARNED_COUNT = "Learned"
PROGRESSION_EQUIPPED_COUNT = "Equipped"
PROGRESSION_NAME = "Name"
PROGRESSION_LEVEL = "Level"
PROGRESSION_EXP = "EXP"
PROGRESSION_STAT_POINTS = "Stat Pts"
PROGRESSION_SKILL_POINTS = "Skill Pts"
PROGRESSION_SKILL_DESCRIPTION = "Skill Description"
PROGRESSION_EQUIPMENT_DESCRIPTION = "Equipment Description"
PROGRESSION_SKILL_BUFFS = "Buff Effects"
PROGRESSION_NO_DESCRIPTION = "No description"
PROGRESSION_SLOT_WEAPON = "Weapon"
PROGRESSION_SLOT_OFFHAND = "Offhand"
PROGRESSION_SLOT_ACCESSORY = "Accessory"

RESULT_TIP = "Enter: Main Menu   ESC: Quit"

ACTION_MENU_TITLE = "Action"
ACTION_MENU_OPTIONS = ["Move", "Attack", "Skill", "Wait"]

SKILL_MENU_TITLE = "Skills"

UNIT_INFO_TITLE = "Unit Info"
UNIT_INFO_NONE = "No unit selected"
UNIT_INFO_HP = "HP"
UNIT_INFO_ATK = "ATK"
UNIT_INFO_DEF = "DEF"
UNIT_INFO_MOVE = "MOVE"
UNIT_INFO_RANGE = "RANGE"
UNIT_INFO_STATUS = "Status"
UNIT_INFO_BUFFS = "Effects"

TURN_PLAYER = "Player Turn"
TURN_ENEMY = "Enemy Turn"
BATTLE_START = "Battle Start"
BATTLE_VICTORY = "Victory"
BATTLE_DEFEAT = "Defeat"
BATTLE_ENDED = "Battle Ended"

SKILL_NAMES = {
    "Power Strike": "Power Strike",
    "Poison Strike": "Poison Strike",
    "Regen Aura": "Regen Aura",
    "Guard Shield": "Guard Shield",
    "Battle Chant": "Battle Chant",
    "Concussion Blow": "Concussion Blow",
    "Counter Stance": "Counter Stance",
    "War Banner": "War Banner",
    "Blood Rush": "Blood Rush",
    "Raise Skeleton": "Raise Skeleton",
    "Revive Prayer": "Revive Prayer",
}

SKILL_DESCRIPTIONS = {
    "Power Strike": "Deal 150% attack damage to one target.",
    "Poison Strike": "Deal normal damage and inflict poison.",
    "Regen Aura": "Apply regeneration to the target.",
    "Guard Shield": "Apply a temporary damage-absorbing shield.",
    "Battle Chant": "Increase the target's attack for a short time.",
    "Concussion Blow": "Deal reduced damage and stun the target.",
    "Counter Stance": "Enable counterattacks after being hit.",
    "War Banner": "Grant an attack aura around the target.",
    "Blood Rush": "Gain lifesteal on hit.",
    "Raise Skeleton": "Summon a temporary allied unit.",
    "Revive Prayer": "Revive a fallen unit with partial HP.",
}

BUFF_NAMES = {
    "poison": "Poison",
    "burn": "Burn",
    "regen": "Regeneration",
    "attack_up": "Attack Up",
    "counter": "Counter",
    "attack_aura": "Attack Aura",
    "lifesteal": "Lifesteal",
    "stun": "Stun",
    "silence": "Silence",
    "shield": "Shield",
}

BUFF_DESCRIPTIONS = {
    "poison": "Takes damage at turn start.",
    "burn": "Takes damage at turn end.",
    "regen": "Recovers HP at turn start.",
    "attack_up": "Temporarily increases attack.",
    "counter": "Counterattacks after taking a hit.",
    "attack_aura": "Grants nearby allies bonus attack.",
    "lifesteal": "Restores HP after dealing damage.",
    "stun": "Cannot act during its turn.",
    "silence": "Cannot cast skills.",
    "shield": "Absorbs incoming damage first.",
}

EQUIPMENT_NAMES = {
    "iron_sword": "Iron Sword",
    "bronze_spear": "Bronze Spear",
    "wooden_shield": "Wooden Shield",
    "swift_boots": "Swift Boots",
    "toxic_charm": "Toxic Charm",
}

EQUIPMENT_DESCRIPTIONS = {
    "iron_sword": "Weapon. Grants ATK +2.",
    "bronze_spear": "Weapon. Grants ATK +1, DEF +1, and Counter Stance.",
    "wooden_shield": "Offhand. Grants DEF +2.",
    "swift_boots": "Accessory. Grants MOVE +1.",
    "toxic_charm": "Accessory. Grants Poison Strike.",
}

STATUS_TEXTS = {
    "normal": "Normal",
    "acted": "Acted",
    "stun": "Stunned",
    "silence": "Silenced",
    "dead": "Down",
    "alive": "Alive",
}


def get_skill_name(skill_id: str) -> str:
    return SKILL_NAMES.get(skill_id, skill_id)


def get_skill_description(skill_id: str) -> str:
    return SKILL_DESCRIPTIONS.get(skill_id, PROGRESSION_NO_DESCRIPTION)


def get_buff_name(buff_id: str) -> str:
    return BUFF_NAMES.get(buff_id, buff_id)


def get_buff_description(buff_id: str) -> str:
    return BUFF_DESCRIPTIONS.get(buff_id, PROGRESSION_NO_DESCRIPTION)


def get_equipment_name(equipment_id: str) -> str:
    return EQUIPMENT_NAMES.get(equipment_id, equipment_id)


def get_equipment_description(equipment_id: str) -> str:
    return EQUIPMENT_DESCRIPTIONS.get(equipment_id, PROGRESSION_NO_DESCRIPTION)


def get_status_text(status_key: str) -> str:
    return STATUS_TEXTS.get(status_key, status_key)


def get_slot_name(slot_id: str) -> str:
    return {
        "weapon": PROGRESSION_SLOT_WEAPON,
        "offhand": PROGRESSION_SLOT_OFFHAND,
        "accessory": PROGRESSION_SLOT_ACCESSORY,
    }.get(slot_id, slot_id)


def format_deployment_slot(index: int, unit_type: str, placement: tuple[int, int] | None) -> str:
    status = str(placement) if placement is not None else DEPLOYMENT_UNPLACED
    return f"{index + 1}. {unit_type} -> {status}"


def format_progression_level_exp(level: int, exp: int) -> str:
    return f"Lv.{level}  EXP {exp}"


def format_progression_points(stat_points: int, skill_points: int) -> str:
    return f"SP {stat_points}  KP {skill_points}"


def format_stat_line(label: str, value: int) -> str:
    return f"{label}: +{value}"


def format_range(min_range: int, max_range: int) -> str:
    return f"Range {min_range}-{max_range}"


def format_result_level(level: int) -> str:
    return f"Level: {level}"


def format_result_exp(exp: int) -> str:
    return f"EXP: {exp}"


def format_progression_message_gain(unit_name: str, stat_name: str) -> str:
    return f"{unit_name} gains +1 {stat_name}"


def format_progression_message_no_stat_points(unit_name: str) -> str:
    return f"{unit_name} has no stat points left"


def format_progression_message_learn(unit_name: str, skill_name: str) -> str:
    return f"{unit_name} learned {get_skill_name(skill_name)}"


def format_progression_message_cannot_learn(skill_name: str) -> str:
    return f"Cannot learn {get_skill_name(skill_name)}"


def format_progression_message_equip(unit_name: str, skill_name: str) -> str:
    return f"{unit_name} equipped {get_skill_name(skill_name)}"


def format_progression_message_cannot_equip(skill_name: str) -> str:
    return f"Cannot equip {get_skill_name(skill_name)}"


def format_progression_message_item_equip(unit_name: str, equipment_name: str, slot_name: str) -> str:
    return f"{unit_name} equipped {get_equipment_name(equipment_name)} in {slot_name}"


def format_progression_message_item_cannot_equip(equipment_name: str) -> str:
    return f"Cannot equip {get_equipment_name(equipment_name)}"


def format_progression_message_item_unequip(unit_name: str, slot_name: str) -> str:
    return f"{unit_name} removed equipment from {slot_name}"


def format_progression_message_item_cannot_unequip(slot_name: str) -> str:
    return f"No equipment in {slot_name}"


def format_equipment_line(slot_name: str, equipment_name: str) -> str:
    return f"{slot_name}: {equipment_name}"


def format_battle_attack(attacker_name: str, defender_name: str, damage: int) -> str:
    return f"{attacker_name} attacks {defender_name} for {damage} damage"


def format_battle_defeated(unit_name: str) -> str:
    return f"{unit_name} is defeated"


def format_battle_move(unit_name: str, from_pos: tuple[int, int], to_pos: tuple[int, int]) -> str:
    return f"{unit_name} moves {from_pos} -> {to_pos}"


def format_battle_wait(unit_name: str) -> str:
    return f"{unit_name} waits"


def format_battle_exp(unit_name: str, exp_value: int) -> str:
    return f"{unit_name} gains {exp_value} EXP"


def format_battle_level_up(unit_name: str, level: int) -> str:
    return f"{unit_name} reaches Lv.{level}"


def format_battle_shield_absorb(unit_name: str, buff_name: str, absorbed: int) -> str:
    return f"{unit_name}'s {get_buff_name(buff_name)} absorbs {absorbed} damage"


def format_battle_counter(unit_name: str, target_name: str, damage: int) -> str:
    return f"{unit_name} counters {target_name} for {damage} damage"


def format_battle_trigger_heal(unit_name: str, heal_value: int, buff_name: str) -> str:
    return f"{unit_name} restores {heal_value} HP through {get_buff_name(buff_name)}"


def format_battle_tick_damage(unit_name: str, damage: int, buff_name: str) -> str:
    return f"{unit_name} takes {damage} damage from {get_buff_name(buff_name)}"


def format_battle_tick_heal(unit_name: str, heal_value: int, buff_name: str) -> str:
    return f"{unit_name} restores {heal_value} HP through {get_buff_name(buff_name)}"


def format_skill_menu_label(skill_name: str, power: float) -> str:
    return f"{get_skill_name(skill_name)} x{power:.1f}"


def format_skill_use(user_name: str, skill_name: str, target_name: str, value: int) -> str:
    return f"{user_name} uses {get_skill_name(skill_name)} on {target_name} for {value} effect"


