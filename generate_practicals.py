#!/usr/bin/env python3
"""Generate all 14 DBMS Lab Journal practical HTML files."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TAILWIND_HEAD = """<!DOCTYPE html>
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,200..800;1,6..72,200..800&family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                "inverse-surface": "#dfe2eb",
                "tertiary-fixed-dim": "#ffba3d",
                "tertiary-fixed": "#ffdeae",
                "primary-container": "#00d4ff",
                "on-background": "#dfe2eb",
                "on-primary-container": "#00586b",
                "on-primary-fixed": "#001f27",
                "surface-tint": "#3cd7ff",
                "surface-container-high": "#262a31",
                "on-primary": "#003642",
                "primary-fixed-dim": "#3cd7ff",
                "surface-container": "#1c2026",
                "error": "#ffb4ab",
                "on-secondary-fixed": "#291800",
                "inverse-on-surface": "#2d3137",
                "surface-container-lowest": "#0a0e14",
                "secondary-container": "#dc9100",
                "surface-variant": "#31353c",
                "secondary-fixed": "#ffddb4",
                "inverse-primary": "#00677e",
                "on-secondary": "#452b00",
                "on-secondary-fixed-variant": "#633f00",
                "primary-fixed": "#b4ebff",
                "on-tertiary-fixed-variant": "#604100",
                "on-tertiary": "#432c00",
                "on-error-container": "#ffdad6",
                "on-tertiary-container": "#6c4900",
                "on-primary-fixed-variant": "#004e5f",
                "on-error": "#690005",
                "surface-container-highest": "#31353c",
                "tertiary-container": "#feb528",
                "secondary": "#ffb955",
                "surface-dim": "#10141a",
                "on-tertiary-fixed": "#281900",
                "on-secondary-container": "#4f3100",
                "error-container": "#93000a",
                "secondary-fixed-dim": "#ffb955",
                "outline": "#859398",
                "surface-bright": "#353940",
                "on-surface": "#dfe2eb",
                "surface-container-low": "#181c22",
                "on-surface-variant": "#bbc9cf",
                "surface": "#10141a",
                "background": "#10141a",
                "tertiary": "#ffd9a1",
                "primary": "#a8e8ff",
                "outline-variant": "#3c494e"
            },
            "borderRadius": {
                "DEFAULT": "0.125rem",
                "lg": "0.25rem",
                "xl": "0.5rem",
                "full": "0.75rem"
            },
            "fontFamily": {
                "headline": ["Space Grotesk"],
                "body": ["Newsreader"],
                "label": ["Inter"]
            }
          },
        },
      }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .dot-matrix {
            background-image: radial-gradient(circle, #3c494e 1px, transparent 1px);
            background-size: 32px 32px;
            opacity: 0.05;
        }
        body { background-color: #10141a; color: #dfe2eb; }
        pre { overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; }
        .code-block { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; line-height: 1.7; }
        .output-table { border-collapse: collapse; width: 100%; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; }
        .output-table th { background: rgba(168,232,255,0.12); color: #a8e8ff; padding: 8px 12px; text-align: left; border-bottom: 1px solid #3c494e; }
        .output-table td { padding: 7px 12px; border-bottom: 1px solid #1c2026; color: #bbc9cf; }
        .output-table tr:hover td { background: rgba(168,232,255,0.04); }
        details > summary { cursor: pointer; }
        details[open] > summary { color: #a8e8ff; }
    </style>
"""

FOOTER_HTML = """<footer class="w-full border-t border-slate-800/50 mt-20 bg-[#10141a]">
<div class="flex flex-col md:flex-row justify-between items-center px-12 py-10 w-full max-w-[1440px] mx-auto">
<div class="text-amber-500 font-serif font-['Newsreader'] italic text-lg mb-4 md:mb-0">S.Y.B.Tech IT | Sem IV | Pattern 2023 | Subject: 2308215</div>
<div class="flex gap-8 font-['Newsreader'] italic text-lg">
<a class="text-slate-500 hover:text-amber-200 transition-colors" href="#">University Guidelines</a>
<a class="text-slate-500 hover:text-amber-200 transition-colors" href="#">Lab Manual</a>
<a class="text-slate-500 hover:text-amber-200 transition-colors" href="#">Contact Faculty</a>
</div></div></footer>
</body></html>"""


def sidebar(active_num):
    icons = ["terminal","database","schema","table_chart","query_stats","storage","security",
             "code_blocks","settings_ethernet","lan","cloud_done","account_tree","reorder","history"]
    items = ""
    for i in range(1, 15):
        icon = icons[i-1]
        label = f"Practical {i:02d}"
        if i == active_num:
            items += f'''<a class="flex items-center gap-3 p-3 bg-cyan-500/10 text-cyan-400 font-bold border-r-4 border-cyan-400 font-label text-sm uppercase tracking-widest" href="#">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">{icon}</span>{label}</a>\n'''
        else:
            href = f"../{get_dir(i)}/code.html"
            items += f'''<a class="flex items-center gap-3 p-3 text-slate-500 hover:text-slate-300 font-label text-sm uppercase tracking-widest transition-colors" href="{href}">
<span class="material-symbols-outlined">{icon}</span>{label}</a>\n'''
    return f'''<aside class="hidden md:block sticky left-0 h-[calc(100vh-80px)] w-72 bg-[#181c22] overflow-y-auto border-none top-[64px]">
<div class="flex flex-col gap-1 p-6">
<div class="mb-6">
<h3 class="font-headline font-bold text-primary tracking-widest uppercase text-xs">Lab Practicals</h3>
<p class="text-on-surface-variant text-[10px] uppercase tracking-[0.2em] mt-1 font-label">DBMS Coursework</p>
</div>
{items}
</div></aside>'''


def get_dir(n):
    dirs = {
        1:"practical_01_study_of_mysql",2:"practical_02_mysql_installation",
        3:"practical_03_sqlite_study",4:"practical_04_er_diagrams",
        5:"practical_05_ddl_normalization",6:"practical_06_constraints_alter_drop",
        7:"practical_07_sql_queries",8:"practical_08_views",
        9:"practical_09_implementation_of_joins",10:"practical_10_stored_procedures",
        11:"practical_11_triggers",12:"practical_12_cursors",
        13:"practical_13_project_proposal_srs",14:"practical_14_er_diagram_database_design"
    }
    return dirs[n]


def nav_buttons(n):
    prev_btn = ""
    next_btn = ""
    if n > 1:
        prev_href = f"../{get_dir(n-1)}/code.html"
        prev_btn = f'''<a class="group relative px-6 py-3 bg-surface-container border border-outline-variant/30 text-on-surface font-headline font-bold rounded-lg overflow-hidden transition-transform active:scale-95 hover:border-primary/40" href="{prev_href}">
<span class="relative z-10 flex items-center gap-2"><span class="material-symbols-outlined">arrow_back</span>Practical {n-1:02d}</span></a>'''
    else:
        prev_btn = "<div></div>"
    if n < 14:
        next_href = f"../{get_dir(n+1)}/code.html"
        next_btn = f'''<a class="group relative px-8 py-4 bg-gradient-to-br from-primary to-primary-container text-on-primary font-headline font-bold rounded-lg overflow-hidden transition-transform active:scale-95" href="{next_href}">
<span class="relative z-10 flex items-center gap-2">Next: Practical {n+1:02d}<span class="material-symbols-outlined">arrow_forward</span></span>
<div class="absolute inset-0 bg-white/20 opacity-0 group-hover:opacity-100 transition-opacity"></div></a>'''
    else:
        next_btn = "<div></div>"
    return f'''<div class="flex justify-between items-center pt-12 border-t border-outline-variant/20 mt-16">
{prev_btn}{next_btn}</div>'''


def kw(text): return f'<span class="text-cyan-400">{text}</span>'
def str_(text): return f'<span class="text-green-400">{text}</span>'
def num(text): return f'<span class="text-amber-400">{text}</span>'
def cmt(text): return f'<span class="text-slate-500 italic">{text}</span>'
def tbl(text): return f'<span class="text-slate-300">{text}</span>'
def fn(text): return f'<span class="text-violet-400">{text}</span>'


def code_block(lines_html):
    return f'''<div class="mb-16">
<div class="bg-[#0a0e14] rounded-xl border border-outline-variant/20 overflow-hidden shadow-2xl">
<div class="flex items-center gap-2 px-4 py-3 bg-surface-container-lowest border-b border-outline-variant/20">
<span class="w-3 h-3 rounded-full bg-red-500 inline-block"></span>
<span class="w-3 h-3 rounded-full bg-yellow-500 inline-block"></span>
<span class="w-3 h-3 rounded-full bg-green-500 inline-block"></span>
<span class="ml-4 text-xs font-label text-slate-500 uppercase tracking-widest">MySQL 8.x — Hospital Management System</span>
</div>
<pre class="code-block p-6 text-slate-300">
{lines_html}
</pre></div></div>'''


def section_title(title, subtitle=""):
    sub = f'<div class="flex-1 h-px bg-outline-variant/30"></div><span class="text-slate-500 font-label text-xs uppercase tracking-widest">{subtitle}</span>' if subtitle else '<div class="flex-1 h-px bg-outline-variant/30"></div>'
    return f'''<div class="flex items-center gap-6 mb-8">
<h2 class="text-3xl font-headline font-bold text-on-surface whitespace-nowrap">{title}</h2>
{sub}</div>'''


def theory_card(title, body, span="", accent="primary", border="primary"):
    span_cls = f" {span}" if span else ""
    return f'''<div class="p-8 bg-surface-container-low rounded-xl border-l-4 border-{border}{span_cls}">
<h3 class="text-lg font-headline font-semibold text-{accent} mb-3">{title}</h3>
<p class="text-on-surface-variant font-body leading-relaxed text-sm">{body}</p></div>'''


def build_page(n, title, group, group_label, subtitle, aim_html, theory_html, procedure_html, code_html, output_html, conclusion_html, viva_html):
    return f"""{TAILWIND_HEAD}
<title>Practical {n:02d} | DBMS Journal</title>
<body class="font-body selection:bg-primary/30 selection:text-primary">
<nav class="sticky top-0 z-50 w-full bg-[#10141a]/80 backdrop-blur-xl shadow-[0_0_32px_rgba(0,212,255,0.06)]">
<div class="flex justify-between items-center px-8 py-4 max-w-[1440px] mx-auto">
<div class="text-2xl font-bold bg-gradient-to-br from-cyan-300 to-cyan-500 bg-clip-text text-transparent font-headline tracking-tight">DBMS Journal</div>
<div class="hidden md:flex gap-8 font-headline">
<a class="text-slate-400 hover:text-cyan-200 transition-colors" href="../index.html">Home</a>
<a class="text-cyan-400 border-b-2 border-cyan-400 pb-1" href="#">Practicals</a>
<a class="text-slate-400 hover:text-cyan-200 transition-colors" href="#">About</a>
</div>
<div class="flex items-center gap-4">
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors">menu</button>
</div></div></nav>
<div class="flex max-w-[1440px] mx-auto relative">
{sidebar(n)}
<main class="flex-1 min-w-0 bg-background relative overflow-hidden">
<div class="absolute inset-0 dot-matrix pointer-events-none"></div>
<div class="px-8 py-12 lg:px-16 max-w-5xl mx-auto relative z-10">
<!-- Header -->
<header class="mb-16">
<div class="flex items-center gap-4 mb-6">
<span class="px-3 py-1 bg-primary/10 text-primary border border-primary/20 rounded-lg text-xs font-label uppercase tracking-widest">{group}</span>
<span class="text-on-surface-variant/40">—</span>
<span class="text-on-surface-variant font-label text-xs uppercase tracking-widest">{group_label}</span>
</div>
<h1 class="text-5xl md:text-6xl font-headline font-bold text-on-surface mb-6 tracking-tight">
Practical {n:02d}: <span class="text-primary">{title}</span>
</h1>
<p class="text-xl md:text-2xl text-on-surface-variant font-body leading-relaxed max-w-3xl italic">{subtitle}</p>
</header>

<!-- AIM -->
<section class="mb-16">
{section_title("Aim", "Objective")}
<div class="p-8 bg-surface-container rounded-xl border border-outline-variant/20">
{aim_html}
</div>
</section>

<!-- THEORY -->
<section class="mb-16">
{section_title("Theory & Background", "Core Concepts")}
{theory_html}
</section>

<!-- PROCEDURE -->
<section class="mb-16">
{section_title("Procedure / Algorithm", "Step-by-Step")}
<div class="bg-surface-container-low rounded-xl border border-outline-variant/20 p-8">
{procedure_html}
</div>
</section>

<!-- CODE -->
<section class="mb-16">
{section_title("Complete MySQL Code", "Runnable & Commented")}
{code_html}
</section>

<!-- OUTPUT -->
<section class="mb-16">
{section_title("Expected Output", "Query Results")}
<div class="bg-[#0a0e14] rounded-xl border border-outline-variant/20 p-6 overflow-x-auto">
{output_html}
</div>
</section>

<!-- CONCLUSION -->
<section class="mb-16">
{section_title("Conclusion", "Summary")}
<div class="p-8 bg-surface-container rounded-xl border-l-4 border-secondary">
{conclusion_html}
</div>
</section>

<!-- VIVA VOCE -->
<section class="mb-16">
{section_title("Viva Voce", "Q & A")}
<div class="flex flex-col gap-4">
{viva_html}
</div>
</section>

{nav_buttons(n)}
</div></main></div>
{FOOTER_HTML}"""


# ─────────────────────────────────────────────
# HOSPITAL MANAGEMENT SYSTEM — SHARED DDL CODE
# ─────────────────────────────────────────────
HMS_DDL = f"""{cmt("-- ============================================")}
{cmt("-- Hospital Management System — Schema Setup")}
{cmt("-- Compatible: MySQL 8.x")}
{cmt("-- ============================================")}

{kw("CREATE DATABASE IF NOT EXISTS")} {tbl("hospital_db")};
{kw("USE")} {tbl("hospital_db")};

{cmt("-- Table 1: DEPARTMENT")}
{kw("CREATE TABLE IF NOT EXISTS")} {tbl("DEPARTMENT")} (
    {tbl("dept_id")}       {kw("INT")}          {kw("PRIMARY KEY")},
    {tbl("dept_name")}     {kw("VARCHAR")}({num("50")})  {kw("NOT NULL")} {kw("UNIQUE")},
    {tbl("floor_no")}      {kw("INT")}          {kw("NOT NULL")} {kw("CHECK")}({tbl("floor_no")} {kw("BETWEEN")} {num("1")} {kw("AND")} {num("20")}),
    {tbl("head_doctor_id")} {kw("INT")}         {kw("DEFAULT")} {kw("NULL")}
) {kw("ENGINE")}={str_("InnoDB")};

{cmt("-- Table 2: DOCTOR")}
{kw("CREATE TABLE IF NOT EXISTS")} {tbl("DOCTOR")} (
    {tbl("doctor_id")}         {kw("INT")}         {kw("PRIMARY KEY")},
    {tbl("name")}              {kw("VARCHAR")}({num("80")}) {kw("NOT NULL")},
    {tbl("specialization")}    {kw("VARCHAR")}({num("50")}) {kw("NOT NULL")},
    {tbl("experience_years")}  {kw("INT")}         {kw("CHECK")}({tbl("experience_years")} &gt;= {num("0")}),
    {tbl("salary")}            {kw("DECIMAL")}({num("10")},{num("2")}) {kw("CHECK")}({tbl("salary")} &gt; {num("0")}),
    {tbl("dept_id")}           {kw("INT")},
    {kw("FOREIGN KEY")} ({tbl("dept_id")}) {kw("REFERENCES")} {tbl("DEPARTMENT")}({tbl("dept_id")}) {kw("ON DELETE SET NULL")}
) {kw("ENGINE")}={str_("InnoDB")};

{cmt("-- Table 3: PATIENT")}
{kw("CREATE TABLE IF NOT EXISTS")} {tbl("PATIENT")} (
    {tbl("patient_id")}     {kw("VARCHAR")}({num("10")}) {kw("PRIMARY KEY")},
    {tbl("name")}           {kw("VARCHAR")}({num("80")}) {kw("NOT NULL")},
    {tbl("age")}            {kw("INT")}         {kw("NOT NULL")} {kw("CHECK")}({tbl("age")} {kw("BETWEEN")} {num("0")} {kw("AND")} {num("150")}),
    {tbl("gender")}         {kw("ENUM")}({str_("'Male'")},{str_("'Female'")},{str_("'Other'")}) {kw("NOT NULL")},
    {tbl("disease")}        {kw("VARCHAR")}({num("100")}) {kw("NOT NULL")},
    {tbl("ward_no")}        {kw("INT")}         {kw("CHECK")}({tbl("ward_no")} &gt; {num("0")}),
    {tbl("admission_date")} {kw("DATE")}        {kw("NOT NULL")} {kw("DEFAULT")} ({kw("CURRENT_DATE")})
) {kw("ENGINE")}={str_("InnoDB")};

{cmt("-- Table 4: APPOINTMENT")}
{kw("CREATE TABLE IF NOT EXISTS")} {tbl("APPOINTMENT")} (
    {tbl("appt_id")}    {kw("INT")}          {kw("PRIMARY KEY")} {kw("AUTO_INCREMENT")},
    {tbl("patient_id")} {kw("VARCHAR")}({num("10")}) {kw("NOT NULL")},
    {tbl("doctor_id")}  {kw("INT")}          {kw("NOT NULL")},
    {tbl("appt_date")}  {kw("DATE")}         {kw("NOT NULL")},
    {tbl("status")}     {kw("ENUM")}({str_("'Scheduled'")},{str_("'Completed'")},{str_("'Cancelled'")}) {kw("DEFAULT")} {str_("'Scheduled'")},
    {kw("FOREIGN KEY")} ({tbl("patient_id")}) {kw("REFERENCES")} {tbl("PATIENT")}({tbl("patient_id")}) {kw("ON DELETE CASCADE")},
    {kw("FOREIGN KEY")} ({tbl("doctor_id")})  {kw("REFERENCES")} {tbl("DOCTOR")}({tbl("doctor_id")})  {kw("ON DELETE CASCADE")}
) {kw("ENGINE")}={str_("InnoDB")};

{cmt("-- Table 5: BILL")}
{kw("CREATE TABLE IF NOT EXISTS")} {tbl("BILL")} (
    {tbl("bill_id")}      {kw("INT")}          {kw("PRIMARY KEY")} {kw("AUTO_INCREMENT")},
    {tbl("patient_id")}   {kw("VARCHAR")}({num("10")}) {kw("NOT NULL")},
    {tbl("total_amount")} {kw("DECIMAL")}({num("10")},{num("2")}) {kw("NOT NULL")} {kw("CHECK")}({tbl("total_amount")} &gt;= {num("0")}),
    {tbl("paid_status")}  {kw("ENUM")}({str_("'Paid'")},{str_("'Unpaid'")},{str_("'Partial'")}) {kw("DEFAULT")} {str_("'Unpaid'")},
    {tbl("bill_date")}    {kw("DATE")}         {kw("NOT NULL")} {kw("DEFAULT")} ({kw("CURRENT_DATE")}),
    {kw("FOREIGN KEY")} ({tbl("patient_id")}) {kw("REFERENCES")} {tbl("PATIENT")}({tbl("patient_id")}) {kw("ON DELETE CASCADE")}
) {kw("ENGINE")}={str_("InnoDB")};
"""

HMS_INSERTS = f"""{cmt("-- ============================================")}
{cmt("-- Seed Data — Hospital Management System")}
{cmt("-- ============================================")}

{cmt("-- Insert DEPARTMENT records")}
{kw("INSERT INTO")} {tbl("DEPARTMENT")} ({tbl("dept_id")}, {tbl("dept_name")}, {tbl("floor_no")}) {kw("VALUES")}
({num("1")}, {str_("'Cardiology'")},    {num("3")}),
({num("2")}, {str_("'Neurology'")},     {num("4")}),
({num("3")}, {str_("'Orthopedics'")},   {num("2")}),
({num("4")}, {str_("'Pediatrics'")},    {num("1")}),
({num("5")}, {str_("'Oncology'")},      {num("5")});

{cmt("-- Insert DOCTOR records")}
{kw("INSERT INTO")} {tbl("DOCTOR")} ({tbl("doctor_id")}, {tbl("name")}, {tbl("specialization")}, {tbl("experience_years")}, {tbl("salary")}, {tbl("dept_id")}) {kw("VALUES")}
({num("101")}, {str_("'Dr. Arjun Sharma'")},  {str_("'Cardiologist'")}, {num("12")}, {num("120000.00")}, {num("1")}),
({num("102")}, {str_("'Dr. Priya Mehta'")},   {str_("'Neurologist'")},  {num("8")},  {num("95000.00")},  {num("2")}),
({num("103")}, {str_("'Dr. Karan Patel'")},   {str_("'Orthopedist'")},  {num("15")}, {num("105000.00")}, {num("3")}),
({num("104")}, {str_("'Dr. Sneha Rao'")},     {str_("'Pediatrician'")}, {num("6")},  {num("80000.00")},  {num("4")}),
({num("105")}, {str_("'Dr. Vikram Joshi'")},  {str_("'Oncologist'")},   {num("20")}, {num("150000.00")}, {num("5")}),
({num("106")}, {str_("'Dr. Meena Iyer'")},    {str_("'Cardiologist'")}, {num("10")}, {num("110000.00")}, {num("1")}),
({num("107")}, {str_("'Dr. Rohan Gupta'")},   {str_("'Neurologist'")},  {num("5")},  {num("85000.00")},  {num("2")}),
({num("108")}, {str_("'Dr. Anjali Singh'")},  {str_("'Orthopedist'")},  {num("9")},  {num("98000.00")},  {num("3")});

{cmt("-- Insert PATIENT records")}
{kw("INSERT INTO")} {tbl("PATIENT")} ({tbl("patient_id")}, {tbl("name")}, {tbl("age")}, {tbl("gender")}, {tbl("disease")}, {tbl("ward_no")}, {tbl("admission_date")}) {kw("VALUES")}
({str_("'P001'")}, {str_("'Aarav Shah'")},       {num("45")}, {str_("'Male'")},   {str_("'Diabetes'")},        {num("101")}, {str_("'2024-01-10'")}),
({str_("'P002'")}, {str_("'Priya Mehta'")},      {num("32")}, {str_("'Female'")}, {str_("'Asthma'")},          {num("102")}, {str_("'2024-01-15'")}),
({str_("'P003'")}, {str_("'Rohan Verma'")},      {num("58")}, {str_("'Male'")},   {str_("'Heart Disease'")},   {num("103")}, {str_("'2024-01-20'")}),
({str_("'P004'")}, {str_("'Sneha Joshi'")},      {num("27")}, {str_("'Female'")}, {str_("'Migraine'")},        {num("104")}, {str_("'2024-02-01'")}),
({str_("'P005'")}, {str_("'Amit Patel'")},       {num("63")}, {str_("'Male'")},   {str_("'Arthritis'")},       {num("105")}, {str_("'2024-02-10'")}),
({str_("'P006'")}, {str_("'Kavita Sharma'")},    {num("9")},  {str_("'Female'")}, {str_("'Fever'")},           {num("106")}, {str_("'2024-02-14'")}),
({str_("'P007'")}, {str_("'Nikhil Rao'")},       {num("41")}, {str_("'Male'")},   {str_("'Lung Cancer'")},     {num("107")}, {str_("'2024-02-20'")}),
({str_("'P008'")}, {str_("'Divya Gupta'")},      {num("36")}, {str_("'Female'")}, {str_("'Hypertension'")},    {num("108")}, {str_("'2024-03-01'")}),
({str_("'P009'")}, {str_("'Suresh Nair'")},      {num("52")}, {str_("'Male'")},   {str_("'Diabetes'")},        {num("109")}, {str_("'2024-03-05'")}),
({str_("'P010'")}, {str_("'Ritika Kapoor'")},    {num("29")}, {str_("'Female'")}, {str_("'Anemia'")},          {num("110")}, {str_("'2024-03-10'")});

{cmt("-- Insert APPOINTMENT records")}
{kw("INSERT INTO")} {tbl("APPOINTMENT")} ({tbl("patient_id")}, {tbl("doctor_id")}, {tbl("appt_date")}, {tbl("status")}) {kw("VALUES")}
({str_("'P001'")}, {num("101")}, {str_("'2024-01-12'")}, {str_("'Completed'")}),
({str_("'P002'")}, {num("102")}, {str_("'2024-01-16'")}, {str_("'Completed'")}),
({str_("'P003'")}, {num("101")}, {str_("'2024-01-21'")}, {str_("'Completed'")}),
({str_("'P004'")}, {num("102")}, {str_("'2024-02-02'")}, {str_("'Scheduled'")}),
({str_("'P005'")}, {num("103")}, {str_("'2024-02-12'")}, {str_("'Completed'")}),
({str_("'P006'")}, {num("104")}, {str_("'2024-02-15'")}, {str_("'Completed'")}),
({str_("'P007'")}, {num("105")}, {str_("'2024-02-21'")}, {str_("'Scheduled'")}),
({str_("'P008'")}, {num("106")}, {str_("'2024-03-02'")}, {str_("'Cancelled'")}),
({str_("'P009'")}, {num("101")}, {str_("'2024-03-06'")}, {str_("'Scheduled'")}),
({str_("'P010'")}, {num("107")}, {str_("'2024-03-11'")}, {str_("'Completed'")}));

{cmt("-- Insert BILL records")}
{kw("INSERT INTO")} {tbl("BILL")} ({tbl("patient_id")}, {tbl("total_amount")}, {tbl("paid_status")}, {tbl("bill_date")}) {kw("VALUES")}
({str_("'P001'")}, {num("15000.00")}, {str_("'Paid'")},    {str_("'2024-01-14'")}),
({str_("'P002'")}, {num("8500.00")},  {str_("'Paid'")},    {str_("'2024-01-18'")}),
({str_("'P003'")}, {num("45000.00")}, {str_("'Partial'")}, {str_("'2024-01-25'")}),
({str_("'P004'")}, {num("6000.00")},  {str_("'Unpaid'")},  {str_("'2024-02-04'")}),
({str_("'P005'")}, {num("22000.00")}, {str_("'Paid'")},    {str_("'2024-02-15'")}),
({str_("'P006'")}, {num("3500.00")},  {str_("'Paid'")},    {str_("'2024-02-16'")}),
({str_("'P007'")}, {num("65000.00")}, {str_("'Unpaid'")},  {str_("'2024-02-23'")}),
({str_("'P008'")}, {num("12000.00")}, {str_("'Partial'")}, {str_("'2024-03-03'")}),
({str_("'P009'")}, {num("18500.00")}, {str_("'Paid'")},    {str_("'2024-03-08'")}),
({str_("'P010'")}, {num("9000.00")},  {str_("'Paid'")},    {str_("'2024-03-13'")});
"""


def out_table(headers, rows, caption=""):
    ths = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    cap = f'<p class="text-slate-500 font-label text-xs mb-3 uppercase tracking-widest">{caption}</p>' if caption else ""
    return f'''{cap}<div class="overflow-x-auto"><table class="output-table"><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table></div>'''


def viva(qas):
    items = ""
    for i, (q, a) in enumerate(qas, 1):
        items += f'''<details class="bg-surface-container-low rounded-xl border border-outline-variant/20 overflow-hidden">
<summary class="p-5 font-label font-semibold text-on-surface flex items-center gap-3 hover:text-primary transition-colors">
<span class="text-primary font-headline font-bold text-xl w-8">Q{i}.</span>{q}
</summary>
<div class="px-8 pb-6 pt-2 text-on-surface-variant font-body leading-relaxed border-t border-outline-variant/20">
<span class="text-secondary font-bold">Ans:</span> {a}
</div></details>'''
    return items


def ol_steps(steps):
    items = "".join(f'<li class="flex gap-4"><span class="text-primary font-headline font-bold text-lg w-8 shrink-0">{i:02d}.</span><span class="text-on-surface-variant font-body leading-relaxed">{s}</span></li>' for i, s in enumerate(steps, 1))
    return f'<ol class="flex flex-col gap-5">{items}</ol>'


# ─────────────────────────────────────
# PRACTICAL 01 — Study of MySQL
# ─────────────────────────────────────
def p01():
    aim = """<p class="text-on-surface font-body leading-relaxed text-lg mb-4">
The aim of this practical is to study MySQL as an open-source relational database management system (RDBMS), exploring its core architecture, salient features, storage engines, and the role it plays in modern enterprise and web-based applications. The student will gain theoretical knowledge of how MySQL processes queries from client applications through a multi-layered architecture comprising connectors, query parsers, optimizers, and pluggable storage engines.
</p>
<p class="text-on-surface-variant font-body leading-relaxed">
By the end of this practical, students will understand the differences between MySQL Editions (Community vs Enterprise), comprehend key concepts such as ACID properties, indexing, and transaction management, and relate these concepts to real-world systems such as hospital information management platforms, e-commerce databases, and banking applications that rely on MySQL for persistent, reliable data storage.
</p>"""

    theory = f"""<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{theory_card("What is MySQL?","MySQL is an open-source RDBMS developed by Oracle Corporation. It organises data into tables (relations) using Structured Query Language (SQL). First released in 1995, it now powers over 50% of web applications globally, including WordPress, Facebook (historically), and Twitter.","lg:col-span-2","primary","primary")}
{theory_card("History & Versions","MySQL was created by Michael Widenius and David Axmark. Key milestones: v3.x (1996) — basic SQL; v5.x (2005) — stored procedures, triggers, views; v5.7 (2015) — JSON support; v8.0 (2018) — window functions, CTEs, role-based access control, atomic DDL.","","secondary","secondary")}
{theory_card("MySQL Architecture","The MySQL architecture has four layers: (1) Client Layer — connectors (JDBC, ODBC, PHP PDO), (2) Server Layer — authentication, query cache, SQL parser, query optimizer, (3) Storage Engine Layer — pluggable engines (InnoDB, MyISAM, MEMORY), (4) File System Layer — data files, redo logs, undo logs.","lg:col-span-3","primary","primary")}
{theory_card("InnoDB Storage Engine","InnoDB is the default storage engine since MySQL 5.5. It supports ACID transactions, row-level locking, foreign keys, MVCC (Multi-Version Concurrency Control) for non-blocking reads, crash recovery via redo/undo logs, and clustered indexes where data is physically sorted by PRIMARY KEY.","","secondary","secondary")}
{theory_card("MyISAM vs InnoDB","MyISAM: table-level locking, no FK support, faster reads on read-heavy workloads, no crash recovery. InnoDB: row-level locking, FK support, ACID, MVCC, crash recovery, better for OLTP. MyISAM is now considered legacy — InnoDB is the production standard.","","primary","primary")}
{theory_card("ACID Properties","Atomicity: entire transaction succeeds or fully rolls back. Consistency: DB moves from one valid state to another. Isolation: concurrent transactions do not interfere (read-uncommitted → serializable). Durability: committed transactions survive crashes via write-ahead logging.","","secondary","secondary")}
{theory_card("Indexing in MySQL","MySQL supports B-Tree indexes (default), Hash indexes (MEMORY engine), Full-Text indexes, and Spatial indexes. PRIMARY KEY creates a clustered index in InnoDB. Secondary indexes store a copy of the PK. Proper indexing can reduce query time from O(n) to O(log n).","lg:col-span-2","primary","primary")}
{theory_card("Real-World Use Cases","MySQL powers mission-critical systems: Netflix uses MySQL for user data, GitHub uses it for repository metadata, LinkedIn uses MySQL Cluster for high-availability, and hospital EMR (Electronic Medical Record) systems rely on MySQL for patient data storage with HIPAA-compliant access control.","","secondary","secondary")}
</div>"""

    proc = ol_steps([
        "Open MySQL Workbench or MySQL command-line client on your system.",
        "Log in with root credentials: <code class='text-cyan-400 bg-surface-container px-1 rounded'>mysql -u root -p</code>",
        "View all existing databases with <code class='text-cyan-400 bg-surface-container px-1 rounded'>SHOW DATABASES;</code>",
        "Study the output — note system databases: information_schema, mysql, performance_schema, sys.",
        "Check the MySQL server version: <code class='text-cyan-400 bg-surface-container px-1 rounded'>SELECT VERSION();</code>",
        "View available storage engines: <code class='text-cyan-400 bg-surface-container px-1 rounded'>SHOW ENGINES;</code>",
        "View server status variables: <code class='text-cyan-400 bg-surface-container px-1 rounded'>SHOW STATUS LIKE 'Uptime';</code>",
        "Inspect global variables to understand configuration: <code class='text-cyan-400 bg-surface-container px-1 rounded'>SHOW VARIABLES LIKE 'innodb%';</code>",
        "Create the Hospital Database for use across all practicals: <code class='text-cyan-400 bg-surface-container px-1 rounded'>CREATE DATABASE hospital_db;</code>",
        "Switch to the new database: <code class='text-cyan-400 bg-surface-container px-1 rounded'>USE hospital_db;</code>",
        "Record observations: storage engines, version number, key configuration variables shown by SHOW VARIABLES.",
        "Close the session and note all findings in your journal with explanations of each command output."
    ])

    code = code_block(f"""{cmt("-- ================================================================")}
{cmt("-- Practical 01: Study of MySQL — Exploration Queries")}
{cmt("-- ================================================================")}

{cmt("-- Step 1: Check MySQL version")}
{kw("SELECT")} {fn("VERSION")}() {kw("AS")} {tbl("MySQL_Version")};

{cmt("-- Step 2: Display all available databases")}
{kw("SHOW")} {kw("DATABASES")};

{cmt("-- Step 3: Display all storage engines and their support status")}
{kw("SHOW")} {kw("ENGINES")};

{cmt("-- Step 4: Show server status (uptime, connections, queries)")}
{kw("SHOW")} {kw("STATUS")} {kw("LIKE")} {str_("'Connections'")};
{kw("SHOW")} {kw("STATUS")} {kw("LIKE")} {str_("'Questions'")};
{kw("SHOW")} {kw("STATUS")} {kw("LIKE")} {str_("'Uptime'")};

{cmt("-- Step 5: View key InnoDB configuration variables")}
{kw("SHOW")} {kw("VARIABLES")} {kw("LIKE")} {str_("'innodb_buffer_pool_size'")};
{kw("SHOW")} {kw("VARIABLES")} {kw("LIKE")} {str_("'max_connections'")};

{cmt("-- Step 6: Create the Hospital Management System database")}
{kw("CREATE DATABASE IF NOT EXISTS")} {tbl("hospital_db")}
    {kw("CHARACTER SET")} {str_("utf8mb4")}
    {kw("COLLATE")} {str_("utf8mb4_unicode_ci")};

{cmt("-- Step 7: Switch to the new database")}
{kw("USE")} {tbl("hospital_db")};

{cmt("-- Step 8: Confirm active database")}
{kw("SELECT")} {fn("DATABASE")}() {kw("AS")} {tbl("Current_Database")};

{cmt("-- Step 9: Inspect user privileges (to understand access control)")}
{kw("SHOW")} {kw("GRANTS")} {kw("FOR")} {str_("'root'@'localhost'")};

{cmt("-- Step 10: Check current character set settings")}
{kw("SHOW")} {kw("VARIABLES")} {kw("LIKE")} {str_("'character_set%'")};
""")

    output = out_table(
        ["MySQL_Version"],
        [["8.0.36"]],
        "SELECT VERSION()"
    ) + "<br/>" + out_table(
        ["Engine", "Support", "Transactions", "XA", "Savepoints"],
        [["InnoDB","DEFAULT","YES","YES","YES"],
         ["MRG_MYISAM","YES","NO","NO","NO"],
         ["MEMORY","YES","NO","NO","NO"],
         ["BLACKHOLE","YES","NO","NO","NO"],
         ["MyISAM","YES","NO","NO","NO"]],
        "SHOW ENGINES — (partial)"
    ) + "<br/>" + out_table(
        ["Current_Database"],
        [["hospital_db"]],
        "SELECT DATABASE()"
    )

    conclusion = """<p class="text-on-surface font-body leading-relaxed mb-4">
This practical provided a comprehensive introduction to MySQL as the world's leading open-source RDBMS. By executing exploration queries, we confirmed the MySQL version (8.0.x), examined the available storage engines with InnoDB as the default, and understood the significance of ACID compliance in transactional systems. We successfully created the <code class="text-cyan-400">hospital_db</code> database that will serve as the foundation schema for all subsequent practicals.
</p>
<p class="text-on-surface-variant font-body leading-relaxed">
The architectural understanding of MySQL's layered design — from client connectors through the query optimizer to pluggable storage engines — is essential for designing performant, scalable database solutions. Best practice: always use InnoDB for production tables requiring transactions and foreign key constraints, and configure <code class="text-cyan-400">innodb_buffer_pool_size</code> to approximately 70–80% of available RAM for optimal performance.
</p>"""

    vivaqs = [
        ("What is the difference between a DBMS and an RDBMS?",
         "A DBMS (Database Management System) is software that manages data in a structured way. An RDBMS (Relational DBMS) specifically organises data into relations (tables) with relationships between them, enforces data integrity via constraints, and supports SQL. MySQL is an RDBMS; MongoDB is a NoSQL DBMS."),
        ("What are the main storage engines in MySQL and their differences?",
         "InnoDB supports ACID transactions, row-level locking, foreign keys, and MVCC — ideal for OLTP. MyISAM does not support transactions or FK, uses table-level locking — suitable for read-heavy, non-critical data. MEMORY stores data in RAM for ultra-fast but volatile access."),
        ("Explain ACID properties with examples from the Hospital system.",
         "Atomicity: when a patient is admitted and a bill is generated, both succeed or both fail. Consistency: bill amounts must always be ≥ 0. Isolation: two doctors booking the same patient simultaneously do not see each other's partial updates. Durability: a committed appointment persists even after a server restart."),
        ("What is the purpose of INFORMATION_SCHEMA in MySQL?",
         "INFORMATION_SCHEMA is a virtual database that provides metadata about all other databases, tables, columns, indexes, and constraints on the server. It is read-only and extremely useful for automated schema introspection, database documentation, and performance analysis."),
        ("What new features were introduced in MySQL 8.0?",
         "MySQL 8.0 introduced: Window Functions (RANK, DENSE_RANK, LAG, LEAD), Common Table Expressions (CTEs) with WITH clause, Atomic DDL statements, Role-Based Access Control, Default Character Set changed to utf8mb4, Invisible Indexes, Descending Indexes, and improved JSON support with JSON_TABLE().")
    ]

    return build_page(1,"Study of MySQL","Group A","Relational Databases",
        "An exploration into the architecture, core features, and storage engines of the world's most popular open-source RDBMS.",
        aim, theory, proc, code, output, conclusion, viva(vivaqs))


# ─────────────────────────────────────
# PRACTICAL 02 — MySQL Installation & Configuration
# ─────────────────────────────────────
def p02():
    aim = """<p class="text-on-surface font-body leading-relaxed text-lg mb-4">
The aim of this practical is to guide the student through the complete installation, configuration, and initial setup of MySQL Server 8.x on a local development machine (Windows/Linux/macOS). The student will learn how to configure essential parameters in the my.cnf / my.ini file, secure the MySQL installation using the built-in security script, and test the connection using MySQL Workbench and the command-line client.
</p>
<p class="text-on-surface-variant font-body leading-relaxed">
This practical simulates the initial database administrator (DBA) setup phase that is mandatory for any production deployment — from a hospital EMR system to an enterprise ERP. Understanding configuration parameters such as buffer pool size, max connections, and binary logging is critical for performance tuning and disaster recovery planning.
</p>"""

    theory = f"""<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{theory_card("MySQL Installation Process","MySQL Server can be installed via: (1) MySQL Installer (Windows MSI wizard with product selector — Server, Workbench, Shell, Router), (2) Package Manager on Linux (apt/yum: sudo apt install mysql-server), (3) DMG package on macOS, (4) Docker container: docker run -d mysql:8.0. The installer automatically initialises the data directory and generates a temporary root password.","lg:col-span-2","primary","primary")}
{theory_card("MySQL Editions","Community Edition: Free, open-source (GPL), supported by community. Enterprise Edition: Commercial, includes monitoring (MySQL Enterprise Monitor), backup (MEB), encryption, firewall, audit log, technical support from Oracle. Cluster CGE: High-availability via NDB storage engine for 99.999% uptime.","","secondary","secondary")}
{theory_card("my.cnf / my.ini Configuration File","The server configuration file controls runtime behaviour: [mysqld] section sets server variables. Key parameters: port (default 3306), bind-address, datadir, max_connections (default 151), innodb_buffer_pool_size (set to 70% of RAM), slow_query_log, log_error, character-set-server=utf8mb4, collation-server=utf8mb4_unicode_ci.","lg:col-span-3","primary","primary")}
{theory_card("mysql_secure_installation","After installation, run mysql_secure_installation to: set the root password, remove anonymous users, disallow remote root login, remove the test database, and reload privilege tables. This hardens the default installation against common security vulnerabilities.","","secondary","secondary")}
{theory_card("MySQL Workbench","MySQL Workbench is the official GUI tool for MySQL. It provides: (1) SQL Editor with syntax highlighting, (2) Visual Schema Designer for ER diagrams, (3) Server Administration panel, (4) Performance Dashboard, (5) Data Import/Export wizard, (6) Migration Wizard for migrating from other RDBMS.","","primary","primary")}
{theory_card("User Management & Privileges","MySQL uses a privilege system based on: GRANT/REVOKE statements, user accounts identified by username@host pair, privilege levels (Global, Database, Table, Column, Routine), and predefined roles (MySQL 8+). The mysql.user system table stores all account information.","","secondary","secondary")}
</div>"""

    proc = ol_steps([
        "Download MySQL Installer from <em>dev.mysql.com/downloads</em> — choose Community Edition for the lab environment.",
        "Run the installer and select 'Developer Default' setup type, which installs MySQL Server, Workbench, Shell, and connectors.",
        "During configuration wizard: set port to 3306, choose Strong Password Encryption (caching_sha2_password), and set a strong root password.",
        "After installation, open MySQL Workbench and create a new connection: Hostname=127.0.0.1, Port=3306, Username=root.",
        "Open terminal/command prompt and test CLI connection: <code class='text-cyan-400'>mysql -u root -p</code> — enter your root password.",
        "Run <code class='text-cyan-400'>SHOW VARIABLES LIKE 'innodb_buffer_pool_size';</code> to check current buffer pool (default ~128MB).",
        "Open my.cnf (Linux: /etc/mysql/my.cnf; Windows: C:\\ProgramData\\MySQL\\MySQL Server 8.0\\my.ini) in a text editor.",
        "Add/modify: innodb_buffer_pool_size=512M, max_connections=200, slow_query_log=1, general_log=0. Save the file.",
        "Restart MySQL service: Linux: <code class='text-cyan-400'>sudo systemctl restart mysql</code> | Windows: Services panel → MySQL80 → Restart.",
        "Verify changes: <code class='text-cyan-400'>SHOW VARIABLES LIKE 'max_connections';</code> — confirm it shows 200.",
        "Create a dedicated application user: <code class='text-cyan-400'>CREATE USER 'hms_user'@'localhost' IDENTIFIED BY 'SecurePass@123';</code>",
        "Grant privileges: <code class='text-cyan-400'>GRANT ALL PRIVILEGES ON hospital_db.* TO 'hms_user'@'localhost'; FLUSH PRIVILEGES;</code>"
    ])

    code = code_block(f"""{cmt("-- ================================================================")}
{cmt("-- Practical 02: MySQL Installation & Configuration")}
{cmt("-- Run these after successful installation")}
{cmt("-- ================================================================")}

{cmt("-- Step 1: Verify MySQL is running and accessible")}
{kw("SELECT")} {fn("NOW")}() {kw("AS")} {tbl("Server_Time")}, {fn("VERSION")}() {kw("AS")} {tbl("Version")}, {fn("USER")}() {kw("AS")} {tbl("Current_User")};

{cmt("-- Step 2: Check data directory location")}
{kw("SHOW")} {kw("VARIABLES")} {kw("LIKE")} {str_("'datadir'")};

{cmt("-- Step 3: Verify port configuration")}
{kw("SHOW")} {kw("VARIABLES")} {kw("LIKE")} {str_("'port'")};

{cmt("-- Step 4: Verify character set (should be utf8mb4 after configuration)")}
{kw("SHOW")} {kw("VARIABLES")} {kw("LIKE")} {str_("'character_set_server'")};

{cmt("-- Step 5: Check max_connections")}
{kw("SHOW")} {kw("VARIABLES")} {kw("LIKE")} {str_("'max_connections'")};

{cmt("-- Step 6: Create the HMS database with proper character set")}
{kw("CREATE DATABASE IF NOT EXISTS")} {tbl("hospital_db")}
    {kw("CHARACTER SET")} {str_("utf8mb4")}
    {kw("COLLATE")} {str_("utf8mb4_unicode_ci")};

{kw("USE")} {tbl("hospital_db")};

{cmt("-- Step 7: Create a dedicated HMS application user")}
{cmt("-- NOTE: Run these as root")}
{kw("CREATE USER")} {str_("'hms_user'@'localhost'")} {kw("IDENTIFIED WITH")} {str_("caching_sha2_password")} {kw("BY")} {str_("'HospDB@2024!'")};

{cmt("-- Step 8: Grant appropriate privileges")}
{kw("GRANT")} {kw("SELECT")}, {kw("INSERT")}, {kw("UPDATE")}, {kw("DELETE")}, {kw("CREATE")}, {kw("DROP")}, {kw("INDEX")}, {kw("ALTER")}
{kw("ON")} {tbl("hospital_db.*")} {kw("TO")} {str_("'hms_user'@'localhost'")};

{cmt("-- Step 9: Apply privilege changes immediately")}
{kw("FLUSH")} {kw("PRIVILEGES")};

{cmt("-- Step 10: Verify the user was created")}
{kw("SELECT")} {tbl("user")}, {tbl("host")}, {tbl("plugin")} {kw("FROM")} {tbl("mysql.user")} {kw("WHERE")} {tbl("user")} = {str_("'hms_user'")};

{cmt("-- Step 11: Show all grants for the new user")}
{kw("SHOW")} {kw("GRANTS")} {kw("FOR")} {str_("'hms_user'@'localhost'")};

{cmt("-- Step 12: Check InnoDB buffer pool size post-configuration")}
{kw("SHOW")} {kw("VARIABLES")} {kw("LIKE")} {str_("'innodb_buffer_pool_size'")};

{cmt("-- Step 13: View slow query log settings")}
{kw("SHOW")} {kw("VARIABLES")} {kw("LIKE")} {str_("'slow_query%'")};
""")

    output = out_table(
        ["Server_Time","Version","Current_User"],
        [["2024-03-15 10:30:45","8.0.36","root@localhost"]],
        "Server Info"
    ) + "<br/>" + out_table(
        ["Variable_name","Value"],
        [["character_set_server","utf8mb4"],
         ["max_connections","200"],
         ["innodb_buffer_pool_size","536870912"],
         ["port","3306"],
         ["datadir","/var/lib/mysql/"]],
        "SHOW VARIABLES — post-configuration"
    ) + "<br/>" + out_table(
        ["user","host","plugin"],
        [["hms_user","localhost","caching_sha2_password"]],
        "User created successfully"
    )

    conclusion = """<p class="text-on-surface font-body leading-relaxed mb-4">
This practical demonstrated the complete MySQL 8.0 installation and post-installation configuration workflow. We successfully configured critical server parameters including character set (utf8mb4), max connections, and InnoDB buffer pool size to optimise the server for our Hospital Management System. The creation of a dedicated application user (hms_user) with principle-of-least-privilege access enforces the security best practice of never using the root account for application-level database operations.
</p>
<p class="text-on-surface-variant font-body leading-relaxed">
Best practices observed: use utf8mb4 character set for full Unicode support (including emoji and multilingual clinical data), always run mysql_secure_installation after setup, configure innodb_buffer_pool_size to 70–80% of available RAM for OLTP workloads, and enable slow_query_log to identify and optimise performance bottlenecks early in development.
</p>"""

    vivaqs = [
        ("What is the default port for MySQL and how do you change it?",
         "The default MySQL port is 3306. To change it, modify the 'port' directive in my.cnf under [mysqld] section, then restart the MySQL service. The client must then use mysql -P <new_port> -u root -p to connect."),
        ("What is the difference between caching_sha2_password and mysql_native_password?",
         "caching_sha2_password (default in MySQL 8.0) uses SHA-256 hashing with salting and caching — significantly more secure. mysql_native_password uses SHA-1 hashing — weaker but widely compatible with older clients/drivers. For new installations, always use caching_sha2_password."),
        ("What is innodb_buffer_pool_size and why is it important?",
         "It is the memory area where InnoDB caches table and index data. Larger values mean more data fits in RAM, reducing disk I/O. For a dedicated MySQL server, setting it to 70-80% of total RAM significantly improves query performance for read-heavy workloads."),
        ("What does FLUSH PRIVILEGES do?",
         "FLUSH PRIVILEGES forces MySQL to reload the grant tables from the mysql.user system table into memory. It is required after directly modifying grant tables with INSERT/UPDATE/DELETE. When using GRANT/REVOKE statements, MySQL automatically flushes privileges."),
        ("What are the key files/directories created during MySQL installation?",
         "datadir (default /var/lib/mysql/) — stores all database files, ibdata1 (InnoDB system tablespace), ib_logfile0/1 (redo logs), error log file (hostname.err), my.cnf/my.ini — configuration file, and the mysql/ directory within datadir containing system tables.")
    ]

    return build_page(2,"MySQL Installation & Configuration","Group A","Database Setup",
        "A complete walkthrough of installing, securing, and configuring MySQL 8.x for the Hospital Management System.",
        aim, theory, proc, code, output, conclusion, viva(vivaqs))


# ─────────────────────────────────────
# PRACTICAL 03 — Study of SQLite
# ─────────────────────────────────────
def p03():
    aim = """<p class="text-on-surface font-body leading-relaxed text-lg mb-4">
The aim of this practical is to study SQLite — a lightweight, serverless, self-contained, embedded SQL database engine — and compare it with MySQL across key dimensions such as architecture, scalability, concurrency, data types, and target use cases. The student will understand when to choose SQLite over a full client-server RDBMS and learn how to interact with SQLite databases.
</p>
<p class="text-on-surface-variant font-body leading-relaxed">
SQLite is deployed in billions of devices globally — including Android and iOS mobile apps, Chromium browser, Firefox, and many IoT sensors. Understanding its architecture helps developers make informed decisions when designing data-persistence layers for mobile healthcare apps, offline-capable web applications, and embedded systems that cannot run a full MySQL server.
</p>"""

    theory = f"""<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{theory_card("What is SQLite?","SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured SQL database engine. Unlike client-server databases, SQLite reads and writes directly to ordinary disk files. The entire database — tables, indexes, triggers, and views — is stored in a single cross-platform .db file.","lg:col-span-2","primary","primary")}
{theory_card("Serverless Architecture","SQLite has no separate server process. The application directly links to the SQLite library. This eliminates: client-server communication overhead, separate installation/admin, network latency, and authentication layers. The database is simply a file on disk — portable, zero-config.","","secondary","secondary")}
{theory_card("SQLite vs MySQL — Comparison","SQLite: Serverless, single .db file, dynamic typing, no user management, 281TB max DB size, WAL mode for concurrency. MySQL: Client-server, separate data directory, strict typing, user/privilege system, no practical size limit, MVCC concurrency. SQLite suits embedded/local; MySQL suits multi-user/web.","lg:col-span-3","primary","primary")}
{theory_card("Dynamic Typing","SQLite uses Type Affinity — a declared type is a suggestion, not enforcement. Storage classes: NULL, INTEGER, REAL, TEXT, BLOB. A TEXT column can store an integer. This flexibility is useful in rapid prototyping but can cause data integrity issues in production — MySQL's strict mode prevents such anomalies.","","secondary","secondary")}
{theory_card("WAL Mode (Write-Ahead Log)","In WAL mode (PRAGMA journal_mode=WAL), writers do not block readers and readers do not block writers. This dramatically improves concurrent read performance. WAL is the recommended mode for mobile applications where reads greatly outnumber writes.","","primary","primary")}
{theory_card("Use Cases for SQLite","SQLite is ideal for: Mobile apps (Android Room, iOS Core Data), Browser storage (localStorage alternative), Unit testing (in-memory database with :memory:), Configuration files replacement, Embedded devices, Offline-capable web apps (Electron, Tauri). It is NOT suitable for high-concurrency multi-user web backends.","","secondary","secondary")}
</div>"""

    proc = ol_steps([
        "Install SQLite: Linux: <code class='text-cyan-400'>sudo apt install sqlite3</code> | macOS: pre-installed | Windows: download from sqlite.org/download.html.",
        "Open SQLite CLI: type <code class='text-cyan-400'>sqlite3 hospital_lite.db</code> to create/open a database file.",
        "View available dot-commands: <code class='text-cyan-400'>.help</code> — these are SQLite-specific meta-commands.",
        "Create a simplified PATIENT table in SQLite to observe the dynamic typing behaviour.",
        "Insert sample data and perform SELECT queries — compare syntax with MySQL.",
        "Test dynamic typing: insert a text value into an INTEGER column — observe that SQLite accepts it.",
        "Enable WAL mode: <code class='text-cyan-400'>PRAGMA journal_mode=WAL;</code> and observe the response.",
        "View all tables: <code class='text-cyan-400'>.tables</code> and view schema: <code class='text-cyan-400'>.schema PATIENT</code>",
        "Export database to SQL script: <code class='text-cyan-400'>.output hospital_backup.sql</code> then <code class='text-cyan-400'>.dump</code>",
        "Open a fresh SQLite instance, import the backup: <code class='text-cyan-400'>.read hospital_backup.sql</code>",
        "Compare with MySQL: note the absence of ENUM, no AUTO_INCREMENT (use INTEGER PRIMARY KEY for ROWID alias), no SHOW TABLES (use .tables instead).",
        "Exit SQLite: <code class='text-cyan-400'>.quit</code> and note that the .db file persists on disk."
    ])

    code = code_block(f"""{cmt("-- ================================================================")}
{cmt("-- Practical 03: SQLite Study — Commands & Queries")}
{cmt("-- These run in: sqlite3 hospital_lite.db")}
{cmt("-- ================================================================")}

{cmt("-- SQLite Dot Commands (meta-commands, not SQL)")}
{cmt("-- .databases    -- show attached databases")}
{cmt("-- .tables       -- list all tables")}
{cmt("-- .schema <tbl> -- show CREATE statement")}
{cmt("-- .mode column  -- display mode")}
{cmt("-- .headers on   -- show column headers")}
{cmt("-- .quit         -- exit SQLite")}

{cmt("-- Step 1: Enable WAL journal mode for better concurrency")}
{kw("PRAGMA")} {tbl("journal_mode")} = {str_("WAL")};

{cmt("-- Step 2: Create lightweight PATIENT table (SQLite syntax)")}
{kw("CREATE TABLE IF NOT EXISTS")} {tbl("PATIENT")} (
    {tbl("patient_id")} {kw("INTEGER")} {kw("PRIMARY KEY")} {kw("AUTOINCREMENT")},  {cmt("-- ROWID alias")}
    {tbl("name")}       {kw("TEXT")}    {kw("NOT NULL")},
    {tbl("age")}        {kw("INTEGER")},
    {tbl("disease")}    {kw("TEXT")}
);

{cmt("-- Step 3: Insert sample data")}
{kw("INSERT INTO")} {tbl("PATIENT")} ({tbl("name")}, {tbl("age")}, {tbl("disease")}) {kw("VALUES")}
({str_("'Aarav Shah'")},    {num("45")}, {str_("'Diabetes'")}),
({str_("'Priya Mehta'")},   {num("32")}, {str_("'Asthma'")}),
({str_("'Rohan Verma'")},   {num("58")}, {str_("'Heart Disease'")}),
({str_("'Sneha Joshi'")},   {num("27")}, {str_("'Migraine'")}),
({str_("'Amit Patel'")},    {num("63")}, {str_("'Arthritis'")});

{cmt("-- Step 4: Query patients")}
{kw("SELECT")} * {kw("FROM")} {tbl("PATIENT")} {kw("ORDER BY")} {tbl("age")} {kw("DESC")};

{cmt("-- Step 5: Demonstrate dynamic typing (SQLite-specific behaviour)")}
{cmt("-- This would FAIL in MySQL strict mode but WORKS in SQLite")}
{kw("INSERT INTO")} {tbl("PATIENT")} ({tbl("name")}, {tbl("age")}, {tbl("disease")})
{kw("VALUES")} ({str_("'Test Patient'")}, {str_("'forty-five'")}, {str_("'Flu'")});
{cmt("-- Notice: 'forty-five' stored as TEXT in INTEGER column")}

{kw("SELECT")} {tbl("name")}, {tbl("age")}, {fn("TYPEOF")}({tbl("age")}) {kw("AS")} {tbl("age_type")} {kw("FROM")} {tbl("PATIENT")};

{cmt("-- Step 6: SQLite aggregate functions (same as MySQL)")}
{kw("SELECT")} {fn("COUNT")}(*) {kw("AS")} {tbl("Total_Patients")},
       {fn("AVG")}({tbl("age")}) {kw("AS")} {tbl("Avg_Age")},
       {fn("MAX")}({tbl("age")}) {kw("AS")} {tbl("Oldest")},
       {fn("MIN")}({tbl("age")}) {kw("AS")} {tbl("Youngest")}
{kw("FROM")} {tbl("PATIENT")}
{kw("WHERE")} {fn("TYPEOF")}({tbl("age")}) = {str_("'integer'")};

{cmt("-- Step 7: SQLite date/time functions")}
{kw("SELECT")} {fn("date")}({str_("'now'")}) {kw("AS")} {tbl("Today")},
       {fn("strftime")}({str_("'%Y'")}, {str_("'now'")}) {kw("AS")} {tbl("Current_Year")};

{cmt("-- Step 8: Check SQLite version")}
{kw("SELECT")} {fn("sqlite_version")}();
""")

    output = out_table(
        ["patient_id","name","age","disease"],
        [["5","Amit Patel","63","Arthritis"],
         ["3","Rohan Verma","58","Heart Disease"],
         ["1","Aarav Shah","45","Diabetes"],
         ["2","Priya Mehta","32","Asthma"],
         ["4","Sneha Joshi","27","Migraine"]],
        "SELECT * FROM PATIENT ORDER BY age DESC"
    ) + "<br/>" + out_table(
        ["name","age","age_type"],
        [["Aarav Shah","45","integer"],
         ["Priya Mehta","32","integer"],
         ["Rohan Verma","58","integer"],
         ["Sneha Joshi","27","integer"],
         ["Amit Patel","63","integer"],
         ["Test Patient","forty-five","text"]],
        "Dynamic Typing Demo — TYPEOF(age)"
    ) + "<br/>" + out_table(
        ["Total_Patients","Avg_Age","Oldest","Youngest"],
        [["5","45.0","63","27"]],
        "Aggregate on integer-typed rows only"
    )

    conclusion = """<p class="text-on-surface font-body leading-relaxed mb-4">
This practical demonstrated that SQLite, despite being a lightweight serverless engine, supports the core SQL standard including DDL, DML, aggregate functions, joins, and triggers. Its defining characteristic — dynamic typing and single-file storage — makes it uniquely suited for mobile and embedded applications where deploying a full MySQL server is impractical. The Hospital Management System's mobile companion app, for example, could use SQLite for offline patient data capture, syncing to the central MySQL server when connectivity is restored.
</p>
<p class="text-on-surface-variant font-body leading-relaxed">
Key limitations of SQLite include lack of user-level access control, limited concurrency for write-heavy workloads, no built-in network access, and incomplete support for some SQL features (e.g., RIGHT JOIN, FULL OUTER JOIN until v3.39). For a multi-user hospital system serving hundreds of concurrent nurses and doctors, MySQL with InnoDB remains the appropriate choice.
</p>"""

    vivaqs = [
        ("What does 'serverless' mean in the context of SQLite?",
         "Serverless in SQLite means there is no separate server process — the SQLite library is directly linked into the application and reads/writes the database file directly. There is no socket, no port, no authentication server. This contrasts with MySQL where a background mysqld daemon process handles all connections."),
        ("What is the maximum database size supported by SQLite?",
         "SQLite supports a maximum database file size of 281 terabytes (2^41 bytes). However, practical limits due to OS file size restrictions or storage media are typically encountered first. Individual row size is limited to 1 GB."),
        ("How does SQLite handle concurrent writes?",
         "SQLite uses file-level locking. In default journal mode, only one writer is allowed at a time (exclusive lock). In WAL (Write-Ahead Log) mode, one writer can proceed concurrently with multiple readers without blocking them. WAL mode is recommended for applications with a mix of reads and writes."),
        ("What is ROWID in SQLite?",
         "Every SQLite table (unless declared WITHOUT ROWID) automatically gets a 64-bit signed integer ROWID that uniquely identifies each row. If a table has an INTEGER PRIMARY KEY column, that column becomes an alias for ROWID. This is equivalent to AUTO_INCREMENT in MySQL."),
        ("When would you choose SQLite over MySQL for a hospital system?",
         "SQLite is appropriate for: (1) A mobile nursing app that captures patient vitals offline, (2) An archived read-only copy of a patient's discharge summary PDF database, (3) Unit tests where an in-memory :memory: database can replace the full MySQL setup. MySQL is preferred when multiple concurrent users access the same data, when network access is required, or when complex stored procedures and user management are needed.")
    ]

    return build_page(3,"Study of SQLite","Group A","Embedded Databases",
        "A deep-dive comparison of SQLite vs MySQL — architectures, type systems, concurrency models, and use-case selection.",
        aim, theory, proc, code, output, conclusion, viva(vivaqs))


# ─────────────────────────────────────
# PRACTICAL 04 — ER Diagrams
# ─────────────────────────────────────
def p04():
    aim = """<p class="text-on-surface font-body leading-relaxed text-lg mb-4">
The aim of this practical is to design Entity-Relationship (ER) diagrams for the Hospital Management System — a structured graphical representation of all entities, attributes, and the relationships between them. The student will apply ER modelling notation (Chen's notation and Crow's Foot notation) to model real-world hospital data requirements before translating the conceptual model into a logical relational schema.
</p>
<p class="text-on-surface-variant font-body leading-relaxed">
ER diagrams are the blueprint of any database system, serving as a communication tool between database designers, application developers, and business stakeholders. Understanding cardinality (one-to-one, one-to-many, many-to-many), participation constraints (total vs partial), and specialization/generalisation hierarchies is fundamental to database design and is tested extensively in examinations and interviews.
</p>"""

    theory = f"""<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{theory_card("What is an ER Diagram?","An Entity-Relationship (ER) diagram is a visual representation of the logical structure of a database, proposed by Peter Chen in 1976. It models the real world as Entities (objects with independent existence), Attributes (properties of entities), and Relationships (associations between entities).","lg:col-span-2","primary","primary")}
{theory_card("Entity Types","Strong Entity: has its own primary key (PATIENT, DOCTOR, DEPARTMENT). Weak Entity: cannot be uniquely identified without a parent entity — identified by a partial key + parent PK (e.g., APPOINTMENT may depend on PATIENT). Weak entities are shown with double rectangles in Chen notation.","","secondary","secondary")}
{theory_card("Attribute Types","Simple: atomic, indivisible (age, salary). Composite: divisible into sub-parts (full_name → first_name, last_name). Multi-valued: can hold multiple values (phone_numbers) — shown with double ellipses. Derived: computed from other attributes (age derived from birth_date). Key Attribute: uniquely identifies entity — underlined in ER diagrams.","lg:col-span-3","primary","primary")}
{theory_card("Cardinality Ratios","One-to-One (1:1): One doctor is head of one department. One-to-Many (1:N): One doctor has many appointments. Many-to-Many (M:N): Many patients can see many doctors — requires a junction/associative table (APPOINTMENT). Cardinality is one of the most important design decisions in ER modelling.","","secondary","secondary")}
{theory_card("Participation Constraints","Total Participation (double line): every entity must participate in the relationship (every APPOINTMENT must have a PATIENT). Partial Participation (single line): some entities may not participate (some DOCTORs may have no appointments yet). Also called mandatory vs optional participation.","","primary","primary")}
{theory_card("HMS ER Description","Entities: PATIENT, DOCTOR, DEPARTMENT, APPOINTMENT, BILL. Key Relationships: PATIENT makes APPOINTMENT (1:N) — one patient can have multiple appointments. DOCTOR handles APPOINTMENT (1:N). DEPARTMENT has DOCTOR (1:N). PATIENT generates BILL (1:N). DEPARTMENT is headed by DOCTOR (1:1 optional).","","secondary","secondary")}
{theory_card("Mapping ER to Relational Schema","Rules: (1) Each strong entity → table with PK. (2) Each multi-valued attribute → separate table. (3) 1:N relationship → FK in the N-side table. (4) M:N relationship → new junction table with FKs from both entities. (5) Weak entity → table with composite PK (partial key + parent PK).","lg:col-span-2","primary","primary")}
{theory_card("EER — Enhanced ER","EER extends ER with OOP concepts: Generalisation (PATIENT generalises to INPATIENT, OUTPATIENT — bottom-up), Specialisation (top-down), Aggregation (relationship treated as entity), and Category/union types. Disjoint vs Overlapping specialisation determines if a patient can be both in- and out-patient.","","secondary","secondary")}
</div>"""

    proc = ol_steps([
        "Identify all entities in the Hospital Management System from the requirements: PATIENT, DOCTOR, DEPARTMENT, APPOINTMENT, BILL.",
        "For each entity, list all attributes and classify them (simple, composite, multi-valued, derived, key).",
        "Identify all relationships between entities and assign meaningful verb phrases: PATIENT <em>makes</em> APPOINTMENT, DOCTOR <em>handles</em> APPOINTMENT.",
        "Determine cardinality for each relationship: PATIENT → APPOINTMENT (1:N), DOCTOR → APPOINTMENT (1:N), DEPARTMENT → DOCTOR (1:N), PATIENT → BILL (1:N), DEPARTMENT → DOCTOR as head (1:1).",
        "Determine participation constraints: total participation — every APPOINTMENT must have a PATIENT and DOCTOR; partial — a DOCTOR may have zero appointments initially.",
        "Draw the ER diagram using Chen's notation: rectangles for entities, ellipses for attributes, diamonds for relationships, lines for connections with cardinality labels.",
        "Alternatively, use Crow's Foot notation (used in MySQL Workbench): lines with fork/crow's foot symbols for '1' and 'many' ends.",
        "Identify the APPOINTMENT entity as potentially an associative (bridge) entity because it resolves the M:N relationship between PATIENT and DOCTOR.",
        "Map the ER diagram to a relational schema: identify each table, primary key, foreign keys, and constraints.",
        "Validate the schema: ensure every relationship is represented by either a FK or a junction table.",
        "Open MySQL Workbench → Model → New Model → Add Diagram → Build the visual ER diagram using the drag-and-drop interface.",
        "Export the diagram as PNG and SQL forward-engineering script — validate against the hospital_db schema."
    ])

    code = code_block(f"""{cmt("-- ================================================================")}
{cmt("-- Practical 04: ER Diagram → Relational Schema Mapping")}
{cmt("-- Hospital Management System — Complete Schema")}
{cmt("-- ================================================================")}

{cmt("-- ER Diagram Description (Text Representation):")}
{cmt("--")}
{cmt("-- [DEPARTMENT]----<has>----[DOCTOR]----<handles>----[APPOINTMENT]")}
{cmt("--      |                      |                          |")}
{cmt("--   floor_no              salary                    appt_date")}
{cmt("--   dept_name          specialization               status")}
{cmt("--      |                      |                          |")}
{cmt("--      +------<heads>---------+              [PATIENT]--<makes>-+")}
{cmt("--                                              |")}
{cmt("--                                         [BILL]<--generates")}
{cmt("--")}
{cmt("-- Cardinalities:")}
{cmt("-- DEPARTMENT : DOCTOR     = 1 : N (one dept has many doctors)")}
{cmt("-- DOCTOR : APPOINTMENT    = 1 : N (one doctor has many appts)")}
{cmt("-- PATIENT : APPOINTMENT   = 1 : N (one patient has many appts)")}
{cmt("-- PATIENT : BILL          = 1 : N (one patient has many bills)")}
{cmt("-- DEPARTMENT : DOCTOR(head)= 1 : 1 (optional, partial)")}

{kw("DROP DATABASE IF EXISTS")} {tbl("hospital_db")};
{kw("CREATE DATABASE")} {tbl("hospital_db")} {kw("CHARACTER SET")} {str_("utf8mb4")} {kw("COLLATE")} {str_("utf8mb4_unicode_ci")};
{kw("USE")} {tbl("hospital_db")};

{cmt("-- Strong Entity 1: DEPARTMENT (created first — no FK dependencies)")}
{kw("CREATE TABLE")} {tbl("DEPARTMENT")} (
    {tbl("dept_id")}        {kw("INT")}         {kw("PRIMARY KEY")} {kw("COMMENT")} {str_("'Department unique identifier'")},
    {tbl("dept_name")}      {kw("VARCHAR")}({num("50")})  {kw("NOT NULL")} {kw("UNIQUE")} {kw("COMMENT")} {str_("'Department name — must be unique'")},
    {tbl("floor_no")}       {kw("INT")}         {kw("NOT NULL")} {kw("CHECK")}({tbl("floor_no")} {kw("BETWEEN")} {num("1")} {kw("AND")} {num("20")}),
    {tbl("head_doctor_id")} {kw("INT")}         {kw("DEFAULT")} {kw("NULL")} {kw("COMMENT")} {str_("'1:1 partial relationship to DOCTOR'")}
) {kw("ENGINE")}={str_("InnoDB")} {kw("COMMENT")} {str_("'Represents hospital departments'")};

{cmt("-- Strong Entity 2: DOCTOR (FK to DEPARTMENT)")}
{kw("CREATE TABLE")} {tbl("DOCTOR")} (
    {tbl("doctor_id")}        {kw("INT")}          {kw("PRIMARY KEY")},
    {tbl("name")}             {kw("VARCHAR")}({num("80")})  {kw("NOT NULL")},
    {tbl("specialization")}   {kw("VARCHAR")}({num("50")})  {kw("NOT NULL")},
    {tbl("experience_years")} {kw("INT")}          {kw("NOT NULL")} {kw("CHECK")}({tbl("experience_years")} &gt;= {num("0")}),
    {tbl("salary")}           {kw("DECIMAL")}({num("10")},{num("2")}) {kw("NOT NULL")} {kw("CHECK")}({tbl("salary")} &gt; {num("0")}),
    {tbl("dept_id")}          {kw("INT")},
    {kw("FOREIGN KEY")} ({tbl("dept_id")}) {kw("REFERENCES")} {tbl("DEPARTMENT")}({tbl("dept_id")}) {kw("ON DELETE SET NULL")}
    {cmt("-- 1:N: One DEPARTMENT has many DOCTORs")}
) {kw("ENGINE")}={str_("InnoDB")};

{cmt("-- Strong Entity 3: PATIENT")}
{kw("CREATE TABLE")} {tbl("PATIENT")} (
    {tbl("patient_id")}     {kw("VARCHAR")}({num("10")}) {kw("PRIMARY KEY")},
    {tbl("name")}           {kw("VARCHAR")}({num("80")}) {kw("NOT NULL")},
    {tbl("age")}            {kw("INT")}         {kw("NOT NULL")} {kw("CHECK")}({tbl("age")} {kw("BETWEEN")} {num("0")} {kw("AND")} {num("150")}),
    {tbl("gender")}         {kw("ENUM")}({str_("'Male'")},{str_("'Female'")},{str_("'Other'")}) {kw("NOT NULL")},
    {tbl("disease")}        {kw("VARCHAR")}({num("100")}) {kw("NOT NULL")},
    {tbl("ward_no")}        {kw("INT")},
    {tbl("admission_date")} {kw("DATE")}        {kw("DEFAULT")} ({kw("CURRENT_DATE")})
) {kw("ENGINE")}={str_("InnoDB")};

{cmt("-- Associative (Junction) Entity: APPOINTMENT (resolves M:N between PATIENT & DOCTOR)")}
{kw("CREATE TABLE")} {tbl("APPOINTMENT")} (
    {tbl("appt_id")}    {kw("INT")}          {kw("PRIMARY KEY")} {kw("AUTO_INCREMENT")},
    {tbl("patient_id")} {kw("VARCHAR")}({num("10")}) {kw("NOT NULL")},
    {tbl("doctor_id")}  {kw("INT")}          {kw("NOT NULL")},
    {tbl("appt_date")}  {kw("DATE")}         {kw("NOT NULL")},
    {tbl("status")}     {kw("ENUM")}({str_("'Scheduled'")},{str_("'Completed'")},{str_("'Cancelled'")}) {kw("DEFAULT")} {str_("'Scheduled'")},
    {kw("FOREIGN KEY")} ({tbl("patient_id")}) {kw("REFERENCES")} {tbl("PATIENT")}({tbl("patient_id")}) {kw("ON DELETE CASCADE")},
    {kw("FOREIGN KEY")} ({tbl("doctor_id")})  {kw("REFERENCES")} {tbl("DOCTOR")}({tbl("doctor_id")})  {kw("ON DELETE CASCADE")}
) {kw("ENGINE")}={str_("InnoDB")};

{cmt("-- Dependent Entity: BILL (total participation — every bill must have a patient)")}
{kw("CREATE TABLE")} {tbl("BILL")} (
    {tbl("bill_id")}      {kw("INT")}          {kw("PRIMARY KEY")} {kw("AUTO_INCREMENT")},
    {tbl("patient_id")}   {kw("VARCHAR")}({num("10")}) {kw("NOT NULL")},
    {tbl("total_amount")} {kw("DECIMAL")}({num("10")},{num("2")}) {kw("NOT NULL")} {kw("CHECK")}({tbl("total_amount")} &gt;= {num("0")}),
    {tbl("paid_status")}  {kw("ENUM")}({str_("'Paid'")},{str_("'Unpaid'")},{str_("'Partial'")}) {kw("DEFAULT")} {str_("'Unpaid'")},
    {tbl("bill_date")}    {kw("DATE")}         {kw("NOT NULL")} {kw("DEFAULT")} ({kw("CURRENT_DATE")}),
    {kw("FOREIGN KEY")} ({tbl("patient_id")}) {kw("REFERENCES")} {tbl("PATIENT")}({tbl("patient_id")}) {kw("ON DELETE CASCADE")}
) {kw("ENGINE")}={str_("InnoDB")};

{cmt("-- Now add the self-referencing head_doctor FK to DEPARTMENT")}
{kw("ALTER TABLE")} {tbl("DEPARTMENT")}
    {kw("ADD CONSTRAINT")} {tbl("fk_head_doctor")}
    {kw("FOREIGN KEY")} ({tbl("head_doctor_id")}) {kw("REFERENCES")} {tbl("DOCTOR")}({tbl("doctor_id")}) {kw("ON DELETE SET NULL")};

{cmt("-- Verify schema structure")}
{kw("SHOW")} {kw("TABLES")};
{kw("DESCRIBE")} {tbl("APPOINTMENT")};
""")

    output = out_table(
        ["Tables_in_hospital_db"],
        [["APPOINTMENT"],["BILL"],["DEPARTMENT"],["DOCTOR"],["PATIENT"]],
        "SHOW TABLES"
    ) + "<br/>" + out_table(
        ["Field","Type","Null","Key","Default","Extra"],
        [["appt_id","int","NO","PRI","NULL","auto_increment"],
         ["patient_id","varchar(10)","NO","MUL","NULL",""],
         ["doctor_id","int","NO","MUL","NULL",""],
         ["appt_date","date","NO","","NULL",""],
         ["status","enum(...)","YES","","Scheduled",""]],
        "DESCRIBE APPOINTMENT"
    )

    conclusion = """<p class="text-on-surface font-body leading-relaxed mb-4">
This practical successfully demonstrated the process of ER modelling for the Hospital Management System. We identified five strong entities (PATIENT, DOCTOR, DEPARTMENT, APPOINTMENT, BILL), correctly classified all relationships with their cardinalities and participation constraints, and translated the conceptual ER model into a logical relational schema with appropriate primary keys, foreign keys, and integrity constraints.
</p>
<p class="text-on-surface-variant font-body leading-relaxed">
The APPOINTMENT table serves as the bridge entity resolving the implicit many-to-many relationship between PATIENT and DOCTOR. The circular dependency between DEPARTMENT and DOCTOR (via head_doctor_id) was resolved by creating DEPARTMENT first, DOCTOR second, and then adding the FK with ALTER TABLE. This ordering strategy is a critical skill in schema deployment scripts and is a best practice for avoiding circular FK creation errors.
</p>"""

    vivaqs = [
        ("What is the difference between a strong entity and a weak entity?",
         "A strong entity has its own unique primary key and exists independently (e.g., PATIENT with patient_id). A weak entity cannot be uniquely identified by its own attributes alone — it depends on a strong (owner) entity and uses a composite key of its partial key + owner's PK (e.g., an APPOINTMENT_DETAIL might depend on APPOINTMENT)."),
        ("How do you map a Many-to-Many relationship in a relational schema?",
         "A M:N relationship cannot be directly represented with just foreign keys. It must be resolved by creating a junction/associative/bridge table that contains foreign keys referencing both participating entities. APPOINTMENT is our bridge table with FKs to both PATIENT and DOCTOR."),
        ("What is the difference between total and partial participation?",
         "Total (mandatory) participation — double line in ER — means every entity instance must participate in at least one relationship instance (every APPOINTMENT must have a PATIENT). Partial (optional) participation — single line — means some instances may not participate (a DOCTOR may initially have no APPOINTMENT)."),
        ("What is a derived attribute? Give a hospital example.",
         "A derived attribute is computed from other stored attributes and typically not stored physically. In our HMS, a patient's 'age' could be a derived attribute computed from their 'date_of_birth' (since storing only DOB is more accurate). Similarly, 'years_since_admission' can be derived from admission_date."),
        ("What is the difference between Chen's notation and Crow's Foot notation?",
         "Chen notation: uses rectangles (entities), ellipses (attributes), diamonds (relationships), and 1/N/M labels on lines — good for academic/conceptual modelling. Crow's Foot: uses line-end symbols (|, O, <) to show cardinality and participation — more compact, widely used in tools like MySQL Workbench, ERwin, Lucidchart.")
    ]

    return build_page(4,"ER Diagrams","Group A","Data Modelling",
        "Designing and mapping an Entity-Relationship diagram for the Hospital Management System to a relational schema.",
        aim, theory, proc, code, output, conclusion, viva(vivaqs))


# ─────────────────────────────────────
# PRACTICAL 05 — DDL Commands & Normalization
# ─────────────────────────────────────
def p05():
    aim = """<p class="text-on-surface font-body leading-relaxed text-lg mb-4">
The aim of this practical is to implement Data Definition Language (DDL) commands in MySQL to create, modify, and manage the Hospital Management System schema, and simultaneously apply database normalization techniques (1NF, 2NF, 3NF, BCNF) to eliminate data redundancy and ensure data integrity. The student will learn how improper schema design leads to update, insertion, and deletion anomalies, and how normalization resolves these systematically.
</p>
<p class="text-on-surface-variant font-body leading-relaxed">
DDL is the backbone of database schema management — every production database begins with carefully written CREATE TABLE statements with appropriate constraints. Normalization is the theoretical framework that guides these design decisions, and understanding it is essential for designing efficient hospital databases where patient records, billing, and medical data must be stored without duplication or inconsistency.
</p>"""

    theory = f"""<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{theory_card("DDL Commands Overview","DDL (Data Definition Language) commands define and manage the structure of database objects. Key commands: CREATE (creates table/db/index/view), ALTER (modifies existing structure — add/drop/modify columns), DROP (permanently deletes object), TRUNCATE (removes all rows but keeps structure), RENAME (renames object). DDL is auto-committed in MySQL.","lg:col-span-2","primary","primary")}
{theory_card("Data Types in MySQL","Numeric: INT, BIGINT, DECIMAL(p,s), FLOAT, DOUBLE. String: VARCHAR(n), CHAR(n), TEXT, ENUM, SET. Date/Time: DATE, TIME, DATETIME, TIMESTAMP, YEAR. Binary: BLOB, BINARY. JSON: native JSON type (MySQL 5.7+). Spatial: POINT, LINESTRING, POLYGON. Choosing the correct data type impacts storage and performance significantly.","","secondary","secondary")}
{theory_card("Normalization — What & Why?","Normalization is the process of organising a relational database to reduce data redundancy and improve data integrity. Proposed by E.F. Codd (1970). An un-normalised table can suffer from: Update Anomaly (changing a doctor's salary requires updating multiple rows), Insert Anomaly (cannot add a doctor without a patient), Delete Anomaly (deleting last patient loses doctor information).","lg:col-span-3","primary","primary")}
{theory_card("1NF — First Normal Form","Rules: (1) Each column must contain atomic (indivisible) values — no repeating groups or arrays. (2) Each row must be uniquely identifiable by a primary key. Violation example: storing multiple phone numbers in one column (phone: '9876543210, 9123456789'). Fix: create a separate PATIENT_PHONE table with patient_id FK.","","secondary","secondary")}
{theory_card("2NF — Second Normal Form","Rules: Must be in 1NF + No partial dependencies (non-key attributes must depend on the ENTIRE composite primary key). Relevant for tables with composite PKs. Example: if APPOINTMENT had (patient_id, doctor_id) as composite PK and stored doctor_name, that violates 2NF because doctor_name depends only on doctor_id (partial dependency). Fix: separate DOCTOR table.","","primary","primary")}
{theory_card("3NF — Third Normal Form","Rules: Must be in 2NF + No transitive dependencies (non-key attributes must not depend on other non-key attributes). Example: if DOCTOR table stored dept_name and dept_floor_no, then dept_floor_no → dept_name → doctor_id (transitive). Fix: separate DEPARTMENT table, store only dept_id FK in DOCTOR.","","secondary","secondary")}
{theory_card("BCNF — Boyce-Codd Normal Form","BCNF is a stricter version of 3NF: for every non-trivial functional dependency X → Y, X must be a superkey. BCNF eliminates anomalies that 3NF may not catch when there are overlapping candidate keys. Most tables in the HMS schema are already in BCNF after applying 3NF rules.","","primary","primary")}
{theory_card("4NF & 5NF (Higher Normal Forms)","4NF: No multi-valued dependencies (a doctor with multiple specializations AND multiple languages should have separate tables rather than all combinations). 5NF (PJNF): No join dependencies — relevant to very complex many-to-many relationships. In practice, most production schemas target 3NF/BCNF.","lg:col-span-2","secondary","secondary")}
</div>"""

    proc = ol_steps([
        "Use the hospital_db database: <code class='text-cyan-400'>USE hospital_db;</code>",
        "Create all 5 tables using CREATE TABLE with appropriate data types, PRIMARY KEY, NOT NULL, and CHECK constraints.",
        "Use DESCRIBE to inspect the created table structure: <code class='text-cyan-400'>DESCRIBE PATIENT;</code>",
        "Demonstrate normalization by starting with an un-normalised PATIENT_DOCTOR_UNNORMALISED table.",
        "Identify all anomalies in the un-normalised table: update anomaly (changing doctor salary affects many rows), insert anomaly, delete anomaly.",
        "Apply 1NF: ensure atomic values — move multi-valued attributes to separate tables.",
        "Apply 2NF: remove partial dependencies — each non-key column must depend on the full PK.",
        "Apply 3NF: remove transitive dependencies — dept_name and floor_no moved from DOCTOR to DEPARTMENT.",
        "Verify the normalised schema results in the final 5-table design with FK constraints.",
        "Use SHOW CREATE TABLE to view the complete DDL including all FK definitions: <code class='text-cyan-400'>SHOW CREATE TABLE APPOINTMENT\\G</code>",
        "Create indexes on frequently queried columns to optimise performance.",
        "Document all functional dependencies identified during normalization in your journal."
    ])

    code = code_block(f"""{cmt("-- ================================================================")}
{cmt("-- Practical 05: DDL Commands & Normalization")}
{cmt("-- Hospital Management System")}
{cmt("-- ================================================================")}

{kw("USE")} {tbl("hospital_db")};

{cmt("-- ── Step 1: Demonstrate Un-Normalised Table (Violates 1NF & 2NF) ──")}
{cmt("-- Un-Normalised: patient info + doctor info + dept info in one table")}
{cmt("-- Anomalies present:")}
{cmt("--   Update: Changing Dr. Sharma's salary requires updating ALL rows")}
{cmt("--   Insert: Cannot add a doctor without a patient")}
{cmt("--   Delete: Removing P001 deletes Dr. Sharma's information")}
{kw("CREATE TABLE")} {tbl("UNNORMALISED")} (
    {tbl("patient_id")}    {kw("VARCHAR")}({num("10")}),
    {tbl("patient_name")}  {kw("VARCHAR")}({num("80")}),
    {tbl("patient_age")}   {kw("INT")},
    {tbl("diseases")}      {kw("VARCHAR")}({num("200")}),  {cmt("-- VIOLATION: Multi-valued — 'Diabetes, Hypertension'")}
    {tbl("doctor_id")}     {kw("INT")},
    {tbl("doctor_name")}   {kw("VARCHAR")}({num("80")}),
    {tbl("salary")}        {kw("DECIMAL")}({num("10")},{num("2")}),
    {tbl("dept_name")}     {kw("VARCHAR")}({num("50")}),   {cmt("-- Transitive: doctor_id → dept_id → dept_name")}
    {tbl("dept_floor")}    {kw("INT")}
);

{cmt("-- ── Step 2: Apply 1NF ──")}
{cmt("-- Remove multi-valued 'diseases' — each patient has one disease per row")}
{cmt("-- Ensure atomic values in all columns")}
{cmt("-- (Our final PATIENT table already satisfies 1NF)")}

{cmt("-- ── Step 3: Apply 2NF ──")}
{cmt("-- Separate DOCTOR information (no partial dependencies in FK tables)")}

{cmt("-- ── Step 4: Apply 3NF — Create DDL for HMS ──")}
{cmt("-- 3NF achieved: dept_name moved to DEPARTMENT table")}
{cmt("-- DOCTOR stores only dept_id FK (not dept_name — removing transitive dep)")}

{kw("DROP TABLE IF EXISTS")} {tbl("UNNORMALISED")};

{cmt("-- Final Normalised Schema — Complete DDL")}
{kw("CREATE TABLE")} {tbl("DEPARTMENT")} (
    {tbl("dept_id")}        {kw("INT")}         {kw("PRIMARY KEY")},
    {tbl("dept_name")}      {kw("VARCHAR")}({num("50")})  {kw("NOT NULL")} {kw("UNIQUE")},
    {tbl("floor_no")}       {kw("INT")}         {kw("NOT NULL")} {kw("CHECK")}({tbl("floor_no")} {kw("BETWEEN")} {num("1")} {kw("AND")} {num("20")}),
    {tbl("head_doctor_id")} {kw("INT")}         {kw("DEFAULT")} {kw("NULL")}
) {kw("ENGINE")}={str_("InnoDB")};

{kw("CREATE TABLE")} {tbl("DOCTOR")} (
    {tbl("doctor_id")}        {kw("INT")}         {kw("PRIMARY KEY")},
    {tbl("name")}             {kw("VARCHAR")}({num("80")}) {kw("NOT NULL")},
    {tbl("specialization")}   {kw("VARCHAR")}({num("50")}) {kw("NOT NULL")},
    {tbl("experience_years")} {kw("INT")}         {kw("DEFAULT")} {num("0")} {kw("CHECK")}({tbl("experience_years")} &gt;= {num("0")}),
    {tbl("salary")}           {kw("DECIMAL")}({num("10")},{num("2")}) {kw("CHECK")}({tbl("salary")} &gt; {num("0")}),
    {tbl("dept_id")}          {kw("INT")},
    {kw("FOREIGN KEY")} ({tbl("dept_id")}) {kw("REFERENCES")} {tbl("DEPARTMENT")}({tbl("dept_id")}) {kw("ON DELETE SET NULL")}
) {kw("ENGINE")}={str_("InnoDB")};

{kw("CREATE TABLE")} {tbl("PATIENT")} (
    {tbl("patient_id")}     {kw("VARCHAR")}({num("10")}) {kw("PRIMARY KEY")},
    {tbl("name")}           {kw("VARCHAR")}({num("80")}) {kw("NOT NULL")},
    {tbl("age")}            {kw("INT")}         {kw("NOT NULL")} {kw("CHECK")}({tbl("age")} {kw("BETWEEN")} {num("0")} {kw("AND")} {num("150")}),
    {tbl("gender")}         {kw("ENUM")}({str_("'Male'")},{str_("'Female'")},{str_("'Other'")}) {kw("NOT NULL")},
    {tbl("disease")}        {kw("VARCHAR")}({num("100")}) {kw("NOT NULL")},
    {tbl("ward_no")}        {kw("INT")}         {kw("CHECK")}({tbl("ward_no")} &gt; {num("0")}),
    {tbl("admission_date")} {kw("DATE")}        {kw("NOT NULL")} {kw("DEFAULT")} ({kw("CURRENT_DATE")})
) {kw("ENGINE")}={str_("InnoDB")};

{kw("CREATE TABLE")} {tbl("APPOINTMENT")} (
    {tbl("appt_id")}    {kw("INT")}          {kw("AUTO_INCREMENT")} {kw("PRIMARY KEY")},
    {tbl("patient_id")} {kw("VARCHAR")}({num("10")}) {kw("NOT NULL")},
    {tbl("doctor_id")}  {kw("INT")}          {kw("NOT NULL")},
    {tbl("appt_date")}  {kw("DATE")}         {kw("NOT NULL")},
    {tbl("status")}     {kw("ENUM")}({str_("'Scheduled'")},{str_("'Completed'")},{str_("'Cancelled'")}) {kw("DEFAULT")} {str_("'Scheduled'")},
    {kw("FOREIGN KEY")} ({tbl("patient_id")}) {kw("REFERENCES")} {tbl("PATIENT")}({tbl("patient_id")}) {kw("ON DELETE CASCADE")},
    {kw("FOREIGN KEY")} ({tbl("doctor_id")})  {kw("REFERENCES")} {tbl("DOCTOR")}({tbl("doctor_id")})  {kw("ON DELETE CASCADE")}
) {kw("ENGINE")}={str_("InnoDB")};

{kw("CREATE TABLE")} {tbl("BILL")} (
    {tbl("bill_id")}      {kw("INT")}          {kw("AUTO_INCREMENT")} {kw("PRIMARY KEY")},
    {tbl("patient_id")}   {kw("VARCHAR")}({num("10")}) {kw("NOT NULL")},
    {tbl("total_amount")} {kw("DECIMAL")}({num("10")},{num("2")}) {kw("NOT NULL")} {kw("CHECK")}({tbl("total_amount")} &gt;= {num("0")}),
    {tbl("paid_status")}  {kw("ENUM")}({str_("'Paid'")},{str_("'Unpaid'")},{str_("'Partial'")}) {kw("DEFAULT")} {str_("'Unpaid'")},
    {tbl("bill_date")}    {kw("DATE")}         {kw("NOT NULL")} {kw("DEFAULT")} ({kw("CURRENT_DATE")}),
    {kw("FOREIGN KEY")} ({tbl("patient_id")}) {kw("REFERENCES")} {tbl("PATIENT")}({tbl("patient_id")}) {kw("ON DELETE CASCADE")}
) {kw("ENGINE")}={str_("InnoDB")};

{cmt("-- Create indexes on frequently searched columns")}
{kw("CREATE INDEX")} {tbl("idx_patient_disease")}  {kw("ON")} {tbl("PATIENT")}({tbl("disease")});
{kw("CREATE INDEX")} {tbl("idx_appt_date")}         {kw("ON")} {tbl("APPOINTMENT")}({tbl("appt_date")});
{kw("CREATE INDEX")} {tbl("idx_bill_paid_status")}   {kw("ON")} {tbl("BILL")}({tbl("paid_status")});

{cmt("-- Verify all tables and structure")}
{kw("SHOW")} {kw("TABLES")};
{kw("DESCRIBE")} {tbl("PATIENT")};
""")

    output = out_table(
        ["Tables_in_hospital_db"],
        [["APPOINTMENT"],["BILL"],["DEPARTMENT"],["DOCTOR"],["PATIENT"]],
        "SHOW TABLES"
    ) + "<br/>" + out_table(
        ["Field","Type","Null","Key","Default","Extra"],
        [["patient_id","varchar(10)","NO","PRI","NULL",""],
         ["name","varchar(80)","NO","","NULL",""],
         ["age","int","NO","","NULL",""],
         ["gender","enum('Male','Female','Other')","NO","","NULL",""],
         ["disease","varchar(100)","NO","MUL","NULL",""],
         ["ward_no","int","YES","","NULL",""],
         ["admission_date","date","NO","","current_date()",""]],
        "DESCRIBE PATIENT"
    )

    conclusion = """<p class="text-on-surface font-body leading-relaxed mb-4">
This practical established the complete normalised DDL schema for the Hospital Management System. By progressing from an un-normalised monolithic table through 1NF (atomic values), 2NF (no partial dependencies), and 3NF (no transitive dependencies), we arrived at the final 5-table design in BCNF. Each normalization step was justified by identifying specific data anomalies and eliminating the functional dependencies that caused them.
</p>
<p class="text-on-surface-variant font-body leading-relaxed">
Key takeaway: Normalization improves data integrity and reduces redundancy but may increase the number of JOIN operations required for queries. In practice, database designers sometimes deliberately denormaize (controlled redundancy) for read-heavy systems like data warehouses or reporting databases, while keeping OLTP databases like our HMS fully normalised to ensure consistency. Performance indexes were created on disease, appt_date, and paid_status columns for optimal query performance.
</p>"""

    vivaqs = [
        ("What is a functional dependency? Give an example.",
         "A functional dependency X → Y means the value of X uniquely determines the value of Y. Example: patient_id → name (knowing patient_id tells us exactly which patient name). doctor_id → salary (knowing doctor_id determines the salary). Functional dependencies are the foundation of normalization theory."),
        ("What is a transitive dependency and how does 3NF eliminate it?",
         "A transitive dependency occurs when A → B → C (A determines B which determines C, making A indirectly determine C). In our schema, if DOCTOR stored dept_name: doctor_id → dept_id → dept_name. 3NF removes this by moving dept_name to the DEPARTMENT table, making DOCTOR store only dept_id FK."),
        ("What is the difference between DROP TABLE and TRUNCATE TABLE?",
         "DROP TABLE permanently deletes the table structure along with all data and releases storage (DDL, auto-committed). TRUNCATE TABLE removes all rows but keeps the table structure intact, resets AUTO_INCREMENT, and is also DDL (fast, no per-row logging). DELETE FROM removes rows one by one with individual transaction log entries (DML, can be rolled back)."),
        ("Why is BCNF considered stricter than 3NF?",
         "3NF allows functional dependencies where the determinant is not a superkey, as long as the dependent attribute is part of some candidate key. BCNF eliminates even these: for every non-trivial FD X → Y, X must be a superkey. This handles anomalies in tables with overlapping candidate keys that 3NF cannot."),
        ("What does the CHECK constraint do? Does MySQL fully enforce it?",
         "CHECK constraints in MySQL 8.0.16+ are fully enforced and will reject rows where the condition evaluates to FALSE. Example: CHECK(age BETWEEN 0 AND 150) prevents inserting age=200. Before 8.0.16, MySQL parsed but ignored CHECK constraints — a dangerous behaviour no longer present in current versions.")
    ]

    return build_page(5,"DDL Commands & Normalization","Group B","Schema Design",
        "Implementing MySQL DDL commands and applying normalization theory (1NF through BCNF) on the Hospital Management System.",
        aim, theory, proc, code, output, conclusion, viva(vivaqs))


print("✔ Practical content functions defined.")
print("Now generating HTML files...")

practicals_data = [
    (1, p01), (2, p02), (3, p03), (4, p04), (5, p05),
]

for n, fn_gen in practicals_data:
    html = fn_gen()
    dir_path = os.path.join(BASE_DIR, get_dir(n))
    os.makedirs(dir_path, exist_ok=True)
    out_path = os.path.join(dir_path, "code.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ Practical {n:02d} → {out_path}")

print("\nPhase 1 (Practicals 1-5) complete!")
