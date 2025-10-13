import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os

# (Paste all your generate_attendance_data, generate_center_diary_data, 
# generate_grades_data, and generate_centre_progress_data functions here)

def generate_attendance_data():
    """Generate sample attendance data"""
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    centers = ['Pune-01', 'Pune-12', 'Mumbai-03', 'Delhi-05', 'Bangalore-07']
    cities = ['Pune', 'Pune', 'Mumbai', 'Delhi', 'Bangalore']
    grades = ['LKG', 'UKG', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th']

    data = []
    students = [
        ('Rahul Kumar', 'Pune-01', 'Pune', '6th'), ('Priya Shah', 'Mumbai-03', 'Mumbai', '7th'),
        ('Amit Patel', 'Pune-12', 'Pune', '5th'), ('Neha Sharma', 'Delhi-05', 'Delhi', '6th'),
        ('Rohan Verma', 'Bangalore-07', 'Bangalore', '8th'), ('Anita Roy', 'Pune-01', 'Pune', '6th'),
        ('Sanjay Kumar', 'Mumbai-03', 'Mumbai', '7th'), ('Meera Desai', 'Pune-12', 'Pune', '5th')
    ]

    for student_name, center, city, grade in students:
        base_attendance = np.random.uniform(0.65, 0.95)
        for date in dates:
            attendance = min(1.0, max(0, base_attendance + np.random.normal(0, 0.1)))
            data.append({
                'date': date, 'student_name': student_name, 'center': center, 'city': city,
                'grade': grade, 'present': 1 if np.random.random() < attendance else 0
            })
    return pd.DataFrame(data)

def generate_center_diary_data():
    """Generate sample center diary data"""
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    centers = ['Pune-01', 'Pune-12', 'Mumbai-03', 'Delhi-05', 'Bangalore-07']
    cities = ['Pune', 'Pune', 'Mumbai', 'Delhi', 'Bangalore']
    volunteers = ['Rajesh Sharma', 'Meena Patel', 'Suresh Kumar', 'Anita Desai', 'Vikram Singh']
    subjects = ['English', 'Maths', 'Language', 'GK']
    data = []
    for date in dates:
        for center, city in zip(centers, cities):
            if np.random.random() > 0.2:
                num_classes = np.random.randint(1, 5)
                students_present = np.random.randint(15, 40)
                for _ in range(num_classes):
                    data.append({
                        'date': date, 'center': center, 'city': city, 'volunteer': np.random.choice(volunteers),
                        'subject': np.random.choice(subjects), 'students_present': students_present,
                        'homework_given': np.random.choice([True, False], p=[0.7, 0.3]),
                        'pt_done': np.random.choice([True, False], p=[0.4, 0.6]),
                        'prayer_done': np.random.choice([True, False], p=[0.5, 0.5]),
                        'extra_activity': np.random.choice([True, False], p=[0.3, 0.7])
                    })
    return pd.DataFrame(data)

def generate_grades_data():
    """Generate sample grades data"""
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    students = [
        ('Rahul Kumar', 'Pune-01', 'Pune', '6th'), ('Priya Shah', 'Mumbai-03', 'Mumbai', '7th'),
        ('Amit Patel', 'Pune-12', 'Pune', '5th'), ('Neha Sharma', 'Delhi-05', 'Delhi', '6th'),
        ('Rohan Verma', 'Bangalore-07', 'Bangalore', '8th'), ('Anita Roy', 'Pune-01', 'Pune', '6th'),
        ('Sanjay Kumar', 'Mumbai-03', 'Mumbai', '7th'), ('Meera Desai', 'Pune-12', 'Pune', '5th')
    ]
    subjects = {'English': (0, 50), 'Maths': (0, 50), 'Language': (0, 50), 'GK': (0, 50)}
    data = []
    for student_name, center, city, grade in students:
        base_performance = np.random.uniform(0.6, 0.9)
        for date in dates:
            for subject, (min_marks, max_marks) in subjects.items():
                performance_factor = base_performance + np.random.normal(0, 0.1)
                marks = int(performance_factor * max_marks)
                marks = min(max_marks, max(min_marks, marks))
                data.append({
                    'date': date, 'student_name': student_name, 'center': center, 'city': city,
                    'grade': grade, 'subject': subject, 'marks': marks, 'max_marks': max_marks
                })
    return pd.DataFrame(data)

# In generate_mock_data.py

def generate_centre_progress_data():
    """Generate mock data for centre progress dashboard"""
    centers = ['Pune-01', 'Pune-12', 'Mumbai-03', 'Delhi-05', 'Bangalore-07']
    cities = ['Pune', 'Pune', 'Mumbai', 'Delhi', 'Bangalore']
    start, end = datetime(2024, 1, 1), datetime(2024, 12, 31)
    
    center_info = pd.DataFrame({
        'center': centers, 'city': cities, 
        'lat': [18.5204, 18.5204, 19.0760, 28.7041, 12.9716], 
        'lon': [73.8567, 73.8567, 72.8777, 77.1025, 77.5946]
    })
    
    months = pd.date_range(start=start, end=end, freq='M')
    
    expense_rows = []
    for center in centers:
        monthly_base = np.random.randint(20000, 60000)
        for m in months:
            amount = int(max(0, monthly_base + np.random.normal(0, monthly_base * 0.2)))
            expense_rows.append({
                'center': center, 'date': m, 'amount': amount, 
                'type': np.random.choice(['Rent', 'Stationery', 'Snacks', 'Utilities', 'Transport']), 
                'remarks': ''
            })
    expenses = pd.DataFrame(expense_rows)
    
    volunteers, visitors, activity_rows, problems, requirements = [], [], [], [], []
    volunteer_names = ['Rajesh Sharma', 'Meena Patel', 'Suresh Kumar', 'Anita Desai', 'Vikram Singh', 'Ritu Jain', 'Deepak Rao']
    visitor_types = ['Donor', 'Local Leader', 'Partner', 'Inspector']

    for center in centers:
        for _ in range(np.random.randint(5, 12)):
            volunteers.append({
                'center': center, 'name': np.random.choice(volunteer_names), 
                'hours': round(np.random.uniform(1, 6), 1), 
                'subject': np.random.choice(['English', 'Maths', 'Language', 'GK']), 
                'date': start + timedelta(days=np.random.randint(0, 365))
            })
        for _ in range(np.random.randint(3, 10)):
            visitors.append({
                'center': center, 'name': 'Visitor ' + str(np.random.randint(1, 200)), 
                'type': np.random.choice(visitor_types), 
                'purpose': np.random.choice(['Visit', 'Donation', 'Check', 'Meeting']), 
                'date': start + timedelta(days=np.random.randint(0, 365))
            })
        for m in months:
            activity_rows.append({
                'center': center, 
                'date': m, 
                'classes': np.random.randint(10, 80),
                'homework_done_pct': round(np.random.uniform(0.4, 0.95), 2),
                'pt_done_pct': round(np.random.uniform(0.2, 0.9), 2),
                # --- ADDED THESE TWO LINES ---
                'prayer_done_pct': round(np.random.uniform(0.3, 0.95), 2),
                'extra_activity_pct': round(np.random.uniform(0.05, 0.6), 2)
            })
        for _ in range(np.random.randint(1, 6)):
            problems.append({
                'center': center, 'date': start + timedelta(days=np.random.randint(0, 365)), 
                'type': np.random.choice(['Staff Shortage', 'Material Shortage', 'Low Attendance']), 
                'notes': 'Auto-generated problem note'
            })
        for _ in range(np.random.randint(1, 6)):
            requirements.append({
                'center': center, 
                'item': np.random.choice(['Books', 'Stationery', 'Projector', 'Chairs', 'Snacks']), 
                'qty': np.random.randint(1, 50), 
                'priority': np.random.choice(['High', 'Medium', 'Low'])
            })
            
    return {
        'center_info': center_info, 
        'expenses': expenses, 
        'volunteers': pd.DataFrame(volunteers), 
        'visitors': pd.DataFrame(visitors), 
        'activities': pd.DataFrame(activity_rows), 
        'problems': pd.DataFrame(problems), 
        'requirements': pd.DataFrame(requirements)
    }

if __name__ == "__main__":
    DATA_DIR = "data"
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Generating and saving data files...")

    generate_attendance_data().to_csv(os.path.join(DATA_DIR, "attendance.csv"), index=False)
    print("✅ Saved attendance.csv")
    generate_grades_data().to_csv(os.path.join(DATA_DIR, "grades.csv"), index=False)
    print("✅ Saved grades.csv")
    generate_center_diary_data().to_csv(os.path.join(DATA_DIR, "center_diary.csv"), index=False)
    print("✅ Saved center_diary.csv")

    centre_data = generate_centre_progress_data()
    for name, df in centre_data.items():
        df.to_csv(os.path.join(DATA_DIR, f"{name}.csv"), index=False)
        print(f"✅ Saved {name}.csv")

    print("\nAll data files generated in the 'data/' folder.")