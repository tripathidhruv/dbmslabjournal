#!/usr/bin/env python3
"""
Direct HTML content updater for all 14 DBMS Lab Journal practicals.
Replaces theory cards, procedure steps, code blocks, and conclusions
while preserving ALL CSS, Tailwind classes, navigation, and structure.
"""

import re, os, html

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── helper ──────────────────────────────────────────────────────────────────

def escape(text):
    """Escape plain text for safe inclusion in HTML."""
    return html.escape(text, quote=False)

def build_theory_cards(cards):
    """
    cards = list of (title, text, border_color, span)
    border_color: 'primary' | 'secondary'
    span: '' | 'lg:col-span-2' | 'lg:col-span-3'
    """
    out = []
    for title, text, color, span in cards:
        cls = f"p-8 bg-surface-container-low rounded-xl border-l-4 border-{color} {span}".strip()
        out.append(
            f'<div class="{cls}">'
            f'<h3 class="text-lg font-headline font-semibold text-{color} mb-3">{escape(title)}</h3>'
            f'<p class="text-on-surface-variant font-body leading-relaxed text-sm">{escape(text)}</p>'
            f'</div>'
        )
    return "\n".join(out)

def build_steps(steps):
    """steps = list of step strings"""
    items = []
    for i, s in enumerate(steps, 1):
        num = f"{i:02d}."
        items.append(
            f'<li class="flex gap-4">'
            f'<span class="text-primary font-headline font-bold text-lg w-8 shrink-0">{num}</span>'
            f'<span class="text-on-surface-variant font-body leading-relaxed">{escape(s)}</span>'
            f'</li>'
        )
    return f'<ol class="flex flex-col gap-5">{"".join(items)}</ol>'

def build_code_block(label, sql_code):
    """Wrap plain SQL in a highlighted pre block (comment/keyword/string colouring)."""
    def colour_line(line):
        if line.strip().startswith("--"):
            return f'<span class="text-slate-500 italic">{escape(line)}</span>'
        # keywords
        kws = [
            "SELECT","FROM","WHERE","INSERT","INTO","VALUES","UPDATE","SET",
            "DELETE","CREATE","TABLE","DATABASE","DROP","ALTER","TRUNCATE",
            "PRIMARY KEY","FOREIGN KEY","REFERENCES","UNIQUE","NOT NULL",
            "DEFAULT","CHECK","AUTO_INCREMENT","CONSTRAINT","INDEX",
            "SHOW","USE","DESCRIBE","EXPLAIN","GRANT","REVOKE","FLUSH",
            "START TRANSACTION","COMMIT","ROLLBACK","SAVEPOINT",
            "PROCEDURE","FUNCTION","TRIGGER","CURSOR","DECLARE","OPEN",
            "FETCH","CLOSE","CALL","DELIMITER","BEGIN","END","IF","THEN",
            "ELSEIF","ELSE","END IF","WHILE","DO","END WHILE","LOOP",
            "LEAVE","REPEAT","UNTIL","END REPEAT","HANDLER","SIGNAL",
            "CONTINUE","EXIT","RETURN","RETURNS","DETERMINISTIC",
            "JOIN","INNER JOIN","LEFT JOIN","RIGHT JOIN","CROSS JOIN",
            "SELF JOIN","ON","GROUP BY","ORDER BY","HAVING","LIMIT",
            "WITH ROLLUP","UNION","UNION ALL","IN","NOT IN","EXISTS",
            "BETWEEN","LIKE","IS NULL","IS NOT NULL","AND","OR","NOT",
            "DISTINCT","AS","WITH CHECK OPTION","ADD COLUMN","MODIFY COLUMN",
            "RENAME COLUMN","DROP COLUMN","DROP INDEX","ADD CONSTRAINT",
            "ON DELETE CASCADE","ON UPDATE CASCADE","ON DELETE RESTRICT",
            "FOR EACH ROW","BEFORE INSERT","AFTER INSERT","BEFORE UPDATE",
            "AFTER UPDATE","BEFORE DELETE","AFTER DELETE","OLD","NEW",
            "ENUM","INT","VARCHAR","TEXT","DATE","DATETIME","DECIMAL",
            "BOOLEAN","BLOB","REAL","INTEGER","YEAR","TIME","FLOAT",
            "CHANGE","RENAME TABLE","SET NAMES","SESSION","GLOBAL",
            "PRAGMA","VIEW","REPLACE","PARTITION","TEMPORARY",
        ]
        # Sort by length desc so longer keywords match first
        coloured = escape(line)
        for kw in sorted(kws, key=len, reverse=True):
            pattern = re.compile(r'(?<![A-Za-z_])' + re.escape(html.escape(kw, quote=False)) + r'(?![A-Za-z_])', re.IGNORECASE)
            coloured = pattern.sub(lambda m: f'<span class="text-cyan-400">{m.group()}</span>', coloured)
        # Strings in green
        coloured = re.sub(r"'([^']*)'", lambda m: f'<span class="text-green-400">\'{m.group(1)}\'</span>', coloured)
        # Numbers in amber
        coloured = re.sub(r'\b(\d+(?:\.\d+)?)\b', lambda m: f'<span class="text-amber-400">{m.group()}</span>', coloured)
        return coloured

    lines = sql_code.split("\n")
    body = "\n".join(colour_line(l) for l in lines)
    return (
        f'<div class="bg-[#0a0e14] rounded-xl border border-outline-variant/20 overflow-hidden shadow-2xl">'
        f'<div class="flex items-center gap-2 px-4 py-3 bg-surface-container-lowest border-b border-outline-variant/20">'
        f'<span class="w-3 h-3 rounded-full bg-red-500 inline-block"></span>'
        f'<span class="w-3 h-3 rounded-full bg-yellow-500 inline-block"></span>'
        f'<span class="w-3 h-3 rounded-full bg-green-500 inline-block"></span>'
        f'<span class="ml-4 text-xs font-label text-slate-500 uppercase tracking-widest">{escape(label)}</span>'
        f'</div>'
        f'<pre class="code-block p-6 text-slate-300">{body}</pre>'
        f'</div>'
    )

def build_conclusion(text):
    return (
        f'<div class="p-8 bg-surface-container rounded-xl border-l-4 border-secondary">'
        f'<p class="text-on-surface font-body leading-relaxed mb-4">{escape(text)}</p>'
        f'</div>'
    )

# ─── replace helpers ──────────────────────────────────────────────────────────

THEORY_SECTION_RE = re.compile(
    r'(<section class="mb-16">[\s\S]*?Theory[^<]*</h2>[\s\S]*?<div class="grid[^>]*>)([\s\S]*?)(</div>\s*</section>)',
    re.MULTILINE
)

PROCEDURE_OL_RE = re.compile(
    r'(<ol class="flex flex-col gap-5">)([\s\S]*?)(</ol>)',
    re.MULTILINE
)

CODE_BLOCK_OUTER_RE = re.compile(
    r'(<div class="mb-16">[\s\S]*?<div class="bg-\[#0a0e14\][^>]*>)([\s\S]*?)(</div>\s*</div>\s*</section>)',
    re.MULTILINE
)

CONCLUSION_RE = re.compile(
    r'(<div class="p-8 bg-surface-container rounded-xl border-l-4 border-secondary">)([\s\S]*?)(</div>\s*</section>[\s\S]*?Viva)',
    re.MULTILINE
)


def patch_file(path, theory_html, steps_html, code_html, conclusion_html):
    with open(path, encoding='utf-8') as f:
        content = f.read()

    # 1. Replace theory grid cards
    m = THEORY_SECTION_RE.search(content)
    if m:
        content = content[:m.start(2)] + "\n" + theory_html + "\n" + content[m.end(2):]
    else:
        print(f"  ⚠  Theory section not found in {os.path.basename(path)}")

    # 2. Replace procedure steps
    m = PROCEDURE_OL_RE.search(content)
    if m:
        content = content[:m.start()] + steps_html + content[m.end():]
    else:
        print(f"  ⚠  Procedure ol not found in {os.path.basename(path)}")

    # 3. Replace code block (the inner terminal div)
    # Strategy: find the first <pre class="code-block and replace from the outer terminal div to </pre></div></div>
    pre_start = content.find('<pre class="code-block')
    if pre_start != -1:
        # Find the wrapping terminal div (the one with traffic-light dots)
        dot_div_start = content.rfind('<div class="bg-[#0a0e14]', 0, pre_start)
        pre_end = content.find('</pre>', pre_start) + len('</pre>')
        # Close the terminal div
        close_div = content.find('</div>', pre_end) + len('</div>')
        # 2 closing divs: </pre></div> (code wrapper) </div> (outer mb-16)
        close_div2 = content.find('</div>', close_div) + len('</div>')
        content = content[:dot_div_start] + code_html + content[close_div2:]
    else:
        print(f"  ⚠  Code block not found in {os.path.basename(path)}")

    # 4. Replace conclusion paragraph(s)
    # Find conclusion section's card div
    conc_div = content.find('<div class="p-8 bg-surface-container rounded-xl border-l-4 border-secondary">')
    if conc_div != -1:
        end_div = content.find('</div>', conc_div) + len('</div>')
        # Some have two <p> tags — find the actual closing </div> of the card
        # Count open/close divs to find the right one
        depth = 0
        scan = conc_div
        while scan < len(content):
            if content[scan:scan+4] == '<div':
                depth += 1
            elif content[scan:scan+6] == '</div>':
                depth -= 1
                if depth == 0:
                    end_div = scan + 6
                    break
            scan += 1
        content = content[:conc_div] + conclusion_html + content[end_div:]
    else:
        print(f"  ⚠  Conclusion div not found in {os.path.basename(path)}")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ Updated: {os.path.relpath(path, BASE)}")


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENT DATA
# ═══════════════════════════════════════════════════════════════════════════════

P01_THEORY = build_theory_cards([
    ("What is MySQL?",
     "MySQL is an open-source RDBMS developed by MySQL AB in 1995, later acquired by Oracle Corporation. It organises data into related tables with rows and columns. Powering over 50% of web applications globally — WordPress, Facebook, Twitter, YouTube — MySQL is the world's most popular open-source database engine.",
     "primary", "lg:col-span-2"),
    ("History & Architecture",
     "MySQL has three layers: (1) Client Layer — mysql CLI, Workbench, JDBC/ODBC connectors; (2) SQL Layer — parser, optimizer, query cache, execution engine; (3) Storage Engine Layer — pluggable engines: InnoDB (default, ACID, row-locking), MyISAM (fast reads, no transactions), MEMORY (RAM-based, volatile). MySQL listens on TCP port 3306 and runs as a background daemon (mysqld).",
     "secondary", ""),
    ("InnoDB & ACID Properties",
     "InnoDB is the default engine since MySQL 5.5. It guarantees ACID: Atomicity (transaction is all-or-nothing), Consistency (DB moves from one valid state to another), Isolation (concurrent transactions don't interfere — four isolation levels), Durability (committed data survives crashes via redo/undo logs). These make MySQL suitable for banking, healthcare, and e-commerce.",
     "primary", "lg:col-span-2"),
    ("Storage Engines Compared",
     "InnoDB supports foreign keys, MVCC, and crash recovery. MyISAM uses table-level locking and is faster for read-heavy, non-critical data, but has no transaction support. MEMORY stores data in RAM for ultra-fast temporary operations. BLACKHOLE discards all data but logs binary events. ARCHIVE compresses rows for historical logging.",
     "secondary", ""),
    ("Configuration & Security",
     "The my.cnf (Linux) or my.ini (Windows) configuration file controls max_connections (default 151), innodb_buffer_pool_size (set to 70-80% of RAM for performance), character-set-server (use utf8mb4), and log file paths. mysql_secure_installation hardens the server by removing anonymous users, disabling remote root login, and dropping the test database.",
     "primary", ""),
    ("Real-World Use Cases",
     "MySQL powers mission-critical systems: Netflix uses it for user session data, GitHub for repository metadata, LinkedIn MySQL Cluster for high availability, and hospital EMR systems for HIPAA-compliant patient records. MySQL 8.0 added Window Functions (RANK, DENSE_RANK, LAG, LEAD), CTEs (WITH clause), Atomic DDL, and Role-Based Access Control.",
     "secondary", "lg:col-span-2"),
])

P01_STEPS = build_steps([
    "Understand the difference between flat files and a relational database — why tables with relationships are superior to CSV files for complex data.",
    "Study the three-tier MySQL architecture: Client → SQL Layer (parser, optimizer) → Storage Engine. Trace how a query travels through each layer.",
    "Learn the main storage engines: InnoDB (default, ACID), MyISAM (read-heavy), MEMORY (RAM-based, volatile), ARCHIVE (compressed history).",
    "Understand all four ACID properties with real-world transaction examples from banking and healthcare.",
    "Explore the MySQL client-server communication model — how multiple clients connect to a single mysqld daemon process on port 3306.",
    "Connect to MySQL using the command-line client: mysql -u root -p and verify the connection is established.",
    "Run system information commands: SELECT VERSION(); SELECT USER(); SELECT NOW();",
    "View available databases with SHOW DATABASES; and study the four system databases: information_schema, mysql, performance_schema, sys.",
    "Explore all available storage engines and their transaction support: SHOW ENGINES;",
    "Inspect key configuration variables: SHOW VARIABLES LIKE 'max_connections'; SHOW VARIABLES LIKE 'character_set_database';",
    "Create a practice database: CREATE DATABASE dbms_lab; USE dbms_lab; SELECT DATABASE();",
    "Record all observations — version number, default engine, character set, port — in your journal with explanations.",
])

P01_CODE = """-- Display the current MySQL version
SELECT VERSION();

-- Display the currently logged-in user
SELECT USER();

-- Display current date and time
SELECT NOW();

-- Show all databases on this MySQL server
SHOW DATABASES;

-- Show all available storage engines and their support status
SHOW ENGINES;

-- Show version-related system variables
SHOW VARIABLES LIKE 'version%';

-- Show default storage engine setting
SHOW VARIABLES LIKE '%engine%';

-- Show maximum allowed connections
SHOW VARIABLES LIKE 'max_connections';

-- Show default character set
SHOW VARIABLES LIKE 'character_set_database';

-- Show the port MySQL is running on
SHOW VARIABLES LIKE 'port';

-- Show InnoDB buffer pool size (set to 70-80% of RAM in production)
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- Create a new database for our lab practicals
CREATE DATABASE dbms_lab;

-- Switch to using that database
USE dbms_lab;

-- Confirm which database is currently active
SELECT DATABASE();

-- Show all tables (will be empty initially)
SHOW TABLES;

-- Show server status: uptime, thread count, queries
SHOW STATUS LIKE 'Uptime';
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Questions';

-- Display full server status including uptime and connection info
STATUS;"""

P01_CONCLUSION = (
    "This practical provided a foundational understanding of MySQL as a relational database management system. "
    "We explored its three-tier architecture and understood how the storage engine layer separates logical query "
    "processing from physical data storage. The ACID properties were studied in context, demonstrating why MySQL "
    "is trusted for mission-critical applications in banking and healthcare. The hands-on commands confirmed the "
    "MySQL installation is functional and correctly configured. Understanding MySQL's architecture is essential "
    "before writing any SQL, as it explains why certain queries perform faster than others. MySQL's open-source "
    "nature and Oracle's continued development make it the industry standard for web applications. This knowledge "
    "forms the base for all subsequent practicals in this lab."
)

# ─── P02 ─────────────────────────────────────────────────────────────────────

P02_THEORY = build_theory_cards([
    ("MySQL Editions & Installation",
     "MySQL comes in Community Edition (free, open-source, sufficient for all academic and most production needs) and Enterprise Edition (paid, advanced monitoring, backups, firewall). MySQL Workbench is the official GUI tool providing a visual interface for query writing, schema design, server administration, and performance monitoring. The mysqld daemon listens on TCP port 3306.",
     "primary", "lg:col-span-2"),
    ("Configuration (my.cnf / my.ini)",
     "The central configuration file my.cnf (Linux/Mac) or my.ini (Windows) controls: max_connections (default 151 — max simultaneous clients), innodb_buffer_pool_size (InnoDB cache, set to 70-80% of RAM), character-set-server (use utf8mb4 for full Unicode), collation-server (utf8mb4_unicode_ci), log_error (error log path), and datadir (data storage location).",
     "secondary", ""),
    ("Security Hardening",
     "mysql_secure_installation automates security hardening: sets root password, removes anonymous users, disables remote root login, drops the test database, and reloads privilege tables. The principle of least privilege means application users should only have SELECT, INSERT, UPDATE on their specific database — never global ALL PRIVILEGES. Always use strong passwords following complexity rules.",
     "primary", "lg:col-span-2"),
    ("User Management",
     "The root user has all privileges and must be protected. CREATE USER creates a new account. GRANT assigns specific privileges (SELECT, INSERT, UPDATE, DELETE, ALL) on specific databases or tables. REVOKE removes privileges. FLUSH PRIVILEGES reloads the grant tables. SHOW GRANTS displays current privileges. DROP USER removes the account entirely.",
     "secondary", ""),
    ("Character Sets & Collations",
     "Character sets define which characters can be stored. UTF8MB4 is recommended as it supports all Unicode characters including emojis. UTF8 in older MySQL only supports 3-byte characters and misses 4-byte characters like emoji. Collation defines sort order — utf8mb4_unicode_ci is case-insensitive and diacritic-aware. Set charset globally in my.cnf for consistency across all databases.",
     "primary", ""),
])

P02_STEPS = build_steps([
    "Download MySQL Community Edition from dev.mysql.com/downloads for your OS (Windows/Linux/Mac).",
    "Run the installer, choose 'Developer Default' setup type which installs Server, Workbench, Shell, and connectors.",
    "Set the root password during installation — use a strong password with uppercase, lowercase, numbers, and symbols.",
    "Start the MySQL service: on Linux use 'sudo systemctl start mysql', on Windows start from Services panel.",
    "Run mysql_secure_installation to remove anonymous users, disable remote root, drop test database.",
    "Connect as root: mysql -u root -p and verify login is successful.",
    "Inspect the configuration: SHOW VARIABLES LIKE 'max_connections'; SHOW VARIABLES LIKE 'character_set_server';",
    "Create a dedicated lab user: CREATE USER 'labuser'@'localhost' IDENTIFIED BY 'Lab@1234';",
    "Grant privileges on lab database: GRANT ALL PRIVILEGES ON dbms_lab.* TO 'labuser'@'localhost';",
    "Test the new user by connecting: mysql -u labuser -p and running SHOW DATABASES;",
    "Create a read-only user, grant only SELECT, verify they cannot INSERT data.",
    "REVOKE privileges, DROP test users, and document all configuration values in your journal.",
])

P02_CODE = """-- Connect to MySQL as root (run in terminal)
-- mysql -u root -p

-- Check current MySQL version after login
SELECT VERSION();

-- View all existing users and their allowed hosts
SELECT User, Host, plugin FROM mysql.user;

-- Create a new database user for lab work
CREATE USER 'labuser'@'localhost' IDENTIFIED BY 'Lab@1234';

-- Grant all privileges on our lab database to the new user
GRANT ALL PRIVILEGES ON dbms_lab.* TO 'labuser'@'localhost';

-- Apply the privilege changes immediately
FLUSH PRIVILEGES;

-- Verify what privileges were granted
SHOW GRANTS FOR 'labuser'@'localhost';

-- Grant only SELECT (restricted read-only user example)
CREATE USER 'readonly_user'@'localhost' IDENTIFIED BY 'Read@5678';
GRANT SELECT ON dbms_lab.* TO 'readonly_user'@'localhost';
FLUSH PRIVILEGES;

-- Show grants for restricted user
SHOW GRANTS FOR 'readonly_user'@'localhost';

-- Revoke INSERT privilege from labuser
REVOKE INSERT ON dbms_lab.* FROM 'labuser'@'localhost';

-- Check important configuration variables
SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE 'character_set_server';
SHOW VARIABLES LIKE 'collation_server';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW VARIABLES LIKE 'datadir';
SHOW VARIABLES LIKE 'log_error';
SHOW VARIABLES LIKE 'port';

-- Change session-level character set (current session only)
SET NAMES 'utf8mb4';

-- Show the current session character set
SHOW VARIABLES LIKE 'character_set_client';

-- Drop the test users when done
DROP USER 'readonly_user'@'localhost';
DROP USER 'labuser'@'localhost';

-- Verify users were dropped
SELECT User, Host FROM mysql.user;"""

P02_CONCLUSION = (
    "This practical covered the complete installation and configuration of MySQL Community Edition. "
    "We successfully installed the MySQL server, configured security using mysql_secure_installation, "
    "and verified the server is operating correctly. User management was demonstrated by creating "
    "application-specific users with restricted privileges, implementing the principle of least privilege. "
    "Configuration variables like max_connections and innodb_buffer_pool_size were inspected and their "
    "impact on performance understood. UTF8MB4 character set was set for proper multilingual support. "
    "This foundational setup ensures a secure, correctly configured database environment for all "
    "subsequent practical work."
)

# ─── P03 ─────────────────────────────────────────────────────────────────────

P03_THEORY = build_theory_cards([
    ("What is SQLite?",
     "SQLite is a self-contained, serverless, zero-configuration, transactional SQL database engine. Unlike MySQL which requires a background server process, SQLite reads and writes directly to a single disk file (.db). Every Android and iOS device has SQLite built in — it is the most deployed database engine in the world with over 1 trillion active deployments.",
     "primary", "lg:col-span-2"),
    ("SQLite vs MySQL",
     "Key differences: SQLite has no user management or network access, no separate server process, no RIGHT JOIN, and limited ALTER TABLE (cannot drop or modify columns easily). However, SQLite requires zero setup, has a ~600KB footprint, is file-based (easily backed up by copying), and is extremely reliable for embedded systems, mobile apps, and small websites with low write concurrency.",
     "secondary", ""),
    ("Type Affinity & Storage Classes",
     "SQLite uses dynamic type affinity rather than strict typing. Five storage classes: NULL (missing value), INTEGER (1-8 bytes), REAL (8-byte float), TEXT (UTF-8 string), and BLOB (binary stored exactly as input). A column declared VARCHAR(100) stores TEXT; INT stores INTEGER — but SQLite is flexible and won't strictly enforce declared types. AUTOINCREMENT ensures IDs are always increasing and never reused.",
     "primary", "lg:col-span-2"),
    ("Dot-Commands (CLI)",
     "SQLite CLI uses dot-commands prefixed with . that control the tool, not SQL. Key commands: .open filename.db (open/create database), .databases (show attached DBs), .tables (list tables), .schema tablename (show CREATE statement), .headers on (show column names), .mode column (formatted output), .output file.txt (redirect output), .quit (exit).",
     "secondary", ""),
    ("Python & SQLite Integration",
     "Python's built-in sqlite3 module provides a complete SQLite interface with no additional installation. Key methods: sqlite3.connect('db.db') opens a connection, conn.cursor() creates a cursor, cursor.execute(sql) runs a query, conn.commit() saves changes, and cursor.fetchall() retrieves results. This makes SQLite the default for Python desktop and web applications.",
     "primary", ""),
    ("PRAGMA Commands",
     "PRAGMA commands query or modify SQLite configuration. PRAGMA table_info(tablename) returns column details (name, type, notnull, default, pk). PRAGMA foreign_keys = ON enables foreign key enforcement (disabled by default). PRAGMA integrity_check verifies database health. PRAGMA journal_mode = WAL enables Write-Ahead Logging for better concurrent read performance.",
     "secondary", "lg:col-span-2"),
])

P03_STEPS = build_steps([
    "Install SQLite3: on Ubuntu 'sudo apt install sqlite3', on Mac it is pre-installed, on Windows download from sqlite.org.",
    "Open or create a database file from terminal: sqlite3 college.db",
    "Enable formatted output: .headers on  then .mode column",
    "Run .databases to see the current in-memory and file-based databases attached.",
    "Create the Students table with INTEGER PRIMARY KEY AUTOINCREMENT, TEXT, REAL, and CHECK constraints.",
    "Insert 15 rows of student data using a multi-row INSERT VALUES statement.",
    "Run SELECT * FROM Students; to verify all rows were inserted correctly.",
    "Practice filtering with WHERE, sorting with ORDER BY, and grouping with GROUP BY and COUNT/AVG.",
    "Use .schema Students to view the exact CREATE TABLE statement that was used.",
    "Export query results to a text file using .output filename.txt then run a SELECT, then .output stdout to resume console output.",
    "Run PRAGMA table_info(Students); to inspect column metadata.",
    "Drop the table with DROP TABLE IF EXISTS Students; and exit with .quit",
])

P03_CODE = """-- Open or create a SQLite database file
-- (run in terminal: sqlite3 college.db)
.open college.db

-- Show all attached databases
.databases

-- Enable column headers in output
.headers on

-- Set output mode to formatted columns
.mode column

-- Create the Students table
CREATE TABLE Students (
    StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Branch TEXT NOT NULL,
    Semester INTEGER CHECK(Semester BETWEEN 1 AND 8),
    CGPA REAL DEFAULT 0.0 CHECK(CGPA BETWEEN 0.0 AND 10.0),
    Email TEXT UNIQUE
);

-- Insert 15 rows of sample student data
INSERT INTO Students (Name, Branch, Semester, CGPA, Email) VALUES
('Aarav Shah', 'IT', 4, 8.5, 'aarav@college.edu'),
('Priya Mehta', 'CS', 4, 9.1, 'priya@college.edu'),
('Rohit Joshi', 'ENTC', 4, 7.8, 'rohit@college.edu'),
('Sneha Patil', 'IT', 4, 8.9, 'sneha@college.edu'),
('Karan Desai', 'Mech', 4, 6.5, 'karan@college.edu'),
('Ananya Iyer', 'CS', 4, 9.4, 'ananya@college.edu'),
('Vikas Rao', 'Civil', 4, 7.2, 'vikas@college.edu'),
('Pooja Nair', 'IT', 4, 8.0, 'pooja@college.edu'),
('Arjun Tiwari', 'CS', 4, 8.7, 'arjun@college.edu'),
('Neha Gupta', 'ENTC', 4, 7.5, 'neha@college.edu'),
('Raj Malhotra', 'IT', 4, 9.0, 'raj@college.edu'),
('Meera Pillai', 'Mech', 4, 6.8, 'meera@college.edu'),
('Dev Sharma', 'CS', 4, 8.3, 'dev@college.edu'),
('Tara Jain', 'IT', 4, 7.9, 'tara@college.edu'),
('Yash Kumar', 'ENTC', 4, 8.1, 'yash@college.edu');

-- Select all students
SELECT * FROM Students;

-- Filter IT branch students
SELECT Name, CGPA FROM Students WHERE Branch = 'IT';

-- Order by CGPA descending (top performers first)
SELECT Name, Branch, CGPA FROM Students ORDER BY CGPA DESC;

-- Count students per branch with average CGPA
SELECT Branch, COUNT(*) AS TotalStudents, AVG(CGPA) AS AvgCGPA
FROM Students GROUP BY Branch;

-- Students with CGPA above 8.5
SELECT Name, CGPA FROM Students WHERE CGPA > 8.5;

-- Show table schema
.schema Students

-- Export results to a text file
.output students_report.txt
SELECT * FROM Students ORDER BY CGPA DESC;
.output stdout

-- Show table info (columns, types, constraints)
PRAGMA table_info(Students);

-- Drop the table
DROP TABLE IF EXISTS Students;

-- Exit SQLite
.quit"""

P03_CONCLUSION = (
    "This practical demonstrated SQLite as a lightweight, serverless database ideal for embedded and mobile "
    "applications. We created a Students database, inserted 15 records with various data types and constraints, "
    "and performed filtering, sorting, and aggregation queries. The dot-commands provided essential CLI control "
    "for output formatting and data export. Key distinctions from MySQL were observed: no server process, "
    "type affinity instead of strict typing, and PRAGMA commands for metadata inspection. SQLite's zero-setup "
    "nature and Python integration make it indispensable for rapid prototyping and local application storage. "
    "The AUTOINCREMENT behavior, CHECK constraints, and UNIQUE enforcement were all verified during the session."
)

# ─── P04 ─────────────────────────────────────────────────────────────────────

P04_THEORY = build_theory_cards([
    ("ER Diagram Fundamentals",
     "An Entity-Relationship (ER) Diagram, invented by Peter Chen in 1976, is a visual blueprint of a database. It models real-world data as Entities (things, shown as rectangles), Attributes (properties, shown as ovals), and Relationships (associations, shown as diamonds). ER diagrams are the standard tool for conceptual database design before writing any SQL — they communicate the data model to non-technical stakeholders.",
     "primary", "lg:col-span-2"),
    ("Entity Types",
     "Strong Entities exist independently (Student, Doctor) — shown as rectangles. Weak Entities depend on a strong entity for identification (Dependent depends on Employee) — shown as double rectangles with a double-line relationship. The identifying relationship that links a weak entity to its owner is shown as a double-line diamond.",
     "secondary", ""),
    ("Attribute Types",
     "Simple attributes are atomic/indivisible (Name, Age). Composite attributes have sub-parts (Address → Street, City, PIN). Derived attributes are calculated from others (Age from DOB) — shown as dashed ovals. Multivalued attributes can hold multiple values (Phone Numbers) — shown as double ovals. Key attributes uniquely identify an entity — shown with underlined text inside the oval.",
     "primary", ""),
    ("Cardinality & Participation",
     "Cardinality: One-to-One (1:1) — one person has one passport; One-to-Many (1:N) — one department has many employees; Many-to-Many (M:N) — students enroll in many courses, courses have many students. Participation: Total participation (double line) means every entity MUST participate; Partial participation (single line) means participation is optional.",
     "secondary", "lg:col-span-2"),
    ("Converting ER to Relational Schema",
     "Each strong entity becomes a table. M:N relationships become junction/associative tables with foreign keys from both sides. Multivalued attributes become separate tables. Composite attributes are flattened into individual columns. Derived attributes are usually not stored (computed on query). Weak entity tables include the owner entity's primary key as a foreign key and use a composite primary key.",
     "primary", ""),
    ("Extended ER Concepts",
     "Specialization (top-down): breaks a general entity into specialized subtypes — Person → Employee, Student. Generalization (bottom-up): combines similar entities into a general one — scooter, car, bus → Vehicle. Aggregation: treats a relationship as an entity for a higher-level relationship. These concepts map to table inheritance patterns — single-table, table-per-subclass, or table-per-hierarchy.",
     "secondary", "lg:col-span-2"),
])

P04_STEPS = build_steps([
    "Identify the real-world problem domain — for this practical: a Hospital Management System.",
    "List all entities: Doctor, Patient, Ward, Treatment, Department.",
    "For each entity, identify all attributes and mark primary keys (underlined), multivalued (double oval), derived (dashed oval), and composite attributes.",
    "Identify relationships between entities and determine their cardinality (1:1, 1:N, M:N).",
    "Determine participation constraints — which entities must always have a relationship (total) vs optionally (partial).",
    "Draw the complete ER diagram on paper or using a tool like draw.io, including all types of attributes and relationships.",
    "Convert the ER diagram to relational schema: strong entities → tables, M:N → junction tables, composite → flat columns.",
    "Create the database schema in MySQL: CREATE DATABASE hospital_db; USE hospital_db;",
    "Create each table following the ER diagram design with appropriate PRIMARY KEY and FOREIGN KEY constraints.",
    "Insert 5 doctors, 5 wards, and 10 patients using INSERT statements.",
    "Insert 10 treatment records creating M:N relationships between patients and doctors.",
    "Run JOIN queries to verify the relationships work correctly: patient-ward, patient-doctor-treatment.",
])

P04_CODE = """-- ER Diagram Case Study: Hospital Management System
CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

-- Strong Entity: Doctor
CREATE TABLE Doctor (
    DoctorID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Specialization VARCHAR(50) NOT NULL,
    Phone VARCHAR(15) UNIQUE,
    Email VARCHAR(100) UNIQUE,
    JoiningDate DATE DEFAULT (CURRENT_DATE)
);

-- Strong Entity: Ward
CREATE TABLE Ward (
    WardID INT PRIMARY KEY AUTO_INCREMENT,
    WardName VARCHAR(50) NOT NULL,
    WardType ENUM('General','ICU','Pediatric','Emergency') NOT NULL,
    Capacity INT CHECK (Capacity > 0),
    Floor INT DEFAULT 1
);

-- Strong Entity: Patient (linked to Ward - 1:N)
CREATE TABLE Patient (
    PatientID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Age INT CHECK (Age > 0 AND Age < 150),
    Gender ENUM('Male','Female','Other') NOT NULL,
    Phone VARCHAR(15),
    Address TEXT,
    WardID INT,
    FOREIGN KEY (WardID) REFERENCES Ward(WardID)
);

-- M:N Relationship: Treatment (Patient-Doctor junction)
CREATE TABLE Treatment (
    TreatmentID INT PRIMARY KEY AUTO_INCREMENT,
    PatientID INT NOT NULL,
    DoctorID INT NOT NULL,
    TreatmentDate DATE NOT NULL,
    Diagnosis VARCHAR(200),
    Prescription TEXT,
    Cost DECIMAL(8,2) DEFAULT 0.00,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);

-- Insert 5 doctors
INSERT INTO Doctor (Name, Specialization, Phone, Email) VALUES
('Dr. Anil Kapoor', 'Cardiology', '9876543210', 'anil@hospital.com'),
('Dr. Sunita Rao', 'Neurology', '9876543211', 'sunita@hospital.com'),
('Dr. Rajan Mehta', 'Orthopedics', '9876543212', 'rajan@hospital.com'),
('Dr. Priya Sharma', 'Pediatrics', '9876543213', 'priya@hospital.com'),
('Dr. Vikram Singh', 'Emergency', '9876543214', 'vikram@hospital.com');

-- Insert 5 wards
INSERT INTO Ward (WardName, WardType, Capacity, Floor) VALUES
('Ward A', 'General', 50, 1), ('Ward B', 'ICU', 10, 2),
('Ward C', 'Pediatric', 20, 3), ('Ward D', 'Emergency', 15, 1),
('Ward E', 'General', 40, 2);

-- Insert 10 patients
INSERT INTO Patient (Name, Age, Gender, Phone, WardID) VALUES
('Ramesh Kumar', 45, 'Male', '9111111111', 1),
('Sunita Devi', 32, 'Female', '9222222222', 3),
('Aakash Singh', 67, 'Male', '9333333333', 2),
('Priya Verma', 28, 'Female', '9444444444', 1),
('Vijay Patil', 55, 'Male', '9555555555', 2),
('Meena Shah', 8, 'Female', '9666666666', 3),
('Rajesh Gupta', 72, 'Male', '9777777777', 2),
('Anita Joshi', 41, 'Female', '9888888888', 4),
('Suresh Nair', 35, 'Male', '9999999999', 1),
('Kavita Pillai', 60, 'Female', '9000000001', 5);

-- Insert 10 treatment records (M:N Patient-Doctor)
INSERT INTO Treatment (PatientID, DoctorID, TreatmentDate, Diagnosis, Cost) VALUES
(1,1,'2024-01-10','Hypertension',2500.00),
(2,2,'2024-01-11','Migraine',1800.00),
(3,1,'2024-01-12','Bypass Surgery',85000.00),
(4,3,'2024-01-13','Knee Replacement',65000.00),
(5,2,'2024-01-14','Stroke',45000.00),
(6,4,'2024-01-15','Fever',500.00),
(7,1,'2024-01-16','Heart Attack',90000.00),
(8,5,'2024-01-17','Fracture',12000.00),
(9,3,'2024-01-18','Back Pain',3500.00),
(10,4,'2024-01-19','Diabetes',2000.00);

-- Query 1: Patient with their Ward (1:N relationship)
SELECT P.Name AS Patient, W.WardName, W.WardType
FROM Patient P JOIN Ward W ON P.WardID = W.WardID;

-- Query 2: Full treatment view (M:N Patient-Doctor relationship)
SELECT P.Name AS Patient, D.Name AS Doctor,
       D.Specialization, T.Diagnosis, T.Cost
FROM Treatment T
JOIN Patient P ON T.PatientID = P.PatientID
JOIN Doctor D ON T.DoctorID = D.DoctorID
ORDER BY T.TreatmentDate;

-- Query 3: Doctors who treated multiple patients
SELECT D.Name, COUNT(T.PatientID) AS PatientCount, SUM(T.Cost) AS Revenue
FROM Doctor D
LEFT JOIN Treatment T ON D.DoctorID = T.DoctorID
GROUP BY D.DoctorID ORDER BY PatientCount DESC;"""

P04_CONCLUSION = (
    "This practical demonstrated the complete process of ER diagram design and its conversion to a relational "
    "database schema. Starting from the Hospital Management System domain, we identified entities (Doctor, Ward, "
    "Patient, Treatment), their attributes (simple, composite, derived, multivalued), and their relationships with "
    "correct cardinality and participation. The M:N Patient-Doctor relationship was resolved into a Treatment "
    "junction table with foreign keys to both parent tables. The SQL implementation confirmed that the ER design "
    "translates correctly — JOIN queries successfully navigated all three relationship types (1:N patient-ward, "
    "M:N patient-doctor). ER diagrams are essential for planning before coding, preventing costly schema redesigns "
    "after data has been inserted."
)

# ─── P05 ─────────────────────────────────────────────────────────────────────

P05_THEORY = build_theory_cards([
    ("DDL Commands Overview",
     "DDL (Data Definition Language) commands define and modify database structure. CREATE creates databases, tables, views, indexes. ALTER modifies existing table structure — ADD COLUMN, MODIFY COLUMN, RENAME COLUMN, DROP COLUMN, ADD CONSTRAINT, DROP INDEX. DROP permanently deletes a table including all data and structure. TRUNCATE removes all rows but keeps structure and resets AUTO_INCREMENT. RENAME changes a table's name.",
     "primary", "lg:col-span-2"),
    ("MySQL Data Types",
     "Numeric: INT (4 bytes), BIGINT (8 bytes), DECIMAL(p,s) for exact decimal values (money!), FLOAT/DOUBLE for approximate. String: CHAR(n) fixed-length (padded), VARCHAR(n) variable-length, TEXT for long strings, ENUM for predefined allowed values. Date/Time: DATE (YYYY-MM-DD), DATETIME, TIMESTAMP (auto-updated on change), TIME, YEAR. Binary: BLOB for binary data.",
     "secondary", ""),
    ("Normalization — Why It Matters",
     "Normalization reduces data redundancy and prevents three anomalies: Update anomaly — same data in multiple rows causes inconsistency when one is updated. Insert anomaly — cannot insert partial data without providing unrelated columns. Delete anomaly — deleting one record accidentally removes other needed information. Proper normalization eliminates these using functional dependency analysis.",
     "primary", ""),
    ("1NF → 2NF → 3NF",
     "1NF: Every column has atomic (indivisible) values, no repeating groups — each row uniquely identifiable. 2NF: Must be in 1NF, and every non-key attribute is fully functionally dependent on the entire primary key (no partial dependencies — only relevant when composite keys exist). 3NF: Must be in 2NF, and no non-key attribute depends on another non-key attribute (no transitive dependencies).",
     "secondary", "lg:col-span-2"),
    ("BCNF & Practical Application",
     "BCNF (Boyce-Codd Normal Form) is stricter than 3NF — every determinant must be a candidate key. In practice, most databases aim for 3NF; BCNF is applied when 3NF anomalies persist. Beyond 3NF, 4NF (no multi-valued dependencies) and 5NF (no join dependencies) exist but are rarely needed. Over-normalization can hurt performance by requiring many JOINs.",
     "primary", ""),
    ("Functional Dependencies",
     "A functional dependency X → Y means the value of X uniquely determines the value of Y. In a Student table: StudentID → Name (StudentID determines Name). In an Enrollment table with composite key (StudentID, CourseID): CourseName depends only on CourseID — this is a partial dependency violating 2NF. ProfessorDept depends on ProfessorName, not CourseID — this is a transitive dependency violating 3NF.",
     "secondary", "lg:col-span-2"),
])

P05_STEPS = build_steps([
    "Understand the anomalies in un-normalized data — draw an example UNF table with repeating groups and explain update, insert, delete anomalies.",
    "Apply 1NF: ensure atomic values by splitting multi-valued columns into separate rows, identify primary key.",
    "Identify all functional dependencies in the 1NF table — map which attributes X determines which Y.",
    "Apply 2NF: remove partial dependencies by moving attributes that depend only on part of the composite key to a new table.",
    "Apply 3NF: remove transitive dependencies by moving attributes that depend on non-key attributes to a new table.",
    "Create the 3NF-compliant schema in MySQL: CREATE DATABASE college_db; USE college_db;",
    "Create separate tables for Students, Professors, Courses, and Enrollment following 3NF.",
    "Insert 15 student records and 3 professor records using multi-row INSERT statements.",
    "Demonstrate ALTER TABLE: ADD COLUMN (Email), MODIFY COLUMN (expand size), RENAME COLUMN, DROP COLUMN.",
    "Use RENAME TABLE to rename a table and DESCRIBE to verify the final structure.",
    "Run SHOW CREATE TABLE to view the complete DDL with all constraints.",
    "Document each normalization step with before/after table diagrams and functional dependency notation.",
])

P05_CODE = """CREATE DATABASE IF NOT EXISTS college_db;
USE college_db;

-- UNNORMALIZED (UNF): Multiple courses in one column - violates 1NF
-- Courses column has 'DBMS, OS, CN' in ONE cell - this is wrong
CREATE TABLE UNF_StudentCourses (
    StudentID INT,
    StudentName VARCHAR(100),
    Courses VARCHAR(500),
    ProfessorNames VARCHAR(500),
    Department VARCHAR(50)
);

-- 1NF: Atomic values - one course per row, unique primary key
CREATE TABLE NF1_StudentCourses (
    StudentID INT,
    StudentName VARCHAR(100),
    CourseID VARCHAR(10),
    CourseName VARCHAR(100),
    ProfessorName VARCHAR(100),
    Department VARCHAR(50),
    PRIMARY KEY (StudentID, CourseID)  -- composite key for uniqueness
);

-- 2NF: Remove partial dependencies
-- StudentName, Department depend only on StudentID (partial dep on composite PK)
-- CourseName, ProfessorName depend only on CourseID (partial dep on composite PK)
CREATE TABLE NF2_Students (
    StudentID INT PRIMARY KEY,
    StudentName VARCHAR(100) NOT NULL,
    Department VARCHAR(50)
);

CREATE TABLE NF2_Courses (
    CourseID VARCHAR(10) PRIMARY KEY,
    CourseName VARCHAR(100) NOT NULL,
    ProfessorName VARCHAR(100),
    ProfessorDept VARCHAR(50)  -- transitive dep: ProfDept depends on ProfName, not CourseID
);

CREATE TABLE NF2_Enrollment (
    StudentID INT,
    CourseID VARCHAR(10),
    EnrollDate DATE DEFAULT (CURRENT_DATE),
    PRIMARY KEY (StudentID, CourseID),
    FOREIGN KEY (StudentID) REFERENCES NF2_Students(StudentID),
    FOREIGN KEY (CourseID) REFERENCES NF2_Courses(CourseID)
);

-- 3NF: Remove transitive dependency
-- ProfessorDept depends on ProfessorName, not on CourseID -> separate table
CREATE TABLE NF3_Professors (
    ProfessorID INT PRIMARY KEY AUTO_INCREMENT,
    ProfessorName VARCHAR(100) NOT NULL,
    Department VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE
);

CREATE TABLE NF3_Courses (
    CourseID VARCHAR(10) PRIMARY KEY,
    CourseName VARCHAR(100) NOT NULL,
    Credits INT DEFAULT 3,
    ProfessorID INT,
    FOREIGN KEY (ProfessorID) REFERENCES NF3_Professors(ProfessorID)
);

-- Insert 15 students
INSERT INTO NF2_Students VALUES
(1,'Aarav Shah','IT'),(2,'Priya Mehta','CS'),(3,'Rohit Joshi','ENTC'),
(4,'Sneha Patil','IT'),(5,'Karan Desai','Mech'),(6,'Ananya Iyer','CS'),
(7,'Vikas Rao','Civil'),(8,'Pooja Nair','IT'),(9,'Arjun Tiwari','CS'),
(10,'Neha Gupta','ENTC'),(11,'Raj Malhotra','IT'),(12,'Meera Pillai','Mech'),
(13,'Dev Sharma','CS'),(14,'Tara Jain','IT'),(15,'Yash Kumar','ENTC');

-- Insert professors (3NF)
INSERT INTO NF3_Professors (ProfessorName, Department, Email) VALUES
('Prof. Sharma','IT','sharma@college.edu'),
('Prof. Verma','CS','verma@college.edu'),
('Prof. Iyer','ENTC','iyer@college.edu');

-- Insert courses linked to professors (3NF)
INSERT INTO NF3_Courses VALUES
('CS101','Data Structures',4,1),('CS102','DBMS',4,2),
('CS103','Operating Systems',3,3),('CS104','Computer Networks',3,1),
('CS105','Artificial Intelligence',4,2);

-- DDL ALTER demonstrations
ALTER TABLE NF2_Students ADD COLUMN Email VARCHAR(100);
ALTER TABLE NF2_Students MODIFY COLUMN Email VARCHAR(150);
ALTER TABLE NF2_Students ADD COLUMN Phone VARCHAR(15) DEFAULT 'Not Provided';
ALTER TABLE NF2_Students DROP COLUMN Phone;
ALTER TABLE NF2_Students RENAME COLUMN Email TO StudentEmail;
RENAME TABLE NF2_Students TO Students;

-- Verify final structure
DESCRIBE Students;
SHOW CREATE TABLE NF3_Courses;"""

P05_CONCLUSION = (
    "This practical demonstrated the complete DDL command set and the normalization process from UNF to 3NF. "
    "Starting with an unnormalized table containing multi-valued attributes and redundancy, we systematically "
    "applied normalization rules: 1NF eliminated repeating groups, 2NF removed partial dependencies on the "
    "composite primary key, and 3NF eliminated transitive dependencies by separating Professor data into its "
    "own table. The final schema has four tables (Students, Professors, Courses, Enrollment) with no data "
    "redundancy. ALTER TABLE commands demonstrated schema evolution without data loss. The normalized schema "
    "prevents update, insert, and delete anomalies that plagued the original design."
)

# ─── P06 ─────────────────────────────────────────────────────────────────────

P06_THEORY = build_theory_cards([
    ("Constraints Overview",
     "Constraints are rules enforced on table columns to ensure data accuracy and integrity. PRIMARY KEY uniquely identifies each row — combines NOT NULL and UNIQUE, only one per table, automatically indexed. FOREIGN KEY links a column to a primary key in another table, enforcing referential integrity. UNIQUE ensures all values differ (table can have multiple UNIQUE constraints and UNIQUE columns can contain NULL). NOT NULL prevents empty values.",
     "primary", "lg:col-span-2"),
    ("CHECK & DEFAULT Constraints",
     "CHECK validates that column values meet a specified condition: Age > 0, Salary BETWEEN 15000 AND 500000, Email LIKE '%@%'. MySQL 8.0.16+ enforces CHECK constraints. DEFAULT assigns an automatic value when no value is provided during INSERT — avoids NULLs for optional fields. DEFAULT (CURRENT_DATE) for date columns, DEFAULT 0 for numeric counters, DEFAULT 'Not Specified' for optional text.",
     "secondary", ""),
    ("Referential Actions",
     "ON DELETE CASCADE automatically deletes child rows when parent is deleted. ON DELETE SET NULL sets FK column to NULL. ON DELETE RESTRICT prevents parent deletion if children exist (checked immediately). ON DELETE NO ACTION is similar to RESTRICT but checked at end of transaction. ON UPDATE CASCADE propagates primary key changes to FK columns. Always choose the correct action based on business rules.",
     "primary", ""),
    ("DELETE vs TRUNCATE vs DROP",
     "DELETE: removes specific rows via WHERE, CAN be rolled back (DML), fires row-level triggers, does NOT reset AUTO_INCREMENT, slow on large tables (row-by-row logging). TRUNCATE: removes ALL rows instantly, CANNOT be rolled back (DDL), does NOT fire row-level triggers, RESETS AUTO_INCREMENT to 1, extremely fast. DROP: destroys the entire table structure plus all data permanently — the table ceases to exist.",
     "secondary", "lg:col-span-2"),
    ("Composite vs Surrogate vs Natural Keys",
     "Composite keys use multiple columns together as a primary key (StudentID + CourseID in Enrollment). Surrogate keys are system-generated AUTO_INCREMENT integers with no business meaning — preferred when no natural unique identifier exists, never change, safe to use as FK. Natural keys use real-world attributes (Aadhar number, PAN, ISBN) — risky because real-world data can change, causing cascading FK updates.",
     "primary", ""),
    ("Foreign Key Checks & Bulk Operations",
     "SET FOREIGN_KEY_CHECKS = 0 temporarily disables FK enforcement — used for bulk data loading or schema migrations. Always re-enable with SET FOREIGN_KEY_CHECKS = 1 after. SHOW CREATE TABLE shows all constraints including FK definitions with their referential actions. INFORMATION_SCHEMA.TABLE_CONSTRAINTS lists all constraints per table for documentation and auditing.",
     "secondary", "lg:col-span-2"),
])

P06_STEPS = build_steps([
    "Use college_db created in Practical 05: USE college_db;",
    "Create Department table demonstrating PRIMARY KEY AUTO_INCREMENT, NOT NULL, UNIQUE, DEFAULT, and CHECK constraints.",
    "Create Employee table with FOREIGN KEY referencing Department with ON DELETE CASCADE and ON UPDATE CASCADE.",
    "Insert 5 departments and 15 employees using multi-row INSERT statements.",
    "Test CHECK constraint violation: try inserting an employee with Salary below 15000 — observe error 3819.",
    "Test NOT NULL violation: try inserting without mandatory EmpName — observe error 1364.",
    "Test UNIQUE violation: try inserting two employees with the same Email — observe error 1062.",
    "Test FOREIGN KEY violation: try inserting an employee with a DeptID that doesn't exist — observe error 1452.",
    "Demonstrate ALTER TABLE: ADD COLUMN, MODIFY COLUMN, RENAME COLUMN, ADD CONSTRAINT, DROP CHECK, DROP COLUMN.",
    "Demonstrate ON DELETE CASCADE: delete a department and verify all its employees are automatically deleted.",
    "Compare DELETE (targeted rows, rollback possible) vs TRUNCATE (all rows, AUTO_INCREMENT reset).",
    "Display the complete table structure with DESCRIBE Employee; and SHOW CREATE TABLE Employee;",
])

P06_CODE = """USE college_db;

-- Create Department table demonstrating all constraint types
CREATE TABLE Department (
    DeptID INT PRIMARY KEY AUTO_INCREMENT,
    DeptName VARCHAR(50) NOT NULL UNIQUE,
    Location VARCHAR(50) NOT NULL DEFAULT 'Main Campus',
    Budget DECIMAL(12,2) CHECK (Budget > 0),
    EstablishedYear YEAR CHECK (EstablishedYear >= 1900)
);

-- Create Employee table with FOREIGN KEY + ON DELETE CASCADE
CREATE TABLE Employee (
    EmpID INT PRIMARY KEY AUTO_INCREMENT,
    EmpName VARCHAR(100) NOT NULL,
    Salary DECIMAL(10,2) NOT NULL CHECK (Salary >= 15000 AND Salary <= 500000),
    JoinDate DATE DEFAULT (CURRENT_DATE),
    Email VARCHAR(100) UNIQUE,
    Gender ENUM('Male','Female','Other') NOT NULL,
    DeptID INT NOT NULL,
    FOREIGN KEY (DeptID) REFERENCES Department(DeptID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Insert 5 departments
INSERT INTO Department (DeptName, Location, Budget, EstablishedYear) VALUES
('Information Technology', 'Building A', 1500000.00, 2000),
('Human Resources', 'Building B', 800000.00, 1995),
('Finance', 'Building C', 2000000.00, 1990),
('Marketing', 'Building D', 1200000.00, 2005),
('Operations', 'Main Campus', 1800000.00, 1985);

-- Insert 15 employees
INSERT INTO Employee (EmpName, Salary, Email, Gender, DeptID) VALUES
('Anil Kumar', 45000, 'anil@co.com', 'Male', 1),
('Sunita Rao', 52000, 'sunita@co.com', 'Female', 2),
('Raj Patel', 61000, 'raj@co.com', 'Male', 1),
('Meena Shah', 38000, 'meena@co.com', 'Female', 3),
('Vikram Singh', 70000, 'vikram@co.com', 'Male', 4),
('Pooja Nair', 43000, 'pooja@co.com', 'Female', 2),
('Arjun Tiwari', 55000, 'arjun@co.com', 'Male', 5),
('Kavya Iyer', 48000, 'kavya@co.com', 'Female', 1),
('Ravi Menon', 62000, 'ravi@co.com', 'Male', 3),
('Deepa Joshi', 41000, 'deepa@co.com', 'Female', 4),
('Suresh Pillai', 75000, 'suresh@co.com', 'Male', 5),
('Anita Desai', 44000, 'anita@co.com', 'Female', 2),
('Manoj Verma', 58000, 'manoj@co.com', 'Male', 1),
('Rekha Gupta', 39000, 'rekha@co.com', 'Female', 3),
('Nikhil Sharma', 67000, 'nikhil@co.com', 'Male', 4);

-- ALTER TABLE demonstrations
ALTER TABLE Employee ADD COLUMN Phone VARCHAR(15);
ALTER TABLE Employee MODIFY COLUMN Phone VARCHAR(20) DEFAULT '0000000000';
ALTER TABLE Employee RENAME COLUMN Phone TO MobileNo;
ALTER TABLE Employee ADD CONSTRAINT chk_join CHECK (JoinDate >= '2000-01-01');
ALTER TABLE Employee DROP CHECK chk_join;
ALTER TABLE Employee DROP COLUMN MobileNo;

-- Demonstrate ON DELETE CASCADE
DELETE FROM Department WHERE DeptID = 5;
-- All Operations department employees are now also deleted
SELECT EmpName, DeptID FROM Employee ORDER BY DeptID;

-- DELETE specific rows (targeted, can rollback, keeps structure)
DELETE FROM Employee WHERE Salary < 40000;

-- TRUNCATE would remove all rows and reset AUTO_INCREMENT
-- TRUNCATE TABLE Employee;

-- Constraint violation examples (educational - these WILL fail)
-- INSERT INTO Employee (EmpName, Salary, Gender, DeptID) VALUES ('X', 5000, 'Male', 1);
-- ERROR 3819: Check constraint 'employee_chk_1' violated (Salary < 15000)
-- INSERT INTO Employee (EmpName, Salary, Email, Gender, DeptID) VALUES ('Y', 35000, 'anil@co.com', 'Female', 1);
-- ERROR 1062: Duplicate entry 'anil@co.com' for key 'Email'

-- Disable foreign key checks for bulk operations
SET FOREIGN_KEY_CHECKS = 0;
SET FOREIGN_KEY_CHECKS = 1;

DESCRIBE Employee;
SHOW CREATE TABLE Employee;"""

P06_CONCLUSION = (
    "This practical demonstrated all six SQL constraint types and their enforcement by MySQL. PRIMARY KEY, "
    "FOREIGN KEY, UNIQUE, NOT NULL, CHECK, and DEFAULT were all implemented on the Department and Employee "
    "tables. Constraint violation tests confirmed that MySQL stops malformed data at the database level, "
    "independent of application code — providing a last line of defense against data corruption. ON DELETE "
    "CASCADE was demonstrated by deleting a department and verifying automatic deletion of all associated "
    "employees, illustrating how referential actions maintain consistency. ALTER TABLE showed schema evolution "
    "without data loss. The critical distinction between DELETE (targeted, rollback-able, slow), TRUNCATE (full "
    "fast reset), and DROP (structural destruction) was verified through live demonstration."
)

# ─── P07 ─────────────────────────────────────────────────────────────────────

P07_THEORY = build_theory_cards([
    ("DML Commands & SELECT Processing",
     "DML (Data Manipulation Language) commands: SELECT retrieves data, INSERT adds rows, UPDATE modifies rows, DELETE removes rows. SELECT executes internally in this order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT. Understanding this order explains why you cannot use SELECT aliases in WHERE clauses but can use them in ORDER BY — aliases don't exist until after the SELECT phase.",
     "primary", "lg:col-span-2"),
    ("WHERE Clause Operators",
     "Comparison: =, !=, >, <, >=, <=. Range: BETWEEN x AND y (inclusive on both ends). Membership: IN (val1, val2) for specific values, NOT IN to exclude. Pattern: LIKE with % (any sequence of characters) and _ (exactly one character). Null checks: IS NULL, IS NOT NULL — using = NULL does NOT work in SQL. Logical: AND, OR, NOT to combine conditions. Operator precedence: NOT > AND > OR.",
     "secondary", ""),
    ("Aggregate Functions & Grouping",
     "COUNT(*) counts all rows, COUNT(col) ignores NULLs. SUM and AVG work on numeric columns. MIN and MAX work on any comparable type. GROUP BY splits rows into groups before aggregation. HAVING filters groups after aggregation — where WHERE filters individual rows before grouping. WITH ROLLUP adds subtotal rows per group and a grand total row at the end.",
     "primary", ""),
    ("Subqueries",
     "A subquery is a SELECT inside another query. Non-correlated subqueries execute once — independent of outer query. Correlated subqueries reference the outer query and execute once per outer row (slower). Subqueries can appear in WHERE (filter), FROM (derived table — must be aliased), or SELECT (scalar value per row). EXISTS returns TRUE if the subquery returns any rows — often faster than IN for large datasets.",
     "secondary", "lg:col-span-2"),
    ("Set Operations",
     "UNION combines results from two SELECT statements, removing duplicates. UNION ALL keeps all rows including duplicates (faster, no deduplication). MySQL 8.0 doesn't natively support INTERSECT or EXCEPT (MINUS) — these must be simulated: INTERSECT via JOIN or IN, EXCEPT via NOT IN or LEFT JOIN WHERE right side IS NULL. Both SELECT statements must have the same number and compatible column types.",
     "primary", ""),
    ("String & Date Functions",
     "String: CONCAT(a, b) joins strings, UPPER/LOWER for case conversion, LENGTH for character count, TRIM removes whitespace, SUBSTRING skips ahead n characters, REPLACE(str, old, new) for substitution. Date: DATE_ADD/DATE_SUB for arithmetic, DATEDIFF for day differences, DATE_FORMAT for custom output, YEAR/MONTH/DAY to extract parts, NOW() for current datetime, CURDATE() for date only.",
     "secondary", "lg:col-span-2"),
])

P07_STEPS = build_steps([
    "Use college_db: USE college_db; and verify the Employee and Department tables have data from P06.",
    "Practice basic SELECT with column selection, DISTINCT, ORDER BY ASC/DESC, and LIMIT.",
    "Filter with WHERE using BETWEEN, IN, NOT IN, LIKE patterns (%, _), IS NULL, IS NOT NULL.",
    "Combine conditions with AND, OR — test operator precedence and use parentheses to clarify intent.",
    "Use aggregate functions: COUNT(*), SUM(Salary), AVG(Salary), MAX(Salary), MIN(Salary) on Employee.",
    "Apply GROUP BY DeptID and HAVING AVG(Salary) > 50000 to filter grouped results.",
    "Use WITH ROLLUP to add subtotals per department and a grand total row.",
    "Write a non-correlated subquery: employees earning above the company average salary.",
    "Write a correlated subquery: find the highest earner in each department.",
    "Use a derived table (subquery in FROM): departments with average salary above 50000.",
    "Practice UNION (removes duplicates) and UNION ALL (keeps duplicates) between two SELECT queries.",
    "Simulate INTERSECT (employees in dept 1 AND earning above 50000) and MINUS using NOT IN.",
])

P07_CODE = """USE college_db;

-- Basic SELECT with all clauses
SELECT EmpName, Salary, DeptID FROM Employee ORDER BY Salary DESC LIMIT 5;

-- DISTINCT: unique department IDs
SELECT DISTINCT DeptID FROM Employee;

-- BETWEEN: salary range
SELECT EmpName, Salary FROM Employee WHERE Salary BETWEEN 45000 AND 65000;

-- IN: specific department IDs
SELECT EmpName, DeptID FROM Employee WHERE DeptID IN (1, 2, 3);

-- NOT IN: exclude departments
SELECT EmpName, DeptID FROM Employee WHERE DeptID NOT IN (4, 5);

-- LIKE patterns
SELECT EmpName FROM Employee WHERE EmpName LIKE 'A%';
SELECT EmpName FROM Employee WHERE EmpName LIKE '%ar%';
SELECT EmpName FROM Employee WHERE EmpName LIKE '_____';

-- NULL checking
SELECT EmpName FROM Employee WHERE Email IS NOT NULL;

-- AND / OR combinations
SELECT EmpName, Salary FROM Employee WHERE DeptID = 1 AND Salary > 50000;
SELECT EmpName FROM Employee WHERE DeptID = 1 OR DeptID = 2;

-- AGGREGATE FUNCTIONS
SELECT COUNT(*) AS Total, SUM(Salary) AS TotalSalary,
       AVG(Salary) AS AvgSalary, MAX(Salary) AS MaxSalary,
       MIN(Salary) AS MinSalary FROM Employee;

-- GROUP BY with HAVING
SELECT DeptID, COUNT(*) AS EmpCount, ROUND(AVG(Salary),2) AS AvgSal
FROM Employee GROUP BY DeptID HAVING AVG(Salary) > 50000;

-- ROLLUP: subtotals per group + grand total
SELECT DeptID, COUNT(*) AS Count, SUM(Salary) AS Total
FROM Employee GROUP BY DeptID WITH ROLLUP;

-- SUBQUERY 1: above company average (non-correlated)
SELECT EmpName, Salary FROM Employee
WHERE Salary > (SELECT AVG(Salary) FROM Employee);

-- SUBQUERY 2: derived table in FROM
SELECT DeptID, AvgSal FROM
    (SELECT DeptID, AVG(Salary) AS AvgSal FROM Employee GROUP BY DeptID) AS DeptAvg
WHERE AvgSal > 50000;

-- SUBQUERY 3: correlated - highest earner per department
SELECT EmpName, Salary, DeptID FROM Employee E1
WHERE Salary = (SELECT MAX(Salary) FROM Employee E2 WHERE E2.DeptID = E1.DeptID);

-- SUBQUERY 4: scalar subquery in SELECT column
SELECT EmpName, Salary,
    (SELECT AVG(Salary) FROM Employee) AS CompanyAvg FROM Employee;

-- SUBQUERY 5: EXISTS
SELECT DeptName FROM Department D
WHERE EXISTS (SELECT 1 FROM Employee E WHERE E.DeptID = D.DeptID);

-- SUBQUERY 6: NOT IN - departments with no employees
SELECT DeptName FROM Department
WHERE DeptID NOT IN (SELECT DISTINCT DeptID FROM Employee);

-- SET OPERATIONS
SELECT EmpName, Salary FROM Employee WHERE Salary > 65000
UNION
SELECT EmpName, Salary FROM Employee WHERE DeptID = 1;

SELECT EmpName FROM Employee WHERE DeptID = 1
UNION ALL
SELECT EmpName FROM Employee WHERE Salary > 55000;

-- INTERSECT simulated (dept 1 AND salary > 50000)
SELECT EmpName FROM Employee WHERE DeptID = 1
AND EmpID IN (SELECT EmpID FROM Employee WHERE Salary > 50000);

-- MINUS (EXCEPT) simulated (dept 1 NOT above 65000)
SELECT EmpName FROM Employee WHERE DeptID = 1
AND EmpID NOT IN (SELECT EmpID FROM Employee WHERE Salary > 65000);

-- STRING FUNCTIONS
SELECT CONCAT(EmpName, ' | Dept: ', DeptID) AS Info FROM Employee;
SELECT UPPER(EmpName), LENGTH(EmpName) AS Len FROM Employee;

-- UPDATE: 10% raise for dept 1
UPDATE Employee SET Salary = Salary * 1.10 WHERE DeptID = 1;

-- DELETE specific rows
DELETE FROM Employee WHERE Salary < 38000;"""

P07_CONCLUSION = (
    "This practical covered the complete DML toolbox through comprehensive SQL queries on the Employee and "
    "Department tables. The internal SELECT execution order (FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY→LIMIT) "
    "was demonstrated and its practical implications understood. WHERE clause operators (BETWEEN, IN, LIKE, IS NULL) "
    "filtered data precisely. Aggregate functions with GROUP BY and HAVING produced meaningful department-level "
    "statistics. Subqueries — non-correlated, correlated, derived table, scalar, EXISTS — demonstrated how "
    "complex business questions can be answered in single SQL statements. UNION and UNION ALL performed set "
    "operations, with INTERSECT and MINUS simulated via IN and NOT IN. UPDATE and DELETE applied targeted "
    "data modifications demonstrating transaction-level operations."
)

# ─── P08 ─────────────────────────────────────────────────────────────────────

P08_THEORY = build_theory_cards([
    ("What is a View?",
     "A View is a virtual table defined by a stored SELECT query. It stores no data itself — every query against a view executes the underlying SELECT and returns the result dynamically. Views simplify complex queries into reusable named objects, enhance security by exposing only specific columns or rows, and provide data abstraction so application code doesn't change when underlying table structures change.",
     "primary", "lg:col-span-2"),
    ("Simple vs Complex Views",
     "Simple Views are based on a single table with no aggregate functions and are generally updatable — INSERT, UPDATE, DELETE through them work. Complex Views involve JOINs, GROUP BY, aggregates, DISTINCT, or subqueries and are NOT updatable. Any attempt to INSERT/UPDATE through a complex view results in Error 1471: The target table of INSERT/UPDATE is not updatable.",
     "secondary", ""),
    ("WITH CHECK OPTION",
     "WITH CHECK OPTION ensures that any INSERT or UPDATE through the view still satisfies the view's WHERE clause — preventing data from being modified in a way that would make it invisible through the view. CASCADED (default) checks all underlying views in the chain. LOCAL only checks the current view's condition. Example: a view WHERE Salary > 50000 with CHECK OPTION blocks UPDATEs that would reduce salary below 50000.",
     "primary", ""),
    ("View Metadata & Management",
     "SHOW FULL TABLES WHERE Table_type = 'VIEW' lists all views in the current database. INFORMATION_SCHEMA.VIEWS table contains view metadata including VIEW_DEFINITION, IS_UPDATABLE, and SECURITY_TYPE. SHOW CREATE VIEW viewname displays the exact DDL. CREATE OR REPLACE VIEW updates a view definition without dropping it — prevents dependent objects from breaking.",
     "secondary", "lg:col-span-2"),
    ("MySQL Materialized Views",
     "MySQL does not natively support Materialized Views (pre-computed, physically stored result sets like Oracle or PostgreSQL). The workaround: create a regular table, populate it with a query result using INSERT...SELECT, and refresh it periodically via a scheduled EVENT or TRIGGER. This trades storage space for query speed on expensive aggregations.",
     "primary", ""),
    ("View Performance & Security",
     "Views on indexed columns with simple filtering perform well. Views with GROUP BY, complex JOINs, or DISTINCT can be slow — MySQL may not optimize view queries as effectively as direct queries. For security, grant SELECT on a view but not on the underlying tables — users can query the view but cannot access raw sensitive data (e.g., hiding salary columns from public view). Revoke direct table access after creating security views.",
     "secondary", "lg:col-span-2"),
])

P08_STEPS = build_steps([
    "Use college_db database: USE college_db; Verify Employee and Department tables from P06 are populated.",
    "Create a simple view: IT_Employees that shows only employees from DeptID = 1.",
    "Query the simple view with SELECT * FROM IT_Employees; and verify it shows only IT employees.",
    "Create a complex JOIN view: Employee_Full_Details joining Employee and Department tables.",
    "Query the JOIN view with a WHERE filter to find high-salary employees in specific departments.",
    "Create an aggregate view: Department_Summary with COUNT, AVG, SUM, MAX, MIN salary by department.",
    "Query the aggregate view and ORDER BY TotalSalaryBill DESC to rank departments by cost.",
    "Create a security view: Employee_Public_Info hiding the Salary column.",
    "Create an updatable view with WITH CHECK OPTION and demonstrate a valid update that satisfies the filter.",
    "Attempt an update that would violate WITH CHECK OPTION — observe the error.",
    "Use CREATE OR REPLACE VIEW to modify IT_Employees to add the Gender column without dropping it.",
    "Inspect view metadata using INFORMATION_SCHEMA.VIEWS and SHOW CREATE VIEW, then DROP a view.",
])

P08_CODE = """USE college_db;

-- Simple View: IT department employees only
CREATE VIEW IT_Employees AS
SELECT EmpID, EmpName, Salary, Email
FROM Employee WHERE DeptID = 1;

SELECT * FROM IT_Employees;

-- Complex View: JOIN employees with department details
CREATE VIEW Employee_Full_Details AS
SELECT E.EmpID, E.EmpName, E.Salary, E.Gender, E.Email,
       D.DeptName, D.Location, D.Budget
FROM Employee E
INNER JOIN Department D ON E.DeptID = D.DeptID;

SELECT * FROM Employee_Full_Details WHERE Salary > 50000;

-- Aggregate View: department salary statistics
CREATE VIEW Department_Summary AS
SELECT D.DeptName,
       COUNT(E.EmpID) AS TotalEmployees,
       ROUND(AVG(E.Salary), 2) AS AvgSalary,
       SUM(E.Salary) AS TotalSalaryBill,
       MAX(E.Salary) AS TopSalary,
       MIN(E.Salary) AS LowestSalary
FROM Department D
LEFT JOIN Employee E ON D.DeptID = E.DeptID
GROUP BY D.DeptName, D.DeptID;

SELECT * FROM Department_Summary ORDER BY TotalSalaryBill DESC;

-- Security View: hide salary from public access
CREATE VIEW Employee_Public_Info AS
SELECT EmpID, EmpName, Gender, Email, DeptID
FROM Employee;

-- Updatable View with WITH CHECK OPTION
CREATE VIEW HighSalary_Employees AS
SELECT EmpID, EmpName, Salary, DeptID
FROM Employee
WHERE Salary > 50000
WITH CHECK OPTION;

-- Valid update: salary stays above 50000 check
UPDATE HighSalary_Employees SET Salary = 72000 WHERE EmpID = 3;

-- This would FAIL with CHECK OPTION violation:
-- UPDATE HighSalary_Employees SET Salary = 25000 WHERE EmpID = 3;
-- ERROR 1369: CHECK OPTION failed 'college_db.HighSalary_Employees'

-- Update view definition without dropping it
CREATE OR REPLACE VIEW IT_Employees AS
SELECT EmpID, EmpName, Salary, Email, Gender
FROM Employee WHERE DeptID = 1;

-- View metadata from information schema
SELECT TABLE_NAME AS ViewName,
       IS_UPDATABLE,
       SECURITY_TYPE
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = 'college_db';

-- Show the DDL of a specific view
SHOW CREATE VIEW Department_Summary;

-- List all views in current database
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- Drop a view that is no longer needed
DROP VIEW IF EXISTS Employee_Public_Info;

-- Verify remaining views
SHOW FULL TABLES WHERE Table_type = 'VIEW';"""

P08_CONCLUSION = (
    "This practical demonstrated the full lifecycle of views in MySQL — creation, querying, modification, "
    "metadata inspection, and deletion. Simple views on single tables proved to be updatable, while the "
    "complex aggregate view (GROUP BY) was correctly identified as not updatable. WITH CHECK OPTION successfully "
    "prevented updates that would have caused rows to disappear from the view's filtered result set. "
    "Security views hiding the Salary column demonstrated how view-based access control protects sensitive "
    "data — users granted SELECT on the public view cannot see salaries even if they know the table exists. "
    "CREATE OR REPLACE VIEW was used to evolve a view definition seamlessly. INFORMATION_SCHEMA.VIEWS provided "
    "programmatic access to view metadata for documentation purposes."
)

# ─── P09 ─────────────────────────────────────────────────────────────────────

P09_THEORY = build_theory_cards([
    ("Why JOINs?",
     "A JOIN combines rows from two or more tables based on a related column — typically a foreign key. Without JOINs, relational databases would be impractical since normalized data is split across tables to reduce redundancy. JOINs re-assemble this data at query time. Always index JOIN columns (foreign keys are usually auto-indexed). Proper JOINs on indexed columns run in O(log n) time; without indexes they degrade to O(n²) Cartesian product scans.",
     "primary", "lg:col-span-2"),
    ("INNER vs OUTER JOINs",
     "INNER JOIN returns only rows where the join condition matches in BOTH tables — excluded rows have no match on either side. LEFT JOIN (LEFT OUTER) returns ALL rows from the left table plus matching rows from the right; unmatched right-side columns are NULL. RIGHT JOIN is the mirror. FULL OUTER JOIN returns all rows from both tables with NULLs where no match exists — MySQL requires UNION of LEFT and RIGHT to simulate this.",
     "secondary", ""),
    ("SELF JOIN & CROSS JOIN",
     "SELF JOIN joins a table with itself — used for hierarchical data (employee-manager), org charts, or comparing rows within the same table. The table must be aliased twice to create two distinct copies. CROSS JOIN produces the Cartesian product — every row from the left paired with every row from the right, resulting in M×N rows. Useful for generating combinations, test data, or calendar grids, but can produce massive datasets — always add WHERE or LIMIT.",
     "primary", ""),
    ("JOIN Performance",
     "EXPLAIN statement shows the query execution plan. Key fields: type (ALL=full table scan=bad; ref, range, eq_ref=index used=good), key (which index was chosen), rows (estimated rows examined), Extra (Using index=fast, Using filesort=slow). Always index FK columns used in JOINs. The query optimizer chooses join order — you can hint with STRAIGHT_JOIN if needed. Avoid joining on functions like WHERE UPPER(col)=x — this prevents index use.",
     "secondary", "lg:col-span-2"),
    ("Non-Equi JOINs",
     "Most JOINs use equality (ON A.id = B.id) — called equi-joins. Non-equi joins use other operators: ON A.Salary BETWEEN B.MinSalary AND B.MaxSalary for salary band lookups, ON A.Date >= B.StartDate AND A.Date <= B.EndDate for date range matching. These are less common but important for complex business logic like mapping transactions to fiscal periods or classifying records into salary bands.",
     "primary", "lg:col-span-2"),
])

P09_STEPS = build_steps([
    "Use college_db: USE college_db; Ensure Employee and Department tables are populated from P06.",
    "Add ManagerID column to Employee for SELF JOIN demo: ALTER TABLE Employee ADD COLUMN ManagerID INT;",
    "Update some employees to assign them managers: UPDATE Employee SET ManagerID = 1 WHERE EmpID IN (2,3,4,5,6);",
    "Create a Project table with DeptID FK to demonstrate 3-table joins.",
    "Insert 5 project records, one per department.",
    "Practice INNER JOIN: Employee INNER JOIN Department — verify only employees with valid DeptID appear.",
    "Practice LEFT JOIN: Department LEFT JOIN Employee — verify ALL departments appear even if empty.",
    "Practice RIGHT JOIN: Department RIGHT JOIN Employee — verify ALL employees appear.",
    "Simulate FULL OUTER JOIN using UNION of LEFT and RIGHT JOIN queries.",
    "Practice SELF JOIN: Employee E JOIN Employee M ON E.ManagerID = M.EmpID to see employee-manager pairs.",
    "Practice CROSS JOIN on a small subset — observe the Cartesian product row count (M × N).",
    "Write a 3-table JOIN: Employee + Department + Project in a single query.",
])

P09_CODE = """USE college_db;

-- Add ManagerID for SELF JOIN demonstration
ALTER TABLE Employee ADD COLUMN ManagerID INT;
UPDATE Employee SET ManagerID = 1 WHERE EmpID IN (2,3,4,5,6);
UPDATE Employee SET ManagerID = 2 WHERE EmpID IN (7,8,9);
UPDATE Employee SET ManagerID = 3 WHERE EmpID IN (10,11,12);

-- Create Projects table
CREATE TABLE IF NOT EXISTS Project (
    ProjectID INT PRIMARY KEY AUTO_INCREMENT,
    ProjectName VARCHAR(100) NOT NULL,
    Budget DECIMAL(12,2),
    DeptID INT,
    FOREIGN KEY (DeptID) REFERENCES Department(DeptID)
);

INSERT INTO Project (ProjectName, Budget, DeptID) VALUES
('ERP System', 500000, 1), ('HR Portal', 200000, 2),
('Budget Tracker', 350000, 3), ('Campaign Manager', 150000, 4),
('Ops Dashboard', 400000, 1);

-- INNER JOIN: matched rows only
SELECT E.EmpName, E.Salary, D.DeptName, D.Location
FROM Employee E
INNER JOIN Department D ON E.DeptID = D.DeptID
ORDER BY D.DeptName;

-- LEFT JOIN: ALL departments including those with no employees
SELECT D.DeptName, E.EmpName, E.Salary
FROM Department D
LEFT JOIN Employee E ON D.DeptID = E.DeptID
ORDER BY D.DeptName;

-- RIGHT JOIN: ALL employees regardless of department existence
SELECT D.DeptName, E.EmpName, E.Salary
FROM Department D
RIGHT JOIN Employee E ON D.DeptID = E.DeptID;

-- FULL OUTER JOIN simulated with UNION
SELECT D.DeptName, E.EmpName
FROM Department D LEFT JOIN Employee E ON D.DeptID = E.DeptID
UNION
SELECT D.DeptName, E.EmpName
FROM Department D RIGHT JOIN Employee E ON D.DeptID = E.DeptID;

-- SELF JOIN: employee and their manager
SELECT E.EmpName AS Employee, M.EmpName AS Manager,
       E.Salary AS EmpSalary
FROM Employee E
LEFT JOIN Employee M ON E.ManagerID = M.EmpID
ORDER BY M.EmpName;

-- CROSS JOIN: all employee-project pairings (Cartesian product)
SELECT E.EmpName, P.ProjectName
FROM Employee E CROSS JOIN Project P
ORDER BY E.EmpName LIMIT 20;

-- 3-TABLE JOIN: Employee + Department + Project
SELECT E.EmpName, D.DeptName, P.ProjectName, P.Budget
FROM Employee E
JOIN Department D ON E.DeptID = D.DeptID
JOIN Project P ON D.DeptID = P.DeptID
ORDER BY D.DeptName;

-- JOIN with WHERE filter
SELECT E.EmpName, D.DeptName, E.Salary
FROM Employee E JOIN Department D ON E.DeptID = D.DeptID
WHERE E.Salary > 55000 AND D.DeptName = 'Information Technology';

-- JOIN with GROUP BY aggregate
SELECT D.DeptName,
       COUNT(E.EmpID) AS Headcount,
       ROUND(AVG(E.Salary),2) AS AvgSalary,
       SUM(E.Salary) AS SalaryBill
FROM Department D
LEFT JOIN Employee E ON D.DeptID = E.DeptID
GROUP BY D.DeptName
ORDER BY SalaryBill DESC;"""

P09_CONCLUSION = (
    "This practical covered all major JOIN types through practical demonstration on the Employee, Department, "
    "and Project tables. INNER JOIN efficiently retrieved only matched rows, LEFT JOIN revealed departments "
    "with no employees (returning NULLs for unmatched Employee columns), and FULL OUTER JOIN was successfully "
    "simulated using UNION of LEFT and RIGHT JOINs. SELF JOIN elegantly modeled the employee-manager hierarchy "
    "by aliasing the Employee table twice. CROSS JOIN demonstrated the Cartesian product and its potential for "
    "data explosion without proper filtering. The 3-table JOIN demonstrated how complex real-world queries "
    "combine multiple relationships in a single readable SQL statement. JOIN performance considerations "
    "including index usage and EXPLAIN analysis were also explored."
)

# ─── P10 ─────────────────────────────────────────────────────────────────────

P10_THEORY = build_theory_cards([
    ("Stored Procedures",
     "A Stored Procedure is a named, precompiled block of SQL statements stored in the database and executed by calling its name with CALL. Benefits: reduced network traffic (only CALL travels over network vs full SQL), precompiled and cached (faster execution), improved security (users can EXECUTE without table access), and code reuse across multiple applications. DELIMITER $$ changes the end-of-statement marker so MySQL doesn't misinterpret semicolons inside the procedure body.",
     "primary", "lg:col-span-2"),
    ("Parameter Types",
     "IN parameters pass values into the procedure (read-only inside — cannot be modified). OUT parameters return values from the procedure to the caller (write-only inside — must be user variables to read after CALL). INOUT parameters both accept input and return a modified value. Local variables are declared with DECLARE inside BEGIN...END and assigned with SET or SELECT...INTO. User session variables start with @ and persist for the session.",
     "secondary", ""),
    ("Control Flow",
     "IF...ELSEIF...ELSE provides conditional branching. CASE...WHEN provides multi-way branching (like a switch statement). WHILE loop runs while condition is TRUE. REPEAT...UNTIL executes at least once, then checks condition — runs until condition becomes TRUE. LOOP with LEAVE provides manual loop control. ITERATE skips to the next iteration (like continue). LEAVE exits a loop or block immediately (like break).",
     "primary", ""),
    ("User-Defined Functions (UDFs)",
     "Functions differ from procedures: they MUST return a single scalar value using RETURN, can be used directly in SELECT statements and WHERE clauses, cannot use transactions, must be declared DETERMINISTIC (same inputs always give same output) or NOT DETERMINISTIC. READS SQL DATA / MODIFIES SQL DATA is required when binary logging is enabled. Drop functions with DROP FUNCTION IF EXISTS.",
     "secondary", "lg:col-span-2"),
    ("Error Handling",
     "DECLARE CONTINUE HANDLER FOR condition action — catches the condition and continues executing. DECLARE EXIT HANDLER FOR condition action — catches and exits the current block. SQLEXCEPTION catches any SQL error. SQLWARNING catches warnings. NOT FOUND catches when no rows returned. Specific SQLSTATE '23000' targets duplicate key errors. Pair error handlers with transaction rollbacks for safe multi-step operations.",
     "primary", ""),
    ("SHOW Procedure Information",
     "SHOW PROCEDURE STATUS WHERE Db = 'dbname' lists all procedures with creation time, type, and definer. SHOW CREATE PROCEDURE procname shows the full DDL. INFORMATION_SCHEMA.ROUTINES contains all procedure and function metadata. DROP PROCEDURE IF EXISTS procname drops a procedure safely. Procedures can be called from application code (JDBC, PHP PDO, Python) using CallableStatement or similar APIs.",
     "secondary", "lg:col-span-2"),
])

P10_STEPS = build_steps([
    "Use college_db: USE college_db; Set DELIMITER to $$ to avoid conflicts inside procedure bodies.",
    "Create Procedure 1 (IN parameter): GetEmployeesByDept that accepts a DeptID and returns all employees.",
    "CALL GetEmployeesByDept(1) and verify it returns only IT department employees sorted by salary.",
    "Create Procedure 2 (OUT parameters): GetDeptStats returning employee count, average, and maximum salary.",
    "CALL GetDeptStats(1, @cnt, @avg, @max) then SELECT @cnt, @avg, @max to display results.",
    "Create Procedure 3 (INOUT): ApplyBonus that accepts a salary and percentage and modifies the salary variable.",
    "Create Procedure 4 with IF-ELSEIF-ELSE: GetEmpGrade that categorizes employees as Junior/Mid/Senior/Executive.",
    "Create Procedure 5 with WHILE loop: SalaryProjection that calculates salary growth over N years at 8% annually using a TEMPORARY TABLE.",
    "Reset DELIMITER back to semicolon after all procedures: DELIMITER ;",
    "Create Function 1: CalcTax(salary) applying 10/20/30% tax brackets — use in SELECT directly.",
    "Create Function 2: ExperienceLevel(joinDate) returning 'Fresher'/'Intermediate'/'Experienced'/'Veteran'.",
    "Create a procedure with error handling using EXIT HANDLER and demonstrate safe vs unsafe inserts.",
])

P10_CODE = """USE college_db;
DELIMITER $$

-- PROCEDURE 1: IN parameter - employees by department
CREATE PROCEDURE GetEmployeesByDept(IN p_DeptID INT)
BEGIN
    SELECT EmpID, EmpName, Salary, Email
    FROM Employee WHERE DeptID = p_DeptID ORDER BY Salary DESC;
END$$
CALL GetEmployeesByDept(1)$$

-- PROCEDURE 2: OUT parameters - department statistics
CREATE PROCEDURE GetDeptStats(
    IN p_DeptID INT,
    OUT p_Count INT,
    OUT p_AvgSalary DECIMAL(10,2),
    OUT p_MaxSalary DECIMAL(10,2)
)
BEGIN
    SELECT COUNT(*), ROUND(AVG(Salary),2), MAX(Salary)
    INTO p_Count, p_AvgSalary, p_MaxSalary
    FROM Employee WHERE DeptID = p_DeptID;
END$$
CALL GetDeptStats(1, @cnt, @avg, @max)$$
SELECT @cnt AS Count, @avg AS AvgSalary, @max AS MaxSalary$$

-- PROCEDURE 3: INOUT - apply salary bonus
CREATE PROCEDURE ApplyBonus(INOUT p_Salary DECIMAL(10,2), IN p_Percent DECIMAL(5,2))
BEGIN
    SET p_Salary = p_Salary + (p_Salary * p_Percent / 100);
END$$
SET @sal = 50000$$
CALL ApplyBonus(@sal, 15)$$
SELECT @sal AS SalaryAfter15PctBonus$$

-- PROCEDURE 4: IF-ELSEIF-ELSE salary grading
CREATE PROCEDURE GetEmpGrade(IN p_EmpID INT)
BEGIN
    DECLARE v_Salary DECIMAL(10,2);
    DECLARE v_Grade VARCHAR(20);
    DECLARE v_Name VARCHAR(100);
    SELECT EmpName, Salary INTO v_Name, v_Salary
    FROM Employee WHERE EmpID = p_EmpID;
    IF v_Salary >= 70000 THEN SET v_Grade = 'A - Executive';
    ELSEIF v_Salary >= 55000 THEN SET v_Grade = 'B - Senior';
    ELSEIF v_Salary >= 40000 THEN SET v_Grade = 'C - Mid-Level';
    ELSE SET v_Grade = 'D - Junior';
    END IF;
    SELECT v_Name AS Name, v_Salary AS Salary, v_Grade AS Grade;
END$$
CALL GetEmpGrade(5)$$

-- PROCEDURE 5: WHILE LOOP - salary projection 5 years at 8% growth
CREATE PROCEDURE SalaryProjection(IN p_EmpID INT, IN p_Years INT)
BEGIN
    DECLARE v_Year INT DEFAULT 1;
    DECLARE v_Salary DECIMAL(10,2);
    SELECT Salary INTO v_Salary FROM Employee WHERE EmpID = p_EmpID;
    DROP TEMPORARY TABLE IF EXISTS Projection;
    CREATE TEMPORARY TABLE Projection (Year INT, Salary DECIMAL(10,2));
    WHILE v_Year <= p_Years DO
        SET v_Salary = ROUND(v_Salary * 1.08, 2);
        INSERT INTO Projection VALUES (v_Year, v_Salary);
        SET v_Year = v_Year + 1;
    END WHILE;
    SELECT * FROM Projection;
END$$
CALL SalaryProjection(1, 5)$$

-- FUNCTION 1: Income tax calculation
CREATE FUNCTION CalcTax(p_Salary DECIMAL(10,2))
RETURNS DECIMAL(10,2) DETERMINISTIC
BEGIN
    IF p_Salary > 80000 THEN RETURN ROUND(p_Salary * 0.30, 2);
    ELSEIF p_Salary > 50000 THEN RETURN ROUND(p_Salary * 0.20, 2);
    ELSE RETURN ROUND(p_Salary * 0.10, 2);
    END IF;
END$$

SELECT EmpName, Salary, CalcTax(Salary) AS TaxAmount,
       Salary - CalcTax(Salary) AS TakeHome FROM Employee$$

-- FUNCTION 2: Experience level from join date
CREATE FUNCTION ExperienceLevel(p_JoinDate DATE)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE v_Years INT;
    SET v_Years = TIMESTAMPDIFF(YEAR, p_JoinDate, CURDATE());
    IF v_Years >= 10 THEN RETURN 'Veteran';
    ELSEIF v_Years >= 5 THEN RETURN 'Experienced';
    ELSEIF v_Years >= 2 THEN RETURN 'Intermediate';
    ELSE RETURN 'Fresher';
    END IF;
END$$

SELECT EmpName, JoinDate, ExperienceLevel(JoinDate) AS Level FROM Employee$$

-- PROCEDURE WITH EXIT HANDLER
CREATE PROCEDURE SafeInsert(IN p_Name VARCHAR(100), IN p_Salary DECIMAL(10,2), IN p_DeptID INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Insert failed: constraint violation or invalid data' AS Error;
    END;
    START TRANSACTION;
    INSERT INTO Employee (EmpName, Salary, Gender, DeptID)
    VALUES (p_Name, p_Salary, 'Male', p_DeptID);
    COMMIT;
    SELECT CONCAT(p_Name, ' added successfully') AS Status;
END$$
CALL SafeInsert('Valid Employee', 45000, 1)$$
CALL SafeInsert('Bad Employee', 1000, 99)$$

DELIMITER ;
SHOW PROCEDURE STATUS WHERE Db = 'college_db';"""

P10_CONCLUSION = (
    "This practical demonstrated the complete spectrum of stored procedure and user-defined function "
    "capabilities in MySQL. Procedures with IN, OUT, and INOUT parameters gave flexibility in data passing — "
    "OUT parameters proved essential for returning multiple computed values from a single CALL. Control flow "
    "constructs (IF-ELSEIF-ELSE, WHILE loop) transformed procedures from simple data retrievers to "
    "computation engines with business logic. The SalaryProjection procedure used a TEMPORARY TABLE to "
    "accumulate and return row-by-row computed results. User-defined functions CalcTax and ExperienceLevel "
    "were embedded directly in SELECT statements, demonstrating their advantage over procedures for "
    "column-level calculations. Error handling with EXIT HANDLER and ROLLBACK ensured atomicity for "
    "multi-step inserts, preventing partial data corruption."
)

# ─── P11 ─────────────────────────────────────────────────────────────────────

P11_THEORY = build_theory_cards([
    ("What is a Trigger?",
     "A Trigger is a database object that automatically executes a predefined SQL block in response to INSERT, UPDATE, or DELETE events on a table. Triggers enforce business rules at the database level, ensuring rules apply regardless of which application or user modifies data. Six trigger types: BEFORE INSERT, AFTER INSERT, BEFORE UPDATE, AFTER UPDATE, BEFORE DELETE, AFTER DELETE.",
     "primary", "lg:col-span-2"),
    ("NEW and OLD Pseudo-Records",
     "Inside triggers: NEW represents the new row values for INSERT and UPDATE — available in BEFORE and AFTER INSERT/UPDATE triggers. OLD represents the previous row values for UPDATE and DELETE — available in BEFORE and AFTER UPDATE/DELETE. In BEFORE triggers, you can MODIFY NEW values (auto-format, calculate derived fields). In AFTER triggers, you can only READ OLD and NEW — cannot modify the triggering row.",
     "secondary", ""),
    ("SIGNAL: Custom Error Validation",
     "SIGNAL SQLSTATE '45000' raises a custom application-level error from inside a trigger, aborting the DML operation. The MESSAGE_TEXT is returned to the client. SQLSTATE '45000' is the generic 'unhandled user-defined exception' code — values like '23000' (duplicate key), '22001' (data too long) are MySQL-defined. SIGNAL is how BEFORE triggers prevent invalid data without a CHECK constraint.",
     "primary", ""),
    ("Audit Logging",
     "Audit logging is the most common real-world trigger use case. An audit table records WHO changed WHAT and WHEN. USER() inside a trigger captures the MySQL username performing the operation. CURRENT_TIMESTAMP captures the time. OLD.* and NEW.* capture before and after values. Organizations use audit logs to meet compliance requirements — SOX (financial), HIPAA (healthcare), GDPR (personal data).",
     "secondary", "lg:col-span-2"),
    ("Trigger Limitations",
     "MySQL allows only ONE trigger per event-timing combination per table (one BEFORE INSERT trigger per table). Workaround: call a stored procedure from the trigger. TRUNCATE does NOT fire row-level triggers (only row INSERT/UPDATE/DELETE). Triggers cannot call COMMIT or ROLLBACK directly. Recursive triggers (trigger modifying its own table) are disabled by default to prevent infinite loops — controlled by innodb_unsafe_for_binlog.",
     "primary", ""),
    ("Trigger Performance",
     "Triggers add overhead to every DML operation — AFTER triggers on high-write tables can significantly impact throughput. Minimize trigger code complexity: avoid complex queries, cursors, or loops inside triggers. AFTER INSERT audit logging is generally acceptable overhead. For bulk operations (LOAD DATA INFILE, large INSERT...SELECT), consider disabling triggers temporarily or using batch-based audit solutions instead.",
     "secondary", "lg:col-span-2"),
])

P11_STEPS = build_steps([
    "Use college_db: USE college_db; Create an Employee_Audit table to log all DML changes with old/new values and timestamp.",
    "Set DELIMITER to $$ before creating triggers.",
    "Create BEFORE INSERT trigger: validate Salary >= 15000 using SIGNAL, auto-format EmpName to Title Case.",
    "Create AFTER INSERT trigger: log new employee details to Employee_Audit table.",
    "Create BEFORE UPDATE trigger: prevent salary reduction using SIGNAL, auto-update JoinDate on department transfer.",
    "Create AFTER UPDATE trigger: log all field changes (old vs new values) to Employee_Audit.",
    "Create BEFORE DELETE trigger: protect high earners (Salary > 90000) from deletion using SIGNAL.",
    "Create AFTER DELETE trigger: log deleted employee details to Employee_Audit.",
    "Reset DELIMITER to semicolon.",
    "Test BEFORE INSERT trigger: insert 'rAHUL sharma' and verify name is auto-formatted to 'Rahul Sharma'.",
    "Test AFTER UPDATE trigger: update Rahul's salary and verify the audit log captures old and new salary.",
    "Test BEFORE DELETE protection: attempt to delete a high-earner — observe rejection. Delete Rahul — verify audit log.",
])

P11_CODE = """USE college_db;
DELIMITER $$

-- Audit table to log all DML changes on Employee
CREATE TABLE IF NOT EXISTS Employee_Audit (
    AuditID INT PRIMARY KEY AUTO_INCREMENT,
    EmpID INT,
    Action VARCHAR(10) NOT NULL,
    OldName VARCHAR(100), NewName VARCHAR(100),
    OldSalary DECIMAL(10,2), NewSalary DECIMAL(10,2),
    OldDeptID INT, NewDeptID INT,
    ChangedBy VARCHAR(100),
    ChangedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    Notes TEXT
);

-- TRIGGER 1: BEFORE INSERT - validate and auto-format name
CREATE TRIGGER trg_before_insert_emp
BEFORE INSERT ON Employee FOR EACH ROW
BEGIN
    IF NEW.Salary < 15000 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Salary must be at least 15000';
    END IF;
    SET NEW.EmpName = CONCAT(UPPER(LEFT(NEW.EmpName,1)),
                             LOWER(SUBSTRING(NEW.EmpName,2)));
END$$

-- TRIGGER 2: AFTER INSERT - log new employee
CREATE TRIGGER trg_after_insert_emp
AFTER INSERT ON Employee FOR EACH ROW
BEGIN
    INSERT INTO Employee_Audit (EmpID, Action, NewName, NewSalary, NewDeptID, ChangedBy)
    VALUES (NEW.EmpID, 'INSERT', NEW.EmpName, NEW.Salary, NEW.DeptID, USER());
END$$

-- TRIGGER 3: BEFORE UPDATE - prevent salary decrease, update JoinDate on dept transfer
CREATE TRIGGER trg_before_update_emp
BEFORE UPDATE ON Employee FOR EACH ROW
BEGIN
    IF NEW.Salary < OLD.Salary THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Salary cannot be reduced';
    END IF;
    IF NEW.DeptID != OLD.DeptID THEN
        SET NEW.JoinDate = CURDATE();
    END IF;
END$$

-- TRIGGER 4: AFTER UPDATE - log all changes
CREATE TRIGGER trg_after_update_emp
AFTER UPDATE ON Employee FOR EACH ROW
BEGIN
    INSERT INTO Employee_Audit (EmpID, Action, OldName, NewName,
        OldSalary, NewSalary, OldDeptID, NewDeptID, ChangedBy)
    VALUES (NEW.EmpID, 'UPDATE', OLD.EmpName, NEW.EmpName,
        OLD.Salary, NEW.Salary, OLD.DeptID, NEW.DeptID, USER());
END$$

-- TRIGGER 5: BEFORE DELETE - protect executives
CREATE TRIGGER trg_before_delete_emp
BEFORE DELETE ON Employee FOR EACH ROW
BEGIN
    IF OLD.Salary > 90000 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete employee with salary above 90000';
    END IF;
END$$

-- TRIGGER 6: AFTER DELETE - log deletion
CREATE TRIGGER trg_after_delete_emp
AFTER DELETE ON Employee FOR EACH ROW
BEGIN
    INSERT INTO Employee_Audit (EmpID, Action, OldName, OldSalary, OldDeptID, ChangedBy)
    VALUES (OLD.EmpID, 'DELETE', OLD.EmpName, OLD.Salary, OLD.DeptID, USER());
END$$

DELIMITER ;

-- TEST: Valid insert (name auto-formatted by BEFORE INSERT trigger)
INSERT INTO Employee (EmpName, Salary, Gender, DeptID)
VALUES ('rAHUL sharma', 35000, 'Male', 1);

-- View audit log after insert
SELECT * FROM Employee_Audit;

-- TEST: Valid salary update (above previous salary)
UPDATE Employee SET Salary = 60000 WHERE EmpName = 'Rahul Sharma';
SELECT * FROM Employee_Audit ORDER BY ChangedAt DESC LIMIT 5;

-- TEST: Delete employee (triggers AFTER DELETE audit log)
DELETE FROM Employee WHERE EmpName = 'Rahul Sharma';
SELECT * FROM Employee_Audit ORDER BY AuditID DESC LIMIT 5;

-- TEST invalid salary (BEFORE INSERT blocks this):
-- INSERT INTO Employee (EmpName, Salary, Gender, DeptID) VALUES ('Test', 5000, 'Male', 1);
-- ERROR 1644: Salary must be at least 15000

-- Show all triggers in the database
SHOW TRIGGERS FROM college_db;"""

P11_CONCLUSION = (
    "This practical demonstrated all six trigger types (BEFORE/AFTER INSERT, UPDATE, DELETE) through a "
    "comprehensive audit logging system on the Employee table. BEFORE INSERT trigger auto-formatted names to "
    "Title Case and validated salary using SIGNAL to abort invalid inserts — proving database-level data "
    "quality enforcement independent of application code. AFTER INSERT/UPDATE/DELETE triggers populated the "
    "Employee_Audit table with complete change history including old values, new values, the MySQL user, "
    "and timestamp — meeting audit trail requirements for compliance. BEFORE UPDATE prevented salary reductions "
    "and auto-updated JoinDate on department transfers. BEFORE DELETE protected high-value employees from "
    "accidental deletion. The audit log created a complete, tamper-evident history of all DML operations "
    "on the Employee table."
)

# ─── P12 ─────────────────────────────────────────────────────────────────────

P12_THEORY = build_theory_cards([
    ("What is a Cursor?",
     "A Cursor is a database object that allows row-by-row processing of a query result set inside stored procedures. Standard SQL is set-based — it operates on all rows at once. Cursors provide procedural row-by-row access when business logic requires per-row decision-making with conditional branching or accumulation that cannot be expressed as a single set operation.",
     "primary", "lg:col-span-2"),
    ("Cursor Lifecycle",
     "Four mandatory stages: DECLARE defines the cursor with a SELECT statement (not yet executed). OPEN executes the SELECT and positions the cursor before the first row. FETCH moves to the next row and reads values into declared variables. CLOSE releases the cursor and associated memory. Always close cursors — open cursors consume server memory. Declare cursors AFTER variable declarations but BEFORE handlers.",
     "secondary", ""),
    ("NOT FOUND Handler",
     "When FETCH tries to move past the last row, MySQL raises a NOT FOUND condition (SQLSTATE '02000'). A DECLARE CONTINUE HANDLER FOR NOT FOUND SET done_flag = 1 catches this and sets a flag variable, allowing the loop to check the flag and exit with LEAVE. Without this handler, the procedure throws an error when the cursor is exhausted. The handler must be declared AFTER the cursor declaration.",
     "primary", ""),
    ("When to Use Cursors",
     "Use cursors ONLY when the logic genuinely requires per-row decision-making that cannot be expressed as a single set operation. Prefer set-based SQL (UPDATE with CASE, INSERT...SELECT) whenever possible. Valid cursor use cases: complex per-row calculations with branching, sending individual email notifications, applying business rules that differ per row based on external state, generating reports with running totals that reset per group.",
     "secondary", "lg:col-span-2"),
    ("Cursor Performance Warning",
     "Cursors are significantly slower than set-based SQL — they execute one row at a time, involve repeated server context switches, and cannot use bulk operation optimizations. On a table with 1 million rows, a cursor-based procedure can take minutes where the equivalent set-based SQL takes seconds. Always benchmark and prefer UPDATE/INSERT...SELECT. Use cursors as a last resort for complex procedural logic.",
     "primary", ""),
    ("Multiple Cursors",
     "MySQL supports multiple cursors in a single procedure — each must be independently declared, opened, fetched, and closed. Nested cursors (one cursor's loop contains another cursor's OPEN/FETCH/CLOSE) are supported but must be carefully managed — inner cursor must be closed before the outer cursor fetches the next row if they share table access. Nested cursor loops greatly amplify the performance penalty.",
     "secondary", "lg:col-span-2"),
])

P12_STEPS = build_steps([
    "Use college_db: USE college_db; Set DELIMITER to $$",
    "Create the first cursor procedure: CategorizeAllEmployees — declare variables for all cursor columns.",
    "Declare the cursor with SELECT EmpID, EmpName, Salary, DeptID FROM Employee ORDER BY DeptID.",
    "Declare the CONTINUE HANDLER FOR NOT FOUND to set the done flag when cursor is exhausted.",
    "Create a TEMPORARY TABLE EmpReport to accumulate categorized results.",
    "OPEN the cursor, run the LOOP, FETCH each row, apply IF-ELSEIF logic for category (Junior/Mid-Level/Senior/Executive), INSERT into EmpReport.",
    "Add the done_flag check inside the loop — IF v_Done THEN LEAVE process_loop; END IF",
    "CLOSE the cursor after the loop and SELECT from EmpReport to display results.",
    "Add a second SELECT with GROUP BY Category to show the category distribution.",
    "Create the second cursor procedure: DeptRunningTotal — reset running total when department changes.",
    "Reset DELIMITER and CALL both procedures to test and verify output.",
    "Discuss the performance implications and when set-based alternatives would be better.",
])

P12_CODE = """USE college_db;
DELIMITER $$

-- CURSOR 1: Categorize all employees by salary band
CREATE PROCEDURE CategorizeAllEmployees()
BEGIN
    DECLARE v_EmpID INT;
    DECLARE v_Name VARCHAR(100);
    DECLARE v_Salary DECIMAL(10,2);
    DECLARE v_DeptID INT;
    DECLARE v_Category VARCHAR(30);
    DECLARE v_Done INT DEFAULT FALSE;

    -- Declare cursor AFTER variable declarations
    DECLARE emp_cursor CURSOR FOR
        SELECT EmpID, EmpName, Salary, DeptID
        FROM Employee ORDER BY DeptID, Salary DESC;

    -- NOT FOUND handler AFTER cursor declaration
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_Done = TRUE;

    DROP TEMPORARY TABLE IF EXISTS EmpReport;
    CREATE TEMPORARY TABLE EmpReport (
        EmpID INT, Name VARCHAR(100),
        Salary DECIMAL(10,2), DeptID INT, Category VARCHAR(30)
    );

    OPEN emp_cursor;

    process_loop: LOOP
        FETCH emp_cursor INTO v_EmpID, v_Name, v_Salary, v_DeptID;
        IF v_Done THEN LEAVE process_loop; END IF;

        -- Per-row categorization logic
        IF v_Salary >= 70000 THEN SET v_Category = 'Executive';
        ELSEIF v_Salary >= 55000 THEN SET v_Category = 'Senior';
        ELSEIF v_Salary >= 40000 THEN SET v_Category = 'Mid-Level';
        ELSE SET v_Category = 'Junior';
        END IF;

        INSERT INTO EmpReport VALUES (v_EmpID, v_Name, v_Salary, v_DeptID, v_Category);
    END LOOP;

    CLOSE emp_cursor;

    -- Show full categorized report
    SELECT * FROM EmpReport ORDER BY DeptID, Salary DESC;

    -- Show category distribution summary
    SELECT Category, COUNT(*) AS Count, ROUND(AVG(Salary),2) AS AvgSalary
    FROM EmpReport GROUP BY Category ORDER BY AvgSalary DESC;
END$$
CALL CategorizeAllEmployees()$$

-- CURSOR 2: Department-wise running salary total
CREATE PROCEDURE DeptRunningTotal()
BEGIN
    DECLARE v_Salary DECIMAL(10,2);
    DECLARE v_DeptName VARCHAR(50);
    DECLARE v_EmpName VARCHAR(100);
    DECLARE v_Running DECIMAL(12,2) DEFAULT 0;
    DECLARE v_CurrentDept VARCHAR(50) DEFAULT '';
    DECLARE v_Done INT DEFAULT FALSE;

    DECLARE dept_cursor CURSOR FOR
        SELECT E.EmpName, E.Salary, D.DeptName
        FROM Employee E
        JOIN Department D ON E.DeptID = D.DeptID
        ORDER BY D.DeptName, E.Salary DESC;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_Done = TRUE;

    DROP TEMPORARY TABLE IF EXISTS RunningTotals;
    CREATE TEMPORARY TABLE RunningTotals (
        DeptName VARCHAR(50), EmpName VARCHAR(100),
        Salary DECIMAL(10,2), RunningDeptTotal DECIMAL(12,2)
    );

    OPEN dept_cursor;

    dept_loop: LOOP
        FETCH dept_cursor INTO v_EmpName, v_Salary, v_DeptName;
        IF v_Done THEN LEAVE dept_loop; END IF;

        -- Reset running total when department changes
        IF v_DeptName != v_CurrentDept THEN
            SET v_Running = 0;
            SET v_CurrentDept = v_DeptName;
        END IF;

        SET v_Running = v_Running + v_Salary;
        INSERT INTO RunningTotals VALUES (v_DeptName, v_EmpName, v_Salary, v_Running);
    END LOOP;

    CLOSE dept_cursor;
    SELECT * FROM RunningTotals;
END$$
CALL DeptRunningTotal()$$

DELIMITER ;"""

P12_CONCLUSION = (
    "This practical demonstrated cursors as a tool for row-by-row processing when set-based SQL is insufficient. "
    "The CategorizeAllEmployees procedure successfully iterated through all employee rows, applied IF-ELSEIF "
    "salary band logic to each row, and accumulated results in a TEMPORARY TABLE — producing both a detailed "
    "report and a category distribution summary. The NOT FOUND handler was essential for detecting cursor "
    "exhaustion and exiting the loop cleanly. The DeptRunningTotal procedure demonstrated cursor usage for "
    "computing running totals that reset per department — a common reporting task where the running sum depends "
    "on prior rows. Critical performance insight: always evaluate whether a set-based alternative (CASE "
    "expression in UPDATE, window functions in MySQL 8) can replace cursor logic before deploying in production."
)

# ─── P13 ─────────────────────────────────────────────────────────────────────

P13_THEORY = build_theory_cards([
    ("Software Requirements Specification (SRS)",
     "A Software Requirements Specification (SRS) document comprehensively describes the intended behavior of a software system — the complete agreement between client and development team. The IEEE 830-1998 standard is the widely adopted format in academia and industry. A good SRS is complete (all requirements documented), consistent (no contradictions), verifiable (each requirement can be tested), and unambiguous (single interpretation).",
     "primary", "lg:col-span-2"),
    ("Functional vs Non-Functional Requirements",
     "Functional Requirements describe WHAT the system does: user login, book search, borrowing, return, fine calculation, report generation. Non-Functional Requirements describe HOW WELL: performance (response < 2 seconds for 90% of queries), scalability (1000 concurrent users), security (AES-256 encryption, bcrypt password hashing), availability (99.9% uptime = < 8.7 hours downtime/year), usability (mobile-responsive UI).",
     "secondary", ""),
    ("Data Flow Diagrams (DFD)",
     "DFDs model data flow through a system. Level 0 (Context Diagram): entire system as ONE process with external entities (Student, Librarian) and data flows (Login Credentials, Book List). Level 1: decompose the main process into sub-processes (Authentication, Book Management, Borrowing Management). Level 2: further decompose each sub-process. Use Yourdon-DeMacro notation: circles for processes, rectangles for external entities, arrows for data flows, open rectangles for data stores.",
     "primary", ""),
    ("Use Case Diagrams",
     "Use Case Diagrams show actors (users or external systems) and use cases (system functions). Relationships: include (always happens — Login is included in every use case), extend (conditional — Fine Calculation extends Return Book), generalization (actor/use case inheritance). Actor: Student can Search Books, Borrow Book, View History. Actor: Librarian can do all Student functions plus Issue Book, Manage Members, Generate Reports.",
     "secondary", "lg:col-span-2"),
    ("Database Schema Aligned with SRS",
     "Each functional requirement maps to database entities: FR-Login → Member table with PasswordHash; FR-Search → Book table with indexes on Title, Author; FR-Borrow → Borrowing table linking Member and Book with DueDate; FR-Fine → FineAmount in Borrowing with calculation trigger; FR-Report → Views on Borrowing, Book, Member. Schema decisions must directly trace back to documented requirements.",
     "primary", ""),
    ("Hardware & Technology Stack",
     "Hardware: Server — Intel Xeon 8-core, 32GB RAM, 1TB SSD RAID-1, 1Gbps NIC. Client — any modern browser with internet access. Software: Ubuntu 22.04 LTS (OS), MySQL 8.0 (database), Python 3.11 + Flask (backend), HTML5/CSS3/JavaScript (frontend), Nginx (web server), Redis (session cache). Each technology choice must be justified against alternatives with specific technical reasons.",
     "secondary", "lg:col-span-2"),
])

P13_STEPS = build_steps([
    "Define project title: Library Management System. State problem statement, objectives, scope, and constraints.",
    "Document Functional Requirements (FR01-FR10): Login, Search, Book Issue, Return, Fine Calculation, Member Management, Book Inventory, Report Generation, Notification, Audit Log.",
    "Document Non-Functional Requirements: performance (sub-2s response), security (bcrypt + HTTPS), availability (99.9%), usability (mobile-first).",
    "Define user roles: Student (search, borrow, return), Faculty (higher book limit), Staff (issue/return only), Librarian (full access), Admin (system configuration).",
    "Create Level 0 DFD: system as one process, actors as external entities, major data flows labeled.",
    "Create Level 1 DFD: decompose into Authentication, Book Management, Borrowing Management, Report Generation sub-processes.",
    "Create Use Case Diagram: Student actor (4 use cases), Librarian actor (8 use cases), relationships (include, extend).",
    "Design the ER diagram: Member, Book, Librarian, Borrowing entities with attributes and relationships.",
    "Create MySQL database following the ER design: CREATE DATABASE library_db; create all 4 tables with constraints.",
    "Insert 15 member records and 10 book records using multi-row INSERT statements.",
    "Implement FR01-FR05 as SQL queries: search books, issue book (decrement AvailableCopies), overdue detection with fine calculation.",
    "Document hardware specifications, technology stack with justifications, and load estimates (1000 students, 100 concurrent queries).",
])

P13_CODE = """-- PROJECT: Library Management System
-- SRS Version 1.0 | IEEE 830-1998 Format

CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Entity 1: Member (FR-01: Login, FR-06: Member Management)
CREATE TABLE Member (
    MemberID INT PRIMARY KEY AUTO_INCREMENT,
    FullName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    MemberType ENUM('Student','Faculty','Staff') DEFAULT 'Student',
    JoinDate DATE DEFAULT (CURRENT_DATE),
    ExpiryDate DATE,
    IsActive BOOLEAN DEFAULT TRUE,
    MaxBooksAllowed INT DEFAULT 3
);

-- Entity 2: Book (FR-03: Search, FR-07: Inventory)
CREATE TABLE Book (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    ISBN VARCHAR(20) UNIQUE NOT NULL,
    Title VARCHAR(200) NOT NULL,
    Author VARCHAR(100) NOT NULL,
    Publisher VARCHAR(100),
    PublishYear YEAR,
    Category VARCHAR(50),
    TotalCopies INT DEFAULT 1 CHECK (TotalCopies >= 0),
    AvailableCopies INT DEFAULT 1 CHECK (AvailableCopies >= 0),
    ShelfLocation VARCHAR(20)
);

-- Entity 3: Librarian (FR-01: Staff Login)
CREATE TABLE Librarian (
    LibID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Username VARCHAR(50) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    LastLogin DATETIME
);

-- Entity 4: Borrowing (FR-04: Issue, FR-05: Return, FR-09: Fine)
CREATE TABLE Borrowing (
    BorrowID INT PRIMARY KEY AUTO_INCREMENT,
    MemberID INT NOT NULL,
    BookID INT NOT NULL,
    LibID INT,
    BorrowDate DATE DEFAULT (CURRENT_DATE),
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    FineAmount DECIMAL(6,2) DEFAULT 0.00,
    Status ENUM('Active','Returned','Overdue') DEFAULT 'Active',
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID),
    FOREIGN KEY (LibID) REFERENCES Librarian(LibID)
);

-- Insert 15 members
INSERT INTO Member (FullName, Email, Phone, MemberType, ExpiryDate) VALUES
('Aarav Shah','aarav@lib.com','9876501001','Student','2025-12-31'),
('Priya Mehta','priya@lib.com','9876501002','Faculty','2026-12-31'),
('Rohit Joshi','rohit@lib.com','9876501003','Student','2025-12-31'),
('Sneha Patil','sneha@lib.com','9876501004','Staff','2026-06-30'),
('Karan Desai','karan@lib.com','9876501005','Student','2025-12-31'),
('Ananya Iyer','ananya@lib.com','9876501006','Student','2025-12-31'),
('Vikas Rao','vikas@lib.com','9876501007','Faculty','2026-12-31'),
('Pooja Nair','pooja@lib.com','9876501008','Student','2025-12-31'),
('Arjun Tiwari','arjun@lib.com','9876501009','Staff','2026-06-30'),
('Neha Gupta','neha@lib.com','9876501010','Student','2025-12-31'),
('Raj Malhotra','raj@lib.com','9876501011','Student','2025-12-31'),
('Meera Pillai','meera@lib.com','9876501012','Faculty','2026-12-31'),
('Dev Sharma','dev@lib.com','9876501013','Student','2025-12-31'),
('Tara Jain','tara@lib.com','9876501014','Student','2025-12-31'),
('Yash Kumar','yash@lib.com','9876501015','Staff','2026-06-30');

-- Insert 10 books
INSERT INTO Book (ISBN, Title, Author, Category, TotalCopies, AvailableCopies, ShelfLocation) VALUES
('978-0-13-110362-7','The C Programming Language','Kernighan & Ritchie','Programming',5,3,'A-01'),
('978-0-13-468599-1','Database System Concepts','Silberschatz','DBMS',8,5,'B-03'),
('978-0-13-235088-4','Computer Networks','Tanenbaum','Networking',4,4,'C-02'),
('978-0-262-03384-8','Introduction to Algorithms','Cormen','Algorithms',6,2,'A-05'),
('978-0-13-597444-0','Operating System Concepts','Silberschatz','OS',7,6,'B-01'),
('978-1-491-95038-8','Python Data Science Handbook','VanderPlas','Data Science',3,3,'D-04'),
('978-0-13-110370-2','Clean Code','Robert Martin','Software Engg',5,4,'A-08'),
('978-0-13-235089-1','Artificial Intelligence','Russell & Norvig','AI',4,1,'D-02'),
('978-1-119-54774-8','Machine Learning','Alpaydin','ML',3,2,'D-03'),
('978-0-13-468600-4','Computer Organization','Patterson','Architecture',5,5,'C-05');

-- FR-03: Search books by title or author
SELECT BookID, Title, Author, AvailableCopies, ShelfLocation
FROM Book WHERE Title LIKE '%Algorithm%' OR Author LIKE '%Silber%';

-- FR-04: Issue a book
INSERT INTO Borrowing (MemberID, BookID, LibID, DueDate)
VALUES (1, 4, 1, DATE_ADD(CURDATE(), INTERVAL 14 DAY));
UPDATE Book SET AvailableCopies = AvailableCopies - 1 WHERE BookID = 4;

-- FR-09: Check overdue books with automatic fine calculation
SELECT M.FullName, B.Title, BR.DueDate,
       DATEDIFF(CURDATE(), BR.DueDate) AS DaysOverdue,
       DATEDIFF(CURDATE(), BR.DueDate) * 5 AS FineRs
FROM Borrowing BR
JOIN Member M ON BR.MemberID = M.MemberID
JOIN Book B ON BR.BookID = B.BookID
WHERE BR.ReturnDate IS NULL AND BR.DueDate < CURDATE();

-- FR-08: Member borrowing history
SELECT B.Title, BR.BorrowDate, BR.DueDate, BR.ReturnDate,
       IFNULL(BR.FineAmount, 0) AS Fine, BR.Status
FROM Borrowing BR
JOIN Book B ON BR.BookID = B.BookID
WHERE BR.MemberID = 1 ORDER BY BR.BorrowDate DESC;

-- FR-10: Most borrowed books report
SELECT B.Title, B.Author, COUNT(BR.BorrowID) AS TimesBorrowed
FROM Book B LEFT JOIN Borrowing BR ON B.BookID = BR.BookID
GROUP BY B.BookID ORDER BY TimesBorrowed DESC LIMIT 5;"""

P13_CONCLUSION = (
    "This practical produced a complete Software Requirements Specification for a Library Management System "
    "following IEEE 830-1998 format. Functional requirements FR01-FR10 were documented with clear acceptance "
    "criteria. Non-functional requirements established measurable quality benchmarks — sub-2-second response, "
    "99.9% availability, and bcrypt password security. The ER design directly traced back to each functional "
    "requirement: Member table for authentication, Book table for inventory and search, Borrowing table for "
    "issue/return/fine tracking with FOREIGN KEY relationships enforcing data integrity. The database schema "
    "was implemented in MySQL with 15 members and 10 books, and key queries demonstrated all major functional "
    "requirements working correctly. Hardware specifications and technology stack choices were justified with "
    "specific technical reasoning."
)

# ─── P14 ─────────────────────────────────────────────────────────────────────

P14_THEORY = build_theory_cards([
    ("Physical Database Design",
     "Physical database design translates logical schema decisions into performance-optimized structures. Key decisions: choosing smallest sufficient data type (INT vs BIGINT, VARCHAR(50) vs VARCHAR(255) — smaller types save storage and speed comparisons), selecting storage engine (InnoDB for transactional, MEMORY for temporary lookup tables), and defining indexes strategically to balance read speed against write overhead.",
     "primary", "lg:col-span-2"),
    ("Indexes — B-Tree & Composite",
     "MySQL indexes (B-Tree by default) store a sorted copy of specified column values with pointers to actual rows, allowing O(log n) lookups instead of O(n) full table scans. PRIMARY KEY is automatically clustered (data physically sorted by PK in InnoDB). Foreign key columns should be manually indexed. Composite indexes (multiple columns) follow the leftmost prefix rule — an index on (DeptID, Salary) helps queries filtering on DeptID alone or DeptID+Salary, but NOT on Salary alone.",
     "secondary", ""),
    ("EXPLAIN Statement",
     "EXPLAIN shows the query execution plan WITHOUT running it. Critical columns: type (ALL=full scan=bad; const, eq_ref, ref, range=index used=good), key (which index chosen; NULL=no index), rows (estimated rows examined — smaller is better), Extra (Using index=covering index=fastest; Using filesort=avoid; Using temporary=very slow). EXPLAIN ANALYZE actually runs the query and shows real timing vs estimated.",
     "primary", ""),
    ("Transactions & ACID",
     "Transactions group multiple SQL statements into an atomic unit. START TRANSACTION begins. COMMIT makes all changes permanent. ROLLBACK undoes all changes since START TRANSACTION. SAVEPOINT name creates a named checkpoint. ROLLBACK TO SAVEPOINT name undoes only changes after that savepoint while keeping earlier changes. Transactions are essential for multi-step operations where partial completion is worse than no completion.",
     "secondary", "lg:col-span-2"),
    ("Isolation Levels",
     "MySQL's four isolation levels (least to most strict): READ UNCOMMITTED (dirty reads possible), READ COMMITTED (no dirty reads), REPEATABLE READ (default — no dirty/non-repeatable reads, phantom reads possible), SERIALIZABLE (full isolation, lowest concurrency). SET SESSION TRANSACTION ISOLATION LEVEL changes the level for the current session. Higher isolation prevents more anomalies but increases lock contention and reduces throughput.",
     "primary", ""),
    ("Index Trade-offs & Covering Indexes",
     "Indexes speed up SELECT/WHERE/JOIN/ORDER BY but slow down INSERT/UPDATE/DELETE (the index structure must also be updated). Over-indexing wastes storage and memory. A covering index includes ALL columns needed for a query — MySQL can answer the query using only the index without accessing the actual table rows (Extra: Using index). Composite indexes for high-frequency query patterns are one of the most impactful performance optimizations.",
     "secondary", "lg:col-span-2"),
])

P14_STEPS = build_steps([
    "Use college_db: USE college_db; Run SHOW INDEX FROM Employee; to see existing indexes.",
    "Create a single-column index on Salary: CREATE INDEX idx_emp_salary ON Employee(Salary);",
    "Create a composite index on (DeptID, Salary): CREATE INDEX idx_emp_dept_salary ON Employee(DeptID, Salary);",
    "Run EXPLAIN SELECT * FROM Employee WHERE DeptID = 1 AND Salary > 50000; and verify the composite index is used.",
    "Compare EXPLAIN output before and after index creation — observe type changing from ALL to ref/range.",
    "Run EXPLAIN on a JOIN query: Employee JOIN Department — verify DeptID FK index is used.",
    "Query INFORMATION_SCHEMA.STATISTICS to list all indexes in college_db with their column order.",
    "Drop an unused index with DROP INDEX idx_emp_salary ON Employee;",
    "Demonstrate Transaction 1: transfer salary bonus between two employees — START TRANSACTION, two UPDATEs, COMMIT.",
    "Demonstrate Transaction 2: use SAVEPOINT — insert three employees, ROLLBACK TO second savepoint, COMMIT.",
    "Demonstrate Transaction 3: full ROLLBACK — DELETE dept 4 employees, verify deletion, ROLLBACK, verify restoration.",
    "Set isolation level and run a query, then EXPLAIN the final reporting query to verify index-optimized execution.",
])

P14_CODE = """USE college_db;

-- View existing indexes on Employee table
SHOW INDEX FROM Employee;

-- Single-column index for salary range queries
CREATE INDEX idx_emp_salary ON Employee(Salary);

-- Composite index for department + salary queries (leftmost prefix rule)
CREATE INDEX idx_emp_dept_salary ON Employee(DeptID, Salary);

-- Index on join date for date-range reports
CREATE INDEX idx_emp_joindate ON Employee(JoinDate);

-- EXPLAIN: check if composite index is used for DeptID + Salary filter
EXPLAIN SELECT * FROM Employee WHERE DeptID = 1 AND Salary > 50000;

-- EXPLAIN: salary range using single-column index
EXPLAIN SELECT EmpName FROM Employee WHERE Salary BETWEEN 40000 AND 70000;

-- EXPLAIN: JOIN query - verify DeptID FK index is used
EXPLAIN SELECT E.EmpName, D.DeptName
FROM Employee E JOIN Department D ON E.DeptID = D.DeptID
WHERE D.DeptName = 'Information Technology';

-- List all indexes in college_db from INFORMATION_SCHEMA
SELECT TABLE_NAME, INDEX_NAME, COLUMN_NAME, SEQ_IN_INDEX, NON_UNIQUE
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = 'college_db'
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;

-- Drop an index that is made redundant by the composite index
DROP INDEX idx_emp_joindate ON Employee;

-- TRANSACTION 1: Salary bonus transfer (atomic)
START TRANSACTION;
UPDATE Employee SET Salary = Salary - 3000 WHERE EmpID = 1;
UPDATE Employee SET Salary = Salary + 3000 WHERE EmpID = 2;
SELECT EmpID, EmpName, Salary FROM Employee WHERE EmpID IN (1,2);
COMMIT;

-- TRANSACTION 2: SAVEPOINT usage
START TRANSACTION;
INSERT INTO Employee (EmpName, Salary, Gender, DeptID)
    VALUES ('Temp Alpha', 32000, 'Male', 1);
SAVEPOINT after_alpha;

INSERT INTO Employee (EmpName, Salary, Gender, DeptID)
    VALUES ('Temp Beta', 36000, 'Female', 2);
SAVEPOINT after_beta;

INSERT INTO Employee (EmpName, Salary, Gender, DeptID)
    VALUES ('Temp Gamma', 29000, 'Male', 3);

-- Rollback only Gamma, keep Alpha and Beta
ROLLBACK TO SAVEPOINT after_beta;
COMMIT;
SELECT EmpName FROM Employee WHERE EmpName LIKE 'Temp%';

-- TRANSACTION 3: Full ROLLBACK demonstration
START TRANSACTION;
DELETE FROM Employee WHERE DeptID = 4;
SELECT COUNT(*) AS RemainingInDept4 FROM Employee WHERE DeptID = 4;
ROLLBACK;  -- restore all deleted rows
SELECT COUNT(*) AS RestoredCount FROM Employee WHERE DeptID = 4;

-- Set isolation level
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT EmpName, Salary FROM Employee WHERE DeptID = 1;
COMMIT;

-- Final optimized reporting query with EXPLAIN
EXPLAIN SELECT D.DeptName,
       COUNT(E.EmpID) AS Headcount,
       ROUND(AVG(E.Salary),2) AS AvgSalary,
       SUM(E.Salary) AS TotalBill,
       MAX(E.Salary) AS TopEarner
FROM Department D
LEFT JOIN Employee E ON D.DeptID = E.DeptID
GROUP BY D.DeptName
ORDER BY TotalBill DESC;

-- Run the actual final departmental report
SELECT D.DeptName,
       COUNT(E.EmpID) AS Headcount,
       ROUND(AVG(E.Salary),2) AS AvgSalary,
       SUM(E.Salary) AS TotalBill,
       MAX(E.Salary) AS TopEarner
FROM Department D
LEFT JOIN Employee E ON D.DeptID = E.DeptID
GROUP BY D.DeptName
ORDER BY TotalBill DESC;"""

P14_CONCLUSION = (
    "This final practical integrated all concepts from Practicals 1-13 into a production-quality database "
    "design. Indexing strategy was established: single-column index on Salary for range queries, composite "
    "index on (DeptID, Salary) for combined filters following the leftmost prefix rule. EXPLAIN output "
    "confirmed indexes were being utilized — type changed from ALL to ref/range, dramatically reducing "
    "estimated rows examined. Three transaction patterns were demonstrated: simple commit, savepoint-based "
    "partial rollback, and full rollback for safety verification. Isolation level was adjusted to READ "
    "COMMITTED to balance consistency and concurrency. The final reporting query with EXPLAIN ANALYZE "
    "confirmed optimal index-driven execution. This practical demonstrates how proper physical database "
    "design — careful indexing, transaction management, and query optimization — is as important as "
    "correct logical schema design for production database systems."
)

# ═══════════════════════════════════════════════════════════════════════════════
# APPLY ALL PATCHES
# ═══════════════════════════════════════════════════════════════════════════════

PRACTICALS = [
    ("practical_01_study_of_mysql",        P01_THEORY, P01_STEPS, P01_CODE, P01_CONCLUSION, "MySQL 8.x — System Exploration Commands"),
    ("practical_02_mysql_installation",    P02_THEORY, P02_STEPS, P02_CODE, P02_CONCLUSION, "MySQL 8.x — Installation & User Management"),
    ("practical_03_sqlite_study",          P03_THEORY, P03_STEPS, P03_CODE, P03_CONCLUSION, "SQLite3 — College Database"),
    ("practical_04_er_diagrams",           P04_THEORY, P04_STEPS, P04_CODE, P04_CONCLUSION, "MySQL 8.x — Hospital Management System"),
    ("practical_05_ddl_normalization",     P05_THEORY, P05_STEPS, P05_CODE, P05_CONCLUSION, "MySQL 8.x — DDL & Normalization"),
    ("practical_06_constraints_alter_drop",P06_THEORY, P06_STEPS, P06_CODE, P06_CONCLUSION, "MySQL 8.x — Constraints & Schema Operations"),
    ("practical_07_sql_queries",           P07_THEORY, P07_STEPS, P07_CODE, P07_CONCLUSION, "MySQL 8.x — DML & Advanced Queries"),
    ("practical_08_views",                 P08_THEORY, P08_STEPS, P08_CODE, P08_CONCLUSION, "MySQL 8.x — Views & Virtual Tables"),
    ("practical_09_implementation_of_joins",P09_THEORY,P09_STEPS, P09_CODE, P09_CONCLUSION, "MySQL 8.x — All JOIN Types"),
    ("practical_10_stored_procedures",     P10_THEORY, P10_STEPS, P10_CODE, P10_CONCLUSION, "MySQL 8.x — Stored Procedures & Functions"),
    ("practical_11_triggers",              P11_THEORY, P11_STEPS, P11_CODE, P11_CONCLUSION, "MySQL 8.x — Triggers & Audit Logging"),
    ("practical_12_cursors",               P12_THEORY, P12_STEPS, P12_CODE, P12_CONCLUSION, "MySQL 8.x — Cursor-Based Processing"),
    ("practical_13_project_proposal_srs",  P13_THEORY, P13_STEPS, P13_CODE, P13_CONCLUSION, "MySQL 8.x — Library Management System"),
    ("practical_14_er_diagram_database_design", P14_THEORY, P14_STEPS, P14_CODE, P14_CONCLUSION, "MySQL 8.x — Indexes, Transactions & Query Optimization"),
]

print("\n🚀 Starting direct HTML content update for all 14 practicals...\n")

success_count = 0
for folder, theory, steps, code, conclusion, label in PRACTICALS:
    path = os.path.join(BASE, folder, "code.html")
    if not os.path.exists(path):
        print(f"  ❌ File not found: {path}")
        continue
    code_html = build_code_block(label, code)
    try:
        patch_file(path, theory, steps, code_html, conclusion)
        success_count += 1
    except Exception as e:
        print(f"  ❌ Error patching {folder}: {e}")

print(f"\n✅ Done! {success_count}/14 practical HTML files updated successfully.\n")
