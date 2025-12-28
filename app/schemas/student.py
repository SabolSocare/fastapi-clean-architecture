from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List
from app.models.student import GenderEnum, GradeEnum, ClassTypeEnum


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    gender: GenderEnum
    class_type: ClassTypeEnum = ClassTypeEnum.SOCIAL_SCIENCE
    foreign_language_score: float = 0.0


class StudentCreate(StudentBase):
    """Schema for creating a new student."""
    # Social Science subjects
    khmer_score: Optional[float] = Field(default=0.0, ge=0.0)
    math_score: float = Field(default=0.0, ge=0.0)  # Shared with Science
    history_score: Optional[float] = Field(default=0.0, ge=0.0)
    geography_score: Optional[float] = Field(default=0.0, ge=0.0)
    ethics_score: Optional[float] = Field(default=0.0, ge=0.0)
    earth_science_score: float = Field(default=0.0, ge=0.0)  # Shared with Science
    
    # Science subjects (optional, used only when class_type is SCIENCE)
    chemistry_score: Optional[float] = Field(default=0.0, ge=0.0)
    physics_score: Optional[float] = Field(default=0.0, ge=0.0)
    biology_score: Optional[float] = Field(default=0.0, ge=0.0)
    physical_education_score: Optional[float] = Field(default=0.0, ge=0.0)
    
    # Optional max scores for Social Science (defaults will be used if not provided)
    khmer_max: Optional[float] = Field(default=75.0, gt=0)
    math_max: Optional[float] = Field(default=125.0, gt=0)
    history_max: Optional[float] = Field(default=75.0, gt=0)
    geography_max: Optional[float] = Field(default=75.0, gt=0)
    ethics_max: Optional[float] = Field(default=75.0, gt=0)
    earth_science_max: Optional[float] = Field(default=50.0, gt=0)
    
    # Optional max scores for Science subjects
    chemistry_max: Optional[float] = Field(default=75.0, gt=0)
    physics_max: Optional[float] = Field(default=75.0, gt=0)
    biology_max: Optional[float] = Field(default=75.0, gt=0)
    physical_education_max: Optional[float] = Field(default=75.0, gt=0)
    
    # Foreign language max score (shared by both class types)
    foreign_language_max: Optional[float] = Field(default=50.0, gt=0)


class StudentUpdate(BaseModel):
    """Schema for updating student information."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[GenderEnum] = None
    class_type: Optional[ClassTypeEnum] = None
    
    # Social Science subjects
    khmer_score: Optional[float] = Field(default=None, ge=0.0)
    math_score: Optional[float] = Field(default=None, ge=0.0)
    history_score: Optional[float] = Field(default=None, ge=0.0)
    geography_score: Optional[float] = Field(default=None, ge=0.0)
    ethics_score: Optional[float] = Field(default=None, ge=0.0)
    earth_science_score: Optional[float] = Field(default=None, ge=0.0)
    
    # Science subjects
    chemistry_score: Optional[float] = Field(default=None, ge=0.0)
    physics_score: Optional[float] = Field(default=None, ge=0.0)
    biology_score: Optional[float] = Field(default=None, ge=0.0)
    physical_education_score: Optional[float] = Field(default=None, ge=0.0)
    
    # Foreign language (shared by both class types)
    foreign_language_score: Optional[float] = Field(default=None, ge=0.0)


class StudentRead(StudentBase):
    """Schema for reading/returning student data."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    class_type: ClassTypeEnum
    
    # Social Science subjects
    khmer_score: Optional[float]
    math_score: float
    history_score: Optional[float]
    geography_score: Optional[float]
    ethics_score: Optional[float]
    earth_science_score: float
    
    # Science subjects
    chemistry_score: Optional[float]
    physics_score: Optional[float]
    biology_score: Optional[float]
    physical_education_score: Optional[float]
    
    # Max scores for Social Science
    khmer_max: Optional[float]
    math_max: float
    history_max: Optional[float]
    geography_max: Optional[float]
    ethics_max: Optional[float]
    earth_science_max: float
    
    # Max scores for Science
    chemistry_max: Optional[float]
    physics_max: Optional[float]
    biology_max: Optional[float]
    physical_education_max: Optional[float]
    
    # Common fields
    foreign_language_score: float
    foreign_language_max: float
    
    total_score: float
    average_score: float
    grade: Optional[GradeEnum]
    created_at: datetime
    updated_at: Optional[datetime]


class StudentStats(BaseModel):
    """Schema for student statistics."""
    total_students: int
    pass_count: int
    fail_count: int
    grade_distribution: dict[str, int]
    subject_stats: dict[str, dict[str, int]]  # subject -> {pass: count, fail: count}


class PaginatedStudentResponse(BaseModel):
    """Schema for paginated student response."""
    model_config = ConfigDict(from_attributes=True)
    
    items: List[StudentRead]
    total: int
    page: int
    page_size: int
    total_pages: int
