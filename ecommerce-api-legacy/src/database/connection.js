const sqlite3 = require('sqlite3').verbose();

let dbInstance = null;
let initPromise = null;

function getDb() {
    if (!dbInstance) {
        dbInstance = new sqlite3.Database(':memory:');
    }
    return dbInstance;
}

function dbRun(sql, params = []) {
    const db = getDb();
    return new Promise((resolve, reject) => {
        db.run(sql, params, function (err) {
            if (err) return reject(err);
            resolve({ lastID: this.lastID, changes: this.changes });
        });
    });
}

function dbGet(sql, params = []) {
    const db = getDb();
    return new Promise((resolve, reject) => {
        db.get(sql, params, (err, row) => {
            if (err) return reject(err);
            resolve(row);
        });
    });
}

function dbAll(sql, params = []) {
    const db = getDb();
    return new Promise((resolve, reject) => {
        db.all(sql, params, (err, rows) => {
            if (err) return reject(err);
            resolve(rows || []);
        });
    });
}

function initDb() {
    if (!initPromise) {
        initPromise = (async () => {
            await dbRun("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, pass TEXT)");
            await dbRun("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, price REAL, active INTEGER)");
            await dbRun("CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, course_id INTEGER)");
            await dbRun("CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY AUTOINCREMENT, enrollment_id INTEGER, amount REAL, status TEXT)");
            await dbRun("CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, created_at DATETIME)");

            const userCountRow = await dbGet("SELECT COUNT(*) as count FROM users");
            if (!userCountRow || userCountRow.count === 0) {
                const crypto = require('crypto');
                const hash = crypto.createHash('sha256').update('123').digest('hex');
                await dbRun("INSERT INTO users (name, email, pass) VALUES ('Leonan', 'leonan@fullcycle.com.br', ?)", [hash]);
                await dbRun("INSERT INTO courses (title, price, active) VALUES ('Clean Architecture', 997.00, 1)");
                await dbRun("INSERT INTO courses (title, price, active) VALUES ('Docker', 497.00, 1)");
                await dbRun("INSERT INTO enrollments (user_id, course_id) VALUES (1, 1)");
                await dbRun("INSERT INTO payments (enrollment_id, amount, status) VALUES (1, 997.00, 'PAID')");
            }
        })();
    }
    return initPromise;
}

module.exports = { getDb, initDb, dbRun, dbGet, dbAll };
