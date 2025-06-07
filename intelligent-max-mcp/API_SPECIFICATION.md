# Intelligent Max MCP Server - API Specification

## MCP Function Definitions

### Knowledge Base Functions

#### `max_query_docs(object_name: str) → Documentation`
Query official Cycling '74 documentation for a specific Max object.

**Parameters:**
- `object_name`: Name of Max object (e.g., "metro", "delay~", "jsui")

**Returns:**
- Complete documentation including description, inlets, outlets, attributes, examples

#### `max_query_minutiae(pattern: str) → MinutiaeResults`
Search our interleaved-max-minutiae knowledge base for patterns and discoveries.

**Parameters:** 
- `pattern`: Search query (e.g., "temporal scaffolding", "breaks manipulation")

**Returns:**
- Relevant knowledge entries with confidence scores and source references

#### `max_enhance_knowledge(discovery: dict) → bool`
Add new discovered pattern to the knowledge base.

**Parameters:**
- `discovery`: Pattern data with metadata, examples, and validation info

**Returns:**
- Success status of knowledge base integration

### Patcher Generation Functions

#### `max_create_patcher(template: str = "basic", config: dict = {}) → PatcherJSON`
Create a new Max patcher with intelligent defaults.

**Parameters:**
- `template`: Base template ("basic", "temporal_scaffolding", "sample_manipulation", "jsui")
- `config`: Configuration options (window size, grid settings, etc.)

**Returns:**
- Complete Max patcher JSON structure

#### `max_add_object(patcher_id: str, obj_type: str, position: tuple, **kwargs) → ObjectID`
Add a Max object to an existing patcher with intelligent positioning and configuration.

**Parameters:**
- `patcher_id`: Target patcher identifier
- `obj_type`: Max object type ("metro", "cycle~", "button", etc.)
- `position`: (x, y) coordinates
- `**kwargs`: Object-specific arguments and attributes

**Returns:**
- Unique identifier for the created object

#### `max_connect_objects(src_id: str, outlet: int, dst_id: str, inlet: int) → ConnectionID`
Create patch cord between objects with validation.

**Parameters:**
- `src_id`: Source object identifier
- `outlet`: Source object outlet number
- `dst_id`: Destination object identifier  
- `inlet`: Destination object inlet number

**Returns:**
- Unique identifier for the connection

### High-Level Generation Functions

#### `max_create_temporal_scaffolding(function_type: str, config: dict) → PatcherJSON`
Generate complete temporal scaffolding system based on mathematical functions.

**Parameters:**
- `function_type`: Mathematical function ("linear", "exponential", "trigonometric", "polynomial")
- `config`: Quantization, output routing, UI options

**Returns:**
- Complete patcher with jsui, function generators, quantization, and output routing

#### `max_create_sample_chain(technique: str, features: list) → PatcherJSON`
Generate sample manipulation chain based on documented techniques.

**Parameters:**
- `technique`: Base technique ("breaks_manipulation", "granular", "timestretch")
- `features`: Additional features to include

**Returns:**
- Complete patcher with buffer objects, processing chain, and controls

#### `max_create_jsui_template(ui_type: str, dimensions: tuple) → PatcherJSON`
Generate jsui-based interface with mathematical visualization capabilities.

**Parameters:**
- `ui_type`: Interface type ("function_plotter", "waveform_display", "control_matrix")
- `dimensions`: (width, height) in pixels

**Returns:**
- Patcher with jsui object and supporting JavaScript code

### Analysis and Optimization Functions

#### `max_analyze_patcher(patcher_json: dict) → AnalysisResult`
Analyze existing patcher for patterns, optimizations, and potential improvements.

**Parameters:**
- `patcher_json`: Complete Max patcher JSON structure

**Returns:**
- Analysis results with suggestions, performance metrics, and pattern recognition

#### `max_optimize_layout(patcher_json: dict, style: str) → PatcherJSON`
Optimize patcher layout based on documented best practices.

**Parameters:**
- `patcher_json`: Patcher to optimize
- `style`: Layout style ("performance", "educational", "compact", "presentation")

**Returns:**
- Optimized patcher with improved object positioning and organization

#### `max_suggest_improvements(patcher_json: dict) → Suggestions`
Provide intelligent suggestions based on knowledge base patterns.

**Parameters:**
- `patcher_json`: Patcher to analyze

**Returns:**
- List of suggestions with confidence scores and implementation details

## Data Types

### PatcherJSON
```python
{
    "patcher": {
        "fileversion": 1,
        "appversion": {"major": 8, "minor": 6, "revision": 4},
        "rect": [100, 100, 800, 600],
        "bglocked": 0,
        "openinpresentation": 0,
        "boxes": [...],  # Object definitions
        "lines": [...],  # Patch cord definitions
        "dependency_cache": [...],
        "autosave": 0
    }
}
```

### Documentation
```python
{
    "object_name": str,
    "description": str,
    "inlets": [{"index": int, "type": str, "description": str}],
    "outlets": [{"index": int, "type": str, "description": str}],
    "attributes": {...},
    "examples": [...],
    "source": "cycling74" | "minutiae",
    "confidence": float
}
```

### MinutiaeResults
```python
{
    "query": str,
    "results": [
        {
            "pattern_name": str,
            "description": str,
            "source_file": str,
            "confidence_score": float,
            "tags": [str],
            "examples": [...]
        }
    ],
    "total_results": int
}
```

### AnalysisResult
```python
{
    "object_count": int,
    "connection_count": int,
    "complexity_score": float,
    "performance_rating": str,
    "identified_patterns": [...],
    "suggested_optimizations": [...],
    "potential_issues": [...]
}
```

## Error Handling

### Standard Error Responses
```python
{
    "error": str,
    "error_code": str,
    "details": dict,
    "suggested_action": str
}
```

### Common Error Codes
- `INVALID_OBJECT_TYPE`: Unknown Max object type
- `CONNECTION_INVALID`: Invalid inlet/outlet connection
- `KNOWLEDGE_BASE_ERROR`: Error accessing knowledge sources
- `GENERATION_FAILED`: Patcher generation failed
- `VALIDATION_ERROR`: Input validation failed

## Usage Examples

### Basic Patcher Creation
```python
# Create temporal scaffolding system
patcher = max_create_temporal_scaffolding(
    function_type="exponential",
    config={
        "quantization": "16th",
        "acceleration": 2.5,
        "output_channels": ["kick", "snare", "hihat"],
        "ui_enabled": True
    }
)
```

### Knowledge Enhancement
```python
# Add discovered pattern
success = max_enhance_knowledge({
    "pattern_name": "efficient_buffer_routing",
    "description": "Optimized buffer~ to groove~ connection pattern",
    "examples": [...],
    "metadata": {"performance_gain": "15%", "complexity": "low"}
})
```

### Analysis and Optimization
```python
# Analyze and optimize existing patcher
analysis = max_analyze_patcher(user_patcher_json)
optimized = max_optimize_layout(user_patcher_json, style="performance")
suggestions = max_suggest_improvements(user_patcher_json)
```

---

*This API specification serves as the contract between the MCP server and clients, ensuring consistent and powerful Max/MSP integration.*
