import aiosqlite

DB_PATH = "bratsk_bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # 1. Пользователи (анкеты)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                district TEXT NOT NULL,
                subcultures TEXT,
                photos TEXT,
                description TEXT,
                gender TEXT NOT NULL,
                looking_for TEXT NOT NULL,
                is_approved INTEGER DEFAULT 0,
                is_banned INTEGER DEFAULT 0,
                is_top INTEGER DEFAULT 0,
                top_until TEXT,
                referrer_id INTEGER,
                referral_count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_seen TEXT
            )
        """)
        # 2. Лайки/дизлайки
        await db.execute("""
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id INTEGER NOT NULL,
                to_user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(from_user_id, to_user_id)
            )
        """)
        # 3. Мэтчи
        await db.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER NOT NULL,
                user2_id INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user1_id, user2_id)
            )
        """)
        # 4. Жалобы
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reporter_id INTEGER NOT NULL,
                reported_id INTEGER NOT NULL,
                reason TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(reporter_id, reported_id)
            )
        """)
        # 5. Баны (история)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                admin_id INTEGER NOT NULL,
                reason TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
        print("✅ База данных инициализирована")