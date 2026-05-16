"""
数据库迁移脚本
用于添加邮箱验证相关字段到现有数据库
"""
import sqlite3
import os

def migrate_database():
    db_path = "gameguide.db"
    if not os.path.exists(db_path):
        db_path = "game_guide.db"

    if not os.path.exists(db_path):
        print("数据库文件不存在，请先运行后端创建数据库")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 检查是否已存在 is_verified 列
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    migrations = []

    if "is_verified" not in columns:
        migrations.append("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT 0")

    if "verification_code" not in columns:
        migrations.append("ALTER TABLE users ADD COLUMN verification_code VARCHAR(6)")

    if "verification_expires" not in columns:
        migrations.append("ALTER TABLE users ADD COLUMN verification_expires TIMESTAMP")

    # ============ games 表迁移 ============
    cursor.execute("PRAGMA table_info(games)")
    game_columns = [column[1] for column in cursor.fetchall()]

    if "views" not in game_columns:
        migrations.append("ALTER TABLE games ADD COLUMN views INTEGER DEFAULT 0")

    # ============ page_views 表迁移 ============
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='page_views'")
    if not cursor.fetchone():
        migrations.append("""
            CREATE TABLE page_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path VARCHAR(500),
                referrer VARCHAR(500),
                user_agent VARCHAR(500),
                ip_hash VARCHAR(64),
                session_id VARCHAR(64),
                content_type VARCHAR(50),
                content_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # 创建索引
        migrations.append("CREATE INDEX idx_page_views_path ON page_views(path)")
        migrations.append("CREATE INDEX idx_page_views_session ON page_views(session_id)")
        migrations.append("CREATE INDEX idx_page_views_created ON page_views(created_at)")
    else:
        # 检查并添加缺失的列
        cursor.execute("PRAGMA table_info(page_views)")
        pv_columns = [column[1] for column in cursor.fetchall()]
        
        if "content_type" not in pv_columns:
            migrations.append("ALTER TABLE page_views ADD COLUMN content_type VARCHAR(50)")
        if "content_id" not in pv_columns:
            migrations.append("ALTER TABLE page_views ADD COLUMN content_id INTEGER")
        if "session_id" not in pv_columns:
            migrations.append("ALTER TABLE page_views ADD COLUMN session_id VARCHAR(64)")

    for migration in migrations:
        try:
            cursor.execute(migration)
            print(f"执行: {migration[:100]}...")
        except Exception as e:
            print(f"跳过: {e}")

    conn.commit()
    conn.close()

    if migrations:
        print("数据库迁移完成！")
    else:
        print("数据库已是最新版本，无需迁移")

if __name__ == "__main__":
    migrate_database()
