from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Project
from ..schemas import ActionItemCreate, ActionItemPatch, ActionItemRead

router = APIRouter(prefix="/action-items", tags=["action_items"])

ALLOWED_SORT_FIELDS = {"id", "description", "completed", "created_at", "updated_at"}


@router.get("/", response_model=list[ActionItemRead])
def list_items(
    db: Session = Depends(get_db),
    completed: bool | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    sort: str = Query("-created_at"),
) -> list[ActionItemRead]:
    stmt = select(ActionItem)
    if completed is not None:
        stmt = stmt.where(ActionItem.completed.is_(completed))

    sort_field = sort.lstrip("-")
    if sort_field not in ALLOWED_SORT_FIELDS:
        allowed = ", ".join(sorted(ALLOWED_SORT_FIELDS))
        raise HTTPException(
            status_code=422, detail=f"Invalid sort field: {sort_field}. Allowed: {allowed}"
        )

    order_fn = desc if sort.startswith("-") else asc
    stmt = stmt.order_by(order_fn(getattr(ActionItem, sort_field)))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [ActionItemRead.model_validate(row) for row in rows]


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    if payload.project_id is not None and not db.get(Project, payload.project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    item = ActionItem(
        description=payload.description, completed=False, project_id=payload.project_id
    )
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.get("/{item_id}", response_model=ActionItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    return ActionItemRead.model_validate(item)


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.patch("/{item_id}", response_model=ActionItemRead)
def patch_item(
    item_id: int, payload: ActionItemPatch, db: Session = Depends(get_db)
) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    if payload.description is not None:
        item.description = payload.description
    if payload.completed is not None:
        item.completed = payload.completed
    if payload.project_id is not None:
        project = db.get(Project, payload.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        item.project_id = payload.project_id
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Response:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    db.delete(item)
    db.flush()
    return Response(status_code=204)
