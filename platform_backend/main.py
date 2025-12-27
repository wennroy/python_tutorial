"""
Python Tutorial Platform - Backend API
FastAPI server that serves curriculum content and user code files.
"""

import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import markdown
import json

# Initialize FastAPI app
app = FastAPI(
    title="Python Tutorial Platform",
    description="Interactive Python learning platform with AI-enhanced tutorials",
    version="1.0.0"
)

# CORS configuration for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
CONTENT_DIR = Path(os.environ.get("CONTENT_DIR", "../curriculum_content"))
WORKSPACE_DIR = Path(os.environ.get("WORKSPACE_DIR", "../workspace"))


def get_curriculum_structure() -> dict:
    """
    Scan the content directory and build a curriculum structure.
    Returns a nested dictionary representing the course structure.
    """
    curriculum = {"modules": []}
    
    if not CONTENT_DIR.exists():
        return curriculum
    
    # Sort directories to maintain order
    for module_dir in sorted(CONTENT_DIR.iterdir()):
        if module_dir.is_dir() and not module_dir.name.startswith('.'):
            module = {
                "id": module_dir.name,
                "title": module_dir.name.replace('_', ' ').title(),
                "chapters": []
            }
            
            # Scan chapter files
            for chapter_file in sorted(module_dir.iterdir()):
                if chapter_file.suffix in ['.md', '.ipynb']:
                    chapter = {
                        "id": chapter_file.stem,
                        "title": chapter_file.stem.replace('_', ' ').title(),
                        "type": "markdown" if chapter_file.suffix == '.md' else "notebook",
                        "path": str(chapter_file.relative_to(CONTENT_DIR))
                    }
                    module["chapters"].append(chapter)
            
            curriculum["modules"].append(module)
    
    return curriculum


def render_markdown(content: str) -> str:
    """
    Convert markdown content to HTML with extensions.
    """
    extensions = [
        'fenced_code',
        'codehilite',
        'tables',
        'toc'
    ]
    return markdown.markdown(content, extensions=extensions)


def render_notebook(notebook_path: Path) -> str:
    """
    Convert Jupyter notebook to HTML.
    Uses nbconvert if available, otherwise returns raw JSON.
    """
    try:
        from nbconvert import HTMLExporter
        import nbformat
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        html_exporter = HTMLExporter()
        html_exporter.template_name = 'basic'
        (body, _) = html_exporter.from_notebook_node(notebook)
        return body
    except ImportError:
        # Fallback: return formatted JSON if nbconvert not available
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Simple rendering of notebook cells
        html_parts = []
        for cell in notebook.get('cells', []):
            cell_type = cell.get('cell_type', '')
            source = ''.join(cell.get('source', []))
            
            if cell_type == 'markdown':
                html_parts.append(render_markdown(source))
            elif cell_type == 'code':
                html_parts.append(f'<pre><code class="language-python">{source}</code></pre>')
        
        return '\n'.join(html_parts)


# ============== API Endpoints ==============

@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {"status": "ok", "message": "Python Tutorial Platform API"}


@app.get("/api/curriculum")
async def get_curriculum():
    """
    Get the complete curriculum structure.
    Returns a JSON object with all modules and chapters.
    """
    return get_curriculum_structure()


@app.get("/api/chapter/{module_id}/{chapter_id}")
async def get_chapter(module_id: str, chapter_id: str):
    """
    Get rendered HTML content for a specific chapter.
    Supports both Markdown (.md) and Jupyter Notebook (.ipynb) files.
    """
    # Try to find the chapter file
    module_path = CONTENT_DIR / module_id
    
    if not module_path.exists():
        raise HTTPException(status_code=404, detail=f"Module '{module_id}' not found")
    
    # Look for markdown or notebook file
    md_path = module_path / f"{chapter_id}.md"
    ipynb_path = module_path / f"{chapter_id}.ipynb"
    
    if md_path.exists():
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        html_content = render_markdown(content)
        return {"type": "markdown", "content": html_content, "raw": content}
    
    elif ipynb_path.exists():
        html_content = render_notebook(ipynb_path)
        return {"type": "notebook", "content": html_content}
    
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Chapter '{chapter_id}' not found in module '{module_id}'"
        )


@app.get("/api/code/{filename}")
async def get_user_code(filename: str):
    """
    Read user's exercise code file from workspace.
    Used for real-time code display and diff comparison.
    """
    # Security: only allow .py files and prevent path traversal
    if not filename.endswith('.py') or '..' in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    file_path = WORKSPACE_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {"filename": filename, "content": content}


from pydantic import BaseModel

class CodeSaveRequest(BaseModel):
    filename: str
    content: str


@app.post("/api/code/save")
async def save_user_code(request: CodeSaveRequest):
    """
    Save or create user's exercise code file in workspace.
    Creates the file if it doesn't exist.
    """
    filename = request.filename
    content = request.content
    
    # Security: only allow .py files and prevent path traversal
    if not filename.endswith('.py') or '..' in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    file_path = WORKSPACE_DIR / filename
    
    # Ensure workspace directory exists
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Write the file (creates if not exists)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return {"status": "ok", "filename": filename, "message": "File saved successfully"}


@app.get("/api/solution/{module_id}/{exercise_id}")
async def get_solution(module_id: str, exercise_id: str):
    """
    Get the reference solution for an exercise.
    Used for diff comparison with user's code.
    """
    solution_path = CONTENT_DIR / module_id / "solutions" / f"{exercise_id}.py"
    
    if not solution_path.exists():
        raise HTTPException(status_code=404, detail="Solution not found")
    
    with open(solution_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {"exercise_id": exercise_id, "solution": content}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
