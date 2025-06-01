# Max Patcher JSON Format - Essential Knowledge

## Overview

Max/MSP patcher files (.maxpat) are **plain-text JSON files** that can be programmatically generated. This document captures essential knowledge for creating working Max patches via code.

## Core Structure

Every Max patch follows this hierarchical JSON structure:

```json
{
  "patcher": {
    // Metadata & settings
    "fileversion": 1,
    "appversion": { "major": 8, "minor": 0, "revision": 0, "architecture": "x64", "modernui": 1 },
    "classnamespace": "box",
    "rect": [59.0, 103.0, 640.0, 480.0],
    
    // Visual settings
    "bglocked": 0,
    "openinpresentation": 0,
    "default_fontsize": 12.0,
    "default_fontface": 0,
    "default_fontname": "Arial",
    "gridonopen": 1,
    "gridsize": [15.0, 15.0],
    
    // Core content
    "boxes": [ /* objects array */ ],
    "lines": [ /* connections array */ ],
    "dependency_cache": [],
    "autosave": 0
  }
}
```

## Three Main Components

### 1. Patcher (Container)
The root object containing all metadata and content arrays.

### 2. Boxes (Objects)
Individual Max objects like `[metro]`, `[random]`, `[dac~]`, etc.

### 3. Patchlines (Connections)
Cable connections between object outlets and inlets.

## Box Structure

Each object in the `boxes` array follows this pattern:

```json
{
  "box": {
    "id": "obj-1",                           // Unique identifier
    "maxclass": "newobj",                    // Object type
    "numinlets": 2,                          // Number of inlets
    "numoutlets": 1,                         // Number of outlets
    "outlettype": ["bang"],                  // Data types from outlets
    "patching_rect": [100.0, 150.0, 63.0, 22.0],  // [x, y, width, height]
    "text": "metro 500"                        // Object content/arguments
  }
}
```

### Object Types (maxclass)

- **`"newobj"`**: Standard objects with text (metro, random, +, *, etc.)
- **`"toggle"`**: UI toggle button
- **`"number"`**: Number box
- **`"flonum"`**: Floating-point number box  
- **`"button"`**: Bang button
- **`"slider"`**: Slider control
- **`"dial"`**: Rotary dial
- **`"comment"`**: Text comment

### UI Objects (Special Parameters)

UI objects often have additional parameters:

```json
{
  "box": {
    "id": "obj-1",
    "maxclass": "toggle",
    "numinlets": 1,
    "numoutlets": 1,
    "outlettype": ["int"],
    "parameter_enable": 0,                   // Parameter automation
    "patching_rect": [100.0, 100.0, 24.0, 24.0]
  }
}
```

## Patchline Structure

Connections are defined in the `lines` array:

```json
{
  "patchline": {
    "destination": ["obj-3", 0],             // [object_id, inlet_number]
    "source": ["obj-2", 0]                   // [object_id, outlet_number]
  }
}
```

### Connection Rules

- **Source**: `[object_id, outlet_index]` (outlet numbers start at 0)
- **Destination**: `[object_id, inlet_index]` (inlet numbers start at 0)
- **Object IDs** must match exactly with box IDs
- **Invalid connections** will cause patch load errors

## Coordinate System

### Positioning (`patching_rect`)
- **Format**: `[x, y, width, height]`
- **Origin**: Top-left corner (0, 0)
- **Units**: Pixels
- **Typical spacing**: 50-100 pixels between objects vertically

### Layout Best Practices
- **Vertical flow**: Objects typically flow top-to-bottom
- **Standard spacing**: 50px vertical, 15px grid alignment
- **Object sizes**: Vary by type (toggle: 24x24, newobj: varies by text)

## Common Object Patterns

### Basic Control Flow
```json
// Toggle → Metro → Random → Number
[
  {"id": "obj-1", "maxclass": "toggle", "patching_rect": [100, 100, 24, 24]},
  {"id": "obj-2", "maxclass": "newobj", "text": "metro 500", "patching_rect": [100, 150, 63, 22]},
  {"id": "obj-3", "maxclass": "newobj", "text": "random 100", "patching_rect": [100, 200, 61, 22]},
  {"id": "obj-4", "maxclass": "number", "patching_rect": [100, 250, 50, 22]}
]
```

### Audio Objects
```json
// Always end audio chains with dac~
{"id": "obj-5", "maxclass": "newobj", "text": "dac~", "patching_rect": [100, 300, 35, 22]}
```

### Math Objects
```json
// Simple arithmetic
{"id": "obj-6", "maxclass": "newobj", "text": "+ 1", "patching_rect": [100, 200, 29, 22]}
{"id": "obj-7", "maxclass": "newobj", "text": "* 0.5", "patching_rect": [100, 250, 35, 22]}
```

## Essential Object Reference

### Timing
- **`metro [interval]`**: Metronome (default: bang per interval ms)
- **`delay [time]`**: Delay bang by time ms
- **`pipe [time]`**: Delay any message by time ms

### Math & Logic
- **`+ [number]`**: Addition
- **`* [number]`**: Multiplication  
- **`random [max]`**: Random integer 0 to max-1
- **`> [number]`**: Greater than comparison

### Audio (MSP)
- **`cycle~ [freq]`**: Sine wave oscillator
- **`dac~`**: Digital-to-analog converter (speakers)
- **`*~ [gain]`**: Audio multiplication
- **`line~`**: Audio ramp generator

### Data
- **`int [initial]`**: Integer storage
- **`float [initial]`**: Float storage
- **`bang`**: Bang button

## Validated Working Example

This JSON creates a functional random number generator:

```json
{
  "patcher": {
    "fileversion": 1,
    "appversion": {"major": 8, "minor": 0, "revision": 0, "architecture": "x64", "modernui": 1},
    "classnamespace": "box",
    "rect": [59.0, 103.0, 640.0, 480.0],
    "boxes": [
      {
        "box": {
          "id": "obj-1",
          "maxclass": "toggle",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": ["int"],
          "parameter_enable": 0,
          "patching_rect": [100.0, 100.0, 24.0, 24.0]
        }
      },
      {
        "box": {
          "id": "obj-2",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": ["bang"],
          "patching_rect": [100.0, 150.0, 63.0, 22.0],
          "text": "metro 500"
        }
      },
      {
        "box": {
          "id": "obj-3",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": ["int"],
          "patching_rect": [100.0, 200.0, 61.0, 22.0],
          "text": "random 100"
        }
      },
      {
        "box": {
          "id": "obj-4",
          "maxclass": "number",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": ["", "bang"],
          "parameter_enable": 0,
          "patching_rect": [100.0, 250.0, 50.0, 22.0]
        }
      }
    ],
    "lines": [
      {"patchline": {"destination": ["obj-2", 0], "source": ["obj-1", 0]}},
      {"patchline": {"destination": ["obj-3", 0], "source": ["obj-2", 0]}},
      {"patchline": {"destination": ["obj-4", 0], "source": ["obj-3", 0]}}
    ],
    "dependency_cache": [],
    "autosave": 0
  }
}
```

## Key Insights & Gotchas

### What Works
- **Consistent ID naming**: Use "obj-1", "obj-2", etc.
- **Proper outlet types**: Match object documentation
- **Standard positioning**: Grid-aligned coordinates
- **Complete metadata**: Include all required patcher properties

### Common Errors
- **Missing commas**: JSON syntax errors break loading
- **Invalid object IDs**: Connections fail if IDs don't match
- **Wrong inlet/outlet numbers**: Connections won't work
- **Missing required properties**: Some objects need specific parameters

### Performance Notes
- **Keep patches simple**: Complex JSON structures can be slow to load
- **Use proper spacing**: Overlapping objects cause visual issues
- **Test incrementally**: Build and test patches step by step

## Future Areas to Explore

1. **Subpatchers**: Nested patcher objects
2. **Audio patching**: MSP-specific object requirements  
3. **JavaScript integration**: jsui and js object parameters
4. **MIDI objects**: Note handling and timing
5. **UI customization**: Presentation mode and custom interfaces
6. **File I/O**: Buffer loading and audio file handling

## Resources

- **py2max library**: Python reference implementation
- **Max SDK**: Official development tools
- **Max documentation**: Object reference and tutorials
- **Project Knowledge**: Max documentation indexes for object research

---

*Generated from practical Max patch creation experience - proven to create working patches!*
