"""
游戏种子数据 - 7款热门游戏
运行方式: cd backend && python3 ../scripts/seed_games.py
"""
import sys
sys.path.insert(0, '/data/game-guide-platform/backend')
from app.database import SessionLocal, engine, Base
from app.models import Game
from datetime import datetime

# 确保表已创建
Base.metadata.create_all(bind=engine)

games = [
    {
        "name": "原神",
        "slug": "genshin-impact",
        "description": "《原神》是由米哈游开发的开放世界冒险RPG。探索七大元素交汇的「提瓦特」大陆，扮演旅行者与伙伴们一同冒险。精美的二次元画面、深度的元素反应战斗系统、持续更新的剧情与地图，使其成为全球现象级游戏。",
        "category": "RPG",
        "developer": "米哈游",
        "publisher": "米哈游",
        "cover_image": "https://fastcdn.hoyoverse.com/mi18n/hk4e/global/website/static/key-visual.jpg",
        "release_date": "2020-09-28",
    },
    {
        "name": "王者荣耀",
        "slug": "honor-of-kings",
        "description": "《王者荣耀》是中国最受欢迎的MOBA手游，日活用户过亿。5v5经典对战、百余位英雄、丰富的皮肤系统。从青铜到王者，每一局都是全新的竞技体验。职业联赛KPL更是中国电竞的顶级赛事。",
        "category": "MOBA",
        "developer": "腾讯天美工作室",
        "publisher": "腾讯游戏",
        "cover_image": "https://www.honorofkings.com/img/share.jpg",
        "release_date": "2015-11-26",
    },
    {
        "name": "崩坏：星穹铁道",
        "slug": "honkai-star-rail",
        "description": "《崩坏：星穹铁道》是米哈游打造的银河冒险RPG。乘坐星穹列车穿越星际，探索各具特色的星球文明。创新性的回合制战斗系统、电影级的剧情演出和角色塑造，荣获2023年TGA最佳手游奖。",
        "category": "RPG",
        "developer": "米哈游",
        "publisher": "米哈游",
        "cover_image": "https://cdn.cloudflare.steamstatic.com/steam/apps/1905820/library_600x900.jpg",
        "release_date": "2023-04-26",
    },
    {
        "name": "绝区零",
        "slug": "zenless-zone-zero",
        "description": "《绝区零》是米哈游推出的都市幻想ARPG。扮演「绳匠」带领代理人在空洞灾害中求生。独特街头艺术风格、爽快连招战斗系统、潮流角色设计，为动作游戏注入全新活力。",
        "category": "ARPG",
        "developer": "米哈游",
        "publisher": "米哈游",
        "cover_image": "https://cdn.cloudflare.steamstatic.com/steam/apps/4162040/header.jpg",
        "release_date": "2024-07-04",
    },
    {
        "name": "英雄联盟",
        "slug": "league-of-legends",
        "description": "《英雄联盟》是全球最受欢迎的PC竞技网游，由Riot Games开发。超过160位英雄选择，5v5召唤师峡谷对战。全球总决赛每年吸引数亿观众，是电子竞技的旗帜性游戏。",
        "category": "MOBA",
        "developer": "Riot Games",
        "publisher": "腾讯游戏",
        "cover_image": "https://cdn.cloudflare.steamstatic.com/steam/apps/20590/header.jpg",
        "release_date": "2011-09-22",
    },
    {
        "name": "黑神话：悟空",
        "slug": "black-myth-wukong",
        "description": "《黑神话：悟空》是游戏科学打造的中国首款3A大作。改编自《西游记》，以UE5引擎呈现震撼的东方神话世界。2024年8月发售即引爆全球，Steam同时在线峰值超240万。",
        "category": "ARPG",
        "developer": "游戏科学",
        "publisher": "游戏科学",
        "cover_image": "https://cdn.cloudflare.steamstatic.com/steam/apps/2358720/library_600x900.jpg",
        "release_date": "2024-08-20",
    },
    {
        "name": "明日方舟",
        "slug": "arknights",
        "description": "《明日方舟》是鹰角网络开发的策略塔防手游。扮演罗德岛博士，招募各具特色的干员对抗矿石病。独特美术风格、丰富世界观设定、极具策略深度的关卡设计，赢得广泛好评。",
        "category": "塔防",
        "developer": "鹰角网络",
        "publisher": "鹰角网络",
        "cover_image": "https://webusstatic.yo-star.com/arknights-us/arknights-us-website/main/h5/ogp.png",
        "release_date": "2019-05-01",
    },
]

db = SessionLocal()
try:
    db.query(Game).delete()
    for g in games:
        game = Game(**g)
        db.add(game)
    db.commit()
    print(f"Inserted {len(games)} games successfully")
    
    for g in db.query(Game).all():
        print(f"  [{g.id}] {g.name} ({g.category})")
except Exception as e:
    db.rollback()
    print(f"ERROR: {e}")
finally:
    db.close()
