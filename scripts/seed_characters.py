import sys
sys.path.insert(0, '/data/game-guide-platform/backend')
from app.database import SessionLocal
from app.models import Character
import json

characters_json = '''[{"game_id": 1, "name": "钟离", "rarity": "★★★★★", "element": "岩", "weapon_type": "长柄武器", "description": "「往生堂」的客卿，通晓古今的博学者。岩王帝君的凡人化身，举手投足间尽显威严与优雅。其护盾能力堪称游戏最强。", "image": "https://uploadstatic.mihoyo.com/contentweb/20210220/2021022019293796818.png"}, {"game_id": 1, "name": "雷电将军", "rarity": "★★★★★", "element": "雷", "weapon_type": "长柄武器", "description": "稻妻的统治者，永恒之神。以「无想的一刀」威震天下，元素爆发可为全队充能。", "image": "https://uploadstatic.mihoyo.com/contentweb/20210826/2021082617531051804.png"}, {"game_id": 1, "name": "胡桃", "rarity": "★★★★★", "element": "火", "weapon_type": "长柄武器", "description": "「往生堂」第七十七代堂主，掌管葬仪事务的少女。以生命换取极高火伤输出。", "image": "https://uploadstatic.mihoyo.com/contentweb/20210302/2021030211292639722.png"}, {"game_id": 1, "name": "纳西妲", "rarity": "★★★★★", "element": "草", "weapon_type": "法器", "description": "须弥的草神，智慧之主。元素战技可标记敌人实现连锁反应。", "image": "https://uploadstatic.mihoyo.com/contentweb/20221102/2022110208532665400.png"}, {"game_id": 1, "name": "芙宁娜", "rarity": "★★★★★", "element": "水", "weapon_type": "单手剑", "description": "枫丹的水神，舞台上的闪耀明星，法庭上的威严裁决者。能切换荒芒双形态。", "image": "https://uploadstatic.mihoyo.com/contentweb/20231108/2023110811030118269.png"}, {"game_id": 2, "name": "李白", "rarity": "传说", "element": "刺客", "weapon_type": "剑", "description": "王者峡谷最飘逸的剑客。三段位移搭配不可选中大招，是无数玩家的信仰英雄。", "image": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/131/131.jpg"}, {"game_id": 2, "name": "武则天", "rarity": "荣耀典藏", "element": "法师", "weapon_type": "权杖", "description": "中国历史上唯一的女皇帝，在峡谷中以全图大招威慑四方。", "image": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/136/136.jpg"}, {"game_id": 2, "name": "鲁班七号", "rarity": "勇者", "element": "射手", "weapon_type": "机关炮", "description": "鲁班大师创造的机关人，峡谷新手最爱射手。被动扫射让敌人闻风丧胆。", "image": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/112/112.jpg"}, {"game_id": 2, "name": "铠", "rarity": "史诗", "element": "战士", "weapon_type": "刀", "description": "长城守卫军的战士，以「不灭魔躯」大招化身铠甲勇士。单挑能力极强。", "image": "https://game.gtimg.cn/images/yxzj/img201606/heroimg/193/193.jpg"}, {"game_id": 3, "name": "景元", "rarity": "★★★★★", "element": "雷", "weapon_type": "智识", "description": "仙舟罗浮的将军，运筹帷幄的智者。召唤神君斩星一击灭敌。", "image": "https://uploadstatic.mihoyo.com/sr/20230517/20230517114933_884431570793.png"}, {"game_id": 3, "name": "卡芙卡", "rarity": "★★★★★", "element": "雷", "weapon_type": "虚无", "description": "星核猎手的核心成员，以言灵术操控敌人。持续伤害体系的核心发动机。", "image": "https://uploadstatic.mihoyo.com/sr/20230809/20230809103148_436816787777.png"}, {"game_id": 3, "name": "丹恒·饮月", "rarity": "★★★★★", "element": "虚数", "weapon_type": "毁灭", "description": "丹恒隐藏的真正形态，罗浮持明龙尊转世。强化普攻造成毁灭性伤害。", "image": "https://uploadstatic.mihoyo.com/sr/20230830/20230830145725_684175935426.png"}, {"game_id": 4, "name": "妮可", "rarity": "S", "element": "物理", "weapon_type": "手枪", "description": "狡兔屋的老大，精明能干的代理人。使用双枪远程输出。", "image": "https://act-webstatic.mihoyo.com/zzz/20240628-183224/upload/fc7db236b3a5f1cc8a8e2b04a3f2c7f7.png"}, {"game_id": 4, "name": "安比", "rarity": "A", "element": "电", "weapon_type": "单手剑", "description": "狡兔屋的沉默剑士，使用电系单手剑快速斩击。", "image": "https://act-webstatic.mihoyo.com/zzz/20240628-183224/upload/df0d510f89c431f2ee37e142a87f30e4.png"}, {"game_id": 4, "name": "艾莲", "rarity": "S", "element": "冰", "weapon_type": "大剑", "description": "维多利亚家政的冰山美人，冰系大剑高爆发输出。", "image": "https://act-webstatic.mihoyo.com/zzz/20240628-183224/upload/5a4e4b2a6c8f7e8c1d4e5f6a7b8c9d0e.png"}, {"game_id": 5, "name": "亚索", "rarity": "450", "element": "战士/刺客", "weapon_type": "武士刀", "description": "疾风剑豪，以「死亡如风常伴吾身」闻名，高操作上限的战场收割机。", "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Yasuo_0.jpg"}, {"game_id": 5, "name": "阿狸", "rarity": "4800", "element": "法师/刺客", "weapon_type": "魔法宝珠", "description": "九尾妖狐，灵活的机动性与真实伤害让她始终是中路热门。", "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ahri_0.jpg"}, {"game_id": 5, "name": "金克丝", "rarity": "4800", "element": "射手", "weapon_type": "机关枪/火箭筒", "description": "暴走萝莉，切换武器在机枪扫射与火箭轰炸间自由变化。", "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Jinx_0.jpg"}, {"game_id": 6, "name": "天命人", "rarity": "主角", "element": "无", "weapon_type": "如意棒", "description": "玩家扮演的孙悟空继承者，掌握七十二变、定身术等神通。", "image": "https://shared.static.heishenhua.com/characters/destined_one.png"}, {"game_id": 6, "name": "猪八戒", "rarity": "伙伴", "element": "无", "weapon_type": "九齿钉耙", "description": "原天蓬元帅，看似懒散贪吃实则战力惊人，亦敌亦友。", "image": "https://shared.static.heishenhua.com/characters/zhu_bajie.png"}, {"game_id": 6, "name": "二郎神", "rarity": "BOSS", "element": "无", "weapon_type": "三尖两刃刀", "description": "天庭第一战神，开场与天命人的对决成为最具话题性的战斗。", "image": "https://shared.static.heishenhua.com/characters/erlang_shen.png"}, {"game_id": 7, "name": "阿米娅", "rarity": "★★★★★", "element": "术师/近卫", "weapon_type": "源石技艺", "description": "罗德岛公开的领袖，拥有双形态切换能力守护感染者未来。", "image": "https://media.prts.wiki/images/char_002_amiya_1.png"}, {"game_id": 7, "name": "银灰", "rarity": "★★★★★★", "element": "近卫", "weapon_type": "单手剑", "description": "谢拉格军阀，以真银斩闻名，开服三幻神之一。", "image": "https://media.prts.wiki/images/char_106_silverash_1.png"}, {"game_id": 7, "name": "能天使", "rarity": "★★★★★★", "element": "狙击", "weapon_type": "冲锋枪", "description": "企鹅物流快递员，极速射击型狙击，速狙体系核心。", "image": "https://media.prts.wiki/images/char_103_angel_1.png"}]'''
characters = json.loads(characters_json)

db = SessionLocal()
try:
    db.query(Character).delete()
    count = 0
    for char_data in characters:
        char = Character(**char_data)
        db.add(char)
        count += 1
    db.commit()
    print(f'Inserted {count} characters successfully')
    print()
    for gid in range(1, 8):
        chars = db.query(Character).filter(Character.game_id == gid).all()
        if chars:
            gname = chars[0].game.name
            names = [c.name for c in chars]
            print(f'  {gname}: {len(chars)} chars - {", ".join(names)}')
except Exception as e:
    db.rollback()
    import traceback
    print(f'ERROR: {e}')
    traceback.print_exc()
finally:
    db.close()