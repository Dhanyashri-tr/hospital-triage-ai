# AI Hospital Triage System

An OpenEnv environment for training and evaluating AI agents in hospital emergency room triage scenarios.

## 🎯 Project Overview

This project simulates a hospital emergency room triage system where an AI agent must analyze patient symptoms and vital signs to make appropriate triage decisions. The agent must prioritize patients based on medical urgency and decide between three actions:

- **TREAT_NOW**: Immediate medical attention required
- **MONITOR**: Observation and further evaluation needed  
- **WAIT**: Non-urgent case that can wait for routine care

## 📋 Problem Description

Hospital emergency rooms face the critical challenge of quickly and accurately prioritizing patients based on their medical condition. Triage errors can lead to serious consequences:

- Delaying treatment for critical patients
- Wasting resources on non-urgent cases
- Poor patient outcomes and increased mortality

This AI system aims to assist medical professionals by providing rapid, evidence-based triage recommendations.

## 🏥 Medical Triage Explanation

Triage is the process of determining the priority of patients' treatments based on the severity of their condition. This system uses a standardized approach:

### Severity Levels
- **CRITICAL (0.8-1.0)**: Life-threatening conditions requiring immediate intervention
- **HIGH (0.6-0.8)**: Serious conditions needing urgent attention
- **MEDIUM (0.4-0.6)**: Moderate conditions requiring monitoring
- **LOW (0.0-0.4)**: Minor conditions that can wait

### Key Medical Indicators
- **Vital Signs**: Heart rate, blood pressure, temperature, oxygen saturation
- **Symptoms**: Patient-reported complaints and observations
- **Medical History**: Pre-existing conditions that affect risk assessment

## 🎮 Action Space

The AI agent can choose from three discrete actions:

| Action | Description | Use Cases |
|--------|-------------|-----------|
| `TREAT_NOW` | Immediate medical intervention required | Heart attack, stroke, severe bleeding, respiratory distress |
| `MONITOR` | Close observation and further evaluation | Moderate infections, dehydration, asthma exacerbation |
| `WAIT` | Non-urgent, routine care acceptable | Minor injuries, cold symptoms, mild pain |

## 👁️ Observation Space

The agent receives comprehensive patient information:

```python
{
    "patient_id": "unique_identifier",
    "symptoms": ["chest pain", "shortness of breath", "sweating"],
    "vitals": {
        "heart_rate": 115,
        "blood_pressure_systolic": 160,
        "blood_pressure_diastolic": 95,
        "temperature": 36.9,
        "respiratory_rate": 26,
        "oxygen_saturation": 91.0,
        "pain_level": 8
    },
    "age": 58,
    "gender": "M",
    "medical_history": ["hypertension", "high cholesterol"],
    "timestamp": "2024-01-01T12:00:00"
}
```

## 🧮 Reward Logic

The reward function provides deterministic scoring from 0.0 to 1.0:

### Score Components
- **Priority Score (40%)**: Correct urgency assessment within expected range
- **Action Type (40%)**: Correct triage decision
- **Reasoning (20%)**: Logical, evidence-based explanation

### Scoring Examples
- Perfect decision: 1.0 (correct priority + action + reasoning)
- Partially correct: 0.6-0.8 (some components correct)
- Incorrect decision: 0.0-0.4 (major errors)

### Penalties
- **Major (-0.5)**: Missing critical cases (TREAT_NOW needed but not chosen)
- **Minor (-0.2)**: Over-treating non-critical cases
- **Small (-0.1)**: Priority scores far outside expected range

## 📁 Project Structure

```
.
├── hospital_env/
│   ├── __init__.py          # Package initialization
│   ├── env.py               # Main environment class
│   ├── models.py            # Pydantic data models
│   ├── grader.py            # Reward function implementation
│   └── tasks.py             # Patient case database
├── inference.py             # AI agent inference script
├── openenv.yaml             # OpenEnv configuration
├── Dockerfile               # Container configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Setup Instructions

### Local Development

1. **Clone and navigate to the project**
   ```bash
   cd ai-hospital-triage
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export API_BASE_URL="https://api.openai.com/v1"
   export MODEL_NAME="gpt-3.5-turbo"
   export OPENAI_API_KEY="your-api-key"
   ```

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t ai-hospital-triage .
   ```

2. **Run the container**
   ```bash
   docker run --rm -e OPENAI_API_KEY=your-key ai-hospital-triage
   ```

### Hugging Face Spaces

1. **Create a new Space** on Hugging Face
2. **Upload all files** to the Space
3. **Set environment variables** in the Space settings
4. **The app will deploy automatically**

## 🏃 Run Instructions

### Basic Usage

```bash
python inference.py
```

### With Custom Difficulty

```python
from hospital_env import HospitalTriageEnv

# Easy mode for beginners
env = HospitalTriageEnv(difficulty="EASY", max_steps=5)

# Hard mode for experts
env = HospitalTriageEnv(difficulty="HARD", max_steps=10)

# Reset and start
observation = env.reset()
```

### Environment API

```python
# Reset environment
observation = env.reset()

# Take action
next_observation, reward, done, info = env.step(action)

# Get current state
state = env.state()

# Render current case
env.render(mode="human")
```

## 📊 Sample Output

```
[START]
[STEP]
Patient ID: patient_12345678
Symptoms: chest pain, shortness of breath, sweating, nausea, pain radiating to left arm
Action: TREAT_NOW
Priority Score: 0.95
Reasoning: Patient presents with classic signs of myocardial infarction including chest pain radiating to left arm, diaphoresis, and nausea. Elevated heart rate and blood pressure indicate cardiac distress. This is a life-threatening emergency requiring immediate intervention.
Reward: 1.000
Cumulative Score: 1.000
Cases Completed: 1
[STEP]
Patient ID: patient_87654321
Symptoms: runny nose, sore throat, mild cough
Action: WAIT
Priority Score: 0.15
Reasoning: Patient presents with mild upper respiratory symptoms, normal vitals, and no signs of distress. This is a common cold that can be managed with supportive care and doesn't require emergency attention.
Reward: 1.000
Cumulative Score: 1.000
Cases Completed: 2
Final Score: 1.000
[END]
```

## 🧪 Validation Checklist

- ✅ **No runtime errors**: All code runs without exceptions
- ✅ **inference.py runs fully**: Complete execution from [START] to [END]
- ✅ **Logs format correct**: Exact [START]/[STEP]/[END] format maintained
- ✅ **Score between 0–1**: All rewards properly normalized
- ✅ **Docker works**: Container builds and runs successfully
- ✅ **HF Space deploys**: Compatible with Hugging Face Spaces

## 🎯 Difficulty Levels

### EASY (3 cases)
- Simple, common conditions (cold, mild fever, minor sprain)
- Clear symptom patterns
- Normal vital signs
- Straightforward decisions

### MEDIUM (3 cases)
- Moderate complexity (dehydration, infection, asthma)
- Multiple symptoms
- Some abnormal vitals
- Requires clinical judgment

### HARD (4 cases)
- Critical conditions (heart attack, stroke, sepsis, trauma)
- Complex symptom combinations
- Severely abnormal vitals
- High-stakes decisions

## 🔬 Technical Details

### Environment Methods
- `reset()`: Initialize new episode with random case
- `step(action)`: Execute triage decision and receive reward
- `state()`: Get current environment state
- `render()`: Display current case information

### Grading Algorithm
The deterministic grader evaluates:
1. **Priority Assessment**: Is the urgency score within expected range?
2. **Action Selection**: Is the triage decision medically correct?
3. **Reasoning Quality**: Is the explanation logical and evidence-based?

### Safety Features
- Fallback to safe default actions on errors
- Penalty system for dangerous decisions
- Comprehensive medical validation
- Deterministic scoring for fair evaluation

## 📈 Performance Metrics

- **Accuracy**: Percentage of correct triage decisions
- **Response Time**: Speed of decision-making
- **Safety Score**: Avoidance of dangerous errors
- **Reasoning Quality**: Logical coherence of explanations

## 🤝 Contributing

This project is designed for the Meta x Scaler OpenEnv Hackathon. The codebase follows OpenEnv specifications and medical best practices for triage systems.

## 📄 License

MIT License - see LICENSE file for details.

## ⚠️ Medical Disclaimer

This system is for educational and research purposes only. It should not be used for actual medical decision-making. Always consult qualified healthcare professionals for medical advice.
