CREATE TABLE IF NOT EXISTS counters (key TEXT PRIMARY KEY, value INTEGER NOT NULL DEFAULT 0);
INSERT OR IGNORE INTO counters(key,value) VALUES ('visits',0);
CREATE TABLE IF NOT EXISTS visitor_days (token_hash TEXT NOT NULL, day TEXT NOT NULL, PRIMARY KEY(token_hash,day));
CREATE TABLE IF NOT EXISTS posts (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nickname TEXT NOT NULL,
 message TEXT NOT NULL,
 parent_id INTEGER,
 created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
 hidden INTEGER NOT NULL DEFAULT 0,
 FOREIGN KEY(parent_id) REFERENCES posts(id)
);
CREATE INDEX IF NOT EXISTS idx_posts_visible ON posts(hidden,id DESC);
CREATE TABLE IF NOT EXISTS post_limits (token_hash TEXT PRIMARY KEY, last_post_ms INTEGER NOT NULL);
