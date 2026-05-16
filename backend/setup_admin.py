"""
初始化管理员账号脚本
运行此脚本创建管理员用户（存储在数据库中）
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal, engine, Base
from app.models import User, AdminUser
from app.auth import get_password_hash, create_admin_in_db

def create_admin_user():
    # 确保数据库表已创建
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # 从环境变量获取管理员账号密码
        admin_username = os.getenv("ADMIN_USERNAME", "Ethangamehub")
        admin_password = os.getenv("ADMIN_PASSWORD", "jxh2917834376")

        # 在 admin_users 表中创建管理员
        success = create_admin_in_db(admin_username, admin_password, db)
        
        if success:
            print(f"[OK] Admin account created in database!")
            print(f"   Username: {admin_username}")
            print(f"   Password: {admin_password}")
        else:
            print(f"[INFO] Admin user '{admin_username}' already exists")
            # 更新密码
            admin = db.query(AdminUser).filter(AdminUser.username == admin_username).first()
            if admin:
                admin.password_hash = get_password_hash(admin_password)
                db.commit()
                print(f"[OK] Admin password updated!")
        
        print(f"\nPlease visit http://localhost:5173/admin/login to login")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to create admin: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
