# Temporal Scaffolding System

## Architecture & Design Specification

### Overview

The **Temporal Scaffolding System** is a mathematical approach to rhythm generation that uses mathematical functions to create temporal onset patterns. Rather than programming static beats, the system generates rhythmic structures by evaluating mathematical functions across time and converting the results into quantized musical events.

---

## Core Concept

**Mathematical functions define temporal relationships, not just rhythmic patterns.**

- **Input**: Mathematical function `f(x)` where `x` represents normalized time (0 to 1)
- **Process**: Function evaluation across quantized time steps
- **Output**: Onset timings that can trigger any musical event (drums, notes, effects, etc.)

### Mathematical Foundation

```
Time Domain: x ∈ [0, 1] (normalized measure/phrase length, flows continuously)
Function Domain: y = f(x) (quantized into threshold levels)
Quantization: Divide function range into N threshold levels (e.g., 0.125, 0.25, 0.375...)
Onset Detection: Fire events when function crosses quantization thresholds
```

**Threshold-Crossing Principle:**

- Mathematical curves naturally create temporal density through their slopes
- Steep function gradients → rapid threshold crossings → dense rhythmic activity
- Gentle function gradients → sparse threshold crossings → spacious timing
- **Agogic Expression**: Natural accelerando/ritardando emerges from curve geometry

---

## System Architecture

### 1. Function Generator Engine

**Core mathematical functions:**

- **Linear**: `y = x` (regular intervals, "4 on the floor")
- **Exponential**: `y = x^n` (accelerating rhythms)
- **Logarithmic**: `y = log(x+1)` (decelerating rhythms)
- **Trigonometric**: `y = sin(πx)`, `y = cos(πx)` (wave-like patterns)
- **Polynomial**: `y = ax^3 + bx^2 + cx + d` (complex curves)
- **Custom**: User-definable mathematical expressions

**Dynamic Parameters:**

- Function coefficients (a, b, c, d)
- Exponents and scaling factors
- Phase shifts and inversions
- Time stretching and compression

### 2. Temporal Quantization System

**Quantization Grid:**

- **Primary Divisions**: Musical subdivisions (4, 8, 16, 32 levels per measure)
- **Polyrhythmic Divisions**: Odd-meter quantizations (5, 7, 11, 13 levels)
- **Cross-Rhythmic Layering**: Different layers use different quantization schemes
- **Time Signatures**: 4/4, 3/4, 7/8, etc. (independent of function quantization)
- **Nested Subdivisions**: Triplets, quintuplets within primary divisions
- **Swing/Groove**: Post-processing templates applied to threshold events

**Onset Detection Algorithms:**

- **Threshold-crossing** (Primary): Fire events when function crosses quantized Y-axis levels
    - Function range quantized to musical divisions (1/8, 1/16, triplets, etc.)
    - Odd-meter quantizations (7, 5, 11 divisions) create polyrhythmic relationships
    - Natural agogic expression through curve slope variations
- **Peak detection**: Trigger at local maxima/minima for accent patterns
- **Derivative-based**: Trigger at points of maximum change for dynamic emphasis
- **Modulo arithmetic**: Secondary rhythmic layers using mathematical intervals
- **Probability gates**: Chance-based triggering influenced by function values

### 3. Multi-Layer System

**Layer Architecture:**

- Multiple simultaneous mathematical functions
- Independent quantization per layer
- Transparency/opacity controls for visual overlay
- Mathematical operations between layers (addition, multiplication, XOR)

**Layer Relationships:**

```
Layer A: y = x² (kick drum pattern)
Layer B: y = sin(2πx) (hi-hat pattern) 
Layer C: y = log(x+1) (snare pattern)
Combined: Various mathematical combinations
```

### 4. Preset Management

**Preset Categories:**

- **Temporal Scales**: Quarter note, whole note, 2-bar, 4-bar patterns
- **Musical Styles**: House, techno, jazz, polyrhythmic, ambient
- **Mathematical Families**: All exponential, all trigonometric, etc.
- **Complexity Levels**: Simple (single function) to complex (multi-layer)

**Morphing System:**

- Smooth interpolation between stored presets
- Real-time parameter crossfading
- Mathematical function blending
- Preset sequences for longer compositions

---

## User Interface Components

### 1. Function Designer (Primary jsui)

**Visual Elements:**

- Real-time function plotting with grid overlay
- Quantization markers as vertical lines
- Onset indicators as colored highlights
- Mathematical equation display
- Parameter sliders for live control

**Interactive Features:**

- Click-and-drag curve editing
- Mathematical expression input
- Function library browser
- Copy/paste function shapes

### 2. Multi-Layer Compositor (Secondary jsui)

**Layer Visualization:**

- Multiple overlaid function curves with transparency
- Color-coded layers for different instruments/voices
- Layer solo/mute controls
- Mathematical operation selectors between layers

**Timeline View:**

- Horizontal timeline showing multiple measures
- Event markers for all active layers
- Zoom controls for detailed editing
- Loop region selectors

### 3. Onset Pattern Display (Tertiary jsui)

**Pattern Grid:**

- Traditional step sequencer view of generated patterns
- Live updating as functions change
- Multiple layers shown simultaneously
- Export patterns to traditional sequencers

### 4. Mathematical Expression Editor

**Advanced Controls:**

- Text-based function input with syntax validation
- Mathematical operator library
- Variable assignment for complex expressions
- Function composition tools

---

## Integration with Max/MSP

### Core Objects

**Timing Foundation:**

- `metro` objects for master clock
- `transport` integration for DAW sync
- `timepoint` for sample-accurate timing
- Custom `js` objects for function evaluation

**Data Flow:**

```
[function generator] → [quantizer] → [onset detector] → [output router]
```

**Storage System:**

- `preset` objects for function storage
- `pattr` system for parameter automation
- `dict` objects for complex data structures
- File I/O for sharing patterns

### Performance Considerations

**Real-time Requirements:**

- Function evaluation optimized for audio rate
- Minimal GUI updates to prevent audio dropouts
- Efficient memory management for multiple layers
- Predictive calculation for smooth parameter changes

**Scalability:**

- Modular design allows adding unlimited layers
- CPU load monitoring and automatic optimization
- Graceful degradation under heavy loads

---

## Output Flexibility

### Interface-Agnostic Design

**Output Types:**

- **Raw Timing Data**: Numerical onset times
- **Max Messages**: Bang triggers with metadata
- **MIDI Events**: Note on/off with velocity/timing
- **CV Voltages**: Via external interfaces (ES-9, etc.)
- **OSC Messages**: For network-based systems

**Event Metadata:**

- Timing precision (ticks, milliseconds, samples)
- Velocity/amplitude based on function values
- Layer identification for routing
- Mathematical function source information

### Routing Matrix

**Flexible Assignment:**

- Any layer can trigger any output
- Multiple layers can control single outputs
- Single layers can control multiple outputs
- Mathematical functions can control non-timing parameters

---

## Advanced Features

### 1. Function Relationships

**Mathematical Operations Between Functions:**

- Function composition: `f(g(x))`
- Arithmetic operations: `f(x) + g(x)`, `f(x) * g(x)`
- Boolean operations: `f(x) AND g(x)`, `f(x) XOR g(x)`

### 4. Stochastic Extensions

**Probability Integration:**

- Random variations within mathematical constraints
- Markov chains for function selection
- Gaussian noise applied to function parameters
- Monte Carlo methods for complex pattern generation

### 5. Temporal Feedback

**Self-Modifying Systems:**

- Functions that evolve based on their own output
- Chaos theory applications (strange attractors)
- Feedback loops between layers
- Historical influence on current generation

### 3. Agogic and Polyrhythmic Extensions

**Natural Time Relationships:**

- Mathematical curves create organic accelerando/ritardando effects
- Slope variations produce natural breathing and phrasing
- Non-linear time perception through function geometry
- Capture of musical expression beyond notation capabilities

**Polyrhythmic Architecture:**

- Simultaneous layers with different function quantizations
- Cross-rhythmic relationships (5 against 7, 11 against 4)
- Mathematical ratios create complex but coherent rhythmic structures
- Emergent polyrhythms from function interactions

---

## Development Phases

### Phase 1: Foundation

- Single function generator with basic math functions
- Simple quantization and onset detection
- Basic jsui visualization
- Core Max/MSP integration

### Phase 2: Multi-Layer

- Multiple simultaneous functions
- Layer transparency and mixing
- Preset storage and recall
- Advanced visualization

### Phase 3: Advanced Mathematics

- Complex function composition
- Real-time parameter morphing
- Mathematical operations between layers
- Performance optimization

### Phase 4: Interface Integration

- MIDI output implementation
- CV output preparation
- OSC networking
- Plugin/standalone versions

---

## Success Metrics

**Technical Goals:**

- Sub-millisecond timing accuracy
- Support for 16+ simultaneous layers
- Real-time parameter updates without audio dropouts
- Intuitive mathematical function creation

**Musical Goals:**

- Generation of rhythmic patterns impossible to create manually
- Seamless integration with existing Max/MSP workflows
- Inspiring new approaches to rhythmic composition
- Bridge between mathematical beauty and musical expression

---

_"Mathematics is the language in which God has written the universe... and perhaps composed its rhythms as well."_

**Next Steps:** Implementation begins with the core Function Generator Engine, focusing on mathematical accuracy and real-time performance.