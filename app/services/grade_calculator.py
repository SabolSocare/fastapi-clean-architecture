from app.models.student import GradeEnum, ClassTypeEnum


class GradeCalculator:
    """Service for calculating student grades based on total scores."""
    
    # Grade thresholds based on percentage of total possible score
    # These can be adjusted based on your grading system
    GRADE_THRESHOLDS = {
        GradeEnum.A: 90.0,  # 90% and above
        GradeEnum.B: 80.0,  # 80-89%
        GradeEnum.C: 70.0,  # 70-79%
        GradeEnum.D: 60.0,  # 60-69%
        GradeEnum.E: 50.0,  # 50-59%
        GradeEnum.F: 0.0,   # Below 50%
    }
    
    @staticmethod
    def calculate_foreign_language_bonus(score: float) -> float:
        """Calculate foreign language bonus score.
        Only scores above 25 contribute to total.
        Each point above 25 adds 1 bonus point.
        Example: 26 adds 1, 30 adds 5, 40 adds 15, 25 or below adds 0.
        """
        if score is None:
            return 0.0
        if score > 25.0:
            return float(score - 25.0)
        return 0.0
    
    @staticmethod
    def calculate_total_score(student) -> float:
        """Calculate total score from all subjects based on class type."""
        # Calculate foreign language bonus (common for both classes)
        foreign_lang_bonus = GradeCalculator.calculate_foreign_language_bonus(student.foreign_language_score)
        
        if student.class_type == ClassTypeEnum.SCIENCE:
            # Science class: Math, Chemistry, Physics, Biology, Khmer, History + Foreign Language bonus
            return (
                student.math_score +
                (student.chemistry_score or 0.0) +
                (student.physics_score or 0.0) +
                (student.biology_score or 0.0) +
                (student.khmer_score or 0.0) +
                (student.history_score or 0.0) +
                foreign_lang_bonus
            )
        else:
            # Social Science class: Khmer, Math, History, Geography, Ethics, Earth Science + Foreign Language bonus
            return (
                (student.khmer_score or 0.0) +
                student.math_score +
                (student.history_score or 0.0) +
                (student.geography_score or 0.0) +
                (student.ethics_score or 0.0) +
                student.earth_science_score +
                foreign_lang_bonus
            )
    
    @staticmethod
    def calculate_max_score(student) -> float:
        """Calculate maximum possible score from all subjects based on class type."""
        # Maximum foreign language bonus is 25 (50 - 25)
        max_foreign_lang_bonus = 25.0
        
        if student.class_type == ClassTypeEnum.SCIENCE:
            # Science class max scores + foreign language max bonus
            return (
                student.math_max +
                (student.chemistry_max or 75.0) +
                (student.physics_max or 75.0) +
                (student.biology_max or 75.0) +
                (student.khmer_max or 75.0) +
                (student.history_max or 50.0) +
                max_foreign_lang_bonus
            )
        else:
            # Social Science class max scores + foreign language max bonus
            return (
                (student.khmer_max or 125.0) +
                student.math_max +
                (student.history_max or 75.0) +
                (student.geography_max or 75.0) +
                (student.ethics_max or 75.0) +
                student.earth_science_max +
                max_foreign_lang_bonus
            )
    
    @staticmethod
    def calculate_average(student) -> float:
        """Calculate average score as percentage.
        Average is calculated based on 475 (base subjects max).
        If total score exceeds 475, average is capped at 100%.
        """
        total_score = GradeCalculator.calculate_total_score(student)
        base_max = 475.0  # Maximum score from base subjects only
        
        # Cap the average at 100% if score exceeds 475
        if total_score >= base_max:
            return 100.0
        
        return (total_score / base_max) * 100.0
    
    @staticmethod
    def calculate_grade(student) -> GradeEnum:
        """Calculate grade based on average percentage."""
        average = GradeCalculator.calculate_average(student)
        
        if average >= GradeCalculator.GRADE_THRESHOLDS[GradeEnum.A]:
            return GradeEnum.A
        elif average >= GradeCalculator.GRADE_THRESHOLDS[GradeEnum.B]:
            return GradeEnum.B
        elif average >= GradeCalculator.GRADE_THRESHOLDS[GradeEnum.C]:
            return GradeEnum.C
        elif average >= GradeCalculator.GRADE_THRESHOLDS[GradeEnum.D]:
            return GradeEnum.D
        elif average >= GradeCalculator.GRADE_THRESHOLDS[GradeEnum.E]:
            return GradeEnum.E
        else:
            return GradeEnum.F
    
    @staticmethod
    def is_passing(grade: GradeEnum) -> bool:
        """Check if a grade is passing (A, B, C, D, E are passing, F is failing)."""
        return grade != GradeEnum.F
    
    @staticmethod
    def update_student_grades(student):
        """Update all calculated fields for a student."""
        student.total_score = GradeCalculator.calculate_total_score(student)
        student.average_score = GradeCalculator.calculate_average(student)
        student.grade = GradeCalculator.calculate_grade(student)

