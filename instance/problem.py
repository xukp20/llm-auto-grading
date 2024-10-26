"""
    Class for student's answer.
"""
from instance.ref_problem import GradingRule

# grading status enum
from enum import Enum
class GradingStatus(Enum):
    ungraded = 1
    graded = 2
    unknown_solution = 3
    error = 4

class StudentGradingRule(GradingRule):
    def __init__(self, grading_rule, process, graded_score):
        super().__init__(grading_rule.rule, grading_rule.score, grading_rule.subproblem_id)
        self.process = process
        self.graded_score = graded_score
    
    def __str__(self):
        return f"{self.rule} ({self.score}) {self.graded_score}"
    
    def format_md_table(self):
        string = "| 评分规则 | 分值 | 得分 | 评分过程 |\n"
        string += "| --- | --- | --- | --- |\n"
        string += f"| {self.rule} | {self.score} | {self.graded_score} | {self.process} |\n"
        return string

# for subproblem
class StudentSolution:
    def __init__(self, answer, subproblem_id):
        self.answer = answer
        self.subproblem_id = subproblem_id

        self.status = GradingStatus.ungraded
        self.rules = []
        self.solution_id = None
        self.trace = None

    def __str__(self):
        return f"{self.answer}"
    
    def set_solution_id(self, solution_id):
        self.solution_id = solution_id

    def set_unknown_solution(self):
        self.status = GradingStatus.unknown_solution
    
    def set_error(self, trace):
        self.status = GradingStatus.error
        self.trace = trace

    def add_score(self, grading_rule, process, score):
        self.rules.append(StudentGradingRule(grading_rule, process, score))
    
    def finalize(self, rule_set):
        if not len(self.rules) == len(rule_set):
            self.set_error("Invalid number of rules")
            return
        
        self.status = GradingStatus.graded
    
# for problem
class StudentProblem:
    def __init__(self, answers):
        self.answers = {key: StudentSolution(value, key) for key, value in answers.items()}

    def __str__(self):
        return f"{self.answers}"
    

class StudentPA:
    def __init__(self, problems):
        self.problems = {key: StudentProblem(value) for key, value in problems.items()}
        
    def __str__(self):
        return f"{self.problems}"
    
    @staticmethod
    def from_json(json_file):
        import json
        with open(json_file, "r") as f:
            data = json.load(f)
        return StudentPA(data)