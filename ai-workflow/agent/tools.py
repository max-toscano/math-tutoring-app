"""
tools.py
Tool registry for the ReAct agent.

Every tool here gives the agent a capability it DOES NOT have on its own.
If GPT-4o can do it in its own response, it's not a tool — it's a prompt instruction.

Tools (4 total):
  - get_hint_strategy      : DB + logic — recommend a tutoring mode based on real mastery data
  - get_student_progress   : DB query   — topic mastery from student_profiles
  - get_weak_areas         : DB query   — weak topics from student_profiles
  - generate_graph         : Pure logic  — render matplotlib graphs (LLM can't make images)
"""

import json
from typing import Callable

from sqlalchemy import text
from sqlalchemy.orm import Session

from api.graph_engine import generate_graph, GRAPH_RENDERERS


# ---------------------------------------------------------------------------
# 1. get_hint_strategy — DB + logic
# ---------------------------------------------------------------------------

def tool_get_hint_strategy(params: dict, **ctx) -> dict:
    """
    Recommend a tutoring mode based on the student's mastery on this topic
    and their current session state.

    This is a real tool because it reads actual data from the database
    and applies deterministic logic the LLM can't replicate by guessing.
    """
    db: Session = ctx.get("db")
    user_id = ctx.get("user_id")
    topic = params.get("topic", "")

    if not db or not user_id:
        return {"recommended_mode": "socratic", "reason": "No database context available, defaulting to socratic"}

    row = db.execute(
        text("SELECT topic_mastery, frustration_threshold FROM student_profiles WHERE student_id = :sid"),
        {"sid": str(user_id)},
    ).mappings().first()

    if not row:
        return {"recommended_mode": "socratic", "reason": "No student profile found, defaulting to socratic"}

    topic_mastery = row["topic_mastery"] or {}
    frustration_threshold = row["frustration_threshold"] or 3

    topic_data = topic_mastery.get(topic, {})
    mastery = topic_data.get("mastery", 0.5)
    trend = topic_data.get("trend", "stable")
    avg_hints = topic_data.get("avg_hints_needed", 0)

    # Check current session for frustration
    session_frustration = 0
    active_session = db.execute(
        text("SELECT session_state FROM agent_sessions WHERE student_id = :sid AND is_active = true"),
        {"sid": str(user_id)},
    ).mappings().first()

    if active_session:
        state = active_session["session_state"] or {}
        session_frustration = state.get("frustration_signals", 0)

    # Decision logic
    if session_frustration >= 2:
        return {
            "recommended_mode": "direct",
            "reason": f"Student showing {session_frustration} frustration signals this session. Switch to direct to reduce friction.",
            "mastery": mastery,
            "trend": trend,
        }

    if mastery < 0.3:
        return {
            "recommended_mode": "concept_first",
            "reason": f"Mastery on '{topic}' is {mastery:.0%} — student needs the foundational concept before attempting problems.",
            "mastery": mastery,
            "trend": trend,
        }

    if mastery < 0.6 and trend == "declining":
        return {
            "recommended_mode": "concept_first",
            "reason": f"Mastery on '{topic}' is {mastery:.0%} and declining — re-teach the concept.",
            "mastery": mastery,
            "trend": trend,
        }

    if avg_hints > 2.0:
        return {
            "recommended_mode": "concept_first",
            "reason": f"Student averages {avg_hints:.1f} hints per problem on '{topic}' — needs stronger foundation.",
            "mastery": mastery,
            "trend": trend,
        }

    return {
        "recommended_mode": "socratic",
        "reason": f"Mastery on '{topic}' is {mastery:.0%} ({trend}) — guide with questions.",
        "mastery": mastery,
        "trend": trend,
    }


# ---------------------------------------------------------------------------
# 2. get_student_progress — DB query (queries student_profiles)
# ---------------------------------------------------------------------------

def tool_get_student_progress(params: dict, **ctx) -> dict:
    """Look up a student's topic mastery from student_profiles."""
    db: Session = ctx.get("db")
    user_id = ctx.get("user_id")
    if not db or not user_id:
        return {"error": "Missing database context"}

    row = db.execute(
        text("""
            SELECT topic_mastery, course_enrollment, total_sessions,
                   total_problems_attempted, overall_success_rate, longest_streak
            FROM student_profiles WHERE student_id = :sid
        """),
        {"sid": str(user_id)},
    ).mappings().first()

    if not row:
        return {"progress": [], "count": 0, "note": "No student profile found"}

    topic_mastery = row["topic_mastery"] or {}
    course = row["course_enrollment"] or {}

    results = []
    for topic, data in topic_mastery.items():
        results.append({
            "topic": topic,
            "mastery": data.get("mastery", 0),
            "trend": data.get("trend", "unknown"),
            "attempts": data.get("attempts", 0),
            "avg_hints_needed": data.get("avg_hints_needed", 0),
            "avg_time_seconds": data.get("avg_time_seconds", 0),
            "last_practiced": data.get("last_practiced"),
        })

    results.sort(key=lambda r: r.get("last_practiced") or "", reverse=True)

    return {
        "progress": results,
        "count": len(results),
        "course": course,
        "lifetime_stats": {
            "total_sessions": row["total_sessions"],
            "total_problems": row["total_problems_attempted"],
            "success_rate": row["overall_success_rate"],
            "longest_streak": row["longest_streak"],
        },
    }


# ---------------------------------------------------------------------------
# 3. get_weak_areas — DB query (queries student_profiles)
# ---------------------------------------------------------------------------

def tool_get_weak_areas(params: dict, **ctx) -> dict:
    """Find topics where the student struggles most, from student_profiles."""
    db: Session = ctx.get("db")
    user_id = ctx.get("user_id")
    if not db or not user_id:
        return {"error": "Missing database context"}

    row = db.execute(
        text("SELECT topic_mastery, weak_areas FROM student_profiles WHERE student_id = :sid"),
        {"sid": str(user_id)},
    ).mappings().first()

    if not row:
        return {"weak_topics": [], "weak_areas": [], "count": 0}

    weak_areas = row["weak_areas"] or []

    topic_mastery = row["topic_mastery"] or {}
    weak_topics = []
    for topic, data in topic_mastery.items():
        mastery = data.get("mastery", 0)
        if mastery < 0.5 and data.get("attempts", 0) >= 2:
            weak_topics.append({
                "topic": topic,
                "mastery": mastery,
                "trend": data.get("trend", "unknown"),
                "attempts": data.get("attempts", 0),
                "avg_hints_needed": data.get("avg_hints_needed", 0),
            })

    weak_topics.sort(key=lambda t: t["mastery"])

    return {
        "weak_topics": weak_topics,
        "weak_areas": weak_areas,
        "count": len(weak_topics),
    }


# ---------------------------------------------------------------------------
# 4. generate_graph — Pure logic (matplotlib)
# ---------------------------------------------------------------------------

def tool_generate_graph(params: dict, **ctx) -> dict:
    """Render a matplotlib graph and return base64 image data."""
    graph_type = params.get("graph_type", "")
    data = params.get("data", {})

    if graph_type not in GRAPH_RENDERERS:
        return {"error": f"Unknown graph type '{graph_type}'. Available: {list(GRAPH_RENDERERS.keys())}"}

    try:
        image_b64 = generate_graph(graph_type, data)
        return {"success": True, "graph_type": graph_type, "image_base64": image_b64}
    except Exception as e:
        return {"error": f"Graph rendering failed: {str(e)}"}


# ---------------------------------------------------------------------------
# Tool schemas (sent to the LLM so it knows how to call each tool)
# ---------------------------------------------------------------------------

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_hint_strategy",
            "description": (
                "Get a recommended tutoring mode for this student on a specific topic. "
                "Looks at the student's mastery level, trend, hint history, and current "
                "session frustration to recommend socratic, direct, or concept_first. "
                "Call this when no mode was selected by the student and you need to "
                "decide how to approach the problem."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic slug (e.g. 'double_angle', 'chain_rule').",
                    },
                },
                "required": ["topic"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_student_progress",
            "description": (
                "Look up the student's topic mastery scores, trends, attempt counts, "
                "and lifetime stats. Shows how well they know each topic they've practiced."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "Optional subject filter (e.g. 'trigonometry', 'calculus_1'). Omit to get all topics.",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weak_areas",
            "description": (
                "Find topics where the student is struggling — low mastery scores, "
                "declining trends, and specific sub-skill weaknesses."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_graph",
            "description": (
                "Generate a math graph/visualization and return it as an image. "
                "Available types: function_plot, tangent_line, derivative_analysis, "
                "riemann_sum, area_between, volume_revolution, limit, newtons_method."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "graph_type": {
                        "type": "string",
                        "enum": list(GRAPH_RENDERERS.keys()),
                        "description": "The type of graph to generate",
                    },
                    "data": {
                        "type": "object",
                        "description": (
                            "Graph-specific parameters. For function_plot: {expressions: ['x**2'], x_range: [-5,5], title: '...'}. "
                            "For tangent_line: {expression: 'x**2', point: 2, title: '...'}. "
                            "For riemann_sum: {expression: 'x**2', a: 0, b: 2, n: 6, method: 'left'}."
                        ),
                    },
                },
                "required": ["graph_type", "data"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Registry: maps tool name -> callable
# ---------------------------------------------------------------------------

TOOL_IMPLEMENTATIONS: dict[str, Callable] = {
    "get_hint_strategy": tool_get_hint_strategy,
    "get_student_progress": tool_get_student_progress,
    "get_weak_areas": tool_get_weak_areas,
    "generate_graph": tool_generate_graph,
}


def execute_tool(tool_name: str, params: dict, **ctx) -> str:
    """Execute a tool by name and return the result as a JSON string."""
    fn = TOOL_IMPLEMENTATIONS.get(tool_name)
    if not fn:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    try:
        result = fn(params, **ctx)
        return json.dumps(result, default=str)
    except Exception as e:
        return json.dumps({"error": f"Tool '{tool_name}' failed: {str(e)}"})
