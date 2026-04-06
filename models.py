from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class ActionType(str, Enum):
    TREAT_NOW = "TREAT_NOW"
    MONITOR = "MONITOR"
    WAIT = "WAIT"


class SeverityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Vitals(BaseModel):
    heart_rate: Optional[int] = Field(None, description="Heart rate in beats per minute")
    blood_pressure_systolic: Optional[int] = Field(None, description="Systolic blood pressure")
    blood_pressure_diastolic: Optional[int] = Field(None, description="Diastolic blood pressure")
    temperature: Optional[float] = Field(None, description="Body temperature in Celsius")
    respiratory_rate: Optional[int] = Field(None, description="Respiratory rate per minute")
    oxygen_saturation: Optional[float] = Field(None, description="Oxygen saturation percentage")
    pain_level: Optional[int] = Field(None, ge=0, le=10, description="Pain level from 0-10")


class Observation(BaseModel):
    patient_id: str = Field(description="Unique patient identifier")
    symptoms: List[str] = Field(description="List of patient-reported symptoms")
    vitals: Vitals = Field(description="Patient vital signs")
    age: Optional[int] = Field(None, ge=0, le=150, description="Patient age in years")
    gender: Optional[str] = Field(None, description="Patient gender")
    medical_history: List[str] = Field(default_factory=list, description="Relevant medical history")
    timestamp: str = Field(description="Timestamp of the observation")
    
    class Config:
        json_encoders = {
            # Add any custom encoders if needed
        }


class Action(BaseModel):
    action_type: ActionType = Field(description="The triage action to take")
    priority_score: float = Field(ge=0.0, le=1.0, description="Priority score from 0.0 to 1.0")
    reasoning: str = Field(description="Reasoning behind the decision")
    estimated_wait_time: Optional[int] = Field(None, ge=0, description="Estimated wait time in minutes")
    recommended_department: Optional[str] = Field(None, description="Recommended medical department")


class Reward(BaseModel):
    score: float = Field(ge=0.0, le=1.0, description="Reward score from 0.0 to 1.0")
    priority_correct: bool = Field(description="Whether priority assessment was correct")
    action_correct: bool = Field(description="Whether action was correct")
    reasoning_valid: bool = Field(description="Whether reasoning was logical")
    feedback: str = Field(description="Detailed feedback on the decision")
    breakdown: Dict[str, float] = Field(description="Breakdown of score components")


class PatientCase(BaseModel):
    case_id: str = Field(description="Unique case identifier")
    observation: Observation = Field(description="Patient observation data")
    correct_action: ActionType = Field(description="Correct triage action")
    correct_priority_range: tuple = Field(description="Expected priority range (min, max)")
    difficulty: str = Field(description="Difficulty level: EASY, MEDIUM, or HARD")
    explanation: str = Field(description="Explanation of the correct triage decision")


class EnvironmentState(BaseModel):
    current_case: Optional[PatientCase] = Field(None, description="Current patient case")
    total_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Cumulative score")
    cases_completed: int = Field(default=0, ge=0, description="Number of cases completed")
    current_step: int = Field(default=0, ge=0, description="Current step in the episode")
    max_steps: int = Field(default=10, ge=1, description="Maximum steps per episode")
    episode_done: bool = Field(default=False, description="Whether the episode is complete")
    history: List[Dict[str, Any]] = Field(default_factory=list, description="History of actions and rewards")
