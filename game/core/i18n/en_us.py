"""English locale pack for UI and battle text output."""

from __future__ import annotations

WINDOW_TITLE = "TBS Prototype"

MAIN_MENU_TITLE = "TBS Prototype"
MAIN_MENU_START = "Enter/Space: Start Game"
MAIN_MENU_QUIT = "ESC: Quit"

LEVEL_SELECT_TITLE = "Level Select"
LEVEL_SELECT_SCENARIO = "Scenario 1 (level_1)"
LEVEL_SELECT_DEPLOYMENT = "Enter: Deployment"
LEVEL_SELECT_PROGRESSION = "P: Progression"
LEVEL_SELECT_BACK = "ESC: Back"

DEPLOYMENT_TITLE = "Deployment"
DEPLOYMENT_TIPS = "Click a unit on the left, then click a blue deployment tile."
DEPLOYMENT_START = "Start Battle"
DEPLOYMENT_READY = "All units deployed. Ready to battle."
DEPLOYMENT_NOT_READY = "Deploy all units first."
DEPLOYMENT_UNPLACED = "Unplaced"

PROGRESSION_TITLE = "Progression"
PROGRESSION_PANEL_UNITS = "Units"
PROGRESSION_PANEL_STATS = "Stats"
PROGRESSION_PANEL_SKILLS = "Skills"
PROGRESSION_NO_SKILLS = "No skills available"
PROGRESSION_HELP = "Mouse: select/add/learn/equip   Wheel: scroll   ESC: back"
PROGRESSION_BUTTON_LEARN = "Learn"
PROGRESSION_BUTTON_EQUIP = "Equip"
PROGRESSION_BUTTON_BACK = "Back"
PROGRESSION_SKILL_STATE_EQUIPPED = "Equipped"
PROGRESSION_SKILL_STATE_LEARNED = "Learned"
PROGRESSION_SKILL_STATE_LOCKED = "Locked"
PROGRESSION_STATS_HEADER = "Allocated Stats:"
PROGRESSION_LEARNED_COUNT = "Learned"
PROGRESSION_EQUIPPED_COUNT = "Equipped"
PROGRESSION_NAME = "Name"
PROGRESSION_LEVEL = "Level"
PROGRESSION_EXP = "EXP"
PROGRESSION_STAT_POINTS = "Stat Pts"
PROGRESSION_SKILL_POINTS = "Skill Pts"
PROGRESSION_SKILL_DESCRIPTION = "Skill Description"
PROGRESSION_SKILL_BUFFS = "Buff Effects"
PROGRESSION_NO_DESCRIPTION = "No description"

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

STATUS_TEXTS = {
    "normal": "Normal",
    "acted": "Acted",
    "stun": "Stunned",
    "silence": "Silenced",
    "dead": "Down",
    "alive": "Alive",
}


def get_skill_description(skill_id: str) -> str:
    return SKILL_DESCRIPTIONS.get(skill_id, PROGRESSION_NO_DESCRIPTION)


def get_buff_description(buff_id: str) -> str:
    return BUFF_DESCRIPTIONS.get(buff_id, PROGRESSION_NO_DESCRIPTION)


def get_status_text(status_key: str) -> str:
    return STATUS_TEXTS.get(status_key, status_key)


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
    return f"{unit_name} learned {skill_name}"


def format_progression_message_cannot_learn(skill_name: str) -> str:
    return f"Cannot learn {skill_name}"


def format_progression_message_equip(unit_name: str, skill_name: str) -> str:
    return f"{unit_name} equipped {skill_name}"


def format_progression_message_cannot_equip(skill_name: str) -> str:
    return f"Cannot equip {skill_name}"


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
    return f"{unit_name}'s {buff_name} absorbs {absorbed} damage"


def format_battle_counter(unit_name: str, target_name: str, damage: int) -> str:
    return f"{unit_name} counters {target_name} for {damage} damage"


def format_battle_trigger_heal(unit_name: str, heal_value: int, buff_name: str) -> str:
    return f"{unit_name} restores {heal_value} HP through {buff_name}"


def format_battle_tick_damage(unit_name: str, damage: int, buff_name: str) -> str:
    return f"{unit_name} takes {damage} damage from {buff_name}"


def format_battle_tick_heal(unit_name: str, heal_value: int, buff_name: str) -> str:
    return f"{unit_name} restores {heal_value} HP through {buff_name}"


def format_skill_menu_label(skill_name: str, power: float) -> str:
    return f"{skill_name} x{power:.1f}"


def format_skill_use(user_name: str, skill_name: str, target_name: str, value: int) -> str:
    return f"{user_name} uses {skill_name} on {target_name} for {value} effect"
