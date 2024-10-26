"""
    Wrapper for the example grading API
"""
from instance.ref_problem import Solution
from instance.problem import StudentSolution

CHECK_PATTERN="""
### 题目文本
{problem}

### 当前题目编号
{subproblem_id}

### 标准答案
{answer}

### 学生答案
{student_answer}

### 评分规则
{grading_rule_md}
"""

def format_inputs(
    problem: str,   # whole problem text
    solution: Solution, # ref solution
    student_solution: StudentSolution,  # student answer
    rule_id: int,   # index of the grading rule
):
    subproblem_id = solution.subproblem_id
    answer = solution.answer
    student_answer = student_solution.answer
    grading_rule = solution.rules[rule_id]
    grading_rule_md = grading_rule.format_md_table()

    return {
        "query": CHECK_PATTERN.format(
            problem=problem,
            subproblem_id=subproblem_id,
            answer=answer,
            student_answer=student_answer,
            grading_rule_md=grading_rule_md,
        ),
    }