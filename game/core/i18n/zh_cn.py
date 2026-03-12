"""简体中文语言包：集中维护界面文案与动态提示。"""

from __future__ import annotations

WINDOW_TITLE = "战棋原型"

MAIN_MENU_TITLE = "战棋原型"
MAIN_MENU_START = "开始游戏"
MAIN_MENU_QUIT = "退出游戏"

LEVEL_SELECT_TITLE = "关卡选择"
LEVEL_SELECT_SCENARIO = "场景 1（level_1）"
LEVEL_SELECT_DEPLOYMENT = "进入部署"
LEVEL_SELECT_PROGRESSION = "角色成长"
LEVEL_SELECT_BACK = "返回主菜单"

DEPLOYMENT_TITLE = "战前部署"
DEPLOYMENT_TIPS = "点击左侧名单选择单位，再点击蓝色部署格放置"
DEPLOYMENT_START = "开始战斗"
DEPLOYMENT_READY = "已全部部署，可以开始战斗"
DEPLOYMENT_NOT_READY = "请先完成全部单位部署"
DEPLOYMENT_UNPLACED = "未部署"

PROGRESSION_TITLE = "角色成长"
PROGRESSION_SELECT_TITLE = "选择成长角色"
PROGRESSION_SELECT_HELP = "鼠标点击角色进入成长   滚轮/左右键：横向切换   ESC：返回"
PROGRESSION_PROFESSION_LABEL = "职业"
PROGRESSION_PROFESSION_UNKNOWN = "未设定"
PROGRESSION_SUMMARY_TITLE = "角色信息"
PROGRESSION_EQUIPMENT_HEADER = "当前装备"
PROGRESSION_PANEL_UNITS = "角色列表"
PROGRESSION_PANEL_STATS = "属性成长"
PROGRESSION_PANEL_SKILLS = "成长功能"
PROGRESSION_TAB_STATS = "属性"
PROGRESSION_TAB_SKILLS = "技能"
PROGRESSION_TAB_EQUIPMENT = "装备"
PROGRESSION_SKILL_SECTION = "技能列表"
PROGRESSION_EQUIPMENT_SECTION = "装备列表"
PROGRESSION_EQUIPMENT_SLOTS = "装备槽位"
PROGRESSION_NO_SKILLS = "暂无可用技能"
PROGRESSION_NO_EQUIPMENT = "当前槽位暂无可装备物品"
PROGRESSION_HELP = "鼠标：选角色/技能/装备/加点   滚轮：滚动   ESC：返回"
PROGRESSION_BUTTON_LEARN = "学习"
PROGRESSION_BUTTON_EQUIP = "装备"
PROGRESSION_BUTTON_UNEQUIP = "卸下"
PROGRESSION_BUTTON_BACK = "返回"
PROGRESSION_SKILL_STATE_EQUIPPED = "已装备"
PROGRESSION_SKILL_STATE_LEARNED = "已学习"
PROGRESSION_SKILL_STATE_LOCKED = "未学习"
PROGRESSION_EQUIP_STATE_EQUIPPED = "当前装备"
PROGRESSION_EQUIP_STATE_AVAILABLE = "可装备"
PROGRESSION_EQUIP_STATE_EMPTY = "未装备"
PROGRESSION_STATS_HEADER = "已分配属性："
PROGRESSION_LEARNED_COUNT = "已学技能"
PROGRESSION_EQUIPPED_COUNT = "已装技能"
PROGRESSION_NAME = "名称"
PROGRESSION_LEVEL = "等级"
PROGRESSION_EXP = "经验"
PROGRESSION_STAT_POINTS = "属性点"
PROGRESSION_SKILL_POINTS = "技能点"
PROGRESSION_SKILL_DESCRIPTION = "技能说明"
PROGRESSION_EQUIPMENT_DESCRIPTION = "装备说明"
PROGRESSION_SKILL_BUFFS = "附带效果"
PROGRESSION_NO_DESCRIPTION = "暂无说明"
PROGRESSION_SLOT_WEAPON = "武器"
PROGRESSION_SLOT_OFFHAND = "副手"
PROGRESSION_SLOT_ACCESSORY = "饰品"

RESULT_TIP = "Enter：回到主菜单   ESC：退出游戏"

ACTION_MENU_TITLE = "行动"
ACTION_MENU_OPTIONS = ["移动", "攻击", "技能", "待机"]

SKILL_MENU_TITLE = "技能"

UNIT_INFO_TITLE = "单位信息"
UNIT_INFO_NONE = "未选择单位"
UNIT_INFO_HP = "生命"
UNIT_INFO_ATK = "攻击"
UNIT_INFO_DEF = "防御"
UNIT_INFO_MOVE = "移动"
UNIT_INFO_RANGE = "射程"
UNIT_INFO_STATUS = "状态"
UNIT_INFO_BUFFS = "效果"

TURN_PLAYER = "玩家回合"
TURN_ENEMY = "敌方回合"
BATTLE_START = "战斗开始"
BATTLE_VICTORY = "胜利"
BATTLE_DEFEAT = "失败"
BATTLE_ENDED = "战斗结束"

SKILL_NAMES = {
    "Power Strike": "强力打击",
    "Poison Strike": "毒击",
    "Regen Aura": "再生光环",
    "Guard Shield": "守护护盾",
    "Battle Chant": "战吼",
    "Concussion Blow": "震荡打击",
    "Counter Stance": "反击架势",
    "War Banner": "战旗",
    "Blood Rush": "嗜血冲动",
    "Raise Skeleton": "召唤骷髅",
    "Revive Prayer": "复苏祷言",
}

SKILL_DESCRIPTIONS = {
    "Power Strike": "造成 150% 攻击力的单体伤害。",
    "Poison Strike": "造成普通伤害，并为目标附加中毒。",
    "Regen Aura": "为目标附加再生效果，持续恢复生命。",
    "Guard Shield": "为目标附加护盾，优先吸收伤害。",
    "Battle Chant": "为目标附加攻击提升效果。",
    "Concussion Blow": "造成较低伤害，并使目标眩晕。",
    "Counter Stance": "进入反击姿态，受击后自动反击。",
    "War Banner": "为目标附加攻击光环，强化周围单位。",
    "Blood Rush": "附加吸血效果，命中后恢复生命。",
    "Raise Skeleton": "召唤一个临时单位加入战场。",
    "Revive Prayer": "复活倒下目标并恢复部分生命。",
}

BUFF_NAMES = {
    "poison": "中毒",
    "burn": "灼烧",
    "regen": "再生",
    "attack_up": "攻击提升",
    "counter": "反击",
    "attack_aura": "攻击光环",
    "lifesteal": "吸血",
    "stun": "眩晕",
    "silence": "沉默",
    "shield": "护盾",
}

BUFF_DESCRIPTIONS = {
    "poison": "回合开始时受到持续伤害。",
    "burn": "回合结束时受到持续伤害。",
    "regen": "回合开始时恢复生命。",
    "attack_up": "攻击力临时提高。",
    "counter": "受击后自动对攻击者反击一次。",
    "attack_aura": "为范围内友军提供攻击加成。",
    "lifesteal": "命中后按伤害比例恢复生命。",
    "stun": "无法移动、攻击，并跳过本回合。",
    "silence": "无法使用技能。",
    "shield": "优先吸收受到的伤害。",
}

EQUIPMENT_NAMES = {
    "iron_sword": "铁剑",
    "bronze_spear": "青铜枪",
    "wooden_shield": "木盾",
    "swift_boots": "迅捷靴",
    "toxic_charm": "毒咒护符",
}

EQUIPMENT_DESCRIPTIONS = {
    "iron_sword": "武器，提供攻击 +2。",
    "bronze_spear": "武器，提供攻击 +1、防御 +1，并授予反击架势。",
    "wooden_shield": "副手，提供防御 +2。",
    "swift_boots": "饰品，提供移动 +1。",
    "toxic_charm": "饰品，授予毒击技能。",
}

STATUS_TEXTS = {
    "normal": "正常",
    "acted": "已行动",
    "stun": "眩晕中",
    "silence": "沉默中",
    "dead": "已倒下",
    "alive": "存活",
}


def get_skill_name(skill_id: str) -> str:
    """返回技能显示名称。"""
    return SKILL_NAMES.get(skill_id, skill_id)


def get_skill_description(skill_id: str) -> str:
    """返回技能说明文本。"""
    return SKILL_DESCRIPTIONS.get(skill_id, PROGRESSION_NO_DESCRIPTION)


def get_buff_name(buff_id: str) -> str:
    """返回 Buff 显示名称。"""
    return BUFF_NAMES.get(buff_id, buff_id)


def get_buff_description(buff_id: str) -> str:
    """返回 Buff 说明文本。"""
    return BUFF_DESCRIPTIONS.get(buff_id, PROGRESSION_NO_DESCRIPTION)


def get_equipment_name(equipment_id: str) -> str:
    """返回装备显示名称。"""
    return EQUIPMENT_NAMES.get(equipment_id, equipment_id)


def get_equipment_description(equipment_id: str) -> str:
    """返回装备说明文本。"""
    return EQUIPMENT_DESCRIPTIONS.get(equipment_id, PROGRESSION_NO_DESCRIPTION)


def get_status_text(status_key: str) -> str:
    """返回状态文本。"""
    return STATUS_TEXTS.get(status_key, status_key)


def get_slot_name(slot_id: str) -> str:
    """返回装备槽位名称。"""
    return {
        "weapon": PROGRESSION_SLOT_WEAPON,
        "offhand": PROGRESSION_SLOT_OFFHAND,
        "accessory": PROGRESSION_SLOT_ACCESSORY,
    }.get(slot_id, slot_id)


def format_deployment_slot(index: int, unit_type: str, placement: tuple[int, int] | None) -> str:
    status = str(placement) if placement is not None else DEPLOYMENT_UNPLACED
    return f"{index + 1}. {unit_type} -> {status}"


def format_progression_level_exp(level: int, exp: int) -> str:
    return f"等级 {level}  经验 {exp}"


def format_progression_points(stat_points: int, skill_points: int) -> str:
    return f"属性点 {stat_points}  技能点 {skill_points}"


def format_stat_line(label: str, value: int) -> str:
    return f"{label}: +{value}"


def format_range(min_range: int, max_range: int) -> str:
    return f"射程 {min_range}-{max_range}"


def format_result_level(level: int) -> str:
    return f"等级：{level}"


def format_result_exp(exp: int) -> str:
    return f"经验：{exp}"


def format_progression_message_gain(unit_name: str, stat_name: str) -> str:
    return f"{unit_name} 的 {stat_name} +1"


def format_progression_message_no_stat_points(unit_name: str) -> str:
    return f"{unit_name} 没有可分配属性点"


def format_progression_message_learn(unit_name: str, skill_name: str) -> str:
    return f"{unit_name} 学会了 {get_skill_name(skill_name)}"


def format_progression_message_cannot_learn(skill_name: str) -> str:
    return f"无法学习 {get_skill_name(skill_name)}"


def format_progression_message_equip(unit_name: str, skill_name: str) -> str:
    return f"{unit_name} 装备了 {get_skill_name(skill_name)}"


def format_progression_message_cannot_equip(skill_name: str) -> str:
    return f"无法装备 {get_skill_name(skill_name)}"


def format_progression_message_item_equip(unit_name: str, equipment_name: str, slot_name: str) -> str:
    return f"{unit_name} 在{slot_name}装备了 {get_equipment_name(equipment_name)}"


def format_progression_message_item_cannot_equip(equipment_name: str) -> str:
    return f"无法装备 {get_equipment_name(equipment_name)}"


def format_progression_message_item_unequip(unit_name: str, slot_name: str) -> str:
    return f"{unit_name} 卸下了{slot_name}装备"


def format_progression_message_item_cannot_unequip(slot_name: str) -> str:
    return f"{slot_name} 当前没有装备可卸下"


def format_equipment_line(slot_name: str, equipment_name: str) -> str:
    return f"{slot_name}: {equipment_name}"


def format_battle_attack(attacker_name: str, defender_name: str, damage: int) -> str:
    return f"{attacker_name} 攻击 {defender_name}，造成 {damage} 点伤害"


def format_battle_defeated(unit_name: str) -> str:
    return f"{unit_name} 被击败"


def format_battle_move(unit_name: str, from_pos: tuple[int, int], to_pos: tuple[int, int]) -> str:
    return f"{unit_name} 移动 {from_pos} -> {to_pos}"


def format_battle_wait(unit_name: str) -> str:
    return f"{unit_name} 待机"


def format_battle_exp(unit_name: str, exp_value: int) -> str:
    return f"{unit_name} 获得 {exp_value} 点经验"


def format_battle_level_up(unit_name: str, level: int) -> str:
    return f"{unit_name} 升到等级 {level}"


def format_battle_shield_absorb(unit_name: str, buff_name: str, absorbed: int) -> str:
    return f"{unit_name} 的 {get_buff_name(buff_name)} 吸收了 {absorbed} 点伤害"


def format_battle_counter(unit_name: str, target_name: str, damage: int) -> str:
    return f"{unit_name} 反击 {target_name}，造成 {damage} 点伤害"


def format_battle_trigger_heal(unit_name: str, heal_value: int, buff_name: str) -> str:
    return f"{unit_name} 通过 {get_buff_name(buff_name)} 恢复 {heal_value} 点生命"


def format_battle_tick_damage(unit_name: str, damage: int, buff_name: str) -> str:
    return f"{unit_name} 因 {get_buff_name(buff_name)} 受到 {damage} 点持续伤害"


def format_battle_tick_heal(unit_name: str, heal_value: int, buff_name: str) -> str:
    return f"{unit_name} 通过 {get_buff_name(buff_name)} 恢复 {heal_value} 点生命"


def format_skill_menu_label(skill_name: str, power: float) -> str:
    return f"{get_skill_name(skill_name)} x{power:.1f}"


def format_skill_use(user_name: str, skill_name: str, target_name: str, value: int) -> str:
    return f"{user_name} 使用 {get_skill_name(skill_name)} 对 {target_name} 造成 {value} 点效果"


