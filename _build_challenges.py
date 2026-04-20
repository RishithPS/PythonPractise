"""Generate CodingChallenges.ipynb (practice) and CodingChallengesSolutions.ipynb (solutions).

Single source of truth: the SECTIONS list below. Each Challenge dict carries the
problem text, signature, tests and reference solution. Two notebooks are emitted
from the same data so they can never drift.

Resume safety: every section block ends with `# BUILD-MARKER: <slug>-complete`.
A resuming session can grep for the last marker to know where to continue.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import nbformat as nbf

REPO = Path(__file__).resolve().parent
PRACTICE_NB = REPO / "CodingChallenges.ipynb"
SOLUTIONS_NB = REPO / "CodingChallengesSolutions.ipynb"

UDEMY_URL = "https://www.udemy.com/course/the-complete-python-bootcamp-13hours-go-from-zero-to-hero/"
PDF_NAME = "Python_Handbook_Data_With_Baraa.pdf"
STUDENT_NAME = "Rishith"


# ---------------------------------------------------------------------------
# Spec schema (plain dicts, no classes — keeps spec data scannable)
#
# SECTION:   {num, title, anchor, intro, subtopics: [SUBTOPIC]}
# SUBTOPIC:  {num, title, anchor, challenges: [CHALLENGE]}
# CHALLENGE: {
#     num, title, difficulty,           # difficulty: "Easy" | "Medium" | "Hard"
#     problem, input_fmt, output_fmt,
#     sample_in, sample_out,
#     constraints,                       # str or list[str]
#     uses,                              # optional list[str] of reused topics
#     signature,                         # str — the def line for the stub/solution
#     tests,                             # list[str] — assert lines
#     solution,                          # str — full function body (one or more defs)
# }
# ---------------------------------------------------------------------------


def section(num, title, anchor, intro, subtopics):
    return {
        "num": num,
        "title": title,
        "anchor": anchor,
        "intro": intro,
        "subtopics": subtopics,
    }


def subtopic(num, title, anchor, challenges):
    return {
        "num": num,
        "title": title,
        "anchor": anchor,
        "challenges": challenges,
    }


def challenge(num, title, difficulty, problem, input_fmt, output_fmt,
              sample_in, sample_out, constraints, signature, tests, solution,
              uses=None):
    return {
        "num": num,
        "title": title,
        "difficulty": difficulty,
        "problem": problem,
        "input_fmt": input_fmt,
        "output_fmt": output_fmt,
        "sample_in": sample_in,
        "sample_out": sample_out,
        "constraints": constraints,
        "uses": uses,
        "signature": signature,
        "tests": tests,
        "solution": solution,
    }


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------

def _ch_anchor(section_num, subtopic_num, challenge_num):
    return f"ch-{section_num}-{subtopic_num}-{challenge_num}"


def _format_constraints(constraints):
    if isinstance(constraints, str):
        return f"- {constraints}"
    return "\n".join(f"- {c}" for c in constraints)


def _problem_md(sec, sub, ch, *, mode):
    """Render the problem statement markdown cell (no cross-link — that lives
    in a separate cell after the test cell so it isn't tempting to peek)."""
    anchor = _ch_anchor(sec["num"], sub["num"], ch["num"])
    challenge_id = f"{sec['num']}.{sub['num']}.{ch['num']}"

    uses_line = ""
    if ch.get("uses"):
        uses_line = f"\n**Uses** — {', '.join(ch['uses'])}.\n"

    md = f"""<a id='{anchor}'></a>
#### Challenge {challenge_id} — {ch['title']}  *({ch['difficulty']})*

**Problem** — {ch['problem']}

**Input Format** — {ch['input_fmt']}

**Output Format** — {ch['output_fmt']}

**Sample Input** — `{ch['sample_in']}`

**Sample Output** — `{ch['sample_out']}`

**Constraints**
{_format_constraints(ch['constraints'])}
{uses_line}"""
    return md


def _cross_link_md(sec, sub, ch, *, mode):
    """Standalone cell rendered AFTER the test cell.

    In practice mode: 'View solution' — placed after tests so the student isn't
    tempted to peek before attempting.
    In solutions mode: 'Back to challenge' — symmetrical back-link.
    """
    anchor = _ch_anchor(sec["num"], sub["num"], ch["num"])
    if mode == "practice":
        return f"[🔑 View solution]({SOLUTIONS_NB.name}#{anchor})"
    return f"[← Back to challenge]({PRACTICE_NB.name}#{anchor})"


def _code_cell_source(ch, *, mode):
    """Return the source for the code cell — stub or full solution."""
    if ch.get("is_project"):
        return ch["starter_code"] if mode == "practice" else ch["solution"]
    if mode == "practice":
        return f"{ch['signature']}\n    # TODO: implement\n    pass"
    return f"{ch['signature']}\n{textwrap.indent(ch['solution'].strip('\n'), '    ')}"


def _test_cell_source(ch):
    """Return the test cell source. try/except wrapper keeps execution clean."""
    test_lines = "\n    ".join(ch["tests"])
    return (
        "try:\n"
        f"    {test_lines}\n"
        '    print("All tests passed!")\n'
        "except AssertionError:\n"
        '    print("Test failed — check your logic.")\n'
        "except (TypeError, NameError):\n"
        '    print("Stub not implemented yet.")\n'
    )


def _toc_md(sections):
    lines = ["## Table of Contents", ""]
    for sec in sections:
        lines.append(f"{sec['num']}. [{sec['title']}](#{sec['anchor']})")
        for sub in sec["subtopics"]:
            lines.append(
                f"    - [{sec['num']}.{sub['num']} {sub['title']}](#{sub['anchor']})"
            )
    lines.append(f"{len(sections) + 1}. [Projects](#projects)")
    lines.append(f"{len(sections) + 2}. [Reference](#reference)")
    return "\n".join(lines)


def _section_header_md(sec):
    return (
        f"<a id='{sec['anchor']}'></a>\n"
        f"# {sec['num']}. {sec['title']}\n\n"
        f"{sec['intro']}"
    )


def _subtopic_header_md(sec, sub):
    return (
        f"<a id='{sub['anchor']}'></a>\n"
        f"### {sec['num']}.{sub['num']} {sub['title']}"
    )


def _title_md():
    return (
        "# Python Coding Challenges\n\n"
        f"A topic-wise practice notebook for **{STUDENT_NAME}**, mapped one-to-one "
        f"to the Udemy course *The Complete Python Bootcamp (13 Hours)*. "
        f"Every challenge has a problem statement, sample I/O, constraints, an empty "
        f"function stub for you to fill in, and a test cell to self-verify. "
        f"Each challenge also has a `🔑 View solution` link that opens the matching "
        f"section of the companion **CodingChallengesSolutions.ipynb**."
    )


def _solutions_title_md():
    return (
        "# Python Coding Challenges — Solutions\n\n"
        f"Reference solutions for every challenge in **CodingChallenges.ipynb**. "
        f"Each cell here mirrors the practice notebook: same problem statement, "
        f"same anchor, same tests — but the code cell contains a worked solution. "
        f"Run any cell to confirm `All tests passed!`."
    )


def _reference_md():
    return (
        "<a id='reference'></a>\n"
        "# Reference\n\n"
        f"- **Udemy course**: [The Complete Python Bootcamp (13 Hours)]({UDEMY_URL})\n"
        f"- **Official handbook (in this folder)**: `{PDF_NAME}`\n"
    )


# ---------------------------------------------------------------------------
# Notebook builder
# ---------------------------------------------------------------------------

def build_notebook(sections, projects, *, mode):
    """Build a notebook in the given mode ("practice" or "solutions")."""
    nb = nbf.v4.new_notebook()
    cells = []

    title = _title_md() if mode == "practice" else _solutions_title_md()
    cells.append(nbf.v4.new_markdown_cell(title))
    cells.append(nbf.v4.new_markdown_cell(_toc_md(sections)))

    for sec in sections:
        cells.append(nbf.v4.new_markdown_cell(_section_header_md(sec)))
        for sub in sec["subtopics"]:
            cells.append(nbf.v4.new_markdown_cell(_subtopic_header_md(sec, sub)))
            for ch in sub["challenges"]:
                cells.append(nbf.v4.new_markdown_cell(_problem_md(sec, sub, ch, mode=mode)))
                cells.append(nbf.v4.new_code_cell(_code_cell_source(ch, mode=mode)))
                cells.append(nbf.v4.new_code_cell(_test_cell_source(ch)))
                cells.append(nbf.v4.new_markdown_cell(_cross_link_md(sec, sub, ch, mode=mode)))

    # Projects
    cells.append(nbf.v4.new_markdown_cell(
        "<a id='projects'></a>\n"
        f"# {len(sections) + 1}. Projects\n\n"
        "These are the three pending capstone projects from the Udemy course. "
        "Each has a brief, a starter-code stub with skeleton signatures, and a "
        "test cell with multiple assertions to verify your implementation."
    ))
    for proj in projects:
        proj_sec = {"num": "P", "anchor": "projects"}
        proj_sub = {"num": proj["num"], "anchor": proj["anchor"]}
        proj_ch = {
            "num": 1,
            "title": proj["title"],
            "difficulty": "Project",
            "problem": proj["problem"],
            "input_fmt": proj["input_fmt"],
            "output_fmt": proj["output_fmt"],
            "sample_in": proj["sample_in"],
            "sample_out": proj["sample_out"],
            "constraints": proj["constraints"],
            "uses": proj.get("uses"),
        }
        cells.append(nbf.v4.new_markdown_cell(_problem_md(proj_sec, proj_sub, proj_ch, mode=mode)))
        cells.append(nbf.v4.new_code_cell(_code_cell_source(proj, mode=mode)))
        cells.append(nbf.v4.new_code_cell(_test_cell_source(proj)))
        cells.append(nbf.v4.new_markdown_cell(_cross_link_md(proj_sec, proj_sub, proj_ch, mode=mode)))

    cells.append(nbf.v4.new_markdown_cell(_reference_md()))
    nb["cells"] = cells
    nb["metadata"]["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    return nb


# ---------------------------------------------------------------------------
# SECTION SPECS
# ---------------------------------------------------------------------------

SECTIONS = []
PROJECTS = []


def project(*, num, title, anchor, problem, input_fmt, output_fmt,
            sample_in, sample_out, constraints, starter_code, solution,
            tests, uses=None):
    """Factory for a capstone project spec (multi-function code block)."""
    return {
        "is_project": True,
        "num": num,
        "anchor": anchor,
        "title": title,
        "difficulty": "Project",
        "problem": problem,
        "input_fmt": input_fmt,
        "output_fmt": output_fmt,
        "sample_in": sample_in,
        "sample_out": sample_out,
        "constraints": constraints,
        "uses": uses,
        "starter_code": starter_code,
        "solution": solution,
        "tests": tests,
    }


# ---------- Section 1: Introduction to Python ----------
SECTIONS.append(section(
    num=1,
    title="Introduction to Python",
    anchor="intro",
    intro=(
        "Warm-up challenges that exercise the very first things you learned: running "
        "a Python program, using `print`, working with simple expressions, and "
        "spotting the basic vocabulary of the language. Every solution is a function "
        "that **returns** a value (instead of printing) so the test cell can verify it."
    ),
    subtopics=[
        subtopic(num=1, title="First Programs", anchor="intro-first", challenges=[
            challenge(
                num=1, title="Hello, Rishith!", difficulty="Easy",
                problem=(
                    "Write a function that returns the greeting "
                    f"`Hello, {STUDENT_NAME}!` — your very first Python output, but "
                    "wrapped in a function so it can be tested."
                ),
                input_fmt="No arguments.",
                output_fmt=f"The literal string `Hello, {STUDENT_NAME}!`.",
                sample_in="hello_rishith()",
                sample_out=f"'Hello, {STUDENT_NAME}!'",
                constraints="Return — do not print.",
                signature="def hello_rishith():",
                tests=[
                    f'assert hello_rishith() == "Hello, {STUDENT_NAME}!"',
                ],
                solution=f'return "Hello, {STUDENT_NAME}!"',
            ),
            challenge(
                num=2, title="Personalised Greeting", difficulty="Easy",
                problem=(
                    "Given a name, return a greeting in the form `Hello, <name>!`. "
                    "Use an f-string."
                ),
                input_fmt="A single string `name` (1 ≤ len ≤ 50).",
                output_fmt="A string `Hello, <name>!`.",
                sample_in='greet("Sandeep")',
                sample_out="'Hello, Sandeep!'",
                constraints="Use an f-string.",
                signature="def greet(name):",
                tests=[
                    'assert greet("Sandeep") == "Hello, Sandeep!"',
                    f'assert greet("{STUDENT_NAME}") == "Hello, {STUDENT_NAME}!"',
                    'assert greet("A") == "Hello, A!"',
                ],
                solution='return f"Hello, {name}!"',
            ),
        ]),
        subtopic(num=2, title="Sanity Checks", anchor="intro-sanity", challenges=[
            challenge(
                num=1, title="Python Version Tag", difficulty="Easy",
                problem=(
                    "Return a string that confirms Python is running, in the exact "
                    "format `Python is running`. This is the Python equivalent of a "
                    "smoke-test."
                ),
                input_fmt="No arguments.",
                output_fmt="The string `Python is running`.",
                sample_in="python_running()",
                sample_out="'Python is running'",
                constraints="Return the exact string — no trailing punctuation.",
                signature="def python_running():",
                tests=[
                    'assert python_running() == "Python is running"',
                ],
                solution='return "Python is running"',
            ),
            challenge(
                num=2, title="Two-Line Banner", difficulty="Easy",
                problem=(
                    "Return a two-line banner using the newline escape sequence `\\n`. "
                    "Line 1: `Welcome`. Line 2: the given name. The two lines must be "
                    "joined by a single `\\n`."
                ),
                input_fmt="A single string `name`.",
                output_fmt="A string with `Welcome`, a newline, then the name.",
                sample_in='banner("Rishith")',
                sample_out="'Welcome\\nRishith'",
                constraints="Use the `\\n` escape — do not use `print`.",
                signature="def banner(name):",
                tests=[
                    'assert banner("Rishith") == "Welcome\\nRishith"',
                    'assert banner("Sandeep") == "Welcome\\nSandeep"',
                ],
                solution='return f"Welcome\\n{name}"',
            ),
        ]),
    ],
))
# BUILD-MARKER: intro-complete


# ---------- Section 2: Python Basic Tools ----------
SECTIONS.append(section(
    num=2,
    title="Python Basic Tools",
    anchor="basic-tools",
    intro=(
        "Sharpen your fluency with the everyday tools: comments, `print`, escape "
        "sequences, variables, and `input`. Each challenge is a function that returns "
        "a value (so we can test it) — the spirit is exactly the same as the Udemy "
        "lectures, just wrapped for verification."
    ),
    subtopics=[
        subtopic(num=1, title="Print & Escape Sequences", anchor="basic-print", challenges=[
            challenge(
                num=1, title="Joined Words", difficulty="Easy",
                problem=(
                    "Given two words, return them joined by a single space — the same "
                    "thing `print(a, b)` would put on screen, but as a returned string."
                ),
                input_fmt="Two strings `a` and `b`.",
                output_fmt="A string in the form `<a> <b>`.",
                sample_in='join_words("Hello", "World")',
                sample_out="'Hello World'",
                constraints="Use an f-string or `+`. Do not call `print`.",
                signature="def join_words(a, b):",
                tests=[
                    'assert join_words("Hello", "World") == "Hello World"',
                    'assert join_words("Python", "rocks") == "Python rocks"',
                    'assert join_words("a", "b") == "a b"',
                ],
                solution='return f"{a} {b}"',
            ),
            challenge(
                num=2, title="Tabbed Pair", difficulty="Easy",
                problem=(
                    "Return two values separated by a single tab character (`\\t`). "
                    "Useful for laying out simple columns in console output."
                ),
                input_fmt="Two strings `label` and `value`.",
                output_fmt="`<label>\\t<value>`.",
                sample_in='tabbed("Name", "Rishith")',
                sample_out="'Name\\tRishith'",
                constraints="Use the `\\t` escape exactly once.",
                signature="def tabbed(label, value):",
                tests=[
                    'assert tabbed("Name", "Rishith") == "Name\\tRishith"',
                    'assert tabbed("Age", "16") == "Age\\t16"',
                ],
                solution='return f"{label}\\t{value}"',
            ),
            challenge(
                num=3, title="Quoted Quote", difficulty="Easy",
                problem=(
                    "Return the given text wrapped in double quotes — but the quotes "
                    "themselves must appear in the output. You'll need the `\\\"` "
                    "escape (or single quotes around the literal)."
                ),
                input_fmt="A single string `text`.",
                output_fmt='`"<text>"` — literal double quotes around the value.',
                sample_in='quoted("hello")',
                sample_out='\'"hello"\'',
                constraints="Result length must be `len(text) + 2`.",
                signature="def quoted(text):",
                tests=[
                    'assert quoted("hello") == "\\"hello\\""',
                    'assert quoted("Rishith") == "\\"Rishith\\""',
                    'assert quoted("") == "\\"\\""',
                ],
                solution='return f"\\"{text}\\""',
            ),
        ]),
        subtopic(num=2, title="Variables", anchor="basic-vars", challenges=[
            challenge(
                num=1, title="Swap", difficulty="Easy",
                problem=(
                    "Given two values `a` and `b`, return them as a tuple `(b, a)` — "
                    "the classic variable-swap. Tuple unpacking is the Pythonic way."
                ),
                input_fmt="Any two values `a`, `b`.",
                output_fmt="A 2-tuple `(b, a)`.",
                sample_in="swap(1, 2)",
                sample_out="(2, 1)",
                constraints="Single-line solution preferred.",
                signature="def swap(a, b):",
                tests=[
                    "assert swap(1, 2) == (2, 1)",
                    'assert swap("x", "y") == ("y", "x")',
                    "assert swap(None, 0) == (0, None)",
                ],
                solution="return b, a",
            ),
            challenge(
                num=2, title="Initials", difficulty="Easy",
                problem=(
                    "Given a first name and a last name, return the initials joined "
                    "with a dot, in upper case. Example: `Rishith Sandeep` → `R.S`."
                ),
                input_fmt="Two strings `first` and `last` (each non-empty).",
                output_fmt="`<F>.<L>` in upper case.",
                sample_in='initials("Rishith", "Sandeep")',
                sample_out="'R.S'",
                constraints="Use indexing `[0]` and `.upper()`.",
                signature="def initials(first, last):",
                tests=[
                    'assert initials("Rishith", "Sandeep") == "R.S"',
                    'assert initials("ada", "lovelace") == "A.L"',
                    'assert initials("Guido", "van Rossum") == "G.V"',
                ],
                solution='return f"{first[0].upper()}.{last[0].upper()}"',
            ),
        ]),
        subtopic(num=3, title="Input → Cast → Use", anchor="basic-input", challenges=[
            challenge(
                num=1, title="Doubled Age", difficulty="Easy",
                problem=(
                    "Real `input()` returns a string. Simulate that step: given an "
                    "age **as a string**, convert it to an integer and return double "
                    "its value."
                ),
                input_fmt="A string `age_str` that represents a non-negative integer.",
                output_fmt="An integer — twice the age.",
                sample_in='double_age("16")',
                sample_out="32",
                constraints="Use `int(...)` to cast.",
                signature="def double_age(age_str):",
                tests=[
                    'assert double_age("16") == 32',
                    'assert double_age("0") == 0',
                    'assert double_age("100") == 200',
                ],
                solution="return int(age_str) * 2",
            ),
            challenge(
                num=2, title="Sentence Builder", difficulty="Easy",
                problem=(
                    "Given a name string and an age string (both as `input()` would "
                    "return them), return the sentence `My name is <name> and I am "
                    "<age> years old.` — with the age cast back to int and printed "
                    "as a number."
                ),
                input_fmt="`name` (str), `age_str` (str of an integer).",
                output_fmt="A complete English sentence as shown.",
                sample_in='sentence("Rishith", "16")',
                sample_out="'My name is Rishith and I am 16 years old.'",
                constraints="Use an f-string. Cast `age_str` to `int` first.",
                signature="def sentence(name, age_str):",
                tests=[
                    'assert sentence("Rishith", "16") == "My name is Rishith and I am 16 years old."',
                    'assert sentence("Sandeep", "40") == "My name is Sandeep and I am 40 years old."',
                ],
                solution='age = int(age_str)\nreturn f"My name is {name} and I am {age} years old."',
            ),
            challenge(
                num=3, title="Echo with Length", difficulty="Medium",
                problem=(
                    "Given a string from `input()`, return a tuple `(text, length)` "
                    "where `length` is the integer length of `text`. Useful little "
                    "helper for validating user input."
                ),
                input_fmt="A single string `text`.",
                output_fmt="A 2-tuple `(text, len(text))`.",
                sample_in='echo_with_length("Rishith")',
                sample_out="('Rishith', 7)",
                constraints="Length must be an `int`, not a string.",
                signature="def echo_with_length(text):",
                tests=[
                    'assert echo_with_length("Rishith") == ("Rishith", 7)',
                    'assert echo_with_length("") == ("", 0)',
                    'assert echo_with_length("Python rocks!") == ("Python rocks!", 13)',
                ],
                solution="return text, len(text)",
            ),
        ]),
    ],
))
# BUILD-MARKER: basic-tools-complete


# ---------- Section 3: Data Types ----------
SECTIONS.append(section(
    num=3,
    title="Data Types",
    anchor="data-types",
    intro=(
        "Get a feel for Python's core data types — `int`, `float`, `str`, `bool` — "
        "and how to convert between them. Knowing which type a value has, and how "
        "to coerce values safely, is the foundation everything else stands on."
    ),
    subtopics=[
        subtopic(num=1, title="Type Inspection", anchor="dt-inspect", challenges=[
            challenge(
                num=1, title="Name the Type", difficulty="Easy",
                problem=(
                    "Given any value, return the name of its type as a string — "
                    "exactly what `type(x).__name__` produces. Example: `42` → `'int'`."
                ),
                input_fmt="Any single value `value`.",
                output_fmt="A string — the type's name.",
                sample_in="name_the_type(42)",
                sample_out="'int'",
                constraints="Use `type(...)` and the `.__name__` attribute.",
                signature="def name_the_type(value):",
                tests=[
                    'assert name_the_type(42) == "int"',
                    'assert name_the_type(3.14) == "float"',
                    'assert name_the_type("hi") == "str"',
                    'assert name_the_type(True) == "bool"',
                ],
                solution="return type(value).__name__",
            ),
            challenge(
                num=2, title="Is It a Number?", difficulty="Easy",
                problem=(
                    "Return `True` when the given value is a number (`int` or `float`), "
                    "`False` otherwise. **Watch out**: `bool` is technically a subclass "
                    "of `int` in Python — explicitly exclude booleans from being numbers."
                ),
                input_fmt="Any single value `value`.",
                output_fmt="A `bool`.",
                sample_in="is_number(3.14)",
                sample_out="True",
                constraints=[
                    "Use `isinstance(...)`.",
                    "`is_number(True)` must be `False`.",
                ],
                signature="def is_number(value):",
                tests=[
                    "assert is_number(3) is True",
                    "assert is_number(3.14) is True",
                    "assert is_number(True) is False",
                    'assert is_number("3") is False',
                    "assert is_number(None) is False",
                ],
                solution="return isinstance(value, (int, float)) and not isinstance(value, bool)",
            ),
        ]),
        subtopic(num=2, title="Type Conversion", anchor="dt-convert", challenges=[
            challenge(
                num=1, title="Safe Int", difficulty="Easy",
                problem=(
                    "Given a string, return its integer value if conversion succeeds; "
                    "otherwise return `None`. Build the safety with `try`/`except` "
                    "around `int(...)`."
                ),
                input_fmt="A single string `s`.",
                output_fmt="`int` or `None`.",
                sample_in='safe_int("42")',
                sample_out="42",
                constraints="Catch `ValueError` only — not all exceptions.",
                signature="def safe_int(s):",
                tests=[
                    'assert safe_int("42") == 42',
                    'assert safe_int("-7") == -7',
                    'assert safe_int("abc") is None',
                    'assert safe_int("") is None',
                ],
                solution="try:\n    return int(s)\nexcept ValueError:\n    return None",
            ),
            challenge(
                num=2, title="Bool to Word", difficulty="Easy",
                problem=(
                    "Given a boolean, return the word `'yes'` for `True` and `'no'` for "
                    "`False`. The simplest possible mapping — practise the inline `if`."
                ),
                input_fmt="A single `bool` `flag`.",
                output_fmt="`'yes'` or `'no'`.",
                sample_in="bool_to_word(True)",
                sample_out="'yes'",
                constraints="Single expression preferred (use the inline `if`).",
                signature="def bool_to_word(flag):",
                tests=[
                    'assert bool_to_word(True) == "yes"',
                    'assert bool_to_word(False) == "no"',
                ],
                solution='return "yes" if flag else "no"',
            ),
            challenge(
                num=3, title="Float Round-Trip", difficulty="Medium",
                problem=(
                    "Given a float, return it converted to `int` (truncation toward "
                    "zero) and then back to `float`. Example: `3.9` → `3.0`, `-2.5` → "
                    "`-2.0`. Useful for understanding precision loss."
                ),
                input_fmt="A single `float` `value`.",
                output_fmt="A `float` whose integer part matches `int(value)`.",
                sample_in="round_trip(3.9)",
                sample_out="3.0",
                constraints="Must return a `float`, not an `int`.",
                signature="def round_trip(value):",
                tests=[
                    "assert round_trip(3.9) == 3.0",
                    "assert round_trip(-2.5) == -2.0",
                    "assert round_trip(0.1) == 0.0",
                    "assert isinstance(round_trip(7.7), float)",
                ],
                solution="return float(int(value))",
            ),
        ]),
        subtopic(num=3, title="Type Categories", anchor="dt-categories", challenges=[
            challenge(
                num=1, title="Category Tag", difficulty="Medium",
                problem=(
                    "Given a value, return the broad category string: `'number'` for "
                    "ints/floats (excluding bools), `'text'` for strings, `'bool'` for "
                    "booleans, and `'other'` for anything else. A tiny dispatcher — "
                    "exactly the kind of helper bigger programs use."
                ),
                input_fmt="Any single value `value`.",
                output_fmt="One of `'number'`, `'text'`, `'bool'`, `'other'`.",
                sample_in='category("hello")',
                sample_out="'text'",
                constraints="Order your `isinstance` checks carefully — `bool` first.",
                signature="def category(value):",
                tests=[
                    'assert category(42) == "number"',
                    'assert category(3.14) == "number"',
                    'assert category("hi") == "text"',
                    'assert category(True) == "bool"',
                    'assert category(None) == "other"',
                    'assert category([1, 2]) == "other"',
                ],
                uses=["data types", "isinstance"],
                solution=(
                    "if isinstance(value, bool):\n    return \"bool\"\n"
                    "if isinstance(value, (int, float)):\n    return \"number\"\n"
                    "if isinstance(value, str):\n    return \"text\"\n"
                    "return \"other\""
                ),
            ),
            challenge(
                num=2, title="Mutable or Not?", difficulty="Medium",
                problem=(
                    "Return `True` if the value's type is one Python treats as "
                    "**mutable** (`list`, `dict`, `set`), `False` otherwise. Knowing "
                    "this stops a whole category of bugs."
                ),
                input_fmt="Any single value `value`.",
                output_fmt="A `bool`.",
                sample_in="is_mutable([1, 2])",
                sample_out="True",
                constraints="Use `isinstance` with a tuple of types.",
                signature="def is_mutable(value):",
                tests=[
                    "assert is_mutable([1, 2]) is True",
                    "assert is_mutable({'a': 1}) is True",
                    "assert is_mutable({1, 2, 3}) is True",
                    "assert is_mutable((1, 2)) is False",
                    'assert is_mutable("hi") is False',
                    "assert is_mutable(42) is False",
                ],
                uses=["data types"],
                solution="return isinstance(value, (list, dict, set))",
            ),
            challenge(
                num=3, title="Class Family Tree", difficulty="Hard",
                problem=(
                    "Given a value, return a list of every class name in its method "
                    "resolution order (MRO), excluding `object`. For `True` you should "
                    "get `['bool', 'int']`; for `42` you get `['int']`. Useful for "
                    "understanding why `isinstance(True, int)` is `True`."
                ),
                input_fmt="Any single value `value`.",
                output_fmt="A list of class-name strings.",
                sample_in="class_family(True)",
                sample_out="['bool', 'int']",
                constraints=[
                    "Use `type(value).__mro__`.",
                    "Drop `object` from the result.",
                ],
                signature="def class_family(value):",
                tests=[
                    'assert class_family(True) == ["bool", "int"]',
                    'assert class_family(42) == ["int"]',
                    'assert class_family(3.14) == ["float"]',
                    'assert class_family("hi") == ["str"]',
                ],
                uses=["data types", "isinstance", "lists"],
                solution=(
                    "return [cls.__name__ for cls in type(value).__mro__ "
                    "if cls is not object]"
                ),
            ),
        ]),
    ],
))
# BUILD-MARKER: data-types-complete


# ---------- Section 4: Working with Strings ----------
SECTIONS.append(section(
    num=4,
    title="Working with Strings",
    anchor="strings",
    intro=(
        "Strings are the workhorses of every program — names, messages, file paths, "
        "user input, log lines. These challenges cover indexing, slicing, the most "
        "common methods (`replace`, `split`, `join`, `strip`, `upper`/`lower`, "
        "`find`/`in`), f-strings, and validation. Each one is a tiny, real-world "
        "task — the kind of code you'll write every day."
    ),
    subtopics=[
        subtopic(num=1, title="Indexing & Slicing", anchor="strings-slicing", challenges=[
            challenge(
                num=1, title="First and Last", difficulty="Easy",
                problem=(
                    "Return a 2-tuple containing the first and last characters of a "
                    "non-empty string. The most direct test of indexing."
                ),
                input_fmt="A non-empty string `s`.",
                output_fmt="`(s[0], s[-1])`.",
                sample_in='first_and_last("Rishith")',
                sample_out="('R', 'h')",
                constraints="Use indexing — no slicing.",
                signature="def first_and_last(s):",
                tests=[
                    'assert first_and_last("Rishith") == ("R", "h")',
                    'assert first_and_last("a") == ("a", "a")',
                    'assert first_and_last("Python") == ("P", "n")',
                ],
                solution="return s[0], s[-1]",
            ),
            challenge(
                num=2, title="Reverse a String", difficulty="Easy",
                problem=(
                    "Return the given string reversed. Use slicing — `[::-1]` is the "
                    "Pythonic one-liner."
                ),
                input_fmt="A string `s`.",
                output_fmt="The string reversed.",
                sample_in='reverse("Rishith")',
                sample_out="'htihsiR'",
                constraints="Must use slicing — do not use `reversed()`.",
                signature="def reverse(s):",
                tests=[
                    'assert reverse("Rishith") == "htihsiR"',
                    'assert reverse("") == ""',
                    'assert reverse("a") == "a"',
                    'assert reverse("ab") == "ba"',
                ],
                solution="return s[::-1]",
            ),
            challenge(
                num=3, title="Every Other Character", difficulty="Medium",
                problem=(
                    "Return every other character of the string, starting from index 0. "
                    "`'ABCDEF'` should give `'ACE'`. Slicing with a step does this in "
                    "one expression."
                ),
                input_fmt="A string `s`.",
                output_fmt="The string formed by characters at even indices.",
                sample_in='every_other("ABCDEF")',
                sample_out="'ACE'",
                constraints="Single-expression slice with step.",
                signature="def every_other(s):",
                tests=[
                    'assert every_other("ABCDEF") == "ACE"',
                    'assert every_other("Rishith") == "Rsih"',
                    'assert every_other("") == ""',
                    'assert every_other("xy") == "x"',
                ],
                solution="return s[::2]",
            ),
            challenge(
                num=4, title="Middle Characters", difficulty="Hard",
                problem=(
                    "Return the middle character if the string length is odd, or the "
                    "two middle characters if it is even. Empty string returns empty "
                    "string."
                ),
                input_fmt="A string `s` (any length, including empty).",
                output_fmt="A 1- or 2-character string (or empty).",
                sample_in='middle("Rishith")',
                sample_out="'h'",
                constraints="Use slicing and `len()` — no loops.",
                signature="def middle(s):",
                tests=[
                    'assert middle("Rishith") == "h"',
                    'assert middle("Python") == "th"',
                    'assert middle("") == ""',
                    'assert middle("a") == "a"',
                    'assert middle("ab") == "ab"',
                    'assert middle("abcd") == "bc"',
                ],
                uses=["strings (slicing)", "len()", "conditionals"],
                solution=(
                    "n = len(s)\n"
                    "mid = n // 2\n"
                    "return s[mid] if n % 2 else s[mid - 1:mid + 1] if n else \"\""
                ),
            ),
        ]),
        subtopic(num=2, title="Methods & Cleaning", anchor="strings-methods", challenges=[
            challenge(
                num=1, title="Trim and Lower", difficulty="Easy",
                problem=(
                    "Given a possibly-messy string, return it with surrounding whitespace "
                    "stripped and converted to lower case — the canonical 'normalise "
                    "user input' move."
                ),
                input_fmt="A string `s`.",
                output_fmt="The cleaned, lower-cased string.",
                sample_in='trim_lower("  Rishith  ")',
                sample_out="'rishith'",
                constraints="Chain `.strip()` and `.lower()`.",
                signature="def trim_lower(s):",
                tests=[
                    'assert trim_lower("  Rishith  ") == "rishith"',
                    'assert trim_lower("HELLO") == "hello"',
                    'assert trim_lower("") == ""',
                    'assert trim_lower("\\tPython\\n") == "python"',
                ],
                solution="return s.strip().lower()",
            ),
            challenge(
                num=2, title="Replace All Spaces", difficulty="Easy",
                problem=(
                    "Replace every space in the string with a hyphen `-`. Useful for "
                    "turning a title into a URL slug."
                ),
                input_fmt="A string `s`.",
                output_fmt="The string with all spaces → `-`.",
                sample_in='hyphenate("hello world")',
                sample_out="'hello-world'",
                constraints="Use `.replace`.",
                signature="def hyphenate(s):",
                tests=[
                    'assert hyphenate("hello world") == "hello-world"',
                    'assert hyphenate("a b c d") == "a-b-c-d"',
                    'assert hyphenate("nospaces") == "nospaces"',
                    'assert hyphenate("") == ""',
                ],
                solution='return s.replace(" ", "-")',
            ),
            challenge(
                num=3, title="Word Count", difficulty="Easy",
                problem=(
                    "Return the number of whitespace-separated words in a string. "
                    "Handle the empty string as 0 words."
                ),
                input_fmt="A string `s`.",
                output_fmt="An `int` — the word count.",
                sample_in='word_count("Hello there Rishith")',
                sample_out="3",
                constraints="Use `.split()` (no arguments — it handles any whitespace).",
                signature="def word_count(s):",
                tests=[
                    'assert word_count("Hello there Rishith") == 3',
                    'assert word_count("one") == 1',
                    'assert word_count("") == 0',
                    'assert word_count("   spaced    out   ") == 2',
                ],
                solution="return len(s.split())",
            ),
            challenge(
                num=4, title="Title Case", difficulty="Medium",
                problem=(
                    "Return the string with the first letter of every word capitalised "
                    "and all other letters in lower case — what `.title()` does, but "
                    "implement it yourself by splitting, transforming, and joining."
                ),
                input_fmt="A string `s`.",
                output_fmt="The title-cased string.",
                sample_in='title_case("hello there rishith")',
                sample_out="'Hello There Rishith'",
                constraints=[
                    "Do not use `.title()`.",
                    "Use `.split`, indexing, `.upper`, `.lower`, `.join`.",
                ],
                signature="def title_case(s):",
                tests=[
                    'assert title_case("hello there rishith") == "Hello There Rishith"',
                    'assert title_case("PYTHON") == "Python"',
                    'assert title_case("") == ""',
                    'assert title_case("a b c") == "A B C"',
                ],
                uses=["strings (split, join)", "indexing"],
                solution=(
                    "return \" \".join(w[0].upper() + w[1:].lower() for w in s.split())"
                ),
            ),
            challenge(
                num=5, title="Acronym", difficulty="Medium",
                problem=(
                    "Given a phrase, return its acronym — the upper-case first letter "
                    "of each word. Example: `'Application Programming Interface'` → "
                    "`'API'`."
                ),
                input_fmt="A string `phrase`.",
                output_fmt="The upper-case acronym.",
                sample_in='acronym("Application Programming Interface")',
                sample_out="'API'",
                constraints="Words separated by single spaces. Empty input → empty output.",
                signature="def acronym(phrase):",
                tests=[
                    'assert acronym("Application Programming Interface") == "API"',
                    'assert acronym("self contained underwater breathing apparatus") == "SCUBA"',
                    'assert acronym("python") == "P"',
                    'assert acronym("") == ""',
                ],
                uses=["strings (split, indexing)"],
                solution='return "".join(w[0].upper() for w in phrase.split())',
            ),
        ]),
        subtopic(num=3, title="f-Strings & Building", anchor="strings-fstrings", challenges=[
            challenge(
                num=1, title="Receipt Line", difficulty="Easy",
                problem=(
                    "Given an item name and a price (float), return a receipt line in "
                    "the form `<item>: $<price>` with the price formatted to exactly "
                    "two decimal places."
                ),
                input_fmt="`item` (str), `price` (float).",
                output_fmt="`<item>: $<price>` (price has 2 decimals).",
                sample_in='receipt_line("Coffee", 3.5)',
                sample_out="'Coffee: $3.50'",
                constraints="Use an f-string with the `:.2f` format spec.",
                signature="def receipt_line(item, price):",
                tests=[
                    'assert receipt_line("Coffee", 3.5) == "Coffee: $3.50"',
                    'assert receipt_line("Bagel", 2) == "Bagel: $2.00"',
                    'assert receipt_line("Tax", 0.1234) == "Tax: $0.12"',
                ],
                solution='return f"{item}: ${price:.2f}"',
            ),
            challenge(
                num=2, title="Pad on the Left", difficulty="Medium",
                problem=(
                    "Right-align a number inside a field of given width, padded with "
                    "leading zeros. Example: `pad(7, 3)` → `'007'`. Useful for ID "
                    "numbers and timestamps."
                ),
                input_fmt="`n` (int, ≥ 0), `width` (int, ≥ 1).",
                output_fmt="A string of length `max(width, len(str(n)))`, zero-padded.",
                sample_in="pad(7, 3)",
                sample_out="'007'",
                constraints="Use the f-string spec `:0<width>d` or `str.zfill`.",
                signature="def pad(n, width):",
                tests=[
                    'assert pad(7, 3) == "007"',
                    'assert pad(42, 5) == "00042"',
                    'assert pad(123, 2) == "123"',
                    'assert pad(0, 4) == "0000"',
                ],
                solution="return f\"{n:0{width}d}\"",
            ),
            challenge(
                num=3, title="Build a Banner", difficulty="Hard",
                problem=(
                    "Given a message string, return a 3-line banner: a top border of "
                    "`#` characters as wide as the message + 4, the message centred in "
                    "a `# <message> #` line (padded with spaces), and an identical "
                    "bottom border. Lines joined with `\\n`. Example: "
                    "`'Hi'` →\n```\n######\n# Hi #\n######\n```"
                ),
                input_fmt="A non-empty string `msg`.",
                output_fmt="A 3-line banner string.",
                sample_in='build_banner("Hi")',
                sample_out="'######\\n# Hi #\\n######'",
                constraints="Use string repetition (`*`) and f-strings.",
                signature="def build_banner(msg):",
                tests=[
                    'assert build_banner("Hi") == "######\\n# Hi #\\n######"',
                    'assert build_banner("Python") == "##########\\n# Python #\\n##########"',
                    'assert build_banner("a") == "#####\\n# a #\\n#####"',
                ],
                uses=["strings (repetition, f-strings)", "len()"],
                solution=(
                    "border = \"#\" * (len(msg) + 4)\n"
                    "return f\"{border}\\n# {msg} #\\n{border}\""
                ),
            ),
        ]),
        subtopic(num=4, title="Membership & Validation", anchor="strings-membership", challenges=[
            challenge(
                num=1, title="Contains Vowel", difficulty="Easy",
                problem=(
                    "Return `True` if the string contains at least one vowel "
                    "(`a, e, i, o, u`, case-insensitive), `False` otherwise."
                ),
                input_fmt="A string `s`.",
                output_fmt="A `bool`.",
                sample_in='has_vowel("Rishith")',
                sample_out="True",
                constraints="Use `in` membership.",
                signature="def has_vowel(s):",
                tests=[
                    'assert has_vowel("Rishith") is True',
                    'assert has_vowel("xyz") is False',
                    'assert has_vowel("") is False',
                    'assert has_vowel("UPPER") is True',
                ],
                solution='return any(ch in "aeiou" for ch in s.lower())',
            ),
            challenge(
                num=2, title="Valid Numeric String", difficulty="Medium",
                problem=(
                    "Return `True` if the string represents a valid non-negative "
                    "integer (only digits, length ≥ 1, no leading `+`/`-`), `False` "
                    "otherwise. Empty strings are invalid."
                ),
                input_fmt="A string `s`.",
                output_fmt="A `bool`.",
                sample_in='is_numeric_string("42")',
                sample_out="True",
                constraints="Use `.isdigit()` plus an emptiness check.",
                signature="def is_numeric_string(s):",
                tests=[
                    'assert is_numeric_string("42") is True',
                    'assert is_numeric_string("0") is True',
                    'assert is_numeric_string("") is False',
                    'assert is_numeric_string("-7") is False',
                    'assert is_numeric_string("3.14") is False',
                    'assert is_numeric_string(" 1 ") is False',
                ],
                uses=["strings (validation)", "logic (and)"],
                solution="return len(s) > 0 and s.isdigit()",
            ),
        ]),
    ],
))
# BUILD-MARKER: strings-complete


# ---------- Section 5: Working with Numbers ----------
SECTIONS.append(section(
    num=5,
    title="Working with Numbers",
    anchor="numbers",
    intro=(
        "Arithmetic, rounding, and number properties — the maths half of programming. "
        "Every challenge returns a number you can verify with a single `assert`. "
        "Reuse string skills from §4 where it helps (digit sums, validation)."
    ),
    subtopics=[
        subtopic(num=1, title="Arithmetic & Operations", anchor="numbers-arith", challenges=[
            challenge(
                num=1, title="Sum of Two", difficulty="Easy",
                problem="Return the sum of two numbers.",
                input_fmt="Two numbers `a`, `b`.",
                output_fmt="A number `a + b`.",
                sample_in="add(2, 3)",
                sample_out="5",
                constraints="Single expression.",
                signature="def add(a, b):",
                tests=[
                    "assert add(2, 3) == 5",
                    "assert add(-1, 1) == 0",
                    "assert add(1.5, 2.5) == 4.0",
                ],
                solution="return a + b",
            ),
            challenge(
                num=2, title="Absolute Difference", difficulty="Easy",
                problem=(
                    "Return the absolute difference between two numbers — always "
                    "non-negative."
                ),
                input_fmt="Two numbers `a`, `b`.",
                output_fmt="`|a - b|`.",
                sample_in="abs_diff(7, 3)",
                sample_out="4",
                constraints="Use the built-in `abs`.",
                signature="def abs_diff(a, b):",
                tests=[
                    "assert abs_diff(7, 3) == 4",
                    "assert abs_diff(3, 7) == 4",
                    "assert abs_diff(-5, 5) == 10",
                    "assert abs_diff(0, 0) == 0",
                ],
                solution="return abs(a - b)",
            ),
            challenge(
                num=3, title="Hours to Seconds", difficulty="Easy",
                problem=(
                    "Convert a duration in hours (an integer or float) into the "
                    "equivalent number of seconds."
                ),
                input_fmt="A number `hours` (≥ 0).",
                output_fmt="A number — total seconds.",
                sample_in="to_seconds(2)",
                sample_out="7200",
                constraints="No imports.",
                signature="def to_seconds(hours):",
                tests=[
                    "assert to_seconds(2) == 7200",
                    "assert to_seconds(0) == 0",
                    "assert to_seconds(0.5) == 1800.0",
                    "assert to_seconds(24) == 86400",
                ],
                solution="return hours * 3600",
            ),
            challenge(
                num=4, title="BMI", difficulty="Medium",
                problem=(
                    "Given height in metres and weight in kilograms, return the BMI "
                    "(`weight / height ** 2`) rounded to one decimal place."
                ),
                input_fmt="`height` (float, > 0), `weight` (float, > 0).",
                output_fmt="A `float` — BMI rounded to 1 decimal.",
                sample_in="bmi(1.75, 70)",
                sample_out="22.9",
                constraints="Use `**` and `round(..., 1)`.",
                signature="def bmi(height, weight):",
                tests=[
                    "assert bmi(1.75, 70) == 22.9",
                    "assert bmi(2.0, 80) == 20.0",
                    "assert bmi(1.5, 50) == 22.2",
                ],
                uses=["numbers (operators, rounding)"],
                solution="return round(weight / height ** 2, 1)",
            ),
        ]),
        subtopic(num=2, title="Rounding & Division", anchor="numbers-rounding", challenges=[
            challenge(
                num=1, title="Round to N", difficulty="Easy",
                problem="Round a float to a given number of decimal places.",
                input_fmt="`x` (float), `digits` (int ≥ 0).",
                output_fmt="A `float` rounded to `digits` decimals.",
                sample_in="round_to(3.14159, 2)",
                sample_out="3.14",
                constraints="Use the built-in `round`.",
                signature="def round_to(x, digits):",
                tests=[
                    "assert round_to(3.14159, 2) == 3.14",
                    "assert round_to(2.5, 0) == 2",
                    "assert round_to(-1.555, 1) == -1.6 or round_to(-1.555, 1) == -1.5",
                ],
                solution="return round(x, digits)",
            ),
            challenge(
                num=2, title="Pages Needed", difficulty="Medium",
                problem=(
                    "You're printing `n` items, with `per_page` items per page. Return "
                    "the number of pages needed (last page may be partial). Example: "
                    "`pages_needed(10, 3)` → `4`."
                ),
                input_fmt="`n` (int ≥ 0), `per_page` (int > 0).",
                output_fmt="`int` — pages required.",
                sample_in="pages_needed(10, 3)",
                sample_out="4",
                constraints="Use the **ceiling division** trick `(n + p - 1) // p` (no imports).",
                signature="def pages_needed(n, per_page):",
                tests=[
                    "assert pages_needed(10, 3) == 4",
                    "assert pages_needed(9, 3) == 3",
                    "assert pages_needed(0, 5) == 0",
                    "assert pages_needed(1, 100) == 1",
                ],
                uses=["numbers (floor division)"],
                solution="return (n + per_page - 1) // per_page",
            ),
            challenge(
                num=3, title="Last Digit", difficulty="Easy",
                problem=(
                    "Return the last digit of a non-negative integer. Modulo by 10 "
                    "is the cleanest way."
                ),
                input_fmt="An integer `n` (≥ 0).",
                output_fmt="An integer 0..9.",
                sample_in="last_digit(12345)",
                sample_out="5",
                constraints="Use `%`.",
                signature="def last_digit(n):",
                tests=[
                    "assert last_digit(12345) == 5",
                    "assert last_digit(0) == 0",
                    "assert last_digit(7) == 7",
                    "assert last_digit(100) == 0",
                ],
                solution="return n % 10",
            ),
        ]),
        subtopic(num=3, title="Number Properties", anchor="numbers-props", challenges=[
            challenge(
                num=1, title="Is Even", difficulty="Easy",
                problem="Return `True` if `n` is even, `False` otherwise.",
                input_fmt="An integer `n`.",
                output_fmt="A `bool`.",
                sample_in="is_even(4)",
                sample_out="True",
                constraints="Use `% 2`.",
                signature="def is_even(n):",
                tests=[
                    "assert is_even(4) is True",
                    "assert is_even(7) is False",
                    "assert is_even(0) is True",
                    "assert is_even(-2) is True",
                ],
                solution="return n % 2 == 0",
            ),
            challenge(
                num=2, title="Multiple Of", difficulty="Easy",
                problem=(
                    "Return `True` when `n` is an exact multiple of `m`, `False` "
                    "otherwise. Treat `m == 0` as 'never a multiple' (return `False`)."
                ),
                input_fmt="Two integers `n`, `m`.",
                output_fmt="A `bool`.",
                sample_in="is_multiple(15, 3)",
                sample_out="True",
                constraints="Guard against division-by-zero.",
                signature="def is_multiple(n, m):",
                tests=[
                    "assert is_multiple(15, 3) is True",
                    "assert is_multiple(15, 4) is False",
                    "assert is_multiple(0, 5) is True",
                    "assert is_multiple(5, 0) is False",
                ],
                uses=["numbers (modulo)", "logic (and)"],
                solution="return m != 0 and n % m == 0",
            ),
            challenge(
                num=3, title="Digit Sum", difficulty="Hard",
                problem=(
                    "Return the sum of the decimal digits of a non-negative integer. "
                    "Example: `1234` → `1+2+3+4` = `10`. The cleanest Pythonic way is "
                    "to convert to a string and sum the digit values."
                ),
                input_fmt="A non-negative integer `n`.",
                output_fmt="An integer ≥ 0 — the digit sum.",
                sample_in="digit_sum(1234)",
                sample_out="10",
                constraints=(
                    "Use string conversion + a generator expression. "
                    "Don't import anything."
                ),
                signature="def digit_sum(n):",
                tests=[
                    "assert digit_sum(1234) == 10",
                    "assert digit_sum(0) == 0",
                    "assert digit_sum(9) == 9",
                    "assert digit_sum(99999) == 45",
                ],
                uses=["strings (iteration)", "data types (cast)"],
                solution="return sum(int(d) for d in str(n))",
            ),
        ]),
    ],
))
# BUILD-MARKER: numbers-complete


# ---------- Section 6: Logic & Operators ----------
SECTIONS.append(section(
    num=6,
    title="Logic & Operators",
    anchor="logic",
    intro=(
        "Boolean values, comparison, logical (`and`, `or`, `not`), membership (`in`) "
        "and identity (`is`) — the building blocks of every decision your code makes. "
        "Get fluent here and conditionals become trivial."
    ),
    subtopics=[
        subtopic(num=1, title="Boolean & Comparison", anchor="logic-bool", challenges=[
            challenge(
                num=1, title="In Range", difficulty="Easy",
                problem=(
                    "Return `True` if `x` lies inside the inclusive range `[lo, hi]`. "
                    "Use Python's chained comparison."
                ),
                input_fmt="Three numbers `x`, `lo`, `hi` with `lo <= hi`.",
                output_fmt="A `bool`.",
                sample_in="in_range(5, 1, 10)",
                sample_out="True",
                constraints="Use the chained `lo <= x <= hi` form.",
                signature="def in_range(x, lo, hi):",
                tests=[
                    "assert in_range(5, 1, 10) is True",
                    "assert in_range(1, 1, 10) is True",
                    "assert in_range(10, 1, 10) is True",
                    "assert in_range(0, 1, 10) is False",
                    "assert in_range(11, 1, 10) is False",
                ],
                solution="return lo <= x <= hi",
            ),
            challenge(
                num=2, title="Truthy Check", difficulty="Easy",
                problem=(
                    "Return `True` if a value is *truthy* in Python's eyes. Empty "
                    "strings, `0`, `None`, empty lists/dicts/sets are falsy; everything "
                    "else is truthy. The built-in `bool` already does this — your job "
                    "is to use it."
                ),
                input_fmt="Any single `value`.",
                output_fmt="A `bool`.",
                sample_in='is_truthy("hello")',
                sample_out="True",
                constraints="Single expression.",
                signature="def is_truthy(value):",
                tests=[
                    'assert is_truthy("hello") is True',
                    "assert is_truthy(0) is False",
                    "assert is_truthy([]) is False",
                    "assert is_truthy([0]) is True",
                    "assert is_truthy(None) is False",
                ],
                solution="return bool(value)",
            ),
            challenge(
                num=3, title="Three-Way Compare", difficulty="Medium",
                problem=(
                    "Compare two numbers and return `-1` if `a < b`, `0` if `a == b`, "
                    "`+1` if `a > b`. The classic 'cmp' function — useful for sorting."
                ),
                input_fmt="Two numbers `a`, `b`.",
                output_fmt="`-1`, `0`, or `1`.",
                sample_in="cmp(3, 5)",
                sample_out="-1",
                constraints="No imports. Use comparisons + inline `if`/`elif`.",
                signature="def cmp(a, b):",
                tests=[
                    "assert cmp(3, 5) == -1",
                    "assert cmp(5, 3) == 1",
                    "assert cmp(4, 4) == 0",
                    "assert cmp(-1, 1) == -1",
                ],
                uses=["logic (comparison)"],
                solution=(
                    "if a < b:\n    return -1\n"
                    "if a > b:\n    return 1\n"
                    "return 0"
                ),
            ),
        ]),
        subtopic(num=2, title="Logical Operators", anchor="logic-logical", challenges=[
            challenge(
                num=1, title="All Three Positive", difficulty="Easy",
                problem="Return `True` only when **all three** numbers are strictly positive.",
                input_fmt="Three numbers `a`, `b`, `c`.",
                output_fmt="A `bool`.",
                sample_in="all_positive(1, 2, 3)",
                sample_out="True",
                constraints="Use `and`.",
                signature="def all_positive(a, b, c):",
                tests=[
                    "assert all_positive(1, 2, 3) is True",
                    "assert all_positive(0, 1, 2) is False",
                    "assert all_positive(-1, 1, 1) is False",
                    "assert all_positive(0.1, 0.1, 0.1) is True",
                ],
                solution="return a > 0 and b > 0 and c > 0",
            ),
            challenge(
                num=2, title="Either Even", difficulty="Easy",
                problem="Return `True` when at least one of the two integers is even.",
                input_fmt="Two integers `a`, `b`.",
                output_fmt="A `bool`.",
                sample_in="either_even(3, 4)",
                sample_out="True",
                constraints="Use `or`.",
                signature="def either_even(a, b):",
                tests=[
                    "assert either_even(3, 4) is True",
                    "assert either_even(4, 4) is True",
                    "assert either_even(3, 5) is False",
                    "assert either_even(0, 1) is True",
                ],
                solution="return a % 2 == 0 or b % 2 == 0",
            ),
            challenge(
                num=3, title="Eligible to Vote", difficulty="Medium",
                problem=(
                    "Return `True` when a person is eligible to vote: at least 18 "
                    "years old **and** a citizen. Two boolean conditions joined by "
                    "`and` — the canonical authorization check."
                ),
                input_fmt="`age` (int), `citizen` (bool).",
                output_fmt="A `bool`.",
                sample_in="can_vote(20, True)",
                sample_out="True",
                constraints="Use `and`.",
                signature="def can_vote(age, citizen):",
                tests=[
                    "assert can_vote(20, True) is True",
                    "assert can_vote(17, True) is False",
                    "assert can_vote(40, False) is False",
                    "assert can_vote(18, True) is True",
                ],
                uses=["logic (and)"],
                solution="return age >= 18 and citizen",
            ),
        ]),
        subtopic(num=3, title="Membership & Identity", anchor="logic-membership", challenges=[
            challenge(
                num=1, title="Letter In Word", difficulty="Easy",
                problem="Return `True` when a single character `letter` appears in `word`.",
                input_fmt="`letter` (str of length 1), `word` (str).",
                output_fmt="A `bool`.",
                sample_in='letter_in("R", "Rishith")',
                sample_out="True",
                constraints="Use the `in` operator.",
                signature="def letter_in(letter, word):",
                tests=[
                    'assert letter_in("R", "Rishith") is True',
                    'assert letter_in("z", "Rishith") is False',
                    'assert letter_in("h", "Rishith") is True',
                    'assert letter_in("a", "") is False',
                ],
                solution="return letter in word",
            ),
            challenge(
                num=2, title="Forbidden Word", difficulty="Easy",
                problem=(
                    "Given a word and a list of forbidden words, return `True` only "
                    "if the word is **not** in the list."
                ),
                input_fmt="`word` (str), `forbidden` (list of str).",
                output_fmt="A `bool`.",
                sample_in='is_allowed("apple", ["banana", "cherry"])',
                sample_out="True",
                constraints="Use `not in`.",
                signature="def is_allowed(word, forbidden):",
                tests=[
                    'assert is_allowed("apple", ["banana", "cherry"]) is True',
                    'assert is_allowed("banana", ["banana", "cherry"]) is False',
                    'assert is_allowed("apple", []) is True',
                ],
                uses=["logic (not in)", "lists"],
                solution="return word not in forbidden",
            ),
            challenge(
                num=3, title="Same Object?", difficulty="Medium",
                problem=(
                    "Return `True` when `a` and `b` refer to the **exact same object** "
                    "in memory (use `is`, not `==`). Two equal lists are *equal* but "
                    "not the *same* object — your function should distinguish them."
                ),
                input_fmt="Two values `a`, `b`.",
                output_fmt="A `bool`.",
                sample_in="x = []; same_object(x, x)",
                sample_out="True",
                constraints="Use the `is` operator.",
                signature="def same_object(a, b):",
                tests=[
                    "x = []",
                    "assert same_object(x, x) is True",
                    "assert same_object([], []) is False",
                    "assert same_object(None, None) is True",
                ],
                uses=["logic (identity)"],
                solution="return a is b",
            ),
            challenge(
                num=4, title="First Truthy", difficulty="Hard",
                problem=(
                    "Given a list of values, return the first **truthy** one (the "
                    "first that `bool(x)` is `True` for). If none exist, return `None`."
                ),
                input_fmt="A list of values.",
                output_fmt="The first truthy value, or `None`.",
                sample_in='first_truthy([0, "", None, "first", "second"])',
                sample_out="'first'",
                constraints=[
                    "Use `next()` and a generator expression.",
                    "Default of `next()` should be `None`.",
                ],
                signature="def first_truthy(values):",
                tests=[
                    'assert first_truthy([0, "", None, "first", "second"]) == "first"',
                    "assert first_truthy([0, 0, 0]) is None",
                    "assert first_truthy([]) is None",
                    "assert first_truthy([False, True]) is True",
                ],
                uses=["logic (truthy)", "lists", "generator expressions"],
                solution="return next((v for v in values if v), None)",
            ),
        ]),
    ],
))
# BUILD-MARKER: logic-complete


# ---------- Section 7: Conditional Statements ----------
SECTIONS.append(section(
    num=7,
    title="Conditional Statements",
    anchor="conditionals",
    intro=(
        "Decisions, decisions: `if`, `elif`, `else`, nested branches, the inline "
        "ternary, and Python 3.10's `match`/`case`. These challenges practise picking "
        "the right tool for the shape of the decision."
    ),
    subtopics=[
        subtopic(num=1, title="if / elif / else", anchor="cond-if", challenges=[
            challenge(
                num=1, title="Pass or Fail", difficulty="Easy",
                problem="Return `'pass'` if a mark is at least 50, otherwise `'fail'`.",
                input_fmt="An integer or float `mark` (0..100).",
                output_fmt="`'pass'` or `'fail'`.",
                sample_in="pass_fail(50)",
                sample_out="'pass'",
                constraints="Single `if`/`else`.",
                signature="def pass_fail(mark):",
                tests=[
                    'assert pass_fail(50) == "pass"',
                    'assert pass_fail(49) == "fail"',
                    'assert pass_fail(100) == "pass"',
                    'assert pass_fail(0) == "fail"',
                ],
                solution=(
                    'if mark >= 50:\n    return "pass"\n'
                    'return "fail"'
                ),
            ),
            challenge(
                num=2, title="Letter Grade", difficulty="Easy",
                problem=(
                    "Convert a numeric mark (0..100) to a letter grade: `A` ≥ 90, "
                    "`B` ≥ 80, `C` ≥ 70, `D` ≥ 60, `F` otherwise."
                ),
                input_fmt="A number `mark` (0..100).",
                output_fmt="One of `'A'`, `'B'`, `'C'`, `'D'`, `'F'`.",
                sample_in="grade(85)",
                sample_out="'B'",
                constraints="Use `if` / `elif` chain — descending thresholds.",
                signature="def grade(mark):",
                tests=[
                    'assert grade(95) == "A"',
                    'assert grade(85) == "B"',
                    'assert grade(75) == "C"',
                    'assert grade(65) == "D"',
                    'assert grade(40) == "F"',
                    'assert grade(90) == "A"',
                ],
                solution=(
                    'if mark >= 90:\n    return "A"\n'
                    'if mark >= 80:\n    return "B"\n'
                    'if mark >= 70:\n    return "C"\n'
                    'if mark >= 60:\n    return "D"\n'
                    'return "F"'
                ),
            ),
            challenge(
                num=3, title="Even or Odd Word", difficulty="Easy",
                problem="Return `'even'` for even integers and `'odd'` for odd ones.",
                input_fmt="An integer `n`.",
                output_fmt="`'even'` or `'odd'`.",
                sample_in="parity(7)",
                sample_out="'odd'",
                constraints="Reuse modulo (§5).",
                signature="def parity(n):",
                tests=[
                    'assert parity(2) == "even"',
                    'assert parity(7) == "odd"',
                    'assert parity(0) == "even"',
                    'assert parity(-3) == "odd"',
                ],
                uses=["numbers (modulo)", "conditionals"],
                solution='return "even" if n % 2 == 0 else "odd"',
            ),
            challenge(
                num=4, title="FizzBuzz One", difficulty="Medium",
                problem=(
                    "Classic FizzBuzz, but for a single number. Return `'FizzBuzz'` if "
                    "`n` is divisible by 15, `'Fizz'` if by 3 only, `'Buzz'` if by 5 "
                    "only, otherwise the number as a string."
                ),
                input_fmt="A positive integer `n`.",
                output_fmt="One of `'FizzBuzz'`, `'Fizz'`, `'Buzz'`, or `str(n)`.",
                sample_in="fizzbuzz_one(15)",
                sample_out="'FizzBuzz'",
                constraints="Order matters — check 15 first.",
                signature="def fizzbuzz_one(n):",
                tests=[
                    'assert fizzbuzz_one(15) == "FizzBuzz"',
                    'assert fizzbuzz_one(9) == "Fizz"',
                    'assert fizzbuzz_one(10) == "Buzz"',
                    'assert fizzbuzz_one(7) == "7"',
                    'assert fizzbuzz_one(30) == "FizzBuzz"',
                ],
                uses=["numbers (modulo)", "conditionals (order)"],
                solution=(
                    'if n % 15 == 0:\n    return "FizzBuzz"\n'
                    'if n % 3 == 0:\n    return "Fizz"\n'
                    'if n % 5 == 0:\n    return "Buzz"\n'
                    "return str(n)"
                ),
            ),
        ]),
        subtopic(num=2, title="Nested & Combined", anchor="cond-nested", challenges=[
            challenge(
                num=1, title="Sign + Magnitude", difficulty="Medium",
                problem=(
                    "Classify a number as one of `'small +'`, `'large +'`, `'small -'`, "
                    "`'large -'`, or `'zero'`. 'Large' means `|n| >= 100`, 'small' "
                    "means `|n| < 100`."
                ),
                input_fmt="A number `n`.",
                output_fmt="One of the five strings.",
                sample_in="classify(50)",
                sample_out="'small +'",
                constraints="Check zero first.",
                signature="def classify(n):",
                tests=[
                    'assert classify(0) == "zero"',
                    'assert classify(50) == "small +"',
                    'assert classify(150) == "large +"',
                    'assert classify(-50) == "small -"',
                    'assert classify(-150) == "large -"',
                ],
                uses=["conditionals", "logic", "numbers (abs)"],
                solution=(
                    'if n == 0:\n    return "zero"\n'
                    'sign = "+" if n > 0 else "-"\n'
                    'size = "large" if abs(n) >= 100 else "small"\n'
                    'return f"{size} {sign}"'
                ),
            ),
            challenge(
                num=2, title="Leap Year", difficulty="Medium",
                problem=(
                    "A year is a leap year if it is divisible by 4 — *unless* it is "
                    "also divisible by 100, in which case it must also be divisible by "
                    "400. Return `True` for leap years, `False` otherwise."
                ),
                input_fmt="A positive integer `year`.",
                output_fmt="A `bool`.",
                sample_in="is_leap(2000)",
                sample_out="True",
                constraints="One return statement preferred.",
                signature="def is_leap(year):",
                tests=[
                    "assert is_leap(2000) is True",
                    "assert is_leap(1900) is False",
                    "assert is_leap(2024) is True",
                    "assert is_leap(2023) is False",
                    "assert is_leap(2100) is False",
                ],
                uses=["logic", "numbers (modulo)"],
                solution="return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)",
            ),
            challenge(
                num=3, title="Triangle Type", difficulty="Hard",
                problem=(
                    "Given three positive side lengths, return the triangle type: "
                    "`'equilateral'` (all sides equal), `'isosceles'` (exactly two "
                    "equal), `'scalene'` (all different), or `'invalid'` if the sides "
                    "can't form a triangle (the sum of any two sides must exceed the "
                    "third)."
                ),
                input_fmt="Three positive numbers `a`, `b`, `c`.",
                output_fmt="One of the four strings.",
                sample_in="triangle_type(3, 3, 3)",
                sample_out="'equilateral'",
                constraints="Check validity first.",
                signature="def triangle_type(a, b, c):",
                tests=[
                    'assert triangle_type(3, 3, 3) == "equilateral"',
                    'assert triangle_type(3, 3, 5) == "isosceles"',
                    'assert triangle_type(3, 4, 5) == "scalene"',
                    'assert triangle_type(1, 2, 3) == "invalid"',
                    'assert triangle_type(5, 5, 1) == "isosceles"',
                ],
                uses=["conditionals (nested)", "logic", "sets (uniqueness)"],
                solution=(
                    'if a + b <= c or a + c <= b or b + c <= a:\n    return "invalid"\n'
                    "uniq = len({a, b, c})\n"
                    'if uniq == 1:\n    return "equilateral"\n'
                    'if uniq == 2:\n    return "isosceles"\n'
                    'return "scalene"'
                ),
            ),
        ]),
        subtopic(num=3, title="Inline if (Ternary)", anchor="cond-ternary", challenges=[
            challenge(
                num=1, title="Max of Two", difficulty="Easy",
                problem="Return the larger of two numbers using a single ternary expression.",
                input_fmt="Two numbers `a`, `b`.",
                output_fmt="The larger one.",
                sample_in="max_of_two(3, 7)",
                sample_out="7",
                constraints="One-line ternary. Don't use `max()`.",
                signature="def max_of_two(a, b):",
                tests=[
                    "assert max_of_two(3, 7) == 7",
                    "assert max_of_two(7, 3) == 7",
                    "assert max_of_two(5, 5) == 5",
                    "assert max_of_two(-1, -2) == -1",
                ],
                solution="return a if a >= b else b",
            ),
            challenge(
                num=2, title="Sign Word", difficulty="Easy",
                problem=(
                    "Return `'positive'`, `'negative'`, or `'zero'` for a number. "
                    "Use a chained ternary (or two `if`s)."
                ),
                input_fmt="A number `n`.",
                output_fmt="One of three strings.",
                sample_in="sign_word(-3)",
                sample_out="'negative'",
                constraints="No imports.",
                signature="def sign_word(n):",
                tests=[
                    'assert sign_word(5) == "positive"',
                    'assert sign_word(-3) == "negative"',
                    'assert sign_word(0) == "zero"',
                ],
                solution=(
                    'return "positive" if n > 0 else "negative" if n < 0 else "zero"'
                ),
            ),
        ]),
        subtopic(num=4, title="match / case", anchor="cond-match", challenges=[
            challenge(
                num=1, title="HTTP Status", difficulty="Easy",
                problem=(
                    "Convert an HTTP status code to its short name: `200` → `'OK'`, "
                    "`404` → `'Not Found'`, `500` → `'Server Error'`, anything else → "
                    "`'Unknown'`. Use a `match`/`case`."
                ),
                input_fmt="An integer `code`.",
                output_fmt="The status name string.",
                sample_in="http_status(404)",
                sample_out="'Not Found'",
                constraints="Use `match`/`case`. Wildcard `_` for unknown.",
                signature="def http_status(code):",
                tests=[
                    'assert http_status(200) == "OK"',
                    'assert http_status(404) == "Not Found"',
                    'assert http_status(500) == "Server Error"',
                    'assert http_status(418) == "Unknown"',
                ],
                solution=(
                    "match code:\n"
                    '    case 200:\n        return "OK"\n'
                    '    case 404:\n        return "Not Found"\n'
                    '    case 500:\n        return "Server Error"\n'
                    '    case _:\n        return "Unknown"'
                ),
            ),
            challenge(
                num=2, title="Day Name", difficulty="Easy",
                problem=(
                    "Convert a weekday number (1=Monday … 7=Sunday) to its full name. "
                    "Anything outside 1..7 returns `'Invalid'`."
                ),
                input_fmt="An integer `n`.",
                output_fmt="The day name or `'Invalid'`.",
                sample_in="day_name(3)",
                sample_out="'Wednesday'",
                constraints="Use `match`/`case`.",
                signature="def day_name(n):",
                tests=[
                    'assert day_name(1) == "Monday"',
                    'assert day_name(3) == "Wednesday"',
                    'assert day_name(7) == "Sunday"',
                    'assert day_name(0) == "Invalid"',
                    'assert day_name(8) == "Invalid"',
                ],
                solution=(
                    "match n:\n"
                    '    case 1: return "Monday"\n'
                    '    case 2: return "Tuesday"\n'
                    '    case 3: return "Wednesday"\n'
                    '    case 4: return "Thursday"\n'
                    '    case 5: return "Friday"\n'
                    '    case 6: return "Saturday"\n'
                    '    case 7: return "Sunday"\n'
                    '    case _: return "Invalid"'
                ),
            ),
            challenge(
                num=3, title="Number Bucket", difficulty="Medium",
                problem=(
                    "Classify an integer using `match`/`case` with **guards**: "
                    "`'negative'` if `< 0`, `'zero'` if `0`, `'small'` if `1..9`, "
                    "`'medium'` if `10..99`, `'large'` if `>= 100`."
                ),
                input_fmt="An integer `n`.",
                output_fmt="One of five bucket strings.",
                sample_in="bucket(50)",
                sample_out="'medium'",
                constraints="Use `match`/`case` with `if` guards (e.g. `case x if x > 0`).",
                signature="def bucket(n):",
                tests=[
                    'assert bucket(-5) == "negative"',
                    'assert bucket(0) == "zero"',
                    'assert bucket(7) == "small"',
                    'assert bucket(50) == "medium"',
                    'assert bucket(1000) == "large"',
                ],
                uses=["conditionals (match guards)", "logic"],
                solution=(
                    "match n:\n"
                    '    case x if x < 0: return "negative"\n'
                    '    case 0: return "zero"\n'
                    '    case x if x < 10: return "small"\n'
                    '    case x if x < 100: return "medium"\n'
                    '    case _: return "large"'
                ),
            ),
        ]),
    ],
))
# BUILD-MARKER: conditionals-complete


# ---------- Section 8: For Loops ----------
SECTIONS.append(section(
    num=8,
    title="For Loops",
    anchor="for-loops",
    intro=(
        "`for` walks over any iterable — strings, lists, ranges, dict keys. These "
        "challenges drill iteration, the loop-control trio (`break`/`continue`/`pass`), "
        "the under-used `for / else`, and nested loops for grid / matrix work."
    ),
    subtopics=[
        subtopic(num=1, title="For Loop Basics", anchor="for-basics", challenges=[
            challenge(
                num=1, title="Sum a List", difficulty="Easy",
                problem="Return the sum of all numbers in a list, computed with a `for` loop.",
                input_fmt="A list of numbers `nums`.",
                output_fmt="The total.",
                sample_in="sum_list([1, 2, 3, 4])",
                sample_out="10",
                constraints="Implement with a `for` loop. Don't use `sum()`.",
                signature="def sum_list(nums):",
                tests=[
                    "assert sum_list([1, 2, 3, 4]) == 10",
                    "assert sum_list([]) == 0",
                    "assert sum_list([-1, 1]) == 0",
                    "assert sum_list([5]) == 5",
                ],
                solution=(
                    "total = 0\n"
                    "for n in nums:\n"
                    "    total += n\n"
                    "return total"
                ),
            ),
            challenge(
                num=2, title="Count Vowels", difficulty="Easy",
                problem=(
                    "Count the vowels (`a, e, i, o, u`, case-insensitive) in a string "
                    "using a `for` loop and an `in` check."
                ),
                input_fmt="A string `s`.",
                output_fmt="An integer count.",
                sample_in='count_vowels("Rishith")',
                sample_out="2",
                constraints="Use a `for` loop.",
                signature="def count_vowels(s):",
                tests=[
                    'assert count_vowels("Rishith") == 2',
                    'assert count_vowels("xyz") == 0',
                    'assert count_vowels("") == 0',
                    'assert count_vowels("AEIOU") == 5',
                ],
                uses=["strings", "for loop"],
                solution=(
                    "count = 0\n"
                    "for ch in s.lower():\n"
                    '    if ch in "aeiou":\n'
                    "        count += 1\n"
                    "return count"
                ),
            ),
            challenge(
                num=3, title="Repeat Each Char", difficulty="Easy",
                problem=(
                    "Return a new string where each character of the input is repeated "
                    "twice. Example: `'abc'` → `'aabbcc'`."
                ),
                input_fmt="A string `s`.",
                output_fmt="The doubled-character string.",
                sample_in='repeat_each("abc")',
                sample_out="'aabbcc'",
                constraints="Use a `for` loop and string concatenation.",
                signature="def repeat_each(s):",
                tests=[
                    'assert repeat_each("abc") == "aabbcc"',
                    'assert repeat_each("") == ""',
                    'assert repeat_each("x") == "xx"',
                    'assert repeat_each("Hi") == "HHii"',
                ],
                uses=["strings", "for loop"],
                solution=(
                    'out = ""\n'
                    "for ch in s:\n"
                    "    out += ch * 2\n"
                    "return out"
                ),
            ),
            challenge(
                num=4, title="Cumulative Sums", difficulty="Medium",
                problem=(
                    "Given a list of numbers, return a list of running totals. "
                    "Example: `[1, 2, 3]` → `[1, 3, 6]`. The first element is itself; "
                    "every subsequent element is the previous total plus the current "
                    "value."
                ),
                input_fmt="A list of numbers `nums`.",
                output_fmt="A list of cumulative sums (same length).",
                sample_in="cumulative([1, 2, 3])",
                sample_out="[1, 3, 6]",
                constraints="Use a `for` loop. Empty input → empty list.",
                signature="def cumulative(nums):",
                tests=[
                    "assert cumulative([1, 2, 3]) == [1, 3, 6]",
                    "assert cumulative([]) == []",
                    "assert cumulative([5]) == [5]",
                    "assert cumulative([1, -1, 1]) == [1, 0, 1]",
                ],
                uses=["lists", "for loop"],
                solution=(
                    "totals = []\n"
                    "running = 0\n"
                    "for n in nums:\n"
                    "    running += n\n"
                    "    totals.append(running)\n"
                    "return totals"
                ),
            ),
        ]),
        subtopic(num=2, title="break / continue / pass", anchor="for-control", challenges=[
            challenge(
                num=1, title="First Negative", difficulty="Easy",
                problem=(
                    "Return the first negative number in a list, or `None` if there "
                    "are no negatives. Use `break` to stop the loop early."
                ),
                input_fmt="A list of numbers.",
                output_fmt="The first negative, or `None`.",
                sample_in="first_negative([1, 2, -3, -4])",
                sample_out="-3",
                constraints="Use `break`.",
                signature="def first_negative(nums):",
                tests=[
                    "assert first_negative([1, 2, -3, -4]) == -3",
                    "assert first_negative([1, 2, 3]) is None",
                    "assert first_negative([]) is None",
                    "assert first_negative([-1]) == -1",
                ],
                uses=["lists", "for loop", "break"],
                solution=(
                    "for n in nums:\n"
                    "    if n < 0:\n"
                    "        return n\n"
                    "return None"
                ),
            ),
            challenge(
                num=2, title="Skip Threes", difficulty="Easy",
                problem=(
                    "Sum the integers from `1` to `n` (inclusive) **except** multiples "
                    "of 3. Use `continue` to skip them."
                ),
                input_fmt="An integer `n` ≥ 0.",
                output_fmt="The sum.",
                sample_in="skip_threes(10)",
                sample_out="37",
                constraints="Use `range`, a `for` loop, and `continue`.",
                signature="def skip_threes(n):",
                tests=[
                    "assert skip_threes(10) == 37",
                    "assert skip_threes(3) == 3",
                    "assert skip_threes(0) == 0",
                    "assert skip_threes(1) == 1",
                ],
                uses=["numbers (modulo)", "for loop", "continue"],
                solution=(
                    "total = 0\n"
                    "for i in range(1, n + 1):\n"
                    "    if i % 3 == 0:\n"
                    "        continue\n"
                    "    total += i\n"
                    "return total"
                ),
            ),
            challenge(
                num=3, title="Index of First Match", difficulty="Medium",
                problem=(
                    "Return the index of the first element equal to `target`, or `-1` "
                    "if not found. Don't use `.index()` — write the loop yourself with "
                    "`enumerate` and `break`."
                ),
                input_fmt="A list `items` and a `target` value.",
                output_fmt="An integer index or `-1`.",
                sample_in='find("c", ["a", "b", "c", "d"])',
                sample_out="2",
                constraints="Use `enumerate` + `break`. Don't use `.index()`.",
                signature="def find(target, items):",
                tests=[
                    'assert find("c", ["a", "b", "c", "d"]) == 2',
                    'assert find("z", ["a", "b", "c"]) == -1',
                    "assert find(3, [1, 2, 3, 3]) == 2",
                    "assert find(1, []) == -1",
                ],
                uses=["lists", "enumerate", "for loop", "break"],
                solution=(
                    "for i, item in enumerate(items):\n"
                    "    if item == target:\n"
                    "        return i\n"
                    "return -1"
                ),
            ),
        ]),
        subtopic(num=3, title="for / else", anchor="for-else", challenges=[
            challenge(
                num=1, title="No Negatives", difficulty="Medium",
                problem=(
                    "Return `True` only if **none** of the numbers are negative. Use "
                    "the `for / else` pattern: `break` when you find a negative; the "
                    "`else` branch runs only if the loop completed without `break`."
                ),
                input_fmt="A list of numbers `nums`.",
                output_fmt="A `bool`.",
                sample_in="no_negatives([1, 2, 3])",
                sample_out="True",
                constraints="Use `for`/`else`. Don't use `all()`.",
                signature="def no_negatives(nums):",
                tests=[
                    "assert no_negatives([1, 2, 3]) is True",
                    "assert no_negatives([1, -2, 3]) is False",
                    "assert no_negatives([]) is True",
                    "assert no_negatives([0]) is True",
                ],
                uses=["lists", "for/else", "break"],
                solution=(
                    "for n in nums:\n"
                    "    if n < 0:\n"
                    "        break\n"
                    "else:\n"
                    "    return True\n"
                    "return False"
                ),
            ),
            challenge(
                num=2, title="Smallest Factor", difficulty="Medium",
                problem=(
                    "Return the smallest factor of `n` greater than 1, or `n` itself if "
                    "`n` is prime. Use `for / else` — break on the first factor; the "
                    "`else` branch fires only when no factor is found."
                ),
                input_fmt="An integer `n` ≥ 2.",
                output_fmt="An integer factor (or `n` if prime).",
                sample_in="smallest_factor(15)",
                sample_out="3",
                constraints="Use `range(2, n)`, `for`/`else`, `break`.",
                signature="def smallest_factor(n):",
                tests=[
                    "assert smallest_factor(15) == 3",
                    "assert smallest_factor(7) == 7",
                    "assert smallest_factor(2) == 2",
                    "assert smallest_factor(49) == 7",
                ],
                uses=["numbers (modulo)", "for/else", "break"],
                solution=(
                    "for i in range(2, n):\n"
                    "    if n % i == 0:\n"
                    "        return i\n"
                    "else:\n"
                    "    return n"
                ),
            ),
        ]),
        subtopic(num=4, title="Nested Loops", anchor="for-nested", challenges=[
            challenge(
                num=1, title="Multiplication Table", difficulty="Easy",
                problem=(
                    "Return an `n × n` multiplication table as a list of lists. "
                    "`table(3)` should give `[[1,2,3],[2,4,6],[3,6,9]]`."
                ),
                input_fmt="A positive integer `n`.",
                output_fmt="A list of `n` lists, each with `n` integers.",
                sample_in="table(3)",
                sample_out="[[1, 2, 3], [2, 4, 6], [3, 6, 9]]",
                constraints="Two nested `for` loops.",
                signature="def table(n):",
                tests=[
                    "assert table(1) == [[1]]",
                    "assert table(3) == [[1, 2, 3], [2, 4, 6], [3, 6, 9]]",
                    "assert table(2) == [[1, 2], [2, 4]]",
                ],
                uses=["lists (nested)", "for loop"],
                solution=(
                    "rows = []\n"
                    "for i in range(1, n + 1):\n"
                    "    row = []\n"
                    "    for j in range(1, n + 1):\n"
                    "        row.append(i * j)\n"
                    "    rows.append(row)\n"
                    "return rows"
                ),
            ),
            challenge(
                num=2, title="Matrix Sum", difficulty="Medium",
                problem=(
                    "Sum every value in a 2D list (matrix) using nested `for` loops."
                ),
                input_fmt="A list of lists of numbers `m`.",
                output_fmt="The total sum.",
                sample_in="matrix_sum([[1, 2], [3, 4]])",
                sample_out="10",
                constraints="Two nested `for` loops.",
                signature="def matrix_sum(m):",
                tests=[
                    "assert matrix_sum([[1, 2], [3, 4]]) == 10",
                    "assert matrix_sum([]) == 0",
                    "assert matrix_sum([[5]]) == 5",
                    "assert matrix_sum([[1, 1, 1], [1, 1, 1]]) == 6",
                ],
                uses=["lists (nested)", "for loop"],
                solution=(
                    "total = 0\n"
                    "for row in m:\n"
                    "    for value in row:\n"
                    "        total += value\n"
                    "return total"
                ),
            ),
            challenge(
                num=3, title="Right Triangle Pattern", difficulty="Hard",
                problem=(
                    "Return a string of `n` lines forming a right-angled triangle of "
                    "stars: line `k` (1-indexed) has `k` stars. Lines joined by `\\n`. "
                    "Example for `n=3`:\n```\n*\n**\n***\n```"
                ),
                input_fmt="A positive integer `n`.",
                output_fmt="A multiline string of `*` characters.",
                sample_in="triangle(3)",
                sample_out="'*\\n**\\n***'",
                constraints="Use a `for` loop and string repetition.",
                signature="def triangle(n):",
                tests=[
                    'assert triangle(1) == "*"',
                    'assert triangle(3) == "*\\n**\\n***"',
                    'assert triangle(5) == "*\\n**\\n***\\n****\\n*****"',
                ],
                uses=["strings (repetition, join)", "for loop", "lists"],
                solution=(
                    'lines = ["*" * i for i in range(1, n + 1)]\n'
                    'return "\\n".join(lines)'
                ),
            ),
        ]),
    ],
))
# BUILD-MARKER: for-loops-complete


# ---------- Section 9: While Loops ----------
SECTIONS.append(section(
    num=9,
    title="While Loops",
    anchor="while-loops",
    intro=(
        "Use `while` when you don't know up front how many iterations you'll need — "
        "you keep going until a condition flips. These challenges practise both "
        "condition-driven loops and the `while True` + `break` pattern."
    ),
    subtopics=[
        subtopic(num=1, title="while <condition>", anchor="while-cond", challenges=[
            challenge(
                num=1, title="Countdown", difficulty="Easy",
                problem=(
                    "Return a list counting down from `n` to `0` inclusive. Use a "
                    "`while` loop."
                ),
                input_fmt="A non-negative integer `n`.",
                output_fmt="A list `[n, n-1, ..., 0]`.",
                sample_in="countdown(3)",
                sample_out="[3, 2, 1, 0]",
                constraints="Use `while`, not `for`.",
                signature="def countdown(n):",
                tests=[
                    "assert countdown(3) == [3, 2, 1, 0]",
                    "assert countdown(0) == [0]",
                    "assert countdown(1) == [1, 0]",
                ],
                uses=["lists", "while loop"],
                solution=(
                    "out = []\n"
                    "while n >= 0:\n"
                    "    out.append(n)\n"
                    "    n -= 1\n"
                    "return out"
                ),
            ),
            challenge(
                num=2, title="Sum to N (while)", difficulty="Easy",
                problem="Return the sum `1 + 2 + … + n`, computed with a `while` loop.",
                input_fmt="A non-negative integer `n`.",
                output_fmt="The sum.",
                sample_in="sum_to(5)",
                sample_out="15",
                constraints="Use `while`. `n == 0` returns `0`.",
                signature="def sum_to(n):",
                tests=[
                    "assert sum_to(5) == 15",
                    "assert sum_to(0) == 0",
                    "assert sum_to(1) == 1",
                    "assert sum_to(100) == 5050",
                ],
                solution=(
                    "total = 0\n"
                    "i = 1\n"
                    "while i <= n:\n"
                    "    total += i\n"
                    "    i += 1\n"
                    "return total"
                ),
            ),
            challenge(
                num=3, title="Largest Power of Two ≤ N", difficulty="Medium",
                problem=(
                    "Return the largest power of two that does **not** exceed `n`. "
                    "Example: `n=10` → `8`. `n=1` → `1`. Multiply by 2 in a `while` "
                    "loop."
                ),
                input_fmt="A positive integer `n` (≥ 1).",
                output_fmt="The largest `2^k` ≤ `n`.",
                sample_in="largest_pow2(10)",
                sample_out="8",
                constraints="Use `while`.",
                signature="def largest_pow2(n):",
                tests=[
                    "assert largest_pow2(10) == 8",
                    "assert largest_pow2(1) == 1",
                    "assert largest_pow2(16) == 16",
                    "assert largest_pow2(63) == 32",
                    "assert largest_pow2(100) == 64",
                ],
                uses=["numbers", "while loop"],
                solution=(
                    "p = 1\n"
                    "while p * 2 <= n:\n"
                    "    p *= 2\n"
                    "return p"
                ),
            ),
            challenge(
                num=4, title="Halve Until 1", difficulty="Medium",
                problem=(
                    "Count how many times you must integer-halve `n` (using `// 2`) "
                    "before reaching 1 or 0. Example: `n=8` halves to `4 → 2 → 1` so "
                    "answer is `3`."
                ),
                input_fmt="A positive integer `n`.",
                output_fmt="The number of halvings.",
                sample_in="halve_until_one(8)",
                sample_out="3",
                constraints="Use `while`.",
                signature="def halve_until_one(n):",
                tests=[
                    "assert halve_until_one(8) == 3",
                    "assert halve_until_one(1) == 0",
                    "assert halve_until_one(2) == 1",
                    "assert halve_until_one(1024) == 10",
                ],
                uses=["numbers", "while loop"],
                solution=(
                    "count = 0\n"
                    "while n > 1:\n"
                    "    n //= 2\n"
                    "    count += 1\n"
                    "return count"
                ),
            ),
        ]),
        subtopic(num=2, title="while True + break", anchor="while-true", challenges=[
            challenge(
                num=1, title="First Over Threshold", difficulty="Easy",
                problem=(
                    "Given a list and a threshold, return the first value strictly "
                    "greater than the threshold, or `None` if none. Use `while True` "
                    "and an index counter — break out when found or when the list runs "
                    "out."
                ),
                input_fmt="A list of numbers `nums`, a number `threshold`.",
                output_fmt="The first qualifying value or `None`.",
                sample_in="first_over([1, 2, 5, 8], 4)",
                sample_out="5",
                constraints="Use `while True` + `break`. Don't use `for`.",
                signature="def first_over(nums, threshold):",
                tests=[
                    "assert first_over([1, 2, 5, 8], 4) == 5",
                    "assert first_over([1, 2, 3], 10) is None",
                    "assert first_over([], 0) is None",
                    "assert first_over([10], 5) == 10",
                ],
                uses=["lists", "while True", "break"],
                solution=(
                    "i = 0\n"
                    "while True:\n"
                    "    if i >= len(nums):\n"
                    "        return None\n"
                    "    if nums[i] > threshold:\n"
                    "        return nums[i]\n"
                    "    i += 1"
                ),
            ),
            challenge(
                num=2, title="Sentinel Sum", difficulty="Medium",
                problem=(
                    "Process a list of integers in order; sum them up but **stop as "
                    "soon as you see `0`** (the 'sentinel'). Don't include the sentinel "
                    "in the sum. Use `while True` + `break`."
                ),
                input_fmt="A list of integers `nums`.",
                output_fmt="The sum of values seen before the first 0.",
                sample_in="sentinel_sum([3, 5, 0, 100])",
                sample_out="8",
                constraints="Use `while True` + `break`.",
                signature="def sentinel_sum(nums):",
                tests=[
                    "assert sentinel_sum([3, 5, 0, 100]) == 8",
                    "assert sentinel_sum([0]) == 0",
                    "assert sentinel_sum([1, 2, 3]) == 6  # no sentinel = sum all",
                    "assert sentinel_sum([]) == 0",
                ],
                uses=["lists", "while True", "break"],
                solution=(
                    "total = 0\n"
                    "i = 0\n"
                    "while True:\n"
                    "    if i >= len(nums) or nums[i] == 0:\n"
                    "        return total\n"
                    "    total += nums[i]\n"
                    "    i += 1"
                ),
            ),
        ]),
        subtopic(num=3, title="for vs while", anchor="while-vs-for", challenges=[
            challenge(
                num=1, title="Same Sum Two Ways", difficulty="Easy",
                problem=(
                    "Return a tuple `(for_sum, while_sum)` that sums `1..n` two ways "
                    "— the first using a `for` loop, the second using a `while` loop. "
                    "Both must give the same answer; the test cell verifies that."
                ),
                input_fmt="A non-negative integer `n`.",
                output_fmt="A 2-tuple of identical integers.",
                sample_in="same_sum(5)",
                sample_out="(15, 15)",
                constraints="Implement both loops yourself; don't call `sum()`.",
                signature="def same_sum(n):",
                tests=[
                    "assert same_sum(5) == (15, 15)",
                    "assert same_sum(0) == (0, 0)",
                    "assert same_sum(10) == (55, 55)",
                ],
                uses=["for loop", "while loop"],
                solution=(
                    "f = 0\n"
                    "for i in range(1, n + 1):\n"
                    "    f += i\n"
                    "w = 0\n"
                    "j = 1\n"
                    "while j <= n:\n"
                    "    w += j\n"
                    "    j += 1\n"
                    "return f, w"
                ),
            ),
            challenge(
                num=2, title="LCM of Two", difficulty="Hard",
                problem=(
                    "Return the **least common multiple** of two positive integers — "
                    "the smallest number that both divide. Use a `while` loop that "
                    "starts at the larger of the two and increments by it until it's "
                    "also divisible by the other."
                ),
                input_fmt="Two positive integers `a`, `b`.",
                output_fmt="The LCM as an integer.",
                sample_in="lcm(4, 6)",
                sample_out="12",
                constraints=(
                    "Use a `while` loop with the increment trick. Don't import `math`."
                ),
                signature="def lcm(a, b):",
                tests=[
                    "assert lcm(4, 6) == 12",
                    "assert lcm(3, 5) == 15",
                    "assert lcm(7, 7) == 7",
                    "assert lcm(1, 100) == 100",
                ],
                uses=["numbers (modulo)", "while loop", "logic"],
                solution=(
                    "hi, lo = (a, b) if a >= b else (b, a)\n"
                    "candidate = hi\n"
                    "while candidate % lo != 0:\n"
                    "    candidate += hi\n"
                    "return candidate"
                ),
            ),
        ]),
    ],
))
# BUILD-MARKER: while-loops-complete


# ---------- Section 10: Lists – Fundamentals ----------
SECTIONS.append(section(
    num=10,
    title="Lists – Fundamentals",
    anchor="lists-fundamentals",
    intro=(
        "Lists are the most-used data structure in Python. These challenges cover "
        "indexing, slicing, mutation (add / remove / update), sorting, reversing, and "
        "the core analysis helpers (`len`, `count`, `index`, `all`, `any`)."
    ),
    subtopics=[
        subtopic(num=1, title="Indexing & Slicing", anchor="lists-slicing", challenges=[
            challenge(
                num=1, title="First Three", difficulty="Easy",
                problem="Return the first three elements of a list (fewer if the list is shorter).",
                input_fmt="A list `items`.",
                output_fmt="A list of at most three elements.",
                sample_in="first_three([1, 2, 3, 4, 5])",
                sample_out="[1, 2, 3]",
                constraints="Use slicing.",
                signature="def first_three(items):",
                tests=[
                    "assert first_three([1, 2, 3, 4, 5]) == [1, 2, 3]",
                    "assert first_three([1]) == [1]",
                    "assert first_three([]) == []",
                    "assert first_three([1, 2, 3]) == [1, 2, 3]",
                ],
                solution="return items[:3]",
            ),
            challenge(
                num=2, title="Last Two", difficulty="Easy",
                problem="Return the last two elements of a list (fewer if shorter).",
                input_fmt="A list `items`.",
                output_fmt="A list of at most two elements.",
                sample_in="last_two([10, 20, 30, 40])",
                sample_out="[30, 40]",
                constraints="Negative slicing.",
                signature="def last_two(items):",
                tests=[
                    "assert last_two([10, 20, 30, 40]) == [30, 40]",
                    "assert last_two([1]) == [1]",
                    "assert last_two([]) == []",
                ],
                solution="return items[-2:]",
            ),
            challenge(
                num=3, title="Reverse a List", difficulty="Easy",
                problem=(
                    "Return a new list in reverse order. Don't mutate the original — "
                    "use slicing."
                ),
                input_fmt="A list `items`.",
                output_fmt="The reversed list.",
                sample_in="reverse_list([1, 2, 3])",
                sample_out="[3, 2, 1]",
                constraints="Use `[::-1]`. Don't use `.reverse()`.",
                signature="def reverse_list(items):",
                tests=[
                    "assert reverse_list([1, 2, 3]) == [3, 2, 1]",
                    "assert reverse_list([]) == []",
                    "assert reverse_list([1]) == [1]",
                    "xs = [1, 2, 3]; _ = reverse_list(xs); assert xs == [1, 2, 3]",
                ],
                solution="return items[::-1]",
            ),
        ]),
        subtopic(num=2, title="Add / Remove / Update", anchor="lists-mutate", challenges=[
            challenge(
                num=1, title="Append and Return", difficulty="Easy",
                problem=(
                    "Append a value to a list and return the updated list. A one-liner "
                    "wrapper around `.append`."
                ),
                input_fmt="A list `items` and a value `value`.",
                output_fmt="The same list with `value` appended.",
                sample_in='append_value([1, 2], 3)',
                sample_out="[1, 2, 3]",
                constraints="Use `.append`.",
                signature="def append_value(items, value):",
                tests=[
                    "assert append_value([1, 2], 3) == [1, 2, 3]",
                    "assert append_value([], 5) == [5]",
                ],
                solution="items.append(value)\nreturn items",
            ),
            challenge(
                num=2, title="Insert at Index", difficulty="Easy",
                problem=(
                    "Insert a value at the given index and return the list. Use "
                    "`.insert`."
                ),
                input_fmt="A list, an integer `index`, a value.",
                output_fmt="The updated list.",
                sample_in='insert_at([1, 3], 1, 2)',
                sample_out="[1, 2, 3]",
                constraints="Use `.insert`.",
                signature="def insert_at(items, index, value):",
                tests=[
                    "assert insert_at([1, 3], 1, 2) == [1, 2, 3]",
                    "assert insert_at([], 0, 99) == [99]",
                    "assert insert_at([1, 2], 100, 3) == [1, 2, 3]",
                ],
                solution="items.insert(index, value)\nreturn items",
            ),
            challenge(
                num=3, title="Remove First Equal", difficulty="Medium",
                problem=(
                    "Remove the first occurrence of `target` from the list and return "
                    "the list. If `target` is absent, return the list unchanged."
                ),
                input_fmt="A list `items` and a value `target`.",
                output_fmt="The updated list.",
                sample_in='remove_first([1, 2, 3, 2], 2)',
                sample_out="[1, 3, 2]",
                constraints=(
                    "Use `.remove` inside `try`/`except ValueError` — absent target must "
                    "not raise."
                ),
                signature="def remove_first(items, target):",
                tests=[
                    "assert remove_first([1, 2, 3, 2], 2) == [1, 3, 2]",
                    "assert remove_first([1, 2, 3], 99) == [1, 2, 3]",
                    "assert remove_first([], 1) == []",
                ],
                uses=["lists", "exceptions"],
                solution=(
                    "try:\n"
                    "    items.remove(target)\n"
                    "except ValueError:\n"
                    "    pass\n"
                    "return items"
                ),
            ),
            challenge(
                num=4, title="Double In Place", difficulty="Medium",
                problem=(
                    "Multiply every element of the list by 2, **in place** (modify the "
                    "original). Return the same list object."
                ),
                input_fmt="A list of numbers.",
                output_fmt="The same list with each element doubled.",
                sample_in="double_in_place([1, 2, 3])",
                sample_out="[2, 4, 6]",
                constraints=(
                    "Must mutate the input list. The test cell verifies object identity."
                ),
                signature="def double_in_place(items):",
                tests=[
                    "xs = [1, 2, 3]",
                    "result = double_in_place(xs)",
                    "assert result is xs",
                    "assert xs == [2, 4, 6]",
                    "assert double_in_place([]) == []",
                ],
                uses=["lists (mutation)", "for loop"],
                solution=(
                    "for i in range(len(items)):\n"
                    "    items[i] *= 2\n"
                    "return items"
                ),
            ),
        ]),
        subtopic(num=3, title="Analysis", anchor="lists-analyze", challenges=[
            challenge(
                num=1, title="Count Occurrences", difficulty="Easy",
                problem="Return how many times `value` appears in the list.",
                input_fmt="A list `items`, a value `value`.",
                output_fmt="An integer count.",
                sample_in='count_occurrences([1, 2, 2, 3, 2], 2)',
                sample_out="3",
                constraints="Use `.count`.",
                signature="def count_occurrences(items, value):",
                tests=[
                    "assert count_occurrences([1, 2, 2, 3, 2], 2) == 3",
                    "assert count_occurrences([1, 2, 3], 99) == 0",
                    "assert count_occurrences([], 1) == 0",
                ],
                solution="return items.count(value)",
            ),
            challenge(
                num=2, title="All Positive", difficulty="Easy",
                problem=(
                    "Return `True` when every element of the list is strictly "
                    "positive. Empty list → `True` (vacuously)."
                ),
                input_fmt="A list of numbers.",
                output_fmt="A `bool`.",
                sample_in="all_positive_list([1, 2, 3])",
                sample_out="True",
                constraints="Use `all()` with a generator expression.",
                signature="def all_positive_list(nums):",
                tests=[
                    "assert all_positive_list([1, 2, 3]) is True",
                    "assert all_positive_list([]) is True",
                    "assert all_positive_list([1, 0, 2]) is False",
                    "assert all_positive_list([-1]) is False",
                ],
                uses=["all()"],
                solution="return all(n > 0 for n in nums)",
            ),
            challenge(
                num=3, title="Any Long Word", difficulty="Easy",
                problem=(
                    "Given a list of words, return `True` when at least one word has "
                    "more than 10 characters."
                ),
                input_fmt="A list of strings.",
                output_fmt="A `bool`.",
                sample_in='any_long(["hi", "there", "programming"])',
                sample_out="True",
                constraints="Use `any()` with a generator expression.",
                signature="def any_long(words):",
                tests=[
                    'assert any_long(["hi", "there", "programming"]) is True',
                    'assert any_long(["hi", "there"]) is False',
                    "assert any_long([]) is False",
                ],
                uses=["any()", "strings"],
                solution="return any(len(w) > 10 for w in words)",
            ),
        ]),
        subtopic(num=4, title="Sorting & Top-K", anchor="lists-sort", challenges=[
            challenge(
                num=1, title="Sort Ascending Copy", difficulty="Easy",
                problem=(
                    "Return a **new** list that is the given list sorted ascending. "
                    "The original must not be mutated."
                ),
                input_fmt="A list of comparable values.",
                output_fmt="The sorted list (new object).",
                sample_in="sort_copy([3, 1, 2])",
                sample_out="[1, 2, 3]",
                constraints="Use `sorted()` (not `.sort()`).",
                signature="def sort_copy(items):",
                tests=[
                    "xs = [3, 1, 2]",
                    "result = sort_copy(xs)",
                    "assert result == [1, 2, 3]",
                    "assert xs == [3, 1, 2]  # unchanged",
                    "assert sort_copy([]) == []",
                ],
                solution="return sorted(items)",
            ),
            challenge(
                num=2, title="Top K Largest", difficulty="Hard",
                problem=(
                    "Return the `k` largest numbers from a list, in descending order. "
                    "If `k` is bigger than the list, return them all (still descending). "
                    "Example: `top_k([3, 1, 4, 1, 5, 9, 2, 6], 3)` → `[9, 6, 5]`."
                ),
                input_fmt="A list of numbers `nums`, a non-negative integer `k`.",
                output_fmt="A list of at most `k` numbers, sorted descending.",
                sample_in="top_k([3, 1, 4, 1, 5, 9, 2, 6], 3)",
                sample_out="[9, 6, 5]",
                constraints="Use `sorted(..., reverse=True)` and slicing.",
                signature="def top_k(nums, k):",
                tests=[
                    "assert top_k([3, 1, 4, 1, 5, 9, 2, 6], 3) == [9, 6, 5]",
                    "assert top_k([1, 2, 3], 0) == []",
                    "assert top_k([1, 2, 3], 10) == [3, 2, 1]",
                    "assert top_k([], 5) == []",
                ],
                uses=["lists (sorting)", "slicing"],
                solution="return sorted(nums, reverse=True)[:k]",
            ),
        ]),
    ],
))
# BUILD-MARKER: lists-fundamentals-complete

SECTIONS.append(section(
    num=11, title="Lists – Advanced", anchor="lists-advanced",
    intro=(
        "Move beyond basics: copies (shallow vs deep), combining lists with `+` "
        "and `zip`, functional tools (`map`, `filter`, `lambda`), and list "
        "comprehensions."
    ),
    subtopics=[
        subtopic(num=1, title="Copy & Combine", anchor="lists-advanced-copy", challenges=[
            challenge(
                num=1, title="Shallow Copy Safe", difficulty="Easy",
                problem=(
                    "Return a **shallow copy** of the given list so that appending "
                    "to the copy does not change the original."
                ),
                input_fmt="A list `items`.",
                output_fmt="A new list with the same elements.",
                sample_in="shallow_copy([1, 2, 3])",
                sample_out="[1, 2, 3]",
                constraints=(
                    "Use `list(items)` or `items[:]`. The test cell verifies object "
                    "identity differs."
                ),
                signature="def shallow_copy(items):",
                tests=[
                    "xs = [1, 2, 3]",
                    "ys = shallow_copy(xs)",
                    "assert ys == [1, 2, 3]",
                    "assert ys is not xs",
                    "ys.append(4)",
                    "assert xs == [1, 2, 3]",
                ],
                uses=["lists"],
                solution="return list(items)",
            ),
            challenge(
                num=2, title="Deep Copy Nested", difficulty="Medium",
                problem=(
                    "Return a **deep copy** of a list that contains inner lists. "
                    "Mutating an inner list of the copy must not affect the original."
                ),
                input_fmt="A list of lists.",
                output_fmt="A deep-copied list of lists.",
                sample_in="deep_copy_nested([[1, 2], [3, 4]])",
                sample_out="[[1, 2], [3, 4]]",
                constraints="Use `copy.deepcopy`.",
                signature="def deep_copy_nested(matrix):",
                tests=[
                    "xs = [[1, 2], [3, 4]]",
                    "ys = deep_copy_nested(xs)",
                    "assert ys == [[1, 2], [3, 4]]",
                    "ys[0].append(99)",
                    "assert xs == [[1, 2], [3, 4]]",
                ],
                uses=["lists (nested)", "copy"],
                solution=(
                    "import copy\n"
                    "return copy.deepcopy(matrix)"
                ),
            ),
            challenge(
                num=3, title="Combine Two Lists", difficulty="Easy",
                problem=(
                    "Return a new list that is the concatenation of `a` followed "
                    "by `b`."
                ),
                input_fmt="Two lists `a` and `b`.",
                output_fmt="A new combined list.",
                sample_in="combine([1, 2], [3, 4])",
                sample_out="[1, 2, 3, 4]",
                constraints="Use the `+` operator.",
                signature="def combine(a, b):",
                tests=[
                    "assert combine([1, 2], [3, 4]) == [1, 2, 3, 4]",
                    "assert combine([], [1]) == [1]",
                    "assert combine([1], []) == [1]",
                    "assert combine([], []) == []",
                ],
                solution="return a + b",
            ),
        ]),
        subtopic(num=2, title="zip & enumerate", anchor="lists-advanced-zip", challenges=[
            challenge(
                num=1, title="Zip Pairs", difficulty="Easy",
                problem=(
                    "Given two equal-length lists of names and scores, return a "
                    "list of `(name, score)` tuples."
                ),
                input_fmt="A list of names and a list of scores (same length).",
                output_fmt="A list of tuples.",
                sample_in='zip_pairs(["A", "B"], [90, 80])',
                sample_out="[('A', 90), ('B', 80)]",
                constraints="Use `zip()` and `list()`.",
                signature="def zip_pairs(names, scores):",
                tests=[
                    'assert zip_pairs(["A", "B"], [90, 80]) == [("A", 90), ("B", 80)]',
                    "assert zip_pairs([], []) == []",
                    'assert zip_pairs(["X"], [1]) == [("X", 1)]',
                ],
                uses=["zip()", "tuples"],
                solution="return list(zip(names, scores))",
            ),
            challenge(
                num=2, title="Enumerate With Offset", difficulty="Medium",
                problem=(
                    "Return a list of `(index, value)` tuples for the given list, "
                    "where indexing starts at `start` (not 0)."
                ),
                input_fmt="A list `items`, an integer `start`.",
                output_fmt="A list of `(index, value)` tuples.",
                sample_in='enum_offset(["a", "b", "c"], 1)',
                sample_out="[(1, 'a'), (2, 'b'), (3, 'c')]",
                constraints="Use `enumerate(..., start=...)`.",
                signature="def enum_offset(items, start):",
                tests=[
                    'assert enum_offset(["a", "b", "c"], 1) == [(1, "a"), (2, "b"), (3, "c")]',
                    'assert enum_offset(["x"], 10) == [(10, "x")]',
                    "assert enum_offset([], 5) == []",
                ],
                uses=["enumerate()", "tuples"],
                solution="return list(enumerate(items, start=start))",
            ),
        ]),
        subtopic(num=3, title="map / filter / lambda", anchor="lists-advanced-functional", challenges=[
            challenge(
                num=1, title="Double via Map", difficulty="Easy",
                problem=(
                    "Return a new list where every number is doubled. Use `map` "
                    "with a `lambda`."
                ),
                input_fmt="A list of numbers.",
                output_fmt="A list of numbers.",
                sample_in="map_double([1, 2, 3])",
                sample_out="[2, 4, 6]",
                constraints="Must use `map()` and `lambda`.",
                signature="def map_double(nums):",
                tests=[
                    "assert map_double([1, 2, 3]) == [2, 4, 6]",
                    "assert map_double([]) == []",
                    "assert map_double([0, -1]) == [0, -2]",
                ],
                uses=["map()", "lambda"],
                solution="return list(map(lambda n: n * 2, nums))",
            ),
            challenge(
                num=2, title="Filter Positives", difficulty="Easy",
                problem=(
                    "Return a new list containing only the strictly-positive "
                    "numbers from the input. Use `filter` with a `lambda`."
                ),
                input_fmt="A list of numbers.",
                output_fmt="A list of positive numbers, preserving order.",
                sample_in="keep_positive([-1, 0, 2, -3, 4])",
                sample_out="[2, 4]",
                constraints="Must use `filter()` and `lambda`.",
                signature="def keep_positive(nums):",
                tests=[
                    "assert keep_positive([-1, 0, 2, -3, 4]) == [2, 4]",
                    "assert keep_positive([]) == []",
                    "assert keep_positive([-1, -2]) == []",
                ],
                uses=["filter()", "lambda"],
                solution="return list(filter(lambda n: n > 0, nums))",
            ),
            challenge(
                num=3, title="Sum of Squares", difficulty="Medium",
                problem=(
                    "Return the sum of squares of the numbers in the list. Use "
                    "`map` with a `lambda` plus `sum()`."
                ),
                input_fmt="A list of numbers.",
                output_fmt="A number.",
                sample_in="sum_of_squares([1, 2, 3])",
                sample_out="14",
                constraints="Must use `map()` (not a comprehension).",
                signature="def sum_of_squares(nums):",
                tests=[
                    "assert sum_of_squares([1, 2, 3]) == 14",
                    "assert sum_of_squares([]) == 0",
                    "assert sum_of_squares([-2, 2]) == 8",
                ],
                uses=["map()", "lambda", "sum()"],
                solution="return sum(map(lambda n: n * n, nums))",
            ),
            challenge(
                num=4, title="Filter Long Words", difficulty="Medium",
                problem=(
                    "Given a list of words and a minimum length `min_len`, return "
                    "the words whose length is **at least** `min_len`. Use "
                    "`filter` with a `lambda`."
                ),
                input_fmt="A list of strings and an integer `min_len`.",
                output_fmt="A list of strings.",
                sample_in='filter_long(["hi", "there", "programming"], 5)',
                sample_out="['there', 'programming']",
                constraints="Must use `filter()` and `lambda`.",
                signature="def filter_long(words, min_len):",
                tests=[
                    'assert filter_long(["hi", "there", "programming"], 5) == ["there", "programming"]',
                    'assert filter_long(["a"], 2) == []',
                    'assert filter_long([], 3) == []',
                ],
                uses=["filter()", "lambda", "strings"],
                solution="return list(filter(lambda w: len(w) >= min_len, words))",
            ),
        ]),
        subtopic(num=4, title="List Comprehensions", anchor="lists-advanced-comprehensions", challenges=[
            challenge(
                num=1, title="Squares Comprehension", difficulty="Easy",
                problem=(
                    "Return a list of squares for `n = 1..limit` (inclusive) using "
                    "a list comprehension."
                ),
                input_fmt="A positive integer `limit`.",
                output_fmt="A list of integers.",
                sample_in="squares_up_to(5)",
                sample_out="[1, 4, 9, 16, 25]",
                constraints="Use a list comprehension.",
                signature="def squares_up_to(limit):",
                tests=[
                    "assert squares_up_to(5) == [1, 4, 9, 16, 25]",
                    "assert squares_up_to(1) == [1]",
                    "assert squares_up_to(0) == []",
                ],
                uses=["list comprehension"],
                solution="return [n * n for n in range(1, limit + 1)]",
            ),
            challenge(
                num=2, title="Filter + Transform", difficulty="Medium",
                problem=(
                    "Given a list of numbers, return the squares of the **even** "
                    "numbers only, preserving order. Use a single list comprehension "
                    "with both a `for` and an `if`."
                ),
                input_fmt="A list of integers.",
                output_fmt="A list of integers.",
                sample_in="even_squares([1, 2, 3, 4, 5])",
                sample_out="[4, 16]",
                constraints="Must be a single list comprehension.",
                signature="def even_squares(nums):",
                tests=[
                    "assert even_squares([1, 2, 3, 4, 5]) == [4, 16]",
                    "assert even_squares([1, 3, 5]) == []",
                    "assert even_squares([]) == []",
                    "assert even_squares([0, 2]) == [0, 4]",
                ],
                uses=["list comprehension", "conditionals"],
                solution="return [n * n for n in nums if n % 2 == 0]",
            ),
            challenge(
                num=3, title="Flatten Nested", difficulty="Hard",
                problem=(
                    "Flatten a list of lists into a single list, preserving order. "
                    "Use a **nested** list comprehension."
                ),
                input_fmt="A list of lists.",
                output_fmt="A flat list.",
                sample_in="flatten([[1, 2], [3, 4], [5]])",
                sample_out="[1, 2, 3, 4, 5]",
                constraints="Must use a nested list comprehension (two `for` clauses).",
                signature="def flatten(matrix):",
                tests=[
                    "assert flatten([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]",
                    "assert flatten([]) == []",
                    "assert flatten([[]]) == []",
                    "assert flatten([[1]]) == [1]",
                ],
                uses=["list comprehension (nested)", "lists (nested)"],
                solution="return [x for row in matrix for x in row]",
            ),
        ]),
    ],
))
# BUILD-MARKER: lists-advanced-complete

SECTIONS.append(section(
    num=12, title="Data Structures", anchor="data-structures",
    intro=(
        "Tuples (immutable ordered), sets (unique unordered with math ops), "
        "and dictionaries (key-value). Pick the right shape for the data."
    ),
    subtopics=[
        subtopic(num=1, title="Tuples", anchor="ds-tuples", challenges=[
            challenge(
                num=1, title="Swap via Tuple", difficulty="Easy",
                problem=(
                    "Given two values `a` and `b`, return them swapped as a "
                    "tuple `(b, a)` using tuple packing/unpacking."
                ),
                input_fmt="Two values `a` and `b`.",
                output_fmt="A tuple `(b, a)`.",
                sample_in="swap(1, 2)",
                sample_out="(2, 1)",
                constraints="Use tuple assignment `a, b = b, a`.",
                signature="def swap(a, b):",
                tests=[
                    "assert swap(1, 2) == (2, 1)",
                    'assert swap("x", "y") == ("y", "x")',
                    "assert swap(0, 0) == (0, 0)",
                ],
                uses=["tuples"],
                solution=(
                    "a, b = b, a\n"
                    "return (a, b)"
                ),
            ),
            challenge(
                num=2, title="Min-Max Tuple", difficulty="Medium",
                problem=(
                    "Given a non-empty list of numbers, return a tuple "
                    "`(minimum, maximum)`."
                ),
                input_fmt="A non-empty list of numbers.",
                output_fmt="A tuple `(min, max)`.",
                sample_in="min_max([3, 1, 4, 1, 5, 9])",
                sample_out="(1, 9)",
                constraints="Use `min()` and `max()`; return a tuple (not a list).",
                signature="def min_max(nums):",
                tests=[
                    "assert min_max([3, 1, 4, 1, 5, 9]) == (1, 9)",
                    "assert min_max([42]) == (42, 42)",
                    "assert min_max([-5, 0, 5]) == (-5, 5)",
                ],
                uses=["tuples", "lists"],
                solution="return (min(nums), max(nums))",
            ),
        ]),
        subtopic(num=2, title="Sets", anchor="ds-sets", challenges=[
            challenge(
                num=1, title="Unique Values", difficulty="Easy",
                problem=(
                    "Return the number of **distinct** values in the given list."
                ),
                input_fmt="A list of values.",
                output_fmt="An integer count.",
                sample_in="unique_count([1, 2, 2, 3, 3, 3])",
                sample_out="3",
                constraints="Use `set()` and `len()`.",
                signature="def unique_count(items):",
                tests=[
                    "assert unique_count([1, 2, 2, 3, 3, 3]) == 3",
                    "assert unique_count([]) == 0",
                    'assert unique_count(["a", "a"]) == 1',
                ],
                uses=["sets"],
                solution="return len(set(items))",
            ),
            challenge(
                num=2, title="Common Tags", difficulty="Medium",
                problem=(
                    "Given two lists of tags, return a sorted list of tags that "
                    "appear in **both** lists (no duplicates)."
                ),
                input_fmt="Two lists of strings.",
                output_fmt="A sorted list of strings.",
                sample_in='common_tags(["py", "ai", "web"], ["ai", "ml", "py"])',
                sample_out="['ai', 'py']",
                constraints="Use set intersection (`&`) then `sorted`.",
                signature="def common_tags(a, b):",
                tests=[
                    'assert common_tags(["py", "ai", "web"], ["ai", "ml", "py"]) == ["ai", "py"]',
                    'assert common_tags([], ["x"]) == []',
                    'assert common_tags(["a", "a"], ["a"]) == ["a"]',
                ],
                uses=["sets", "lists"],
                solution="return sorted(set(a) & set(b))",
            ),
            challenge(
                num=3, title="Is Subset", difficulty="Medium",
                problem=(
                    "Given two lists `small` and `big`, return `True` when every "
                    "element of `small` is present in `big` (duplicates ignored)."
                ),
                input_fmt="Two lists.",
                output_fmt="A `bool`.",
                sample_in="is_subset([1, 2], [1, 2, 3])",
                sample_out="True",
                constraints="Use `set.issubset` or the `<=` operator.",
                signature="def is_subset(small, big):",
                tests=[
                    "assert is_subset([1, 2], [1, 2, 3]) is True",
                    "assert is_subset([1, 4], [1, 2, 3]) is False",
                    "assert is_subset([], [1, 2]) is True",
                    "assert is_subset([1, 1, 2], [1, 2]) is True",
                ],
                uses=["sets"],
                solution="return set(small).issubset(set(big))",
            ),
            challenge(
                num=4, title="Symmetric Difference", difficulty="Hard",
                problem=(
                    "Return a sorted list of values that appear in exactly **one** "
                    "of the two input lists (not both)."
                ),
                input_fmt="Two lists of comparable values.",
                output_fmt="A sorted list.",
                sample_in="sym_diff([1, 2, 3], [2, 3, 4])",
                sample_out="[1, 4]",
                constraints="Use `set.symmetric_difference` or the `^` operator.",
                signature="def sym_diff(a, b):",
                tests=[
                    "assert sym_diff([1, 2, 3], [2, 3, 4]) == [1, 4]",
                    "assert sym_diff([], [1]) == [1]",
                    "assert sym_diff([1, 2], [1, 2]) == []",
                ],
                uses=["sets"],
                solution="return sorted(set(a) ^ set(b))",
            ),
        ]),
        subtopic(num=3, title="Dictionaries", anchor="ds-dicts", challenges=[
            challenge(
                num=1, title="Build Phonebook", difficulty="Easy",
                problem=(
                    "Given two equal-length lists `names` and `phones`, return a "
                    "dictionary mapping each name to its phone number."
                ),
                input_fmt="Two equal-length lists.",
                output_fmt="A dictionary.",
                sample_in='build_phonebook(["Ria", "Om"], ["111", "222"])',
                sample_out="{'Ria': '111', 'Om': '222'}",
                constraints="Use `zip` and `dict`.",
                signature="def build_phonebook(names, phones):",
                tests=[
                    'assert build_phonebook(["Ria", "Om"], ["111", "222"]) == {"Ria": "111", "Om": "222"}',
                    "assert build_phonebook([], []) == {}",
                    'assert build_phonebook(["A"], ["1"]) == {"A": "1"}',
                ],
                uses=["dict", "zip()"],
                solution="return dict(zip(names, phones))",
            ),
            challenge(
                num=2, title="Safe Lookup", difficulty="Easy",
                problem=(
                    "Return the value stored at `key` in the dictionary. If the "
                    "key is absent, return the string `\"unknown\"`."
                ),
                input_fmt="A dictionary and a key.",
                output_fmt="The value or the string `\"unknown\"`.",
                sample_in='safe_lookup({"a": 1}, "a")',
                sample_out="1",
                constraints="Use `dict.get` with a default.",
                signature="def safe_lookup(d, key):",
                tests=[
                    'assert safe_lookup({"a": 1}, "a") == 1',
                    'assert safe_lookup({"a": 1}, "b") == "unknown"',
                    'assert safe_lookup({}, "x") == "unknown"',
                ],
                uses=["dict"],
                solution='return d.get(key, "unknown")',
            ),
            challenge(
                num=3, title="Word Frequency", difficulty="Medium",
                problem=(
                    "Given a sentence, return a dictionary mapping each word "
                    "(lower-cased, whitespace-split) to its count."
                ),
                input_fmt="A string `sentence`.",
                output_fmt="A dictionary `{word: count}`.",
                sample_in='word_freq("to be or not to be")',
                sample_out="{'to': 2, 'be': 2, 'or': 1, 'not': 1}",
                constraints=(
                    "Split on whitespace, lower-case, then count. Use a plain "
                    "dict (no `Counter`)."
                ),
                signature="def word_freq(sentence):",
                tests=[
                    'assert word_freq("to be or not to be") == {"to": 2, "be": 2, "or": 1, "not": 1}',
                    'assert word_freq("") == {}',
                    'assert word_freq("Hi hi HI") == {"hi": 3}',
                ],
                uses=["dict", "strings"],
                solution=(
                    "counts = {}\n"
                    "for w in sentence.lower().split():\n"
                    "    counts[w] = counts.get(w, 0) + 1\n"
                    "return counts"
                ),
            ),
            challenge(
                num=4, title="Invert Dict", difficulty="Medium",
                problem=(
                    "Given a dictionary with unique values, return a new "
                    "dictionary whose keys and values are swapped."
                ),
                input_fmt="A dictionary with unique values.",
                output_fmt="A dictionary.",
                sample_in='invert({"a": 1, "b": 2})',
                sample_out="{1: 'a', 2: 'b'}",
                constraints=(
                    "Use a dict comprehension. You may assume values are "
                    "hashable and unique."
                ),
                signature="def invert(d):",
                tests=[
                    'assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}',
                    "assert invert({}) == {}",
                    'assert invert({"x": 9}) == {9: "x"}',
                ],
                uses=["dict", "dict comprehension"],
                solution="return {v: k for k, v in d.items()}",
            ),
            challenge(
                num=5, title="Top-Spender", difficulty="Hard",
                problem=(
                    "Given a dictionary mapping customer name → spend amount, "
                    "return the name of the **biggest spender**. If the dict is "
                    "empty, return `None`. If multiple customers tie for the top, "
                    "return the one whose name is alphabetically first."
                ),
                input_fmt="A dict `{name: amount}`.",
                output_fmt="A string (or `None`).",
                sample_in='top_spender({"Ria": 100, "Om": 250, "Ana": 250})',
                sample_out="'Ana'",
                constraints=(
                    "Use `max` with a `key=` function, or sort `items()`. Break "
                    "ties alphabetically by name."
                ),
                signature="def top_spender(spend):",
                tests=[
                    'assert top_spender({"Ria": 100, "Om": 250, "Ana": 250}) == "Ana"',
                    'assert top_spender({"X": 5}) == "X"',
                    "assert top_spender({}) is None",
                ],
                uses=["dict", "sorting", "tuples"],
                solution=(
                    "if not spend:\n"
                    "    return None\n"
                    "return sorted(spend.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]"
                ),
            ),
            challenge(
                num=6, title="Students by Grade", difficulty="Hard",
                problem=(
                    "Given a list of `(name, grade)` tuples, return a dictionary "
                    "mapping each grade to a **sorted** list of names at that "
                    "grade."
                ),
                input_fmt="A list of `(name, grade)` tuples.",
                output_fmt="A dict `{grade: [names...]}` with each list sorted.",
                sample_in='group_by_grade([("Ria","A"),("Om","B"),("Ana","A")])',
                sample_out="{'A': ['Ana', 'Ria'], 'B': ['Om']}",
                constraints=(
                    "Loop once, append to per-grade buckets, then sort each list."
                ),
                signature="def group_by_grade(pairs):",
                tests=[
                    'assert group_by_grade([("Ria","A"),("Om","B"),("Ana","A")]) == {"A": ["Ana", "Ria"], "B": ["Om"]}',
                    "assert group_by_grade([]) == {}",
                    'assert group_by_grade([("X","Z")]) == {"Z": ["X"]}',
                ],
                uses=["dict", "lists", "tuples", "sorting"],
                solution=(
                    "groups = {}\n"
                    "for name, grade in pairs:\n"
                    "    groups.setdefault(grade, []).append(name)\n"
                    "for g in groups:\n"
                    "    groups[g].sort()\n"
                    "return groups"
                ),
            ),
        ]),
    ],
))
# BUILD-MARKER: data-structures-complete

SECTIONS.append(section(
    num=13, title="Functions", anchor="functions",
    intro=(
        "Parameters vs arguments, defaults, `*args`/`**kwargs`, return types "
        "(action / transformation / validation / orchestrator), and scope "
        "(local / global / nonlocal). Clean functions do one thing well."
    ),
    subtopics=[
        subtopic(num=1, title="Parameters & Arguments", anchor="fn-params", challenges=[
            challenge(
                num=1, title="Greet by Name", difficulty="Easy",
                problem=(
                    "Write a function that takes a `name` and returns "
                    "`\"Hello, <name>!\"`."
                ),
                input_fmt="A string `name`.",
                output_fmt="A greeting string.",
                sample_in='greet_by_name("Rishith")',
                sample_out="'Hello, Rishith!'",
                constraints="Single positional parameter.",
                signature="def greet_by_name(name):",
                tests=[
                    'assert greet_by_name("Rishith") == "Hello, Rishith!"',
                    'assert greet_by_name("A") == "Hello, A!"',
                ],
                uses=["functions", "strings"],
                solution='return f"Hello, {name}!"',
            ),
            challenge(
                num=2, title="Full Name", difficulty="Medium",
                problem=(
                    "Return a full name built from `first`, optional `middle`, "
                    "and `last`. When `middle` is empty, skip it and the extra "
                    "space."
                ),
                input_fmt="Three strings (middle may be empty).",
                output_fmt="A full-name string.",
                sample_in='full_name("Ria", "S", "Kumar")',
                sample_out="'Ria S Kumar'",
                constraints="Use positional params. No leading/trailing spaces.",
                signature='def full_name(first, middle, last):',
                tests=[
                    'assert full_name("Ria", "S", "Kumar") == "Ria S Kumar"',
                    'assert full_name("Om", "", "Patel") == "Om Patel"',
                    'assert full_name("A", "", "B") == "A B"',
                ],
                uses=["functions", "strings", "conditionals"],
                solution=(
                    "if middle:\n"
                    '    return f"{first} {middle} {last}"\n'
                    'return f"{first} {last}"'
                ),
            ),
            challenge(
                num=3, title="Keyword-Only Tax", difficulty="Medium",
                problem=(
                    "Write a function `apply_tax(amount, *, rate)` that requires "
                    "`rate` to be passed as a keyword argument. Return "
                    "`amount * (1 + rate)` rounded to 2 decimals."
                ),
                input_fmt="A number `amount` and a keyword-only `rate`.",
                output_fmt="A float rounded to 2 decimals.",
                sample_in="apply_tax(100, rate=0.1)",
                sample_out="110.0",
                constraints=(
                    "The `*` in the signature forces keyword use. Calling "
                    "`apply_tax(100, 0.1)` must raise `TypeError`."
                ),
                signature="def apply_tax(amount, *, rate):",
                tests=[
                    "assert apply_tax(100, rate=0.1) == 110.0",
                    "assert apply_tax(50, rate=0.2) == 60.0",
                    "try:",
                    "    apply_tax(100, 0.1)",
                    '    raise AssertionError("should require keyword arg")',
                    "except TypeError:",
                    "    pass",
                ],
                uses=["functions (keyword-only)", "numbers"],
                solution="return round(amount * (1 + rate), 2)",
            ),
        ]),
        subtopic(num=2, title="Defaults", anchor="fn-defaults", challenges=[
            challenge(
                num=1, title="Greeting With Default", difficulty="Easy",
                problem=(
                    "Write `greet(name, greeting=\"Hi\")` that returns "
                    "`\"<greeting>, <name>!\"`."
                ),
                input_fmt="A name and an optional greeting.",
                output_fmt="A greeting string.",
                sample_in='greet("Rishith")',
                sample_out="'Hi, Rishith!'",
                constraints="Use a default value.",
                signature='def greet(name, greeting="Hi"):',
                tests=[
                    'assert greet("Rishith") == "Hi, Rishith!"',
                    'assert greet("Ria", "Hello") == "Hello, Ria!"',
                    'assert greet("Om", greeting="Hey") == "Hey, Om!"',
                ],
                uses=["functions (defaults)"],
                solution='return f"{greeting}, {name}!"',
            ),
            challenge(
                num=2, title="Safe Divide", difficulty="Medium",
                problem=(
                    "Divide `a` by `b` and return the result. When `b` is zero, "
                    "return the `fallback` value (default `0`)."
                ),
                input_fmt="Two numbers and an optional fallback.",
                output_fmt="A number.",
                sample_in="safe_divide(10, 2)",
                sample_out="5.0",
                constraints="Return the fallback instead of raising.",
                signature="def safe_divide(a, b, fallback=0):",
                tests=[
                    "assert safe_divide(10, 2) == 5.0",
                    "assert safe_divide(5, 0) == 0",
                    'assert safe_divide(5, 0, fallback="N/A") == "N/A"',
                    "assert safe_divide(0, 5) == 0.0",
                ],
                uses=["functions (defaults)", "conditionals"],
                solution=(
                    "if b == 0:\n"
                    "    return fallback\n"
                    "return a / b"
                ),
            ),
        ]),
        subtopic(num=3, title="*args and **kwargs", anchor="fn-varargs", challenges=[
            challenge(
                num=1, title="Sum Any", difficulty="Easy",
                problem=(
                    "Write `sum_any(*nums)` that returns the sum of any number "
                    "of numeric arguments. Zero arguments → `0`."
                ),
                input_fmt="Any number of numeric arguments.",
                output_fmt="A number.",
                sample_in="sum_any(1, 2, 3)",
                sample_out="6",
                constraints="Use `*args`.",
                signature="def sum_any(*nums):",
                tests=[
                    "assert sum_any(1, 2, 3) == 6",
                    "assert sum_any() == 0",
                    "assert sum_any(10) == 10",
                    "assert sum_any(1.5, 2.5) == 4.0",
                ],
                uses=["functions (*args)", "sum()"],
                solution="return sum(nums)",
            ),
            challenge(
                num=2, title="Merge Dicts", difficulty="Medium",
                problem=(
                    "Write `merge_dicts(**kwargs)` that returns a plain dict of "
                    "all keyword arguments passed in."
                ),
                input_fmt="Any number of keyword arguments.",
                output_fmt="A dict.",
                sample_in="merge_dicts(a=1, b=2)",
                sample_out="{'a': 1, 'b': 2}",
                constraints="Return a plain `dict(kwargs)` copy.",
                signature="def merge_dicts(**kwargs):",
                tests=[
                    'assert merge_dicts(a=1, b=2) == {"a": 1, "b": 2}',
                    "assert merge_dicts() == {}",
                    'assert merge_dicts(x=9) == {"x": 9}',
                ],
                uses=["functions (**kwargs)", "dict"],
                solution="return dict(kwargs)",
            ),
            challenge(
                num=3, title="Describe Pet", difficulty="Medium",
                problem=(
                    "Write `describe_pet(name, *traits, **details)` that returns "
                    "a dict `{\"name\": name, \"traits\": list(traits), \"details\": "
                    "dict(details)}`."
                ),
                input_fmt=(
                    "One positional `name`, variable positional `traits`, "
                    "variable keyword `details`."
                ),
                output_fmt="A dict with 3 keys.",
                sample_in='describe_pet("Leo", "furry", "loud", age=3)',
                sample_out="{'name': 'Leo', 'traits': ['furry', 'loud'], 'details': {'age': 3}}",
                constraints="Combine positional, `*args`, and `**kwargs`.",
                signature="def describe_pet(name, *traits, **details):",
                tests=[
                    'assert describe_pet("Leo", "furry", "loud", age=3) == {"name": "Leo", "traits": ["furry", "loud"], "details": {"age": 3}}',
                    'assert describe_pet("Mo") == {"name": "Mo", "traits": [], "details": {}}',
                ],
                uses=["functions (*args, **kwargs)", "dict", "lists"],
                solution=(
                    'return {"name": name, "traits": list(traits), "details": dict(details)}'
                ),
            ),
        ]),
        subtopic(num=4, title="Return Types: Validation / Transformation / Orchestrator", anchor="fn-return-types", challenges=[
            challenge(
                num=1, title="Is Valid Email (Simple)", difficulty="Easy",
                problem=(
                    "Return `True` when `email` is a non-empty string containing "
                    "exactly one `@` and at least one `.` after the `@`."
                ),
                input_fmt="A string `email`.",
                output_fmt="A `bool`.",
                sample_in='is_valid_email("a@b.com")',
                sample_out="True",
                constraints="Validation function: returns `True`/`False` only.",
                signature="def is_valid_email(email):",
                tests=[
                    'assert is_valid_email("a@b.com") is True',
                    'assert is_valid_email("a@bcom") is False',
                    'assert is_valid_email("a@@b.com") is False',
                    'assert is_valid_email("") is False',
                    'assert is_valid_email("no_at_sign.com") is False',
                ],
                uses=["functions (validation)", "strings"],
                solution=(
                    "if not isinstance(email, str) or email.count('@') != 1:\n"
                    "    return False\n"
                    "after_at = email.split('@')[1]\n"
                    "return '.' in after_at"
                ),
            ),
            challenge(
                num=2, title="Apply Discount", difficulty="Medium",
                problem=(
                    "Write a **transformation** function that takes a price and "
                    "discount percentage (0–100) and returns the discounted "
                    "price rounded to 2 decimals. Do not mutate anything."
                ),
                input_fmt="A float `price`, a float `pct` in [0, 100].",
                output_fmt="A float rounded to 2 decimals.",
                sample_in="apply_discount(100.0, 20)",
                sample_out="80.0",
                constraints=(
                    "Pure transformation — no I/O, no mutation, only compute "
                    "and return."
                ),
                signature="def apply_discount(price, pct):",
                tests=[
                    "assert apply_discount(100.0, 20) == 80.0",
                    "assert apply_discount(50.0, 0) == 50.0",
                    "assert apply_discount(199.99, 10) == 179.99",
                ],
                uses=["functions (transformation)", "numbers"],
                solution="return round(price * (1 - pct / 100), 2)",
            ),
            challenge(
                num=3, title="Process Order (Orchestrator)", difficulty="Hard",
                problem=(
                    "Write `process_order(email, price, pct)` that orchestrates "
                    "the previous two functions:\n"
                    "- If `is_valid_email(email)` is `False`, return "
                    "`\"invalid email\"`.\n"
                    "- Otherwise return a dict "
                    "`{\"email\": email, \"final_price\": apply_discount(price, pct)}`."
                ),
                input_fmt="An email, a price, and a discount percent.",
                output_fmt=(
                    "A dict with `email` and `final_price`, or the string "
                    "`\"invalid email\"`."
                ),
                sample_in='process_order("a@b.com", 100.0, 20)',
                sample_out="{'email': 'a@b.com', 'final_price': 80.0}",
                constraints=(
                    "Orchestrator: calls the validation and transformation "
                    "functions rather than re-implementing their logic."
                ),
                signature="def process_order(email, price, pct):",
                tests=[
                    'assert process_order("a@b.com", 100.0, 20) == {"email": "a@b.com", "final_price": 80.0}',
                    'assert process_order("bad", 100.0, 20) == "invalid email"',
                    'assert process_order("x@y.z", 50.0, 0) == {"email": "x@y.z", "final_price": 50.0}',
                ],
                uses=["functions (orchestrator)", "dict", "conditionals"],
                solution=(
                    "if not is_valid_email(email):\n"
                    '    return "invalid email"\n'
                    'return {"email": email, "final_price": apply_discount(price, pct)}'
                ),
            ),
        ]),
        subtopic(num=5, title="Scope & Closures", anchor="fn-scope", challenges=[
            challenge(
                num=1, title="Local vs Global", difficulty="Easy",
                problem=(
                    "A module-level variable `COUNTER = 0` exists. Write "
                    "`bump_global()` that increments it by 1 and returns the "
                    "new value. Use the `global` keyword."
                ),
                input_fmt="No arguments.",
                output_fmt="An integer — the new counter value.",
                sample_in="bump_global()  # first call",
                sample_out="1",
                constraints="Use `global COUNTER`.",
                signature="def bump_global():",
                tests=[
                    "COUNTER = 0",
                    "assert bump_global() == 1",
                    "assert bump_global() == 2",
                    "assert COUNTER == 2",
                ],
                uses=["functions (scope: global)"],
                solution=(
                    "global COUNTER\n"
                    "COUNTER += 1\n"
                    "return COUNTER"
                ),
            ),
            challenge(
                num=2, title="Counter Closure", difficulty="Medium",
                problem=(
                    "Write `make_counter()` that returns a function. Each call "
                    "to the returned function increments and returns an "
                    "internal counter starting at 1. Use `nonlocal`."
                ),
                input_fmt="No arguments.",
                output_fmt="A function (closure).",
                sample_in="c = make_counter(); c(); c()",
                sample_out="2",
                constraints="Use a nested function + `nonlocal`.",
                signature="def make_counter():",
                tests=[
                    "c = make_counter()",
                    "assert c() == 1",
                    "assert c() == 2",
                    "assert c() == 3",
                    "c2 = make_counter()",
                    "assert c2() == 1  # independent state",
                ],
                uses=["functions (closure, nonlocal)"],
                solution=(
                    "count = 0\n"
                    "def inner():\n"
                    "    nonlocal count\n"
                    "    count += 1\n"
                    "    return count\n"
                    "return inner"
                ),
            ),
            challenge(
                num=3, title="Accumulator Factory", difficulty="Hard",
                problem=(
                    "Write `make_accumulator(start=0)` that returns a function "
                    "`add(x)`. Each call to `add(x)` adds `x` to an internal "
                    "running total and returns the new total. Factories with "
                    "the same `start` must have **independent** totals."
                ),
                input_fmt="Optional starting total (default 0).",
                output_fmt="A function of one argument.",
                sample_in="acc = make_accumulator(); acc(5); acc(3)",
                sample_out="8",
                constraints="Use `nonlocal` to mutate the captured total.",
                signature="def make_accumulator(start=0):",
                tests=[
                    "acc = make_accumulator()",
                    "assert acc(5) == 5",
                    "assert acc(3) == 8",
                    "assert acc(-2) == 6",
                    "acc2 = make_accumulator(100)",
                    "assert acc2(1) == 101",
                    "assert acc(0) == 6  # unaffected",
                ],
                uses=["functions (closure, nonlocal, defaults)"],
                solution=(
                    "total = start\n"
                    "def add(x):\n"
                    "    nonlocal total\n"
                    "    total += x\n"
                    "    return total\n"
                    "return add"
                ),
            ),
        ]),
    ],
))
# BUILD-MARKER: functions-complete


# ---------------------------------------------------------------------------
# PROJECT SPECS
# ---------------------------------------------------------------------------

PROJECTS.append(project(
    num=1,
    title="Secure User Registration System",
    anchor="proj-registration",
    problem=(
        "Build a **user registration system** that validates inputs against "
        "security rules and stores accepted users in a dictionary keyed by "
        "username.\n\n"
        "**Requirements**\n\n"
        "- `is_valid_username(username)` — between 3 and 20 characters, only "
        "letters / digits / underscore.\n"
        "- `is_valid_email(email)` — non-empty, contains exactly one `@`, and "
        "at least one `.` after the `@`.\n"
        "- `is_valid_password(password)` — at least 8 characters, contains at "
        "least one letter and at least one digit.\n"
        "- `register(users, username, email, password)` — orchestrator that "
        "calls the validators and inserts the user as "
        "`users[username] = {\"email\": email, \"password\": password}` when "
        "all three pass **and** the username is not already taken. Returns "
        "`\"ok\"` on success; returns one of "
        "`\"invalid username\"`, `\"invalid email\"`, `\"invalid password\"`, "
        "or `\"username taken\"` on failure (in that priority order)."
    ),
    input_fmt=(
        "A `users` dict (starts empty), plus string `username`, `email`, "
        "`password`."
    ),
    output_fmt="The string `\"ok\"` or one of the error strings listed above.",
    sample_in='register({}, "rishith", "r@b.com", "secret12")',
    sample_out="'ok'",
    constraints=(
        "Validators return `bool` only. `register` does not print — it "
        "returns. The priority order must match: username → email → password "
        "→ duplicate-check."
    ),
    uses=[
        "strings (validation)", "conditionals", "functions (validation, "
        "orchestrator)", "dict",
    ],
    starter_code=(
        "def is_valid_username(username):\n"
        "    # TODO: 3–20 chars, letters / digits / underscore only\n"
        "    pass\n"
        "\n"
        "def is_valid_email(email):\n"
        "    # TODO: exactly one '@', at least one '.' after it\n"
        "    pass\n"
        "\n"
        "def is_valid_password(password):\n"
        "    # TODO: >=8 chars, at least 1 letter and 1 digit\n"
        "    pass\n"
        "\n"
        "def register(users, username, email, password):\n"
        "    # TODO: orchestrate validators, then insert into users dict\n"
        "    pass"
    ),
    solution=(
        "def is_valid_username(username):\n"
        "    if not isinstance(username, str):\n"
        "        return False\n"
        "    if not (3 <= len(username) <= 20):\n"
        "        return False\n"
        "    return all(c.isalnum() or c == '_' for c in username)\n"
        "\n"
        "def is_valid_email(email):\n"
        "    if not isinstance(email, str) or email.count('@') != 1:\n"
        "        return False\n"
        "    return '.' in email.split('@')[1]\n"
        "\n"
        "def is_valid_password(password):\n"
        "    if not isinstance(password, str) or len(password) < 8:\n"
        "        return False\n"
        "    has_letter = any(c.isalpha() for c in password)\n"
        "    has_digit = any(c.isdigit() for c in password)\n"
        "    return has_letter and has_digit\n"
        "\n"
        "def register(users, username, email, password):\n"
        "    if not is_valid_username(username):\n"
        "        return 'invalid username'\n"
        "    if not is_valid_email(email):\n"
        "        return 'invalid email'\n"
        "    if not is_valid_password(password):\n"
        "        return 'invalid password'\n"
        "    if username in users:\n"
        "        return 'username taken'\n"
        "    users[username] = {'email': email, 'password': password}\n"
        "    return 'ok'"
    ),
    tests=[
        "users = {}",
        'assert register(users, "rishith", "r@b.com", "secret12") == "ok"',
        'assert users["rishith"] == {"email": "r@b.com", "password": "secret12"}',
        'assert register(users, "rishith", "r@b.com", "secret12") == "username taken"',
        'assert register({}, "ab", "r@b.com", "secret12") == "invalid username"',
        'assert register({}, "rishith", "bad", "secret12") == "invalid email"',
        'assert register({}, "rishith", "r@b.com", "short") == "invalid password"',
        'assert register({}, "rishith", "r@b.com", "nodigits!") == "invalid password"',
        "assert is_valid_username('ok_1') is True",
        "assert is_valid_username('bad!') is False",
    ],
))

PROJECTS.append(project(
    num=2,
    title="Expense Tracking System",
    anchor="proj-expenses",
    problem=(
        "Build a simple **expense tracker** using a list of expense dicts.\n\n"
        "**Requirements**\n\n"
        "- `add_expense(expenses, amount, category, date)` — append "
        "`{\"amount\": amount, \"category\": category, \"date\": date}` to "
        "`expenses` and return `expenses`.\n"
        "- `total(expenses)` — return the sum of all amounts, rounded to 2 "
        "decimals.\n"
        "- `by_category(expenses)` — return a dict mapping each category to "
        "the total spent in it (rounded to 2 decimals).\n"
        "- `top_categories(expenses, n)` — return the top-`n` category names "
        "by total spend, descending. Break ties alphabetically. When `n` is "
        "larger than the number of categories, return all of them."
    ),
    input_fmt=(
        "An `expenses` list (starts empty), plus amount / category / date / "
        "n arguments as the functions require."
    ),
    output_fmt="Numbers, dicts, or lists per the function contract above.",
    sample_in='add_expense([], 12.5, "food", "2026-04-20")',
    sample_out="[{'amount': 12.5, 'category': 'food', 'date': '2026-04-20'}]",
    constraints=(
        "No printing — return values. Round totals with `round(x, 2)`. "
        "`top_categories` must sort by `(-total, name)`."
    ),
    uses=[
        "numbers (rounding)", "lists", "dict", "sorting", "lambda",
        "functions (action + transformation + orchestrator)",
    ],
    starter_code=(
        "def add_expense(expenses, amount, category, date):\n"
        "    # TODO: append a dict and return the list\n"
        "    pass\n"
        "\n"
        "def total(expenses):\n"
        "    # TODO: sum of amounts, rounded to 2 decimals\n"
        "    pass\n"
        "\n"
        "def by_category(expenses):\n"
        "    # TODO: dict {category: total} rounded to 2 decimals\n"
        "    pass\n"
        "\n"
        "def top_categories(expenses, n):\n"
        "    # TODO: top-n categories by spend, ties broken alphabetically\n"
        "    pass"
    ),
    solution=(
        "def add_expense(expenses, amount, category, date):\n"
        "    expenses.append({'amount': amount, 'category': category, 'date': date})\n"
        "    return expenses\n"
        "\n"
        "def total(expenses):\n"
        "    return round(sum(e['amount'] for e in expenses), 2)\n"
        "\n"
        "def by_category(expenses):\n"
        "    totals = {}\n"
        "    for e in expenses:\n"
        "        totals[e['category']] = totals.get(e['category'], 0) + e['amount']\n"
        "    return {k: round(v, 2) for k, v in totals.items()}\n"
        "\n"
        "def top_categories(expenses, n):\n"
        "    totals = by_category(expenses)\n"
        "    ranked = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))\n"
        "    return [name for name, _ in ranked[:n]]"
    ),
    tests=[
        "expenses = []",
        'add_expense(expenses, 12.5, "food", "2026-04-20")',
        'add_expense(expenses, 7.5, "food", "2026-04-21")',
        'add_expense(expenses, 40.0, "travel", "2026-04-22")',
        'add_expense(expenses, 10.0, "books", "2026-04-22")',
        "assert total(expenses) == 70.0",
        'assert by_category(expenses) == {"food": 20.0, "travel": 40.0, "books": 10.0}',
        'assert top_categories(expenses, 2) == ["travel", "food"]',
        'assert top_categories(expenses, 10) == ["travel", "food", "books"]',
        "assert top_categories([], 3) == []",
    ],
))

PROJECTS.append(project(
    num=3,
    title="Mini Banking System",
    anchor="proj-banking",
    problem=(
        "Build a **mini banking system** using a dict of accounts keyed by "
        "account number.\n\n"
        "**Requirements**\n\n"
        "- `create_account(bank, acc_no, initial=0)` — add account with "
        "balance `initial` and empty history list. Returns `\"ok\"`, or "
        "`\"exists\"` when the number is already taken.\n"
        "- `deposit(bank, acc_no, amount)` — add `amount` to balance, append "
        "`(\"deposit\", amount)` to history. Returns new balance, or "
        "`\"no account\"` when the account doesn't exist.\n"
        "- `withdraw(bank, acc_no, amount)` — subtract `amount` if balance "
        "allows, append `(\"withdraw\", amount)` to history. Returns new "
        "balance, or `\"insufficient funds\"`, or `\"no account\"`.\n"
        "- `transfer(bank, from_acc, to_acc, amount)` — move money between "
        "accounts. Return `\"ok\"`, or one of `\"no account\"` / "
        "`\"insufficient funds\"`. Both history lists must record the "
        "transaction: `(\"transfer_out\", to_acc, amount)` and "
        "`(\"transfer_in\", from_acc, amount)`.\n"
        "- `statement(bank, acc_no)` — return the account's history list, or "
        "`\"no account\"`."
    ),
    input_fmt=(
        "A `bank` dict (starts empty), plus account numbers and amounts as "
        "required by each function."
    ),
    output_fmt="Strings, numbers, or lists per the function contract above.",
    sample_in='create_account({}, "A1", 100)',
    sample_out="'ok'",
    constraints=(
        "No printing — return values. `transfer` must be all-or-nothing: if "
        "the `from_acc` has insufficient funds, neither balance changes and "
        "neither history is updated. Priority for `transfer`: missing account "
        "→ insufficient funds."
    ),
    uses=[
        "dict (nested)", "conditionals", "loops", "tuples",
        "functions (action + orchestrator)",
    ],
    starter_code=(
        "def create_account(bank, acc_no, initial=0):\n"
        "    # TODO: reject duplicates, else add {'balance': initial, 'history': []}\n"
        "    pass\n"
        "\n"
        "def deposit(bank, acc_no, amount):\n"
        "    # TODO: update balance, record history, or return 'no account'\n"
        "    pass\n"
        "\n"
        "def withdraw(bank, acc_no, amount):\n"
        "    # TODO: check balance, update, record history, or return error\n"
        "    pass\n"
        "\n"
        "def transfer(bank, from_acc, to_acc, amount):\n"
        "    # TODO: all-or-nothing move between two accounts\n"
        "    pass\n"
        "\n"
        "def statement(bank, acc_no):\n"
        "    # TODO: return history list or 'no account'\n"
        "    pass"
    ),
    solution=(
        "def create_account(bank, acc_no, initial=0):\n"
        "    if acc_no in bank:\n"
        "        return 'exists'\n"
        "    bank[acc_no] = {'balance': initial, 'history': []}\n"
        "    return 'ok'\n"
        "\n"
        "def deposit(bank, acc_no, amount):\n"
        "    if acc_no not in bank:\n"
        "        return 'no account'\n"
        "    bank[acc_no]['balance'] += amount\n"
        "    bank[acc_no]['history'].append(('deposit', amount))\n"
        "    return bank[acc_no]['balance']\n"
        "\n"
        "def withdraw(bank, acc_no, amount):\n"
        "    if acc_no not in bank:\n"
        "        return 'no account'\n"
        "    if bank[acc_no]['balance'] < amount:\n"
        "        return 'insufficient funds'\n"
        "    bank[acc_no]['balance'] -= amount\n"
        "    bank[acc_no]['history'].append(('withdraw', amount))\n"
        "    return bank[acc_no]['balance']\n"
        "\n"
        "def transfer(bank, from_acc, to_acc, amount):\n"
        "    if from_acc not in bank or to_acc not in bank:\n"
        "        return 'no account'\n"
        "    if bank[from_acc]['balance'] < amount:\n"
        "        return 'insufficient funds'\n"
        "    bank[from_acc]['balance'] -= amount\n"
        "    bank[to_acc]['balance'] += amount\n"
        "    bank[from_acc]['history'].append(('transfer_out', to_acc, amount))\n"
        "    bank[to_acc]['history'].append(('transfer_in', from_acc, amount))\n"
        "    return 'ok'\n"
        "\n"
        "def statement(bank, acc_no):\n"
        "    if acc_no not in bank:\n"
        "        return 'no account'\n"
        "    return bank[acc_no]['history']"
    ),
    tests=[
        "bank = {}",
        'assert create_account(bank, "A1", 100) == "ok"',
        'assert create_account(bank, "A1") == "exists"',
        'assert create_account(bank, "A2", 50) == "ok"',
        'assert deposit(bank, "A1", 20) == 120',
        'assert withdraw(bank, "A1", 30) == 90',
        'assert withdraw(bank, "A1", 1000) == "insufficient funds"',
        'assert deposit(bank, "ZZ", 1) == "no account"',
        'assert transfer(bank, "A1", "A2", 40) == "ok"',
        'assert bank["A1"]["balance"] == 50',
        'assert bank["A2"]["balance"] == 90',
        'assert transfer(bank, "A1", "A2", 999) == "insufficient funds"',
        'assert bank["A1"]["balance"] == 50  # rolled back',
        'assert transfer(bank, "A1", "NOPE", 1) == "no account"',
        'assert statement(bank, "A1") == [("deposit", 20), ("withdraw", 30), ("transfer_out", "A2", 40)]',
        'assert statement(bank, "NOPE") == "no account"',
    ],
))
# BUILD-MARKER: projects-complete


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    practice = build_notebook(SECTIONS, PROJECTS, mode="practice")
    solutions = build_notebook(SECTIONS, PROJECTS, mode="solutions")

    nbf.write(practice, PRACTICE_NB)
    nbf.write(solutions, SOLUTIONS_NB)

    n_challenges = sum(
        len(sub["challenges"])
        for sec in SECTIONS
        for sub in sec["subtopics"]
    ) + len(PROJECTS)
    print(f"Wrote {PRACTICE_NB.name} and {SOLUTIONS_NB.name} ({n_challenges} items).")


if __name__ == "__main__":
    main()
