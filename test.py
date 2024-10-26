from instance.problem import StudentPA
from instance.ref_problem import RefPA

import os
base_path = os.path.dirname(os.path.realpath(__file__))

ref_path = "data/1/refs/HW1.json"
student_path = "data/1/raw/example.json"
ref_path = os.path.join(base_path, ref_path)
student_path = os.path.join(base_path, student_path)

ref_pa = RefPA.from_json(ref_path)
student_pa = StudentPA.from_json(student_path)

key_path = "configs/grading_key.txt"
app_key = open(key_path, "r").read().strip()

from checker.example_checker import ExampleChecker
checker = ExampleChecker(app_key)

student_pa = checker.check(ref_pa, student_pa)
