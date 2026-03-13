# 💰 FutureFund — Life-Path Financial Simulator

A modern fintech dashboard built with Python + Streamlit that helps users plan their financial goals, simulate investment growth, and understand their lifetime wealth journey.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app (from project root)
streamlit run dashboard/dashboard_app.py
```

Open http://localhost:8501 in your browser.

---

## 📁 Project Structure

```
futurefund/
├── dashboard/
│   ├── dashboard_app.py     # Main Streamlit app — entry point
│   ├── styles.py            # CSS theme, Finley mascot HTML, chart layouts
│   ├── ui_components.py     # Reusable HTML/Streamlit UI building blocks
│   └── finley_chatbot.py    # Finley AI assistant (rule-based NLP)
│
├── src/
│   ├── financial_engine.py  # Core financial formulas (FV, SIP, affordability)
│   ├── projections.py       # Month-by-month growth timeseries
│   ├── monte_carlo.py       # Monte Carlo simulation engine
│   └── life_simulator.py    # Lifetime wealth projection across life phases
│
├── utils/
│   ├── goal_manager.py      # Goal CRUD, SIP aggregation, priority helpers
│   └── helpers.py           # INR formatting, color helpers, labels
│
├── requirements.txt
└── README.md
```

---

## ✨ Features

### 🎯 Goal Notebook (Left Panel)
- Add goals with: name, category, cost, time horizon, priority, personal notes
- Goals displayed as **sticky note cards** with a yellow note aesthetic
- Auto-calculates inflation-adjusted future cost and required SIP per goal
- Aggregate SIP vs. savings budget health indicator

### 📊 Dashboard (Center Panel)
#### Tab 1 — Investment Growth Chart
- Month-by-month portfolio value vs. amount invested
- Gains from compounding clearly separated
- Goal target reference line
- Final value, total invested, returns breakdown

#### Tab 2 — Monte Carlo Simulation
- 500–5000 simulations of investment growth with random market returns
- Distribution histogram: green (meets goal) vs. red (below goal)
- **Probability of achieving the goal** with confidence label
- P10/P25/P50/P75/P90 percentile breakdown
- Configurable volatility slider

#### Tab 3 — Lifetime Wealth Projection
- Wealth journey from current age to 85
- Life phase shading: Early Career, Growth, Peak, Pre-Retirement, Retirement
- Goal withdrawal markers overlaid on chart
- Peak net worth, retirement corpus metrics

#### Tab 4 — Goal Summary
- All goals in a sortable table with affordability status
- SIP allocation pie chart

### 🤖 Finley AI Assistant
- Animated walking mascot at the bottom of the screen
- Context-aware chatbot with pattern-matched NLP
- Answers: savings advice, car/house/education questions, SIP explanations, retirement planning, inflation impact
- Quick-prompt buttons for common questions

### 👤 Profile Panel (Right Panel)
- Income, savings, age, risk profile inputs
- Inflation and expected return assumption sliders
- Auto-suggests return rate based on risk profile
- Financial health scorecard: savings rate, real return quality
- Rule of 72 and Rule of 70 calculators

---

## 🧮 Financial Logic

### Core Formulas (`src/financial_engine.py`)

| Formula | Description |
|---------|-------------|
| `FV = PV × (1 + i)^n` | Inflate goal cost to future value |
| `SIP = FV × r / [((1+r)^n − 1) × (1+r)]` | Required monthly SIP |
| `FV_sip = P × [((1+r)^n − 1) / r] × (1+r)` | SIP future value |

### Monte Carlo (`src/monte_carlo.py`)
- Simulates N paths using `np.random.default_rng`
- Monthly returns drawn from `Normal(mean_return/12, volatility/√12)`
- Probability = fraction of simulations meeting goal target
- Reproducible with fixed seed (configurable)

### Life Simulator (`src/life_simulator.py`)
- 5 life phases with income growth rates and savings rates
- Annual net worth compounding with goal withdrawal events

---

## 🎨 Design Decisions

- **Dark fintech theme** inspired by modern trading platforms
- **Sora font** for display numbers, **Inter** for body text
- **Sticky note cards** in yellow for a personal, tactile feel
- **Animated SVG mascot** (Finley) walks across the screen with a CSS keyframe animation
- All charts use a **custom Plotly dark layout** (`get_chart_layout()`) for consistency
- Colors: Blue `#58a6ff`, Green `#3fb950`, Gold `#d29922`, Red `#f85149`, Purple `#bc8cff`

---

## ⚠️ Disclaimer

FutureFund is for **educational and illustrative purposes only**.  
All projections are estimates — actual market returns will vary.  
This is not financial advice. Consult a SEBI-registered investment advisor.
