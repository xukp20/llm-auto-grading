"""
    An example checker for the problem.
"""

import json

from checker.base import BaseChecker
from instance.problem import *
from instance.ref_problem import *
from utils.wrappers.example_grading import format_inputs
from utils.apis.dify_api import completion_messages

# tools 
# wrapper for checker api

class ExampleChecker(BaseChecker):
    def __init__(self, grading_key):
        self.grading_key = grading_key

    def parse_grading_response(self, response):
        response = response.strip("```json").strip("```").replace("\\", "\\\\").replace("\\\\\\\\", "\\\\")
        response = json.loads(response)
        process = response["process"]
        score = int(response["score"])
        return process, score

    def check(self, ref_pa, student_pa):
        for problem_id, ref_problem in ref_pa.problems.items():
            student_problem = student_pa.problems[problem_id]
            
            for subproblem_id, ref_subproblem in ref_problem.answers.items():
                student_solution = student_problem.answers[subproblem_id]
                
                # TODO: add solution matching logic here
                solution_id = 0
                ref_solution = ref_subproblem.solutions[solution_id]
                student_solution.set_solution_id(solution_id)

                # check rule by rule
                for id, rule in enumerate(ref_solution.rules):
                    inputs = format_inputs(
                        ref_problem.problem,
                        ref_solution,
                        student_solution,
                        id,
                    )
                    print(inputs["query"])
                    # call the grading api
                    response = completion_messages(inputs, self.grading_key)
                    process, score = self.parse_grading_response(response)
                    
                    print(f"Process: {process}")
                    print(f"Score: {score}")
                    if not rule.check_valid_score(score):
                        student_solution.set_error(f"Invalid score {score} for rule {rule.rule} (max {rule.score})")

                    student_solution.add_score(rule, process, score)
                
                student_solution.finalize(ref_solution.rules)

        return student_pa