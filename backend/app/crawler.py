"""
游戏攻略聚合平台 - 爬虫模块 v2.1
可靠数据源：Steam Store API (游戏信息) + Steam RSS Feed (新闻文章)
"""
import httpx
import time
import re
import logging
import random
import xml.etree.ElementTree as ET
from typing import Optional
from bs4 import BeautifulSoup

logger = logging.getLogger("crawler")

STEAM_APP_IDS = {
    4: 4162040, 6: 2358720, 9: 2064650, 10: 2501360,
    11: 1203220, 12: 3227100, 16: 1245620, 17: 1091500,
    19: 2909400, 21: 2246340, 23: 289070, 24: 648800,
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
]

def rand_ua() -> str:
    return random.choice(USER_AGENTS)


class SteamAPI:
    BASE = "https://store.steampowered.com/api"

    @staticmethod
    def get_app_details(appid: int, lang: str = "zh") -> Optional[dict]:
        for lang_try in [lang, "en"]:
            url = f"{SteamAPI.BASE}/appdetails?appids={appid}&l={lang_try}"
            try:
                resp = httpx.get(url, headers={"User-Agent": rand_ua()}, timeout=15)
                resp.raise_for_status()
                data = resp.json()
                app_data = data.get(str(appid), {})
                if app_data.get("success") and app_data.get("data"):
                    return app_data["data"]
            except Exception as e:
                logger.warning(f"Steam appdetails({appid}): {e}")
            time.sleep(1.5)
        return None

    @staticmethod
    def get_news_rss(appid: int) -> list[dict]:
        """从 Steam RSS feed 获取新闻"""
        url = f"https://store.steampowered.com/feeds/news/app/{appid}/"
        try:
            resp = httpx.get(url, headers={
                "User-Agent": rand_ua(),
                "Accept": "application/rss+xml, application/xml, text/xml"
            }, timeout=15)
            resp.raise_for_status()

            # Parse RSS XML
            root = ET.fromstring(resp.text)
            items = []
            for item in root.findall(".//item")[:5]:
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                desc = item.findtext("description", "")
                pubdate = item.findtext("pubDate", "")

                if title:
                    items.append({
                        "title": title.strip(),
                        "url": link.strip() if link else "",
                        "description": desc.strip() if desc else "",
                        "pubdate": pubdate.strip() if pubdate else "",
                    })
            return items
        except Exception as e:
            logger.warning(f"Steam RSS({appid}): {e}")
        return []


def clean_html(html: str, max_len: int = 3000) -> str:
    if not html:
        return ""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header", "img"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)[:max_len]


def update_game_from_steam(db, game_id: int) -> bool:
    from .models import Game

    appid = STEAM_APP_IDS.get(game_id)
    if not appid:
        return False

    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return False

    data = SteamAPI.get_app_details(appid, lang="zh")
    if not data:
        return False

    updated = False
    zh_desc = data.get("detailed_description") or data.get("short_description") or ""
    if zh_desc:
        cleaned = clean_html(zh_desc, max_len=3000)
        if len(cleaned) > len(game.description or "") + 10:  # 10 char margin
            game.description = cleaned
            updated = True

    header_img = data.get("header_image") or ""
    if header_img and not game.cover_image:
        game.cover_image = header_img
        updated = True

    devs = data.get("developers", [])
    pubs = data.get("publishers", [])
    if devs and not game.developer:
        game.developer = devs[0]
        updated = True
    if pubs and not game.publisher:
        game.publisher = pubs[0]
        updated = True

    if updated:
        db.commit()
        logger.info(f"Steam更新: [{game_id}] {game.name} desc={len(game.description or '')}c")

    return updated


def pull_steam_rss_articles(db, author_id: int = 1) -> int:
    """从 Steam RSS 新闻 -> 文章"""
    from .models import Game, Article
    import uuid

    total = 0
    for game_id, appid in STEAM_APP_IDS.items():
        game = db.query(Game).filter(Game.id == game_id).first()
        if not game:
            continue

        logger.info(f"RSS: [{game_id}] {game.name}")
        items = SteamAPI.get_news_rss(appid)
        created = 0

        for item in items:
            title = item["title"]
            if len(title) < 5:
                continue

            existing = db.query(Article).filter(Article.title == title).first()
            if existing:
                continue

            content = clean_html(item.get("description", ""), max_len=2000) or title

            slug = re.sub(r'[^\w\u4e00-\u9fff-]', '', title)[:60]
            slug = f"rss-{slug}-{uuid.uuid4().hex[:6]}"

            article = Article(
                title=title,
                slug=slug,
                content=content,
                game_id=game_id,
                author_id=author_id,
                category="news",
                tags="Steam新闻,RSS",
                is_published=True,
                views=0, likes=0,
            )
            db.add(article)
            created += 1
            total += 1

        if created:
            db.commit()
            logger.info(f"  -> {created} 篇")
        time.sleep(2)

    return total


def crawl_all(db, author_id: int = 1) -> dict:
    logger.info("[1/2] Steam 游戏信息")
    sr = {"updated": [], "skipped": [], "failed": []}
    for gid in STEAM_APP_IDS:
        try:
            if update_game_from_steam(db, gid):
                sr["updated"].append(gid)
            else:
                sr["skipped"].append(gid)
            time.sleep(1.5)
        except Exception as e:
            logger.error(f"[{gid}] 异常: {e}")
            sr["failed"].append(gid)

    time.sleep(2)
    logger.info("[2/2] Steam RSS 新闻")
    news = pull_steam_rss_articles(db, author_id)

    logger.info(f"完成: 游戏更新={len(sr['updated'])} 新闻={news}")
    return {"steam_updated": sr["updated"], "news_articles": news}


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        r = crawl_all(db)
        print(f"\nDone: Steam={len(r['steam_updated'])} News={r['news_articles']}")
    finally:
        db.close()
