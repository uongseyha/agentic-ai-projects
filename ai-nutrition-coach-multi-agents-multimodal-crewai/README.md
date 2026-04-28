# AI-Nutrition-coach-multi-agents-multimodal-crewai

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/AI-Multi--Agent-orange" alt="AI Agent">
</p>

---

## Demo Walkthrough

<video controls src="https://github.com/user-attachments/assets/150a5629-073f-458c-861f-7980fe1c0d80" title="AI-Nutrition-coach-multi-agents-multimodal-crewai"></video>

---

## � Project Description

**AI NourishBot** is a multi-agent AI nutrition coach that uses computer vision and large language models to analyze food images, provide nutritional insights, and generate recipe suggestions.

### What It Does

| Feature | Description |
|---------|-------------|
| **Image-Based Ingredient Detection** | Upload any food photo and GPT-4o vision identifies all ingredients automatically |
| **Dietary Restriction Filtering** | Filter ingredients based on diets: vegan, vegetarian, gluten-free, keto, paleo, dairy-free, nut-free |
| **Nutritional Analysis** | Get detailed breakdown of macros (protein, carbs, fats), vitamins, minerals, and total calories |
| **Health Evaluation** | Receive an expert assessment of the meal's health benefits and concerns |
| **Recipe Generation** | Get creative recipe ideas using detected ingredients that match your dietary needs |

### How It Works

The system uses **CrewAI's multi-agent framework** with four specialized AI agents:

1. **Vision AI Specialist** — Detects ingredients from food images using GPT-4o
2. **Nutritionist AI Specialist** — Filters ingredients based on dietary restrictions
3. **Nutrition Analysis Specialist** — Analyzes nutritional content and provides health evaluation
4. **Recipe Generation Specialist** — Creates recipe suggestions from filtered ingredients

Each agent has specific tools and tasks, working together through a sequential workflow to deliver comprehensive nutrition insights.

### Use Cases

- 🥗 **Health-conscious individuals** tracking daily nutrition
- 🍳 **Home cooks** looking for recipe inspiration from fridge contents
- 🏋️ **Fitness enthusiasts** calculating macro/calorie intake
- 🥦 **People with dietary restrictions** ensuring meal compliance
- 📸 **Food bloggers** analyzing dish nutrition quickly

---

## �📋 Problem Statement

Modern users struggle with:

| Problem | Description |
|---------|-------------|
| **Manual Nutrition Tracking** | Manually logging food intake is time-consuming and error-prone |
| **Limited Food Recognition** | Existing apps require text input or barcode scanning |
| **Dietary Compliance** | Users with specific diets (vegan, gluten-free, keto) need automated filtering |
| **Calorie Estimation** | Estimating calories and nutrients from meals is challenging |
| **Recipe Discovery** | Finding recipes that match available ingredients and dietary needs |

Users want a seamless way to:
- Upload a photo of their meal
- Automatically detect ingredients via computer vision
- Filter based on dietary restrictions
- Get nutritional analysis
- Receive recipe suggestions

---

## 🎯 Objective

Build an **AI-powered multimodal nutrition coach** that:

1. **Accepts food images** as input via a user-friendly Gradio interface
2. **Uses GPT-4o vision capabilities** to detect and identify ingredients
3. **Filters ingredients** based on user dietary restrictions (vegan, gluten-free, keto, etc.)
4. **Analyzes nutritional content** including macros, vitamins, minerals, and calories
5. **Suggests recipes** using detected/filtered ingredients that meet dietary goals

The system leverages **CrewAI's multi-agent framework** to orchestrate specialized AI agents for each task.

---

## 🔄 Project Processing Detail

### Workflow 1: Recipe Suggestion Flow

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│   User Upload   │────▶│  Ingredient Detection│────▶│ Dietary Filtering   │
│   Food Image    │     │       Agent          │     │       Agent         │
└─────────────────┘     └──────────────────────┘     └─────────────────────┘
                                │                                    │
                                ▼                                    ▼
                        ExtractIngredients                   FilterIngredients
                        Tool + FilterIngredients            Tool + DietaryFilter
                                │                                    │
                                ▼                                    ▼
                        ┌──────────────────────┐     ┌─────────────────────┐
                        │  Detected Ingredients │────▶│ Filtered Ingredients │
                        └──────────────────────┘     └─────────────────────┘
                                                              │
                                                              ▼
                                                ┌─────────────────────┐
                                                │ Recipe Suggestion   │
                                                │       Agent         │
                                                └─────────────────────┘
                                                              │
                                                              ▼
                                                ┌─────────────────────┐
                                                │  Recipe Ideas with  │
                                                │  Instructions &     │
                                                │  Calorie Estimates  │
                                                └─────────────────────┘
```

### Workflow 2: Nutritional Analysis Flow

```
┌─────────────────┐     ┌──────────────────────┐
│   User Upload   │────▶│  Nutrient Analysis    │
│   Food Image    │     │       Agent          │
└─────────────────┘     └──────────────────────┘
                                │
                                ▼
                        ┌──────────────────────┐
                        │  NutrientAnalysis    │
                        │        Tool          │
                        └──────────────────────┘
                                │
                                ▼
                        ┌──────────────────────┐
                        │  Detailed Nutrient   │
                        │  Breakdown + Health  │
                        │    Evaluation        │
                        └──────────────────────┘
```

### Step-by-Step Processing

| Step | Agent | Tool | Input | Output |
|------|-------|------|-------|--------|
| 1 | **Ingredient Detection Agent** | `ExtractIngredientsTool`, `FilterIngredientsTool` | Food image | Raw ingredient list |
| 2 | **Dietary Filtering Agent** | `DietaryFilterTool` | Raw ingredients + dietary restrictions | Filtered ingredient list |
| 3 | **Nutrient Analysis Agent** | `NutrientAnalysisTool` | Food image | Macronutrients, vitamins, minerals, calories |
| 4 | **Recipe Suggestion Agent** | (LLM only) | Filtered ingredients | Recipe ideas with instructions |

### Data Flow Example

```python
# Input
image = "food_photo.jpg"
dietary_restrictions = "vegan"

# Processing Pipeline
1. Image → GPT-4o Vision → ["chicken", "rice", "broccoli", "soy sauce"]
2. Ingredients + "vegan" → LLM Filter → ["rice", "broccoli"]  # removed chicken
3. Filtered ingredients → Recipe Agent → [Recipe 1, Recipe 2, Recipe 3]

# Output
recipes = [
    {
        "title": "Vegan Buddha Bowl",
        "ingredients": ["rice", "broccoli", "chickpeas", "tahini"],
        "instructions": "...",
        "calorie_estimate": 450
    },
    ...
]
```

---

## 🏗️ Architecture ASCII Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI NourishBot Architecture                        │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────────┐
                              │   Gradio Web UI     │
                              │   (User Interface)  │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │      app.py         │
                              │  (Main Controller)  │
                              └──────────┬──────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    │                                             │
                    ▼                                             ▼
      ┌─────────────────────────────┐           ┌─────────────────────────────┐
      │   NourishBotRecipeCrew      │           │   NourishBotAnalysisCrew   │
      │   (Sequential Process)      │           │   (Sequential Process)      │
      └─────────────┬───────────────┘           └─────────────┬───────────────┘
                    │                                             │
        ┌───────────┼───────────┬───────────┐                     │
        ▼           ▼           ▼           ▼                     ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      ┌───────────────┐
   │Ingredient│ │ Dietary │ │ Recipe  │ │  Task   │      │  Nutrient     │
   │Detection │ │Filtering│ │Suggestion│ │Output   │      │  Analysis     │
   │  Agent   │ │  Agent  │ │  Agent  │ │(JSON)   │      │    Agent      │
   └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘      └───────┬───────┘
        │           │           │           │                    │
        ▼           ▼           ▼           ▼                    ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      ┌───────────────┐
   │Extract  │ │Dietary  │ │   LLM   │ │ Recipe  │      │   Nutrient    │
   │Ingredients│Filter   │ │ (GPT-4o)│ │Output   │      │   Analysis    │
   │  Tool   │ │  Tool   │ │         │ │ Model   │      │     Tool      │
   └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘      └───────┬───────┘
        │           │           │           │                    │
        └───────────┴───────────┴───────────┴────────────────────┘
                                        │
                                        ▼
                              ┌─────────────────────┐
                              │   Output Models     │
                              │  (Pydantic Base)    │
                              └─────────────────────┘
```

### Component Details

```
┌────────────────────────────────────────────────────────────────────────┐
│                           COMPONENT LAYERS                              │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    PRESENTATION LAYER                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │   │
│  │  │  Gradio UI  │  │   Custom    │  │   Output Formatter  │   │   │
│  │  │  Interface  │  │   CSS/JS    │  │   (Markdown/Tables) │   │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                   │                                      │
│                                   ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      ORCHESTRATION LAYER                       │   │
│  │  ┌─────────────────────────────────────────────────────────┐  │   │
│  │  │                    CrewAI Framework                      │  │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │  │   │
│  │  │  │   Agent 1   │  │   Agent 2   │  │   Agent 3   │     │  │   │
│  │  │  │ (Detection)│  │ (Filtering) │  │ (Analysis)  │     │  │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘     │  │   │
│  │  │         │                 │                 │          │  │   │
│  │  │         └─────────────────┼─────────────────┘          │  │   │
│  │  │                           ▼                            │  │   │
│  │  │              ┌────────────────────────┐               │  │   │
│  │  │              │   Task Coordination    │               │  │   │
│  │  │              │   (Sequential Flow)    │               │  │   │
│  │  │              └────────────────────────┘               │  │   │
│  │  └─────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                   │                                      │
│                                   ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                       TOOL LAYER                                │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │   │
│  │  │  Extract     │ │  Dietary    │ │  Nutrient    │           │   │
│  │  │  Ingredients │ │  Filter      │ │  Analysis    │           │   │
│  │  │    Tool      │ │    Tool      │ │    Tool      │           │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                   │                                      │
│                                   ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      MODEL LAYER                                │   │
│  │  ┌──────────────────────┐  ┌────────────────────────────────┐  │   │
│  │  │   GPT-4o (Vision)   │  │   GPT-4o-mini (Text)            │  │   │
│  │  │   - Image Analysis   │  │   - Text Processing            │  │   │
│  │  │   - Ingredient Det. │  │   - Filtering                   │  │   │
│  │  └──────────────────────┘  └────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Framework** | [CrewAI](https://crewai.com) | Latest | Multi-agent orchestration |
| **UI** | [Gradio](https://gradio.app) | Latest | Web interface for image upload |
| **LLM (Vision)** | OpenAI GPT-4o | Latest | Image analysis & ingredient detection |
| **LLM (Text)** | OpenAI GPT-4o-mini | Latest | Text processing & filtering |
| **Data Models** | [Pydantic](https://docs.pydantic.dev) | v2 | Schema validation & output models |
| **Config** | [PyYAML](https://pyyaml.org) | Latest | Agent & task configuration |
| **Environment** | python-dotenv | Latest | API key management |
| **Image Processing** | Pillow (PIL) | Latest | Image handling |

### Dependencies

```txt
crewai>=0.28.0
gradio>=4.0.0
openai>=1.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
pyyaml>=6.0
pillow>=10.0.0
requests>=2.31.0
```

### Project Structure

```
ai-nutrition-coach-multi-agents-multimodal-crewai/
├── app.py                      # Main Gradio application
├── .env                        # Environment variables (API keys)
├── src/
│   ├── crew.py                # CrewAI crew definitions
│   ├── models.py              # Pydantic output models
│   ├── tools.py               # Custom CrewAI tools
│   └── config/
│       ├── agents.yaml        # Agent configurations
│       └── tasks.yaml         # Task definitions
└── examples/                  # Example usage
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
# Create virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows
# source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file:

```env
OPENAI_API_KEY=sk-your-openai-key-here
```

### 3. Run the Application

```bash
python app.py
```

### 4. Access the UI

Open your browser to: **http://localhost:7860**

---

## 📱 Usage

### Option 1: Recipe Suggestion

1. Upload a photo of your meal
2. Select workflow type: `recipe`
3. Enter dietary restrictions (optional): `vegan`, `gluten-free`, `keto`
4. Click **Submit**
5. View generated recipes with ingredients, instructions, and calorie estimates

### Option 2: Nutritional Analysis

1. Upload a photo of your meal
2. Select workflow type: `analysis`
3. Click **Submit**
4. View detailed nutrient breakdown including:
   - Macronutrients (protein, carbs, fats)
   - Vitamins (% Daily Value)
   - Minerals
   - Total calories
   - Health evaluation

---

## 🔑 Key Features

- ✅ **Multi-modal Input**: Process food images using GPT-4o vision
- ✅ **Multi-Agent System**: Specialized agents for detection, filtering, analysis, and recipe generation
- ✅ **Dietary Filtering**: Support for vegan, gluten-free, keto, and other diets
- ✅ **Sequential Processing**: CrewAI process for ordered task execution
- ✅ **Structured Output**: Pydantic models for type-safe responses
- ✅ **User-Friendly UI**: Gradio interface with custom styling

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- [CrewAI](https://crewai.com) - Multi-agent framework
- [OpenAI](https://openai.com) - GPT-4o vision models
- [Gradio](https://gradio.app) - UI framework