"""
graph.py
Endpoint for generating math graphs on the server.
Used by the Learn tab — AI includes graph requests in its JSON response,
frontend calls this endpoint to render them.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Optional

from api.graph_engine import generate_graph, GRAPH_RENDERERS

router = APIRouter(prefix="/graph", tags=["graph"])


class GraphRequest(BaseModel):
    graph_type: str       # e.g. "function_plot", "tangent_line", etc.
    data: dict[str, Any]  # type-specific parameters


class GraphResponse(BaseModel):
    image_base64: str     # PNG as base64 string
    graph_type: str


@router.post("/generate", response_model=GraphResponse)
def generate(req: GraphRequest):
    """Generate a math graph and return as base64-encoded PNG."""
    if req.graph_type not in GRAPH_RENDERERS:
        raise HTTPException(
            400,
            f"Unknown graph type '{req.graph_type}'. "
            f"Valid types: {sorted(GRAPH_RENDERERS.keys())}"
        )
    try:
        image_b64 = generate_graph(req.graph_type, req.data)
        return GraphResponse(image_base64=image_b64, graph_type=req.graph_type)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Graph generation failed: {e}")


@router.get("/types")
def list_types():
    """List all available graph types."""
    return {"graph_types": sorted(GRAPH_RENDERERS.keys())}
