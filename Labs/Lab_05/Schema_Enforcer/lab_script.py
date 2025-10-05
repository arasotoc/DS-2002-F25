import csv
import json
import pandas as pd

Dataset=[
    {"student_id":1, "major":"CS", "GPA":3.6, "is_cs_major": "Yes", "credits_taken": '18.0'},
    {"student_id":2, "major":"History", "GPA":3.6, "is_cs_major": "No", "credits_taken": '15.0'},
    {"student_id":3, "major":"Art", "GPA":3.1, "is_cs_major": "No", "credits_taken": '21.0'},
    {"student_id":4, "major":"CS", "GPA":3.3, "is_cs_major": "Yes", "credits_taken": '15.0'},
    {"student_id":5, "major":"Physics", "GPA":3.7, "is_cs_major": "No", "credits_taken": '15.0'},
]

with open("raw_survey_data.csv","w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["student_id","major","GPA", "is_cs_major", "credits_taken"])
    writer.writeheader()
    writer.writerows(Dataset)

courses = [
  {
    "course_id": "DS2002",
    "section": "001",
    "title": "Data Science Systems",
    "level": 200,
    "instructors": [
      {"name": "Austin Rivera", "role": "Primary"}, 
      {"name": "Heywood Williams-Tracy", "role": "TA"} 
    ]
  },
  {
    "course_id": "GD3100",
    "title": "Development on Ground",
    "level": 300,
    "instructors": [
      {"name": "David Edmunds", "role": "Primary"}
    ]
  },
  {
    "course_id": "DS2004",
    "title": "Data Ethics",
    "level": 200,
    "instructors": [
      {"name": "Emanuel Moss", "role": "Primary"},
      {"name": "Aniyah McWilliams", "role": "TA"}
    ]
  },
  {
    "course_id": "PL3200",
    "title": "African-American Political Thought",
    "level": 300,
    "instructors": [
      {"name": "Lawrie Balfour", "role": "Primary"},
      {"name": "Grace Stearns", "role": "TA"} 
    ]
  },
  {
    "course_id": "EN3500",
    "title": "Rhetoric of Crime",
    "level": 300,
    "instructors": [
      {"name": "Rhiannon Goad", "role": "Primary"}
    ]
  }
]

with open("raw_course_catalog.json","w") as f:
    json.dump(courses, f, indent=4)

df = pd.read_csv("raw_survey_data.csv")

df["is_cs_major"] = df["is_cs_major"].replace({"Yes": True, "No": False})

df = df.astype({"GPA": 'float64', "credits_taken": 'float64'})

df.to_csv("clean_survey_data.csv", index=False)

with open("raw_course_catalog.json","r") as f:
    data = json.load(f)

df_json = pd.json_normalize(data, record_path=['instructors'], meta=['course_id', 'title', 'level'])

df_json.to_csv("clean_course_catalog.csv", index=False)

