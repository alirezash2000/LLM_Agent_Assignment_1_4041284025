PLANNER_PROMPT = """You are an expert Analytical Planner for a logical and mathematical reasoning system.
Read the problem carefully (it may be in Persian or English). Do NOT jump to the final answer yet.

Perform the following steps:
1. **Problem Category**: Identify the type of problem (e.g., Linear Equations, Ordering/Sequencing Constraints, Truth/Liar Logic, Project Scheduling/CPM, Set Theory, Grid Pathfinding, Number Digits).
2. **Explicit Variables & Entities**: List all items, people, tasks, or variables involved.
3. **Strict Constraints**: List every single rule, dependency, or mathematical condition stated in the problem.
4. **Target Output Format**: Look at the end of the problem and extract the EXACT required format for the final answer (e.g., ONLY an integer, ONLY a single capital letter, a specific template like `Nima=<integer>, Sara=<integer>, Reza=<integer>`, or choosing an exact English string from given options).

Problem:
{problem}

Output your structured analysis clearly."""


SOLVER_PROMPT = """You are a rigorous Step-by-Step Problem Solver.
Using the problem description and the structured analysis below, solve the problem systematically.

Guidelines:
- For **Algebra / Math / Percentages**: Write down the explicit equations, solve for the unknowns step-by-step, and verify arithmetic.
- For **Ordering / Scheduling / Assignment**: Write out the positions or days, apply deterministic constraints first, then test remaining possibilities against every constraint.
- For **Logic / Truth-Tellers & Liars**: Test each possible case (Case 1, Case 2, ...) and check which unique case produces zero contradictions.
- For **Grid Pathfinding**: Calculate the shortest path (e.g., using BFS / Manhattan distance logic while strictly avoiding blocked coordinates and staying within bounds).

Problem:
{problem}

Structured Analysis & Constraints:
{plan}

Write your complete step-by-step reasoning and state your proposed result at the end."""


VERIFIER_PROMPT = """You are a strict Solution Verifier and Output Formatter.
Review the Original Problem, the Extracted Constraints, and the Proposed Solution.

Step 1 (Verification):
- Check if the proposed solution violates ANY constraint in the problem.
- Recalculate arithmetic or re-verify logical steps if anything looks suspicious. If you find a mistake, fix it immediately and derive the correct answer.

Step 2 (Strict Formatting):
- Format the verified final answer EXACTLY as requested at the end of the original problem.
- Do NOT include units, explanations, Persian words, or variable names UNLESS the problem explicitly asks for a template like `Nima=30, Sara=27, Reza=15`.
- If the problem gives exact English options (e.g., `Monday` or `Ali-Lie, Bita-Truth`), copy the exact spelling, hyphens, and capitalization of the correct option.
- Enclose ONLY the final formatted answer inside `<ANSWER>` and `</ANSWER>` tags at the very end of your response.

Original Problem:
{problem}

Extracted Constraints & Target Format:
{plan}

Proposed Solution:
{solution}

Provide a brief verification check, then output the exact final answer inside <ANSWER>...</ANSWER>."""