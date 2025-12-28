from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class GenderEnum(str, enum.Enum):
    MALE = "M"
    FEMALE = "F"


class GradeEnum(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"


class ClassTypeEnum(str, enum.Enum):
    SOCIAL_SCIENCE = "social_science"
    SCIENCE = "science"


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(Enum(GenderEnum, values_callable=lambda x: [e.value for e in x]), nullable=False)
    class_type = Column(Enum(ClassTypeEnum, values_callable=lambda x: [e.value for e in x]), nullable=False, default=ClassTypeEnum.SOCIAL_SCIENCE)
    
    # Social Science subjects (ថ្នាក់សង្គមវិទ្យា)
    khmer_score = Column(Float, default=0.0)
    math_score = Column(Float, default=0.0)
    history_score = Column(Float, default=0.0)
    geography_score = Column(Float, default=0.0)
    ethics_score = Column(Float, default=0.0)
    earth_science_score = Column(Float, default=0.0)
    
    # Science subjects (ថ្នាក់វិទ្យាសាស្ត្រ) - reuse some fields
    # math_score is shared
    chemistry_score = Column(Float, default=0.0, nullable=True)  # គីមីវិទ្យា
    physics_score = Column(Float, default=0.0, nullable=True)    # គ្រឹស្តវិទ្យា
    biology_score = Column(Float, default=0.0, nullable=True)    # ជីវវិទ្យា
    physical_education_score = Column(Float, default=0.0, nullable=True)  # សិល្បៈ កាយវិការ
    # earth_science_score is shared
    
    # Common subject for both tracks
    foreign_language_score = Column(Float, default=0.0)  # ភាសាបរទេស (Foreign Language)
    
    # Maximum scores for Social Science subjects
    khmer_max = Column(Float, default=125.0)
    math_max = Column(Float, default=75.0)
    history_max = Column(Float, default=75.0)
    geography_max = Column(Float, default=75.0)
    ethics_max = Column(Float, default=75.0)
    earth_science_max = Column(Float, default=50.0)
    
    # Maximum scores for Science subjects
    chemistry_max = Column(Float, default=75.0, nullable=True)
    physics_max = Column(Float, default=75.0, nullable=True)
    biology_max = Column(Float, default=75.0, nullable=True)
    physical_education_max = Column(Float, default=75.0, nullable=True)
    
    # Common subject max score
    foreign_language_max = Column(Float, default=50.0)
    
    # Calculated fields
    total_score = Column(Float, default=0.0)
    average_score = Column(Float, default=0.0)
    grade = Column(Enum(GradeEnum), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

