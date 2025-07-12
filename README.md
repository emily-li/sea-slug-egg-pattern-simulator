# sea-slug-egg-pattern-simulator

A NetLogo-style bird's-eye view simulation of sea slug egg laying patterns with progressive pattern formation.

## Features

- 🔍 **Bird's Eye View**: Watch egg laying patterns emerge from above like NetLogo simulations
- 🎯 **Progressive Pattern Formation**: See patterns build step-by-step as the sea slug moves and lays eggs
- ⏯️ **Smooth Animation Controls**: 100 fine-grained steps with variable speed autoplay
- 🌊 **Real-time Pattern Building**: Watch spirals, ribbons, and clusters form progressively
- 🎨 **Species-specific Patterns**: Different laying behaviors create distinct visual patterns
- � **Live Statistics**: Track egg count, pattern completion, and environmental effects

## Visualization Modes

### Pattern Types

- **Spiral Patterns**: Watch anticlockwise/clockwise spirals form from center outward
- **Ribbon Patterns**: See sinusoidal ribbons laid in flowing motions
- **Cluster Patterns**: Observe discrete clusters placed strategically
- **Coil Patterns**: View tube-like coils forming through body rotation

### Interactive Controls

- **Step Controls**: Jump ±1 or ±10 steps, or use autoplay
- **Variable Speed**: 0.5x to 5x playback speed
- **Real-time Updates**: Change species/environment and see immediate effects

## Setup

### Prerequisites

- Python 3.13+

### Installation

```bash
pip install -r requirements.txt
```

### Run the Simulation

```bash
python -m streamlit run streamlit_app.py
```

## How to Use

1. **Select Species & Environment**: Choose from scientifically-modeled species and set conditions
2. **Watch Pattern Formation**: Use autoplay to see the complete laying process unfold
3. **Step Through Manually**: Use the control buttons to examine specific moments
4. **Compare Patterns**: Try different species to see how laying behaviors differ

## Species Available

- **Pacific Sea Lemon** - Large anticlockwise spiral ribbons (up to 2M eggs)
- **Spanish Dancer Nudibranch** - Rose-like ruffled spirals with defensive toxins
- **Vayssierea felis** - Small strategic clusters with direct development (1-5 eggs)
- **Aglajid Sea Slug** - Unique coil patterns formed by body rotation

## Scientific Accuracy

Based on real marine biology research, this simulation models:

- Hermaphroditic mating behaviors
- Species-specific egg mass morphologies
- Environmental impact on laying patterns
- Coiling directions and substrate preferences
