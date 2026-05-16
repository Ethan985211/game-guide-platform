"""
补角色脚本 - 为缺少角色的游戏注入角色数据
"""
import sqlite3, os, sys

for p in ['game_guide.db', 'gameguide.db',
          '/data/game-guide-platform/backend/game_guide.db']:
    if os.path.exists(p):
        DB_PATH = p
        break
else:
    print("找不到数据库")
    sys.exit(1)

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

# 游戏名→ID
cur.execute("SELECT id, name FROM games")
name_to_id = {r[1]: r[0] for r in cur.fetchall()}

# 每个游戏现有角色数
cur.execute("SELECT game_id, COUNT(*) FROM characters GROUP BY game_id")
existing = {r[0]: r[1] for r in cur.fetchall()}

print("=== 当前角色分布 ===")
for name, gid in sorted(name_to_id.items(), key=lambda x: x[1]):
    cnt = existing.get(gid, 0)
    flag = " ⚠️" if cnt < 3 else ""
    print(f"  [{gid}] {name}: {cnt}个角色{flag}")

# 需要补充的角色数据
# 格式: (游戏名, 角色名, 稀有度, 元素/职业, 武器/位置, 描述, 图片)
NEW_CHARS = [
    # ===== 原神 (目前5个 → 补到14) =====
    ('原神', '神里绫华', '★★★★★', '冰', '单手剑',
     '社奉行大小姐。元素爆发霜灭造成大范围冰伤，重击手感极佳。冻结队核心主C。', '/images/characters/ayaka.jpg'),
    ('原神', '艾尔海森', '★★★★★', '草', '单手剑',
     '须弥教令院书记官。草元素站场C，棱镜协同攻击伤害可观。不抽专武也能玩。', '/images/characters/alhaitham.jpg'),
    ('原神', '珊瑚宫心海', '★★★★★', '水', '法器',
     '海祇岛现人神巫女。水母持续挂水+群体治疗，冻结队和绽放队的神级辅助。', '/images/characters/kokomi.jpg'),
    ('原神', '提纳里', '★★★★★', '草', '弓',
     '道成林巡林官。蓄力射击追踪箭，蔓激化伤害不俗。常驻池就能出。', '/images/characters/tighnari.jpg'),

    # ===== 王者荣耀 (目前4个 → 8个) =====
    ('王者荣耀', '武则天', '传说', '法师', '中路',
     '唯一女帝，大招全屏眩晕+伤害。需要荣耀水晶兑换。', '/images/characters/wuzetian.jpg'),
    ('王者荣耀', '铠', '史诗', '战士', '对抗路',
     '长城守卫军。开启大招变身铠甲勇士，单挑几乎无敌。', '/images/characters/kai.jpg'),
    ('王者荣耀', '鲁班七号', '史诗', '射手', '发育路',
     '王者峡谷最可爱的小短腿。被动扫射伤害爆表，但也是全峡谷死亡次数最多的英雄。', '/images/characters/luban.jpg'),
    ('王者荣耀', '露娜', '传说', '战士', '打野',
     '月光之女。无限连招的代名词，会玩的露娜一打五不是梦。', '/images/characters/luna.jpg'),

    # ===== 星穹铁道 (目前3个 → 9个) =====
    ('崩坏：星穹铁道', '布洛妮娅', '★★★★★', '风', '同谐',
     '贝洛伯格大守护者。拉条+暴伤BUFF，泛用性极强。', '/images/characters/bronya.jpg'),
    ('崩坏：星穹铁道', '罗刹', '★★★★★', '虚数', '丰饶',
     '棺材板奶爸。自动回血+解控，生存位T0。', '/images/characters/luocha.jpg'),
    ('崩坏：星穹铁道', '藿藿', '★★★★★', '风', '丰饶',
     '十王司小判官。解控+回能，功能性最强的丰饶角色。', '/images/characters/huohuo.jpg'),
    ('崩坏：星穹铁道', '停云', '★★★★', '雷', '同谐',
     '仙舟商人。单体加攻+回能，几乎所有C的完美搭档。', '/images/characters/tingyun.jpg'),
    ('崩坏：星穹铁道', '佩拉', '★★★★', '冰', '虚无',
     '银鬃铁卫副官。全队减防，四星战神，培养成本极低。', '/images/characters/pela.jpg'),
    ('崩坏：星穹铁道', '艾丝妲', '★★★★', '火', '同谐',
     '空间站站长。全队加速+火伤加成，火队核心辅助。', '/images/characters/asta.jpg'),

    # ===== 绝区零 (目前3个 → 6个) =====
    ('绝区零', '苍角', 'A级', '风', '击破',
     '对空六课的沉默巨汉。击破效率高，失衡期能为队伍创造大量输出窗口。', '/images/characters/soukaku.jpg'),
    ('绝区零', '11号', 'S级', '火', '强攻',
     '防卫军的火焰剑士。蓄力火焰斩范围伤害极高，攻坚利器。', '/images/characters/soldier11.jpg'),
    ('绝区零', '比利·奇德', 'A级', '物理', '强攻',
     '狡兔屋的枪手。双枪持续输出，远程安全清杂兵。', '/images/characters/billy.jpg'),

    # ===== 英雄联盟 (目前0个 → 5个) =====
    ('英雄联盟', '亚索', None, None, None,
     '疾风剑豪。全英雄最高登场率（和最高死亡率）。风墙挡技能、EQ闪接大招。', '/images/characters/yasuo.jpg'),
    ('英雄联盟', '劫', None, None, None,
     '影流之主。影子换位+三重手里剑，一套连招秒脆皮。Faker的成名英雄之一。', '/images/characters/zed.jpg'),
    ('英雄联盟', '锤石', None, None, None,
     '魂锁典狱长。Q钩子+W灯笼+E扫+大招囚笼，辅助天花板。', '/images/characters/thresh.jpg'),
    ('英雄联盟', '盲僧', None, None, None,
     '李青。摸眼回旋踢+R闪，打野招牌英雄。', '/images/characters/leesin.jpg'),
    ('英雄联盟', '金克丝', None, None, None,
     '暴走萝莉。火箭炮超远射程+被动跑速，Arcane女主角。', '/images/characters/jinx.jpg'),

    # ===== 黑神话：悟空 (目前0个 → 4个) =====
    ('黑神话：悟空', '天命人', '主角', None, None,
     '沉默的取经人。三种棍势、定身术、身外身法。猴子的每一步成长都是玩家的修行。', '/images/characters/wukong.jpg'),
    ('黑神话：悟空', '二郎神', '隐藏Boss', None, None,
     '三尖两刃刀+天眼+哮天犬。六阶段战斗堪称动作游戏巅峰。', '/images/characters/yangjian.jpg'),
    ('黑神话：悟空', '黄风大圣', 'Boss', None, None,
     '黄风岭的黄毛貂鼠精。漫天风沙中辨不清方向。', '/images/characters/huangfeng.jpg'),
    ('黑神话：悟空', '虎先锋', 'Boss', None, None,
     '血池中蹿出的猛虎。拳拳到肉，新手噩梦。', '/images/characters/huxianfeng.jpg'),

    # ===== 明日方舟 (目前0个 → 6个) =====
    ('明日方舟', '史尔特尔', '★★★★★★', '近卫', None,
     '三技能黄昏毁天灭地，单挑任何Boss。真正的「唯一神」。', '/images/characters/surtr.jpg'),
    ('明日方舟', '玛恩纳', '★★★★★★', '近卫', None,
     '临光家族的骑士。三技能真银斩清屏，改变了高难图的打法。', '/images/characters/mlynar.jpg'),
    ('明日方舟', '浊心斯卡蒂', '★★★★★★', '辅助', None,
     '斯卡蒂异格形态。全队增伤+召唤物阻挡，高难图中几乎必带。', '/images/characters/skadi.jpg'),
    ('明日方舟', '凯尔希', '★★★★★★', '医疗', None,
     '罗德岛医疗主管。Mon3tr真伤+高速治疗，能奶能打能抗的全能选手。', '/images/characters/kaltsit.jpg'),
    ('明日方舟', '伊内丝', '★★★★★★', '先锋', None,
     '前整合运动间谍。快速回费+束缚控制+不错输出，新时代先锋标杆。', '/images/characters/ines.jpg'),
    ('明日方舟', '缄默德克萨斯', '★★★★★★', '特种', None,
     '企鹅物流员工异格。快速复活+大范围眩晕，战术价值极高。', '/images/characters/texas.jpg'),

    # ===== 鸣潮 =====
    ('鸣潮', '忌炎', 'S级', '冰', '大剑',
     '开服最强主C。蓄力重击伤害惊人，冰队绝对核心。', '/images/characters/jiyan.jpg'),
    ('鸣潮', '吟霖', 'S级', '雷', '法器',
     '后台雷伤+全队增伤。与卡卡罗组成雷队双核。', '/images/characters/yinlin.jpg'),
    ('鸣潮', '卡卡罗', 'S级', '雷', '单手剑',
     '雷系主C，大招期间输出爆表。', '/images/characters/calcharo.jpg'),
    ('鸣潮', '鉴心', 'S级', '风', '拳套',
     '风系全能，聚怪+减抗+治疗三合一。', '/images/characters/jianxin.jpg'),
    ('鸣潮', '秧秧', 'A级', '水', '法器',
     '免费奶妈，后台持续回血，开荒必练。', '/images/characters/yanyan.jpg'),

    # ===== 幻塔 =====
    ('幻塔', '凌寒', 'SSR', '冰', '大剑',
     '3.0冰系天花板。剑气连斩伤害爆炸。', '/images/characters/linghan.jpg'),
    ('幻塔', '菲欧娜', 'SSR', '物理', '双枪',
     '物理C顶点。高速射击+穿透伤害，大世界效率第一。', '/images/characters/fiona.jpg'),
    ('幻塔', '榴火', 'SSR', '火', '镰刀',
     '火系群伤之王。AOE能力冠绝全角色。', '/images/characters/liuhuo.jpg'),

    # ===== 崩坏3 =====
    ('崩坏3', '琪亚娜·卡斯兰娜', 'S级', '生物', '双枪',
     '终焉之律者·薪炎。从废柴大小姐到拯救世界的战士。', '/images/characters/kiana.jpg'),
    ('崩坏3', '雷电芽衣', 'S级', '异能', '太刀',
     '始源之律者。雷之律者形态，雷电女王的真正力量。', '/images/characters/mei.jpg'),
    ('崩坏3', '布洛妮娅·扎伊切克', 'S级', '机械', '重炮',
     '真理之律者。从冰冷杀手到温暖的同伴。', '/images/characters/bronya_hi3.jpg'),
    ('崩坏3', '希儿', 'S级', '量子', '镰刀',
     '死生之律者。量子之海中的蝶，死与生的界限。', '/images/characters/seele.jpg'),

    # ===== 永劫无间 =====
    ('永劫无间', '季沧海', None, None, None,
     '火球消耗+爆发型英雄。F技能震地+大招天火，单排上分利器。', '/images/characters/jicanghai.jpg'),
    ('永劫无间', '迦南', None, None, None,
     '隐身刺客。F技能瞬移+大招隐身领域，拉扯天花板。', '/images/characters/jianan.jpg'),
    ('永劫无间', '天海', None, None, None,
     '金钟罩+大佛变身。六臂金刚毁天灭地，三排中的开团机器。', '/images/characters/tianhai.jpg'),

    # ===== 三角洲行动 =====
    ('三角洲行动', '凯·莫雷诺', None, '突击兵', None,
     '前三角洲队员。钩索+滑铲高速机动，近距离交战专家。', '/images/characters/kai.jpg'),
    ('三角洲行动', '维克拉姆', None, '狙击手', None,
     '远程侦察兵。无人机标记+远距离狙击，团队的眼睛。', '/images/characters/vikram.jpg'),
    ('三角洲行动', '露娜', None, '医疗兵', None,
     '战场救护。治疗手枪可以远程救治倒地队友，生存率大增。', '/images/characters/luna_df.jpg'),

    # ===== DNF手游 =====
    ('地下城与勇士：起源', '鬼剑士', None, None, None,
     '最经典的初始职业。可选择转职为狂战士、剑魂、鬼泣、阿修罗。', '/images/characters/slayer.jpg'),
    ('地下城与勇士：起源', '格斗家', None, None, None,
     '近身格斗的王者。转职选择：散打、气功师、街霸、柔道家。', '/images/characters/fighter.jpg'),
    ('地下城与勇士：起源', '神枪手', None, None, None,
     '远程火力压制。转职选择：漫游枪手、枪炮师、机械师、弹药专家。', '/images/characters/gunner.jpg'),

    # ===== 碧蓝航线 =====
    ('碧蓝航线', '企业', 'SSR', '航母', None,
     '开服战神。技能触发后伤害翻倍，至今仍是最强航母之一。', '/images/characters/enterprise.jpg'),
    ('碧蓝航线', '胡德', 'SSR', '战列', None,
     '皇家海军的荣耀。弹幕覆盖全场，推图利器。', '/images/characters/hood.jpg'),
    ('碧蓝航线', '海伦娜', 'SSR', '轻巡', None,
     '雷达扫描增伤40%，永远的神。', '/images/characters/helena.jpg'),

    # ===== 少女前线2 =====
    ('少女前线2：追放', '桑朵莱希', 'SSR', '动能', None,
     '单点爆发主C。技能连发伤害惊人。', '/images/characters/sandolexi.jpg'),
    ('少女前线2：追放', '寇尔芙', 'SSR', '爆破', None,
     'AOE清杂专家。无人机轰炸范围伤害。', '/images/characters/colphne.jpg'),
    ('少女前线2：追放', '奇塔', 'SR', '轻型', None,
     '行动点回复辅助。让队友多动一回合的含金量。', '/images/characters/cheeta.jpg'),

    # ===== 艾尔登法环 =====
    ('艾尔登法环', '玛莲妮亚', '半神', None, None,
     '米凯拉的锋刃，女武神。水鸟乱舞秒杀一切，让无数褪色者砸手柄。', '/images/characters/malenia.jpg'),
    ('艾尔登法环', '拉塔恩', '半神', None, None,
     '碎星将军。骑着小马抡双刀，陨石砸地全屏秒杀。', '/images/characters/radahn.jpg'),
    ('艾尔登法环', '菈妮', '半神', None, None,
     '魔女菈妮。群星结局的关键NPC，玩家心中人气最高的角色。', '/images/characters/ranni.jpg'),

    # ===== 赛博朋克2077 =====
    ('赛博朋克2077', 'V', '佣兵', None, None,
     '夜之城最传奇的雇佣兵。从街头小混混到荒坂塔袭击者。', '/images/characters/v.jpg'),
    ('赛博朋克2077', '强尼·银手', '传奇', None, None,
     '武侍乐队主唱。2023年炸了荒坂塔的摇滚恐怖分子。', '/images/characters/johnny.jpg'),
    ('赛博朋克2077', '朱迪·阿尔瓦雷兹', None, None, None,
     '超梦编辑专家。夜之城最暖心的存在之一。', '/images/characters/judy.jpg'),

    # ===== 塞尔达传说 =====
    ('塞尔达传说：王国之泪', '林克', '勇者', None, None,
     '海拉鲁的剑士。究极手+通天术+余料建造，创造力即战斗力。', '/images/characters/link.jpg'),
    ('塞尔达传说：王国之泪', '塞尔达', '公主', None, None,
     '海拉鲁王国的公主。穿越时空的光之力量继承者。', '/images/characters/zelda.jpg'),
    ('塞尔达传说：王国之泪', '盖侬多夫', '魔王', None, None,
     '格鲁德族的王。瘴气之力腐化海拉鲁的源头。', '/images/characters/ganondorf.jpg'),

    # ===== 最终幻想VII =====
    ('最终幻想VII 重生', '克劳德·斯特莱夫', '主角', None, None,
     '前神罗战士。破坏剑的继承者，记忆与身份的追寻者。', '/images/characters/cloud.jpg'),
    ('最终幻想VII 重生', '蒂法·洛克哈特', None, None, None,
     '雪崩组织成员。拳法格斗家，第七天堂酒吧老板娘。', '/images/characters/tifa.jpg'),
    ('最终幻想VII 重生', '萨菲罗斯', 'Boss', None, None,
     '片翼天使。史上最具魅力的反派之一。', '/images/characters/sephiroth.jpg'),

    # ===== GTA6 =====
    ('侠盗猎车手VI', '露西亚', '主角', None, None,
     'GTA系列首个女性主角。与杰森组成雌雄大盗，搅翻罪恶都市。', '/images/characters/lucia.jpg'),
    ('侠盗猎车手VI', '杰森', '主角', None, None,
     '露西亚的搭档。两人之间的化学反应是剧情核心。', '/images/characters/jason.jpg'),

    # ===== 怪物猎人：荒野 =====
    ('怪物猎人：荒野', '辟兽', '大型怪物', None, None,
     '群居牙兽种。领袖「辟兽王」体型巨大，擅长冲撞和甩尾。', '/images/characters/doshaguma.jpg'),
    ('怪物猎人：荒野', '炎尾龙', '大型怪物', None, None,
     '飞龙种。尾部火焰攻击，新爆破属性异常。', '/images/characters/yanweilong.jpg'),
    ('怪物猎人：荒野', '缠蛙', '大型怪物', None, None,
     '两生种。舌头束缚攻击，水域附近尤为危险。', '/images/characters/chanwa.jpg'),

    # ===== 死亡搁浅2 =====
    ('死亡搁浅2：海滩之上', '山姆·波特', '主角', None, None,
     '传奇快递员回归。用绳索和连接让分裂的世界重新联结。', '/images/characters/sam.jpg'),
    ('死亡搁浅2：海滩之上', '翡若捷', None, None, None,
     '艾丽·范宁饰演的神秘角色。与山姆的互动是故事核心。', '/images/characters/fragile.jpg'),

    # ===== 文明VII =====
    ('文明VII', '凯撒', '领袖', None, None,
     '罗马的独裁官。在VII中系统大幅革新，凯撒不再绑定单一文明。', '/images/characters/caesar.jpg'),
    ('文明VII', '克利奥帕特拉', '领袖', None, None,
     '埃及的最后法老。文化融合机制让她可以兼收希腊和罗马的优势。', '/images/characters/cleopatra.jpg'),
    ('文明VII', '孔子', '领袖', None, None,
     '首次加入中国哲学领袖。文化传播+科技研究双加成。', '/images/characters/confucius.jpg'),
]

# 执行
added = 0
now_str = __import__('datetime').datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
for game_name, name, rarity, element, weapon, desc, image in NEW_CHARS:
    gid = name_to_id.get(game_name)
    if not gid:
        print(f"  未找到游戏: {game_name}")
        continue
    # 检查是否已存在同名角色
    cur.execute("SELECT id FROM characters WHERE game_id=? AND name=?", (gid, name))
    if cur.fetchone():
        continue
    cur.execute("""
        INSERT INTO characters (game_id, name, rarity, element, weapon_type, description, image, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (gid, name, rarity, element, weapon, desc, image, now_str))
    added += 1

conn.commit()

# 最终统计
cur.execute("SELECT COUNT(*) FROM characters")
total = cur.fetchone()[0]
print(f"\n本次新增角色: {added}")
print(f"角色总数: {total}")

# 按游戏分布
cur.execute("""
    SELECT g.name, COUNT(c.id)
    FROM games g LEFT JOIN characters c ON g.id=c.game_id
    GROUP BY g.id ORDER BY g.id
""")
for name, cnt in cur.fetchall():
    print(f"  {name}: {cnt}个角色")

conn.close()
print("\n完成!")
