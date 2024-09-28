from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from .auth import get_current_active_user
from ..schema import Vote, UserResponse
from ..dependencies import db



router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: Vote, current_user: Annotated[UserResponse, Depends(get_current_active_user)]):
    post_exists = await db.fetchall("SELECT * FROM posts WHERE id = ($1) LIMIT 1",
                                 (vote.post_id,))
    if post_exists is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Post does not exists")
    rows = await db.fetchall("SELECT * FROM votes WHERE post_id = ($1) AND user_id = ($2);",
                                 (vote.post_id, current_user.id))
    if vote.liked == 1:
        if rows:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} already likes post {vote.post_id}")
        await db.execute("INSERT INTO votes (post_id, user_id) VALUES (($1),($2))", (vote.post_id, current_user.id))
        return {"message": "Vote added"}
    else:
        if not rows:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exists")
        await db.execute_and_get_record("DELETE FROM votes WHERE post_id = ($1) AND user_id = ($2)", (vote.post_id, current_user.id))
        return {"message": "Vote deleted"}