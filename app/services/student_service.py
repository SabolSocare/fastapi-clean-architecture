from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc, asc
from app.models.student import Student, GradeEnum, ClassTypeEnum
from app.services.grade_calculator import GradeCalculator
from typing import Optional, List
from app.schemas.student import StudentCreate, StudentUpdate, StudentStats


class StudentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def list_students(self) -> List[Student]:
        """Get all students from database."""
        result = await self.db.execute(select(Student).order_by(Student.id))
        students = result.scalars().all()
        return list(students)
    
    async def list_students_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        search: Optional[str] = None,
        grade: Optional[str] = None,
        class_type: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> dict:
        """Get students with pagination, filtering, and sorting."""
        # Base query
        query = select(Student)
        
        # Apply search filter (name)
        if search and search.strip():
            search_term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Student.first_name.ilike(search_term),
                    Student.last_name.ilike(search_term),
                    func.concat(Student.first_name, ' ', Student.last_name).ilike(search_term)
                )
            )
        
        # Apply grade filter
        if grade and grade in ['A', 'B', 'C', 'D', 'E', 'F']:
            query = query.where(Student.grade == grade)
        
        # Apply class_type filter
        if class_type and class_type.strip():
            query = query.where(Student.class_type == class_type.strip())
        
        # Apply sorting
        if sort_by:
            sort_column = getattr(Student, sort_by, None)
            if sort_column is not None:
                if sort_order == "desc":
                    query = query.order_by(desc(sort_column))
                else:
                    query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(Student.id)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        # Execute query
        result = await self.db.execute(query)
        students = result.scalars().all()
        
        # Convert to list of Student objects (already ORM models, will be serialized by Pydantic)
        return {
            "items": list(students),
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    async def get_student(self, student_id: int) -> Optional[Student]:
        """Get a specific student by ID."""
        result = await self.db.execute(
            select(Student).where(Student.id == student_id)
        )
        return result.scalar_one_or_none()
    
    async def create_student(self, student_data: StudentCreate) -> Student:
        """Create a new student with grade calculations."""
        # Adjust max scores based on class_type
        if student_data.class_type == ClassTypeEnum.SOCIAL_SCIENCE:
            # Social Science: khmer_max=125, math_max=75
            khmer_max = 125.0
            math_max = 75.0
            history_max = 75.0
        else:  # ClassTypeEnum.SCIENCE
            # Science: math_max=125, khmer_max=75, history_max=50
            khmer_max = 75.0
            math_max = 125.0
            history_max = 50.0
        
        db_student = Student(
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            gender=student_data.gender,
            class_type=student_data.class_type,
            khmer_score=student_data.khmer_score,
            math_score=student_data.math_score,
            history_score=student_data.history_score,
            geography_score=student_data.geography_score,
            ethics_score=student_data.ethics_score,
            earth_science_score=student_data.earth_science_score,
            chemistry_score=student_data.chemistry_score,
            physics_score=student_data.physics_score,
            biology_score=student_data.biology_score,
            physical_education_score=student_data.physical_education_score,
            foreign_language_score=student_data.foreign_language_score,
            khmer_max=khmer_max,
            math_max=math_max,
            history_max=history_max,
            geography_max=student_data.geography_max,
            ethics_max=student_data.ethics_max,
            earth_science_max=student_data.earth_science_max,
            chemistry_max=student_data.chemistry_max,
            physics_max=student_data.physics_max,
            biology_max=student_data.biology_max,
            physical_education_max=student_data.physical_education_max,
            foreign_language_max=student_data.foreign_language_max,
        )
        
        # Calculate grades
        GradeCalculator.update_student_grades(db_student)
        
        self.db.add(db_student)
        await self.db.commit()
        await self.db.refresh(db_student)
        return db_student
    
    async def update_student(
        self, student_id: int, student_data: StudentUpdate
    ) -> Optional[Student]:
        """Update a student and recalculate grades."""
        student = await self.get_student(student_id)
        if not student:
            return None
        
        # Update fields if provided
        update_data = student_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(student, field, value)
        
        # Recalculate grades after update
        GradeCalculator.update_student_grades(student)
        
        await self.db.commit()
        await self.db.refresh(student)
        return student
    
    async def delete_student(self, student_id: int) -> bool:
        """Delete a student."""
        student = await self.get_student(student_id)
        if not student:
            return False
        
        await self.db.delete(student)
        await self.db.commit()
        return True
    
    async def get_statistics(self) -> StudentStats:
        """Get statistics about all students."""
        # Get all students
        students = await self.list_students()
        total_students = len(students)
        
        # Count pass/fail
        pass_count = sum(
            1 for s in students 
            if s.grade and GradeCalculator.is_passing(s.grade)
        )
        fail_count = total_students - pass_count
        
        # Grade distribution
        grade_distribution = {grade.value: 0 for grade in GradeEnum}
        for student in students:
            if student.grade:
                grade_distribution[student.grade.value] += 1
        
        # Subject statistics (pass/fail per subject)
        # A subject is passing if score >= 50% of max
        subject_stats = {
            "khmer": {"pass": 0, "fail": 0},
            "math": {"pass": 0, "fail": 0},
            "history": {"pass": 0, "fail": 0},
            "geography": {"pass": 0, "fail": 0},
            "ethics": {"pass": 0, "fail": 0},
            "earth_science": {"pass": 0, "fail": 0},
        }
        
        for student in students:
            subjects = [
                ("khmer", student.khmer_score, student.khmer_max),
                ("math", student.math_score, student.math_max),
                ("history", student.history_score, student.history_max),
                ("geography", student.geography_score, student.geography_max),
                ("ethics", student.ethics_score, student.ethics_max),
                ("earth_science", student.earth_science_score, student.earth_science_max),
            ]
            
            for subject_name, score, max_score in subjects:
                if max_score > 0:
                    percentage = (score / max_score) * 100
                    if percentage >= 50:
                        subject_stats[subject_name]["pass"] += 1
                    else:
                        subject_stats[subject_name]["fail"] += 1
        
        return StudentStats(
            total_students=total_students,
            pass_count=pass_count,
            fail_count=fail_count,
            grade_distribution=grade_distribution,
            subject_stats=subject_stats,
        )

    async def get_detailed_statistics(self, class_type: Optional[str] = None) -> dict:
        """Get detailed analytics with subject averages, score distributions, and demographics."""
        # Get all students or filter by class_type
        query = select(Student)
        if class_type:
            query = query.where(Student.class_type == class_type)
        
        result = await self.db.execute(query)
        students = list(result.scalars().all())
        
        if not students:
            return {
                "total_students": 0,
                "subject_averages": {},
                "score_distribution": {},
                "gender_stats": {},
                "performance_tiers": {}
            }
        
        # Determine subjects based on class_type
        if class_type == 'science':
            subjects = ['math', 'chemistry', 'physics', 'biology', 'khmer', 'history', 'foreign_language']
        elif class_type == 'social_science':
            subjects = ['khmer', 'math', 'history', 'geography', 'ethics', 'earth_science', 'foreign_language']
        else:
            # All subjects
            subjects = ['khmer', 'math', 'history', 'geography', 'ethics', 'earth_science', 
                       'chemistry', 'physics', 'biology', 'foreign_language']
        
        # Calculate subject averages and score distributions
        subject_averages = {}
        score_distribution = {}
        
        for subject in subjects:
            score_attr = f"{subject}_score"
            max_attr = f"{subject}_max"
            
            scores = []
            max_scores = []
            for student in students:
                max_score = getattr(student, max_attr, 0)
                if max_score > 0:  # Only include if subject is applicable
                    score = getattr(student, score_attr, 0)
                    scores.append(score)
                    max_scores.append(max_score)
            
            if scores:
                # Use the first max_score as reference (should be consistent for all students)
                subject_max = max_scores[0] if max_scores else 100
                
                subject_averages[subject] = {
                    "average": round(sum(scores) / len(scores), 2),
                    "highest": round(max(scores), 2),
                    "lowest": round(min(scores), 2),
                    "total_students": len(scores),
                    "max_score": subject_max
                }
                
                # Score ranges based on percentage: 0-24%, 25-49%, 50-74%, 75-100%
                ranges = {"0-24%": 0, "25-49%": 0, "50-74%": 0, "75-100%": 0}
                for score in scores:
                    percentage = (score / subject_max) * 100
                    if percentage < 25:
                        ranges["0-24%"] += 1
                    elif percentage < 50:
                        ranges["25-49%"] += 1
                    elif percentage < 75:
                        ranges["50-74%"] += 1
                    else:  # 75-100%
                        ranges["75-100%"] += 1
                
                score_distribution[subject] = ranges
        
        # Gender-based statistics
        gender_stats = {
            "male": {"count": 0, "average": 0, "pass": 0},
            "female": {"count": 0, "average": 0, "pass": 0}
        }
        
        male_students = [s for s in students if s.gender == 'M']
        female_students = [s for s in students if s.gender == 'F']
        
        if male_students:
            gender_stats["male"]["count"] = len(male_students)
            gender_stats["male"]["average"] = round(
                sum(s.average_score for s in male_students) / len(male_students), 2
            )
            gender_stats["male"]["pass"] = sum(
                1 for s in male_students if s.grade and GradeCalculator.is_passing(s.grade)
            )
        
        if female_students:
            gender_stats["female"]["count"] = len(female_students)
            gender_stats["female"]["average"] = round(
                sum(s.average_score for s in female_students) / len(female_students), 2
            )
            gender_stats["female"]["pass"] = sum(
                1 for s in female_students if s.grade and GradeCalculator.is_passing(s.grade)
            )
        
        # Performance tiers (based on average score)
        performance_tiers = {
            "excellent": 0,   # 90-100%
            "good": 0,        # 75-89%
            "average": 0,     # 60-74%
            "below_average": 0,  # 50-59%
            "poor": 0         # <50%
        }
        
        for student in students:
            avg = student.average_score
            if avg >= 90:
                performance_tiers["excellent"] += 1
            elif avg >= 75:
                performance_tiers["good"] += 1
            elif avg >= 60:
                performance_tiers["average"] += 1
            elif avg >= 50:
                performance_tiers["below_average"] += 1
            else:
                performance_tiers["poor"] += 1
        
        # Grade distribution
        grade_distribution = {grade.value: 0 for grade in GradeEnum}
        for student in students:
            if student.grade:
                grade_distribution[student.grade.value] += 1
        
        return {
            "total_students": len(students),
            "subject_averages": subject_averages,
            "score_distribution": score_distribution,
            "gender_stats": gender_stats,
            "performance_tiers": performance_tiers,
            "grade_distribution": grade_distribution
        }

