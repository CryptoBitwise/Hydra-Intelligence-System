import aiosqlite
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path


class Storage:
    """Simple SQLite storage with zero-setup.

    Tables:
      - intelligence(head, competitor, discovery, threat_level, confidence, timestamp, data, recommended_action)
    """

    def __init__(self, db_path: str | Path = "hydra.db") -> None:
        self.db_path = str(db_path)

    async def init(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS intelligence (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  head TEXT NOT NULL,
                  competitor TEXT NOT NULL,
                  discovery TEXT NOT NULL,
                  threat_level TEXT NOT NULL,
                  confidence REAL NOT NULL,
                  timestamp TEXT NOT NULL,
                  data TEXT,
                  recommended_action TEXT
                )
                """
            )
            await db.commit()

    async def save_intelligence(self, record: Dict[str, Any]) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                INSERT INTO intelligence (head, competitor, discovery, threat_level, confidence, timestamp, data, recommended_action)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.get("head"),
                    record.get("competitor"),
                    record.get("discovery"),
                    record.get("threat_level"),
                    float(record.get("confidence", 0)),
                    record.get("timestamp"),
                    record.get("data"),
                    record.get("recommended_action"),
                ),
            )
            await db.commit()
            return cursor.lastrowid or 0

    async def recent_intelligence(self, limit: int = 50) -> List[Tuple]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT id, head, competitor, discovery, threat_level, confidence, timestamp, recommended_action FROM intelligence ORDER BY id DESC LIMIT ?",
                (limit,),
            ) as cursor:
                return await cursor.fetchall()

