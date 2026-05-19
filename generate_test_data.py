import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)
n = 300

# ── PII columns (for Data Privacy page) ──
ids = [f'EMP{str(i).zfill(4)}' for i in range(1, n+1)]
first_names = ['Alice','Bob','Carol','David','Eva','Frank','Grace','Henry','Iris','Jack']
last_names  = ['Johnson','Smith','White','Brown','Martinez','Lee','Kim','Wilson','Chen','Taylor']
names = [f'{random.choice(first_names)} {random.choice(last_names)}' for _ in range(n)]
emails = [f'{nm.split()[0].lower()}{random.randint(1,99)}@company.com' for nm in names]
phones = [f'+91-{random.randint(7000000000, 9999999999)}' for _ in range(n)]

# ── Categorical columns ──
depts  = np.random.choice(['Engineering','Sales','HR','Finance','Marketing','Operations'], n)
roles  = np.random.choice(['Junior','Senior','Lead','Manager','Director'], n, p=[0.3,0.3,0.2,0.15,0.05])
cities = np.random.choice(['Mumbai','Delhi','Bangalore','Hyderabad','Chennai','Kolkata','Pune'], n)
status = np.random.choice(['Active','On Leave','Probation','Resigned'], n, p=[0.7,0.1,0.15,0.05])

# ── Numeric columns ──
age        = np.random.normal(35, 8, n).clip(22, 65).astype(int).astype(float)
salary     = np.random.lognormal(11, 0.5, n).clip(20000, 500000).astype(int)   # right-skewed
score_1    = np.random.normal(72, 15, n).clip(0, 100).round(2)
score_2    = np.random.normal(68, 20, n).clip(0, 100).round(2)
experience = np.random.exponential(5, n).clip(0, 30).round(1)                  # right-skewed
projects   = np.random.poisson(4, n)
rating     = np.random.choice([1,2,3,4,5], n, p=[0.05,0.10,0.25,0.40,0.20])
bonus_pct  = np.random.normal(12, 5, n).clip(0, 40).round(2)

# ── Inject outliers (for Outlier tab) ──
for i in random.sample(range(n), 10):
    salary[i] = random.choice([1500, 1800000, 2000000])
for i in random.sample(range(n), 8):
    score_1[i] = random.choice([-80, 180, 250])

# ── Text columns with HTML and URLs (for Text Cleaning tab) ──
feedbacks = [
    'Great performance this quarter!',
    'Needs improvement in communication skills.',
    'Visit https://performance.company.com for full details.',
    'Excellent work on all project deliverables.',
    'Check http://hr-portal.com for the full review report.',
    'Shows strong leadership and teamwork qualities.',
    'Consistently meets targets and deadlines every cycle.',
    'Refer to the internal portal at www.company-portal.com',
    '<b>Outstanding</b> results this year, keep it up!',
    'Employee attended <br> mandatory compliance training.',
]
feedback = [random.choice(feedbacks) for _ in range(n)]
notes = list(np.random.choice(
    ['On track', 'At risk', 'Exceeding expectations', 'Needs coaching', ''],
    n, p=[0.4, 0.2, 0.2, 0.1, 0.1]
))

# ── Date columns (for Date/Time tab) ──
start = pd.date_range('2018-01-01', '2024-01-01', periods=n)
join_date        = [d.strftime('%Y-%m-%d') for d in start]
last_review_date = [
    f'{random.randint(2022,2024)}-{str(random.randint(1,12)).zfill(2)}-{str(random.randint(1,28)).zfill(2)}'
    for _ in range(n)
]

# ── Introduce missing values ──
for i in random.sample(range(n), 50):  age[i]        = np.nan   # 16% missing
for i in random.sample(range(n), 34):  depts[i]      = None     # 11% missing
for i in random.sample(range(n), 22):  score_1[i]    = np.nan   #  7% missing
for i in random.sample(range(n), 15):  experience[i] = np.nan   #  5% missing
for i in random.sample(range(n), 8):   bonus_pct[i]  = np.nan   #  3% missing

depts = list(depts)

df = pd.DataFrame({
    'employee_id':      ids,
    'full_name':        names,
    'email':            emails,
    'phone':            phones,
    'department':       depts,
    'role':             roles,
    'city':             cities,
    'employment_status':status,
    'age':              age,
    'salary':           salary,
    'experience_years': experience,
    'score_1':          score_1,
    'score_2':          score_2,
    'projects_completed': projects,
    'performance_rating': rating,
    'bonus_pct':        bonus_pct,
    'feedback':         feedback,
    'notes':            notes,
    'join_date':        join_date,
    'last_review_date': last_review_date,
})

# ── Add 15 duplicate rows (for Duplicates tab) ──
dup_rows = df.sample(15, random_state=42)
df = pd.concat([df, dup_rows], ignore_index=True)

df.to_csv('test_dataset.csv', index=False)
print(f'Done: {len(df)} rows x {df.shape[1]} columns')
print(f'Missing values: {df.isnull().sum().sum()}')
print(f'Duplicates: {df.duplicated().sum()}')
print('Columns:', list(df.columns))
