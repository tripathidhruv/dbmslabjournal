#!/usr/bin/env python3
import os
from generate_base import (build_page, theory_card, ol_steps, code_block, out_table, viva, write_practical, kw, tbl, num, cmt, str_, fn)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────
# PRACTICAL 12 — Cursors
# ─────────────────────────────────────
def p12():
    aim = """<p class="text-on-surface font-body leading-relaxed text-lg mb-4">
The aim of this practical is to study and implement Cursor mechanisms inside Stored Procedures. 
The student will understand how to bypass SQL's default set-based nature to iterate over result sets row-by-row, permitting complex procedural operations on individual rows retrieved from the database.
</p>"""

    theory = f"""<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{theory_card("What is a Cursor?","Normally, SQL operates on sets (all matching rows at once). A cursor allows you to iterate over a query result set row-by-row. Think of it as a pointer that loops through the results of a SELECT statement in procedural PL/SQL code.","lg:col-span-2","primary","primary")}
{theory_card("Lifecycle of a Cursor","1. DECLARE (define the query), 2. OPEN (execute query and load results into memory), 3. FETCH (pull one row from memory into variables), 4. CLOSE (free memory).","","secondary","secondary")}
{theory_card("Handlers (NOT FOUND)","MySQL cursors don't natively know their length bounds. You must define a CONTINUE HANDLER FOR NOT FOUND to gracefully break the loop when FETCH no longer finds any more records to pull.","lg:col-span-3","primary","primary")}
</div>"""

    proc = ol_steps([
        "Change the delimiter to allow block structure.",
        "Create a stored procedure (e.g., UpdateAllDoctorSalaries).",
        "Declare variables to hold row data (e.g., v_doc_id, v_salary).",
        "Declare a variable (done = 0) loop-breaker and declare the cursor for the SELECT query.",
        "Declare the NOT FOUND handler to set done = 1.",
        "Open cursor, begin a LOOP, Fetch into variables.",
        "Add an IF done THEN LEAVE loop conditional.",
        "Perform row-based action (e.g., giving 5% raise).",
        "Close cursor and end process."
    ])

    code = code_block(f"""{cmt("-- Practical 12: Cursors")}
{kw("USE")} {tbl("hospital_db")};

{kw("DELIMITER //")}

{kw("CREATE PROCEDURE")} {tbl("ApplyBonusToDoctors")}()
{kw("BEGIN")}
    {cmt("-- Variables to hold fetched data")}
    {kw("DECLARE")} {tbl("v_doc_id")} {kw("INT")};
    {kw("DECLARE")} {tbl("v_salary")} {kw("DECIMAL")}({num("10")},{num("2")});
    
    {cmt("-- Loop control variable")}
    {kw("DECLARE")} {tbl("done")} {kw("INT")} {kw("DEFAULT")} {num("0")};
    
    {cmt("-- Cursor Declaration")}
    {kw("DECLARE")} {tbl("doctor_cursor")} {kw("CURSOR FOR")} 
        {kw("SELECT")} {tbl("doctor_id")}, {tbl("salary")} {kw("FROM")} {tbl("DOCTOR")};
        
    {cmt("-- NOT FOUND handler: trips when cursor reaches end of dataset")}
    {kw("DECLARE CONTINUE HANDLER FOR NOT FOUND SET")} {tbl("done")} = {num("1")};
    
    {cmt("-- Open the Cursor")}
    {kw("OPEN")} {tbl("doctor_cursor")};
    
    {tbl("read_loop")}: {kw("LOOP")}
        {cmt("-- Fetch current row into variables")}
        {kw("FETCH")} {tbl("doctor_cursor")} {kw("INTO")} {tbl("v_doc_id")}, {tbl("v_salary")};
        
        {cmt("-- Check if we reached the end")}
        {kw("IF")} {tbl("done")} = {num("1")} {kw("THEN")}
            {kw("LEAVE")} {tbl("read_loop")};
        {kw("END IF")};
        
        {cmt("-- Procedural logic for each row: e.g., 5% bonus")}
        {kw("UPDATE")} {tbl("DOCTOR")}
        {kw("SET")} {tbl("salary")} = {tbl("v_salary")} * {num("1.05")}
        {kw("WHERE")} {tbl("doctor_id")} = {tbl("v_doc_id")};
        
    {kw("END LOOP")};
    
    {cmt("-- Close the connection and free memory")}
    {kw("CLOSE")} {tbl("doctor_cursor")};
    
{kw("END //")}
{kw("DELIMITER ;")}

{cmt("-- Run the procedure containing the cursor")}
{kw("CALL")} {tbl("ApplyBonusToDoctors")}();

{cmt("-- Verify changes")}
{kw("SELECT")} {tbl("doctor_id")}, {tbl("name")}, {tbl("salary")} {kw("FROM")} {tbl("DOCTOR")} {kw("ORDER BY")} {tbl("salary")} {kw("DESC")};
""")
    output = out_table(
        ["doctor_id","name","salary (After +5%)"],
        [["105","Dr. Vikram Joshi","157500.00"],
         ["101","Dr. Arjun Sharma","126000.00"],
         ["106","Dr. Meena Iyer","115500.00"]],
        "Verifying Row-Level Operations"
    )

    conclusion = """<p class="text-on-surface font-body leading-relaxed mb-4">
We employed a database cursor successfully to bridge the gap between relational set logic and program loop logic. Handling individual rows via OPEN, FETCH, and CLOSE statements gave fine-grain procedural control otherwise difficult to execute via raw declarative SQL updates safely.
</p>"""
    vivaqs = [
        ("What is the primary difference between normal SQL queries and Cursors?", "SQL acts on sets of data simultaneously. Cursors iterate sequentially over records row-by-row, permitting procedural control flow logic like loop conditional branching per record."),
        ("Why isn't a cursor recommended for large bulk updates?", "Since cursors fetch row-by-row, they carry significant overhead and execute DML operations singly instead of in optimized batches. Normal UPDATE queries are almost always orders of magnitude faster."),
        ("What does the CONTINUE HANDLER do in a cursor?", "It prevents the stored procedure from throwing a terminal error when a FETCH retrieves nothing. Instead, it flips a variable status (e.g. done = 1) allowing the code to break the loop naturally."),
        ("What are the mandatory sequential steps for a cursor?", "DECLARE the cursor -> OPEN the cursor -> FETCH rows in a LOOP -> CLOSE the cursor."),
        ("Can you update data directly through a cursor?", "Yes, databases often support updating the currently fetched record using the syntax UPDATE ... WHERE CURRENT OF cursor_name, though explicit updates matched by ID (like our example) are more universally compatible syntax.")
    ]
    return build_page(12,"Cursors","Group C","Row-Level Iteration",
        "Applying row-by-row procedural processing constructs within stored functions.",
        aim, theory, proc, code, output, conclusion, viva(vivaqs))

# ─────────────────────────────────────
# PRACTICAL 13 — Project Proposal / SRS
# ─────────────────────────────────────
def p13():
    aim = """<p class="text-on-surface font-body leading-relaxed text-lg mb-4">
The aim of this practical is to author a complete Software Requirements Specification (SRS) representing a fully planned project architecture. 
The student will understand how to convert purely academic coding into a defined corporate system proposal detailing Scope, Modules, Roles, Hardware considerations, and Load estimations.
</p>"""

    theory = f"""<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
{theory_card("Introduction & Scope","Project Title: Hospital Management System (HMS) / MindSense Medical Wing. Objective: Centralize and secure patient history, billing, ward allocations, and departmental staff records. Minimize human error through normalization and UI access controls.","lg:col-span-2","primary","primary")}
{theory_card("System Features","1. Patient Management: Registration, history keeping, bed assignment. 2. Staff Records: Employee allocations, department tagging, payroll triggers. 3. Billing: Dynamic calculation engine, part-payments. 4. Auditing: Triggers logging historical actions without fail.","","secondary","secondary")}
{theory_card("User Roles","Admin (Full structural DB access), Doctor (Read patient history, writes prescriptions/diseases), Receptionist (Read/write appointments, read patient basic info, billing operator). Views and GRANT commands secure these roles structurally.","","primary","primary")}
{theory_card("Hardware & Software Req","Environment requirements: Target DB: MySQL 8.x. OS: Linux standard environment. RAM: 4GB minimum for robust buffer pools matching scale. Frontend application connectivity via standard ODBC or native network drivers expecting JSON REST or direct driver.","lg:col-span-2","secondary","secondary")}
</div>"""

    proc = ol_steps([
        "Formulate a title and global objective for the proposed software.",
        "Breakdown the overall vision into 4-6 distinct systemic backend modules.",
        "Categorize interacting user personas (DBA, Cashier, Doctor).",
        "Define hardware limitations based on intended deployment environments.",
        "Draft the textual SRS as the initial structural guide."
    ])

    code = code_block(f"""{cmt("/* ")}
{cmt("   ======================================================")}
{cmt("   Software Requirements Specification (Database View)")}
{cmt("   Project: Hospital Management System (HMS)")}
{cmt("   ======================================================")}
{cmt("")}
{cmt("   1. PROJECT OVERVIEW:")}
{cmt("   The HMS relies heavily on relational accuracy to maintain")}
{cmt("   patient health records and financial transactions safely.")}
{cmt("")}
{cmt("   2. KEY DATABASE MODULES REQUIRED:")}
{cmt("   - User Entity Module (Doctors, Patients)")}
{cmt("   - Operations Module (Departments, Wards, Appointments)")}
{cmt("   - Financial Module (Bills, Payroll, Payments)")}
{cmt("   - Analytics Module (Complex Views & Reporting queries)")}
{cmt("")}
{cmt("   3. DATA CAPACITY ESTIMATION:")}
{cmt("   - Expected patients per year: 20,000")}
{cmt("   - Expected appointments scaling: 50,000 per year")}
{cmt("   - Size per row estimating index weight: ~2KB")}
{cmt("   - Yearly DB growth: 100MB+ depending on schema changes.")}
{cmt("")}
{cmt("   4. RELATIONAL INTEGRITY GOALS:")}
{cmt("   - No bills can be deleted accidentally; only updated to void.")}
{cmt("   - Doctors cannot be deleted if active patients are queued.")}
{cmt("*/")}
""")
    output = out_table(
        ["Component","Status","Assigned Complexity Factor"],
        [["Requirements Authored","Complete","High"],
         ["Data Metrics Formulated","Complete","Medium"]],
        "SRS Status"
    )

    conclusion = """<p class="text-on-surface font-body leading-relaxed mb-4">
By abstracting the goal into an SRS document, the conceptual foundation for a massive software application is standardized. Generating metrics on capacity, outlining business models, and identifying human interactivity structures ensures that subsequent Database structure designs reflect actual application needs.
</p>"""
    vivaqs = [
        ("What does SRS stand for?", "Software Requirements Specification. It is a comprehensive description of the intended purpose and environment for software under development."),
        ("Why estimate load in an SRS before coding?", "Estimating data volume dictates hardware requirements, identifies which variables might need BIGINT over INT, and indicates where index creation will be most critical to future-proof performance."),
        ("How do User Roles map to DBMS concepts?", "User roles in the SRS directly map to Database User Profiles governed by GRANT and REVOKE commands (e.g. Reception gets GRANT SELECT, INSERT; but REVOE DELETE)."),
        ("What makes a Database 'relational'?", "The methodology of storing data points across multiple interconnected tables (relations), minimizing data redundancy while enforcing accuracy using keys.")
    ]
    return build_page(13,"Project Proposal (SRS)","Group D","Project Planning",
        "Authoring a complete structural requirements specification for a proposed backend system.",
        aim, theory, proc, code, output, conclusion, viva(vivaqs))


# ─────────────────────────────────────
# PRACTICAL 14 — ER Diagram & Database Design for Project
# ─────────────────────────────────────
def p14():
    aim = """<p class="text-on-surface font-body leading-relaxed text-lg mb-4">
The aim of this practical is to synthesize the previously established structural SRS into a fully operational Database Design. 
The student will draft an Entity Relational Diagram and commit the final schema design confirming it meets BCNF normalization parameters and fully connects the overarching application dependencies.
</p>"""

    theory = f"""<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{theory_card("Final ER Diagram Construction","Every strong entity defined in the SRS becomes a relational table construct. Multivalued traits become linking structures. ER acts as the final layout agreement linking the raw specifications to the final Codd-normalized environment deployment.","lg:col-span-2","primary","primary")}
{theory_card("Design Verification","The resulting final schema must be evaluated against all DML use cases envisioned. If 'Finding a patient history' takes 4 excessive sub-joins, the schema must be evaluated on balance vs speed vs normalization.","","secondary","secondary")}
</div>"""

    proc = ol_steps([
        "Map entities strictly against SRS documents.",
        "Assign and verify Primary and Partial keys.",
        "Enforce strict Relational lines avoiding cross-dependency loops.",
        "Execute the final unifying schema codebase.",
        "Export and construct final Diagram."
    ])

    code = code_block(f"""{cmt("-- Practical 14: Final ER & Project Schema Finalization")}
{cmt("-- This is a comprehensive review verifying that the entire Hospital architecture is sound.")}

{kw("USE")} {tbl("hospital_db")};

{cmt("-- Output entire finalized structural blueprint of the system.")}

{cmt("-- Confirm active counts matching ER projections.")}
{kw("SELECT")} 
    ({kw("SELECT")} {fn("COUNT")}(*) {kw("FROM")} {tbl("DEPARTMENT")}) {kw("AS")} {tbl("Dept_Count")},
    ({kw("SELECT")} {fn("COUNT")}(*) {kw("FROM")} {tbl("DOCTOR")}) {kw("AS")} {tbl("Doctor_Count")},
    ({kw("SELECT")} {fn("COUNT")}(*) {kw("FROM")} {tbl("PATIENT")}) {kw("AS")} {tbl("Patient_Count")},
    ({kw("SELECT")} {fn("COUNT")}(*) {kw("FROM")} {tbl("APPOINTMENT")}) {kw("AS")} {tbl("Appointments")},
    ({kw("SELECT")} {fn("COUNT")}(*) {kw("FROM")} {tbl("BILL")}) {kw("AS")} {tbl("Financial_Records")};

{cmt("-- Identify referential mapping on schemas created")}
{kw("SELECT")} 
    {tbl("table_name")}, 
    {tbl("column_name")}, 
    {tbl("referenced_table_name")}, 
    {tbl("referenced_column_name")}
{kw("FROM")} {tbl("INFORMATION_SCHEMA")}.{tbl("KEY_COLUMN_USAGE")}
{kw("WHERE")} {tbl("referenced_table_schema")} = {str_("'hospital_db'")};
""")
    output = out_table(
        ["Dept_Count","Doctor_Count","Patient_Count", "Appointments", "Financial_Records"],
        [["5","8","10","10","10"]],
        "Verification Count"
    ) + "<br/>" + out_table(
        ["table_name", "column_name", "referenced_table", "referenced_column"],
        [["APPOINTMENT", "patient_id", "PATIENT", "patient_id"],
         ["APPOINTMENT", "doctor_id", "DOCTOR", "doctor_id"],
         ["DOCTOR", "dept_id", "DEPARTMENT", "dept_id"],
         ["DEPARTMENT", "head_doctor_id", "DOCTOR", "doctor_id"],
         ["BILL", "patient_id", "PATIENT", "patient_id"]],
        "Referential Maps (ER Edges)"
    )

    conclusion = """<p class="text-on-surface font-body leading-relaxed mb-4">
Through a systematic translation of text-based SRS outlines into concrete relational structures, the Hospital Management Architecture is brought to a fully functional completion. Foreign keys successfully mirror conceptual boundaries, guaranteeing data flows correctly per analytical expectations.
</p>"""
    vivaqs = [
        ("How does an ER diagram support Project Management?", "It acts as the visual contract between software developers creating the frontend interface, and database architects maintaining the backend structures."),
        ("What does an entity correspond to in physical SQL layout?", "An entity is translated into a structured TABLE."),
        ("What indicates a 1:N relationship visually in an ER diagram?", "Commonly a 'Crow's Foot' or simply 1 and N labels extending between a Diamond relationship box toward the rectangle entity boundaries."),
        ("Can an ER Diagram have errors?", "Yes. Most commonly 'Chasm traps' or 'Fan traps' where relationships are ambiguous, meaning the eventual SQL schema will fail to associate data correctly across multiple joined links.")
    ]
    return build_page(14,"ER Diagram & Custom DB Design","Group D","Project Construction",
        "Executing the final normalized creation architecture of the target custom project proposal.",
        aim, theory, proc, code, output, conclusion, viva(vivaqs))

if __name__ == "__main__":
    write_practical(12, p12(), BASE_DIR)
    write_practical(13, p13(), BASE_DIR)
    write_practical(14, p14(), BASE_DIR)
    print("Batch 12-14 generated.")
