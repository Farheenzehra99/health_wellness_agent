# Health & Wellness Agent 🌟

AI-powered health and wellness assistant that provides personalized diet and exercise recommendations based on your goals and preferences, leveraging OpenAI's Agent SDK for intelligent conversations and real-time interactions.

## Features ✨

- **Personalized Health Goals** - Set and track your fitness and wellness objectives with AI-driven goal analysis
- **Smart Diet Planning** - Get AI-generated meal plans with real-time streaming updates
- **Workout Recommendations** - Receive customized exercise routines with safety checks
- **Progress Tracking** - Monitor your health journey with interactive charts and persistent state management
- **PDF Reports** - Generate detailed progress reports with comprehensive analytics
- **Real-time Chat** - Multi-turn conversations with context awareness and intelligent handoffs

## Tech Stack 🛠️

- Python 3.8+
- OpenAI Agent SDK
- Streamlit (UI Framework)
- SQLAlchemy (State Persistence)
- Pandas & NumPy (Data Processing)
- Plotly (Data Visualization)
- ReportLab (PDF Generation)
- AsyncIO (Asynchronous Operations)

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/yourusername/health-wellness-agent.git
cd health-wellness-agent
```
## Features in Detail 📋
### Intelligent Agent System
- OpenAI Agent SDK integration
- Multi-turn conversation management
- Context-aware responses
- Automated handoffs
- Input/output guardrails
### User Profile
- Input personal details (age, weight, height)
- Automatic BMI calculation
- Smart goal analysis and validation
- Progress persistence
### Diet Planning
- Real-time streaming meal plan generation
- Nutritional analysis and validation
- Dietary restrictions support
- Shopping list generation
### Workout Plans
- Personalized exercise routines
- Safety checks and progression tracking
- Injury prevention with AI validation
- Real-time modifications
### Progress Monitoring
- Interactive charts and graphs
- Weight and metrics tracking
- Goal achievement analytics
- State persistence and recovery
### Error Handling & Safety
- Robust error management
- Retry mechanisms
- Input validation
- Medical safety checks
## Project Structure 📁
```
health_wellness_agent/
├── src/
│   └── health_wellness_agent/
│       ├── agent.py          # Main agent implementation
│       ├── context.py        # Context management
│       ├── conversation.py    # Conversation handling
│       ├── guardrails.py     # Input/output validation
│       ├── hooks.py          # Lifecycle hooks
│       ├── agents/           # Agent components
│       ├── dashboard/        # Streamlit UI
│       ├── database/         # Data persistence
│       ├── tools/            # AI tools and utilities
│       └── utils/            # Common utilities
├── .env                      # Environment variables
├── .gitignore                # Git ignore rules
└── pyproject.toml            # Project dependencies
```
## Contributing 🤝
Contributions are welcome! Please feel free to submit a Pull Request.