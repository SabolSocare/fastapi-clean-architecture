"""
Script to clear all students and seed with realistic exam scores.
Creates 20 Social Science students and 20 Science students with standard exam score distributions.
Run: python seed_realistic_students.py
"""
import asyncio
from app.db.session import AsyncSessionLocal
from app.models.student import Student, GenderEnum, ClassTypeEnum
from app.services.grade_calculator import GradeCalculator
from sqlalchemy import select, delete

# Sample Khmer names
FIRST_NAMES_MALE = [
    "សុខា", "សុផល", "សុខុម", "សុខុន", "វិទូ", "វិចិត្រ", "ចន្ថា", "រតនៈ",
    "សុខិត", "វណ្णៈ", "ពិសិដ្ឋ", "សុវណ្ណ", "រតនៈ", "វិរៈ", "សុភា", "មុនី",
    "ប្រាក់", "ប៊ុន", "ចាន់", "សាន"
]

FIRST_NAMES_FEMALE = [
    "រតនា", "ចន្ថា", "សុភា", "វិចិត្រា", "សុខណា", "ពេជ្រ", "រស្មី", "លីដា",
    "សុផាត់", "មាលា", "រ៉ាណា", "ស្រីពៅ", "ដារ៉ា", "វិមាន", "សុខដា", "ពេជ្រាត់",
    "ច័ន្ទ", "គង់", "ផុន", "សុខ"
]

LAST_NAMES = [
    "ជ័យ", "ម៉ម", "សុខ", "រតនៈ", "សុផល", "វិចិត្រ", "សុខុម", "ចន្ថា",
    "សុខុន", "វិទូ", "មុនី", "គឹម", "ស៊ុន", "លី", "យិម", "ហុក",
    "ផាន់", "ឃុន", "ចាន់", "សាន"
]

def generate_realistic_score(max_score: float, grade_level: str) -> float:
    """
    Generate realistic exam scores based on grade level.
    Grade levels: 'excellent', 'good', 'average', 'below_average', 'poor'
    """
    import random
    
    if grade_level == 'excellent':  # 85-95% (A grade)
        percentage = random.uniform(0.85, 0.95)
    elif grade_level == 'good':  # 70-84% (B-C grade)
        percentage = random.uniform(0.70, 0.84)
    elif grade_level == 'average':  # 55-69% (D-E grade)
        percentage = random.uniform(0.55, 0.69)
    elif grade_level == 'below_average':  # 40-54% (E-F grade)
        percentage = random.uniform(0.40, 0.54)
    else:  # poor - 20-39% (F grade)
        percentage = random.uniform(0.20, 0.39)
    
    # Add slight variation to make it more realistic
    variation = random.uniform(-0.03, 0.03)
    final_percentage = max(0, min(1, percentage + variation))
    
    return round(max_score * final_percentage, 2)

def generate_foreign_language_score(grade_level: str) -> float:
    """
    Generate foreign language score (optional subject).
    Some students don't take it (score 0), others get varying scores.
    """
    import random
    
    # 30% of students don't take foreign language
    if random.random() < 0.3:
        return 0.0
    
    # For others, generate realistic scores (max 50)
    if grade_level == 'excellent':
        return round(random.uniform(38, 48), 2)
    elif grade_level == 'good':
        return round(random.uniform(28, 37), 2)
    elif grade_level == 'average':
        return round(random.uniform(20, 27), 2)
    else:
        return round(random.uniform(10, 19), 2)

async def clear_all_students():
    """Delete all existing students from database."""
    async with AsyncSessionLocal() as db:
        await db.execute(delete(Student))
        await db.commit()
        print("✓ Cleared all existing students")

async def create_social_science_students():
    """Create 20 Social Science students with realistic scores."""
    import random
    
    async with AsyncSessionLocal() as db:
        print("\n📚 Creating Social Science students...")
        
        # Define grade distribution (realistic distribution)
        grade_distribution = [
            'excellent',  # 1 student (5%)
            'good', 'good', 'good', 'good', 'good',  # 5 students (25%)
            'average', 'average', 'average', 'average', 'average', 'average', 'average',  # 7 students (35%)
            'below_average', 'below_average', 'below_average', 'below_average',  # 4 students (20%)
            'poor', 'poor', 'poor'  # 3 students (15%)
        ]
        
        random.shuffle(grade_distribution)
        
        for i in range(20):
            # Random gender
            gender = random.choice([GenderEnum.MALE, GenderEnum.FEMALE])
            
            # Select name based on gender
            if gender == GenderEnum.MALE:
                first_name = random.choice(FIRST_NAMES_MALE)
            else:
                first_name = random.choice(FIRST_NAMES_FEMALE)
            
            last_name = random.choice(LAST_NAMES)
            
            # Get grade level for this student
            grade_level = grade_distribution[i]
            
            # Generate scores for Social Science subjects
            khmer_score = generate_realistic_score(125.0, grade_level)
            math_score = generate_realistic_score(75.0, grade_level)
            history_score = generate_realistic_score(75.0, grade_level)
            geography_score = generate_realistic_score(75.0, grade_level)
            ethics_score = generate_realistic_score(75.0, grade_level)
            earth_science_score = generate_realistic_score(50.0, grade_level)
            foreign_language_score = generate_foreign_language_score(grade_level)
            
            # Create student
            student = Student(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                class_type=ClassTypeEnum.SOCIAL_SCIENCE,
                khmer_score=khmer_score,
                math_score=math_score,
                history_score=history_score,
                geography_score=geography_score,
                ethics_score=ethics_score,
                earth_science_score=earth_science_score,
                foreign_language_score=foreign_language_score,
                # Set max scores for Social Science
                khmer_max=125.0,
                math_max=75.0,
                history_max=75.0,
                geography_max=75.0,
                ethics_max=75.0,
                earth_science_max=50.0,
                foreign_language_max=50.0,
            )
            
            # Calculate grades
            GradeCalculator.update_student_grades(student)
            
            db.add(student)
            print(f"  {i+1}. {first_name} {last_name} ({gender.value}) - Grade: {student.grade.value if student.grade else 'N/A'} - Total: {student.total_score:.0f}")
        
        await db.commit()
        print("✓ Successfully created 20 Social Science students!")

async def create_science_students():
    """Create 20 Science students with realistic scores."""
    import random
    
    async with AsyncSessionLocal() as db:
        print("\n🔬 Creating Science students...")
        
        # Define grade distribution (realistic distribution)
        grade_distribution = [
            'excellent',  # 1 student (5%)
            'good', 'good', 'good', 'good', 'good',  # 5 students (25%)
            'average', 'average', 'average', 'average', 'average', 'average', 'average',  # 7 students (35%)
            'below_average', 'below_average', 'below_average', 'below_average',  # 4 students (20%)
            'poor', 'poor', 'poor'  # 3 students (15%)
        ]
        
        random.shuffle(grade_distribution)
        
        for i in range(20):
            # Random gender
            gender = random.choice([GenderEnum.MALE, GenderEnum.FEMALE])
            
            # Select name based on gender
            if gender == GenderEnum.MALE:
                first_name = random.choice(FIRST_NAMES_MALE)
            else:
                first_name = random.choice(FIRST_NAMES_FEMALE)
            
            last_name = random.choice(LAST_NAMES)
            
            # Get grade level for this student
            grade_level = grade_distribution[i]
            
            # Generate scores for Science subjects
            math_score = generate_realistic_score(125.0, grade_level)  # Math is 125 for Science
            chemistry_score = generate_realistic_score(75.0, grade_level)
            physics_score = generate_realistic_score(75.0, grade_level)
            biology_score = generate_realistic_score(75.0, grade_level)
            physical_education_score = generate_realistic_score(75.0, grade_level)
            earth_science_score = generate_realistic_score(50.0, grade_level)
            foreign_language_score = generate_foreign_language_score(grade_level)
            
            # Create student
            student = Student(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                class_type=ClassTypeEnum.SCIENCE,
                math_score=math_score,
                chemistry_score=chemistry_score,
                physics_score=physics_score,
                biology_score=biology_score,
                physical_education_score=physical_education_score,
                earth_science_score=earth_science_score,
                foreign_language_score=foreign_language_score,
                # Set max scores for Science
                math_max=125.0,
                chemistry_max=75.0,
                physics_max=75.0,
                biology_max=75.0,
                physical_education_max=75.0,
                earth_science_max=50.0,
                foreign_language_max=50.0,
            )
            
            # Calculate grades
            GradeCalculator.update_student_grades(student)
            
            db.add(student)
            print(f"  {i+1}. {first_name} {last_name} ({gender.value}) - Grade: {student.grade.value if student.grade else 'N/A'} - Total: {student.total_score:.0f}")
        
        await db.commit()
        print("✓ Successfully created 20 Science students!")

async def main():
    """Main function to clear and reseed database."""
    print("=" * 60)
    print("🔄 CLEARING AND RESEEDING DATABASE")
    print("=" * 60)
    
    # Clear existing data
    await clear_all_students()
    
    # Create new students
    await create_social_science_students()
    await create_science_students()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE SEEDING COMPLETE!")
    print("=" * 60)
    print("📊 Summary:")
    print("  - Social Science students: 20")
    print("  - Science students: 20")
    print("  - Total students: 40")
    print("  - Scores: Realistic exam distribution")
    print("  - Foreign Language: Optional (some students take it)")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
