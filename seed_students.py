"""
Script to seed the database with 20 sample students with scores.
Run this script to populate the database with example data.
"""
import asyncio
import random
from app.db.session import AsyncSessionLocal
from app.models.student import Student, GenderEnum
from app.services.grade_calculator import GradeCalculator

# Sample Khmer names
FIRST_NAMES = [
    "សុខា", "រតនា", "សុផល", "វិចិត្រ", "សុខុម", "ចន្ថា", "សុខុន", 
    "វិទូ", "សុខុន", "ចន្ថា", "សុខា", "រតនា", "សុផល", "វិចិត្រ",
    "មុនី", "រតនៈ", "សុខុម", "ចន្ថា", "សុខុន", "វិទូ"
]

LAST_NAMES = [
    "ជ័យ", "ម៉ម", "សុខ", "រតនៈ", "សុផល", "វិចិត្រ", "សុខុម",
    "ចន្ថា", "សុខុន", "វិទូ", "មុនី", "រតនៈ", "សុខុម", "ចន្ថា",
    "សុខុន", "វិទូ", "មុនី", "រតនៈ", "សុខុម", "ចន្ថា"
]

async def create_sample_students():
    """Create 20 sample students with random scores."""
    async with AsyncSessionLocal() as db:
        # Check if students already exist
        from sqlalchemy import select
        result = await db.execute(select(Student))
        existing = result.scalars().all()
        
        if len(existing) >= 20:
            print(f"✓ Database already has {len(existing)} students. Skipping seed.")
            return
        
        print("Creating 20 sample students...")
        
        students_created = 0
        for i in range(20):
            # Random gender
            gender = random.choice([GenderEnum.MALE, GenderEnum.FEMALE])
            
            # Random first and last name
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            
            # Generate realistic scores (some students do better than others)
            # Create a mix of high, medium, and low performers
            performance_level = random.choice(['high', 'medium', 'low', 'very_low'])
            
            if performance_level == 'high':
                # High performers: 70-100% of max
                khmer_score = random.uniform(87, 125)
                math_score = random.uniform(52, 75)
                history_score = random.uniform(52, 75)
                geography_score = random.uniform(52, 75)
                ethics_score = random.uniform(52, 75)
                earth_science_score = random.uniform(35, 50)
            elif performance_level == 'medium':
                # Medium performers: 50-70% of max
                khmer_score = random.uniform(62, 87)
                math_score = random.uniform(37, 52)
                history_score = random.uniform(37, 52)
                geography_score = random.uniform(37, 52)
                ethics_score = random.uniform(37, 52)
                earth_science_score = random.uniform(25, 35)
            elif performance_level == 'low':
                # Low performers: 30-50% of max
                khmer_score = random.uniform(37, 62)
                math_score = random.uniform(22, 37)
                history_score = random.uniform(22, 37)
                geography_score = random.uniform(22, 37)
                ethics_score = random.uniform(22, 37)
                earth_science_score = random.uniform(15, 25)
            else:  # very_low
                # Very low performers: 0-30% of max
                khmer_score = random.uniform(0, 37)
                math_score = random.uniform(0, 22)
                history_score = random.uniform(0, 22)
                geography_score = random.uniform(0, 22)
                ethics_score = random.uniform(0, 22)
                earth_science_score = random.uniform(0, 15)
            
            # Create student - SQLAlchemy should handle the enum automatically
            # But we'll pass the enum object directly
            student = Student(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                khmer_score=round(khmer_score, 2),
                math_score=round(math_score, 2),
                history_score=round(history_score, 2),
                geography_score=round(geography_score, 2),
                ethics_score=round(ethics_score, 2),
                earth_science_score=round(earth_science_score, 2),
                khmer_max=125.0,
                math_max=75.0,
                history_max=75.0,
                geography_max=75.0,
                ethics_max=75.0,
                earth_science_max=50.0,
            )
            
            # Calculate grades
            GradeCalculator.update_student_grades(student)
            
            db.add(student)
            students_created += 1
            print(f"  Created student {i+1}/20: {first_name} {last_name} - Grade: {student.grade.value if student.grade else 'N/A'}")
        
        await db.commit()
        print(f"\n✓ Successfully created {students_created} students!")
        print("✓ All grades have been automatically calculated.")

if __name__ == "__main__":
    asyncio.run(create_sample_students())

