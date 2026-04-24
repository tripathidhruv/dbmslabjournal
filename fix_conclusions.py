#!/usr/bin/env python3
"""
Fix the conclusion card wrapper in all 14 HTML files.
The patcher previously placed the conclusion text bare inside the section
without its card div. This script wraps it correctly.
"""

import re, os, html

BASE = os.path.dirname(os.path.abspath(__file__))

def escape(t): return html.escape(t, quote=False)

# ─── Conclusion texts for all 14 practicals ──────────────────────────────────

CONCLUSIONS = {
    "practical_01_study_of_mysql": (
        "This practical provided a foundational understanding of MySQL as a relational database management system. "
        "We explored its three-tier architecture and understood how the storage engine layer separates logical query "
        "processing from physical data storage. The ACID properties were studied in context, demonstrating why MySQL "
        "is trusted for mission-critical applications in banking and healthcare. The hands-on commands confirmed the "
        "MySQL installation is functional and correctly configured. Understanding MySQL's architecture is essential "
        "before writing any SQL, as it explains why certain queries perform faster than others. MySQL's open-source "
        "nature and Oracle's continued development make it the industry standard for web applications. This knowledge "
        "forms the base for all subsequent practicals in this lab."
    ),
    "practical_02_mysql_installation": (
        "This practical covered the complete installation and configuration of MySQL Community Edition. "
        "We successfully installed the MySQL server, configured security using mysql_secure_installation, "
        "and verified the server is operating correctly. User management was demonstrated by creating "
        "application-specific users with restricted privileges, implementing the principle of least privilege. "
        "Configuration variables like max_connections and innodb_buffer_pool_size were inspected and their "
        "impact on performance understood. UTF8MB4 character set was set for proper multilingual support. "
        "This foundational setup ensures a secure, correctly configured database environment for all "
        "subsequent practical work."
    ),
    "practical_03_sqlite_study": (
        "This practical demonstrated SQLite as a lightweight, serverless database ideal for embedded and "
        "mobile applications. We created a Students database, inserted 15 records with various data types "
        "and constraints, and performed filtering, sorting, and aggregation queries. The dot-commands provided "
        "essential CLI control for output formatting and data export. Key distinctions from MySQL were observed: "
        "no server process, type affinity instead of strict typing, and PRAGMA commands for metadata inspection. "
        "SQLite's zero-setup nature and Python integration make it indispensable for rapid prototyping and local "
        "application storage. AUTOINCREMENT behavior, CHECK constraints, and UNIQUE enforcement were all verified."
    ),
    "practical_04_er_diagrams": (
        "This practical demonstrated the complete process of ER diagram design and its conversion to a relational "
        "database schema. Starting from the Hospital Management System domain, we identified entities (Doctor, Ward, "
        "Patient, Treatment), their attributes (simple, composite, derived, multivalued), and their relationships "
        "with correct cardinality and participation. The M:N Patient-Doctor relationship was resolved into a Treatment "
        "junction table with foreign keys to both parent tables. JOIN queries successfully navigated all three "
        "relationship types (1:N patient-ward, M:N patient-doctor). ER diagrams are essential for planning before "
        "coding, preventing costly schema redesigns after data has been inserted into production systems."
    ),
    "practical_05_ddl_normalization": (
        "This practical demonstrated the complete DDL command set and the normalization process from UNF to 3NF. "
        "Starting with an unnormalized table containing multi-valued attributes and redundancy, we systematically "
        "applied normalization rules: 1NF eliminated repeating groups, 2NF removed partial dependencies on the "
        "composite primary key, and 3NF eliminated transitive dependencies by separating Professor data into its "
        "own table. The final schema has four tables (Students, Professors, Courses, Enrollment) with no data "
        "redundancy. ALTER TABLE commands demonstrated schema evolution without data loss. The normalized schema "
        "prevents update, insert, and delete anomalies that plagued the original un-normalized design."
    ),
    "practical_06_constraints_alter_drop": (
        "This practical demonstrated all six SQL constraint types and their enforcement by MySQL. PRIMARY KEY, "
        "FOREIGN KEY, UNIQUE, NOT NULL, CHECK, and DEFAULT were all implemented on the Department and Employee "
        "tables. Constraint violation tests confirmed that MySQL stops malformed data at the database level, "
        "independent of application code — providing a last line of defense against data corruption. ON DELETE "
        "CASCADE was demonstrated by deleting a department and verifying automatic deletion of all associated "
        "employees. ALTER TABLE showed schema evolution without data loss. The critical distinction between "
        "DELETE (targeted, rollback-able, slow), TRUNCATE (full fast reset), and DROP (structural destruction) "
        "was verified through live demonstration on the Employee table."
    ),
    "practical_07_sql_queries": (
        "This practical covered the complete DML toolbox through comprehensive SQL queries on the Employee and "
        "Department tables. The SELECT execution order (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → "
        "LIMIT) was demonstrated and its implications understood. WHERE clause operators (BETWEEN, IN, LIKE, IS NULL) "
        "filtered data precisely. Aggregate functions with GROUP BY and HAVING produced department-level statistics. "
        "Subqueries — non-correlated, correlated, derived table, scalar, EXISTS — answered complex business questions "
        "in single SQL statements. UNION and UNION ALL performed set operations, with INTERSECT and MINUS simulated "
        "via IN and NOT IN. UPDATE and DELETE applied targeted data modifications with transaction semantics."
    ),
    "practical_08_views": (
        "This practical demonstrated the full lifecycle of views in MySQL — creation, querying, modification, "
        "metadata inspection, and deletion. Simple views on single tables proved updatable, while the complex "
        "aggregate view (GROUP BY) was correctly identified as not updatable. WITH CHECK OPTION successfully "
        "prevented updates that would cause rows to disappear from the view's filtered result set. Security "
        "views hiding the Salary column demonstrated how view-based access control protects sensitive data — "
        "users granted SELECT on the public view cannot see salaries even if they know the table exists. "
        "CREATE OR REPLACE VIEW evolved a view definition seamlessly. INFORMATION_SCHEMA.VIEWS provided "
        "programmatic access to view metadata for documentation and auditing purposes."
    ),
    "practical_09_implementation_of_joins": (
        "This practical covered all major JOIN types through demonstration on the Employee, Department, and "
        "Project tables. INNER JOIN retrieved only matched rows, LEFT JOIN revealed departments with no employees "
        "by returning NULLs, and FULL OUTER JOIN was successfully simulated using UNION. SELF JOIN elegantly "
        "modeled the employee-manager hierarchy by aliasing the Employee table twice. CROSS JOIN demonstrated "
        "the Cartesian product and its potential for data explosion without proper filtering. The 3-table JOIN "
        "demonstrated how complex real-world queries combine multiple relationships in a single readable SQL "
        "statement. JOIN performance considerations including index usage and EXPLAIN analysis were explored, "
        "confirming that indexed FK columns drastically reduce the rows examined per query."
    ),
    "practical_10_stored_procedures": (
        "This practical demonstrated the complete spectrum of stored procedure and user-defined function "
        "capabilities in MySQL. Procedures with IN, OUT, and INOUT parameters gave flexibility in data passing — "
        "OUT parameters proved essential for returning multiple computed values from a single CALL. Control flow "
        "constructs (IF-ELSEIF-ELSE, WHILE loop) transformed procedures from simple data retrievers into "
        "computation engines with embedded business logic. The SalaryProjection procedure used a TEMPORARY TABLE "
        "to accumulate and return row-by-row computed results. User-defined functions CalcTax and ExperienceLevel "
        "were embedded directly in SELECT statements, demonstrating their advantage for column-level calculations. "
        "Error handling with EXIT HANDLER and ROLLBACK ensured atomicity for multi-step inserts."
    ),
    "practical_11_triggers": (
        "This practical demonstrated all six trigger types (BEFORE/AFTER INSERT, UPDATE, DELETE) through a "
        "comprehensive audit logging system on the Employee table. The BEFORE INSERT trigger auto-formatted names "
        "to Title Case and validated salary using SIGNAL to abort invalid inserts — proving database-level data "
        "quality enforcement independent of application code. AFTER INSERT/UPDATE/DELETE triggers populated the "
        "Employee_Audit table with complete change history including old values, new values, the MySQL user, and "
        "timestamp — meeting audit trail requirements for compliance. BEFORE UPDATE prevented salary reductions "
        "and auto-updated JoinDate on department transfers. BEFORE DELETE protected high-value employees from "
        "accidental deletion. The audit log created a complete, tamper-evident history of all DML operations."
    ),
    "practical_12_cursors": (
        "This practical demonstrated cursors as a tool for row-by-row processing when set-based SQL is insufficient. "
        "The CategorizeAllEmployees procedure successfully iterated through all employee rows, applied IF-ELSEIF "
        "salary band logic to each row, and accumulated results in a TEMPORARY TABLE — producing both a detailed "
        "report and a category distribution summary. The NOT FOUND handler was essential for detecting cursor "
        "exhaustion and exiting the loop cleanly without an error. The DeptRunningTotal procedure demonstrated "
        "cursor usage for computing running totals that reset per department — a common reporting task where the "
        "running sum depends on prior rows. Critical insight: always evaluate whether a set-based alternative "
        "(CASE in UPDATE, window functions in MySQL 8) can replace cursor logic before deploying in production."
    ),
    "practical_13_project_proposal_srs": (
        "This practical produced a complete Software Requirements Specification for a Library Management System "
        "following IEEE 830-1998 format. Functional requirements FR01-FR10 were documented with clear acceptance "
        "criteria. Non-functional requirements established measurable quality benchmarks — sub-2-second response, "
        "99.9% availability, and bcrypt password security. The ER design directly traced to each functional "
        "requirement: Member table for authentication, Book table for inventory and search, Borrowing table for "
        "issue/return/fine tracking with FOREIGN KEY relationships enforcing data integrity. The database schema "
        "was implemented with 15 members and 10 books, and key queries demonstrated all major functional "
        "requirements working correctly. Hardware and technology stack choices were justified with specific "
        "technical reasoning comparing alternatives."
    ),
    "practical_14_er_diagram_database_design": (
        "This final practical integrated all concepts from Practicals 1-13 into a production-quality database "
        "design. Indexing strategy was established: single-column index on Salary for range queries, composite "
        "index on (DeptID, Salary) for combined filters following the leftmost prefix rule. EXPLAIN output "
        "confirmed indexes were being utilized — type changed from ALL to ref/range, dramatically reducing "
        "estimated rows examined. Three transaction patterns were demonstrated: simple commit, savepoint-based "
        "partial rollback, and full rollback for safety verification. Isolation level was adjusted to READ "
        "COMMITTED to balance consistency and concurrency. The final reporting query with EXPLAIN confirmed "
        "optimal index-driven execution, demonstrating how proper physical database design — careful indexing, "
        "transaction management, and query optimization — is as important as correct logical schema design."
    ),
}

# ─── Pattern to find and fix the conclusion section ──────────────────────────

# Matches: the heading div block + bare text until </section>
# (before the Viva Voce section)
CONCLUSION_SECTION_RE = re.compile(
    r'(<!-- CONCLUSION -->[\s\S]*?whitespace-nowrap">Conclusion</h2>[\s\S]*?</div>)'  # heading row
    r'([\s\S]*?)'   # current content (may be bare text or wrong div)
    r'(</section>\s*\n\s*<!-- VIVA VOCE -->)',
    re.MULTILINE
)

def fix_conclusion(path, text):
    with open(path, encoding='utf-8') as f:
        content = f.read()

    card = (
        f'\n<div class="p-8 bg-surface-container rounded-xl border-l-4 border-secondary">'
        f'<p class="text-on-surface font-body leading-relaxed mb-4">{escape(text)}</p>'
        f'</div>\n'
    )

    m = CONCLUSION_SECTION_RE.search(content)
    if m:
        new_content = content[:m.start(2)] + card + content[m.start(3):]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✅ Fixed conclusion: {os.path.basename(os.path.dirname(path))}/code.html")
    else:
        # Fallback: look for the Conclusion h2 and inject after its section header row
        conc_idx = content.find('>Conclusion</h2>')
        if conc_idx == -1:
            print(f"  ⚠  Conclusion h2 not found in {path}")
            return

        # Find end of the heading row div (closes the flex div with the h2)
        # The heading row ends with </div></div> - find the second </div> after h2
        after_h2 = conc_idx + len('>Conclusion</h2>')
        # Find closing of the heading flex row
        close1 = content.find('</div>', after_h2)
        close2 = content.find('</div>', close1 + 6)
        insert_at = close2 + 6

        # Find end of section (before VIVA or before next major section)
        viva_idx = content.find('<!-- VIVA VOCE -->', insert_at)
        if viva_idx == -1:
            viva_idx = content.find('</section>', insert_at) + 10

        # Replace everything between insert_at and viva_idx with the card
        section_end = content.rfind('</section>', insert_at, viva_idx) + 10
        new_content = content[:insert_at] + card + content[section_end - 10:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✅ Fixed (fallback) conclusion: {os.path.basename(os.path.dirname(path))}/code.html")


print("\n🔧 Fixing conclusion card wrappers in all 14 practicals...\n")

for folder, text in CONCLUSIONS.items():
    path = os.path.join(BASE, folder, "code.html")
    if not os.path.exists(path):
        print(f"  ❌ Not found: {path}")
        continue
    try:
        fix_conclusion(path, text)
    except Exception as e:
        print(f"  ❌ {folder}: {e}")

print("\n✅ Conclusion fix complete!\n")
