#!/usr/bin/env python3
"""Shared HTML templates and functions for DBMS Lab Journal."""
import os

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

def sidebar(active_num):
    icons = ["terminal","database","schema","table_chart","query_stats","storage","security",
             "code_blocks","settings_ethernet","lan","cloud_done","account_tree","reorder","history"]
    items = ""
    for i in range(1, 15):
        icon = icons[i-1]
        label = f"Practical {i:02d}"
        if i == active_num:
            items += f'''<a class="flex items-center gap-3 p-3 bg-cyan-500/10 text-cyan-400 font-bold border-r-4 border-cyan-400 font-label text-sm uppercase tracking-widest" href="#">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">{icon}</span>{label}</a>'''
        else:
            href = f"../{get_dir(i)}/code.html"
            items += f'''<a class="flex items-center gap-3 p-3 text-slate-500 hover:text-slate-300 font-label text-sm uppercase tracking-widest transition-colors" href="{href}">
<span class="material-symbols-outlined">{icon}</span>{label}</a>'''
    return f'''<aside class="hidden md:block sticky left-0 h-[calc(100vh-80px)] w-72 bg-[#181c22] overflow-y-auto border-none top-[64px] scrollbar-hide">
<div class="flex flex-col gap-1 p-6">
<div class="mb-6">
<h3 class="font-headline font-bold text-primary tracking-widest uppercase text-xs">Lab Practicals</h3>
<p class="text-on-surface-variant text-[10px] uppercase tracking-[0.2em] mt-1 font-label">DBMS Coursework</p>
</div>
{items}
</div></aside>'''

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

def write_practical(n, html_content, base_dir):
    dir_path = os.path.join(base_dir, get_dir(n))
    os.makedirs(dir_path, exist_ok=True)
    out_path = os.path.join(dir_path, "code.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated Practical {n:02d} at {out_path}")
