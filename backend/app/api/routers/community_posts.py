from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.core.database import get_db
from app.models.community_post import CommunityPost
from app.models.user import User
from app.schemas.community_post import (
    CommunityPost as CommunityPostSchema,
    CommunityPostCreate, CommunityPostUpdate, CommunityPostListResponse
)
from app.schemas.common import PaginationMeta
from app.core.security import get_current_user

router = APIRouter()


@router.get("/community-posts", response_model=CommunityPostListResponse)
def get_community_posts(
    search: Optional[str] = None,
    category: Optional[str] = None,
    club_id: Optional[int] = None,
    author_id: Optional[int] = None,
    keyword: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(CommunityPost)

    if search:
        query = query.filter(
            or_(
                CommunityPost.community_post_title.ilike(f"%{search}%"),
                CommunityPost.community_post_description.ilike(f"%{search}%")
            )
        )

    if category:
        query = query.filter(CommunityPost.community_post_category == category)

    if club_id:
        query = query.filter(CommunityPost.club_id == club_id)

    if author_id:
        query = query.filter(CommunityPost.user_id == author_id)

    if keyword:
        # Check if keyword is part of the comma-separated keywords string
        query = query.filter(CommunityPost.community_post_keywords.ilike(f"%{keyword}%"))

    total_items = query.count()
    offset = (page - 1) * page_size
    posts = query.offset(offset).limit(page_size).all()
    
    total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1

    meta = PaginationMeta(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages
    )

    return CommunityPostListResponse(items=posts, meta=meta)


@router.post("/community-posts", response_model=CommunityPostSchema, status_code=status.HTTP_201_CREATED)
def create_community_post(
    payload: CommunityPostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    keywords_str = None
    if payload.community_post_keywords:
        keywords_str = ",".join([k.strip() for k in payload.community_post_keywords if k.strip()])

    new_post = CommunityPost(
        community_post_title=payload.community_post_title,
        community_post_description=payload.community_post_description,
        community_post_category=payload.community_post_category,
        community_post_keywords=keywords_str,
        club_id=payload.club_id,
        user_id=current_user.user_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/community-posts/{postId}", response_model=CommunityPostSchema)
def get_community_post_by_id(
    postId: int,
    db: Session = Depends(get_db)
):
    post = db.query(CommunityPost).filter(CommunityPost.community_post_id == postId).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community post not found"
        )
    return post


@router.patch("/community-posts/{postId}", response_model=CommunityPostSchema)
def update_community_post(
    postId: int,
    payload: CommunityPostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(CommunityPost).filter(CommunityPost.community_post_id == postId).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community post not found"
        )

    # Ownership check
    if post.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this post"
        )

    update_data = payload.dict(exclude_unset=True)

    if "community_post_keywords" in update_data:
        keywords = update_data["community_post_keywords"]
        if keywords:
            update_data["community_post_keywords"] = ",".join([k.strip() for k in keywords if k.strip()])
        else:
            update_data["community_post_keywords"] = None

    for field, value in update_data.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post


@router.delete("/community-posts/{postId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_community_post(
    postId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(CommunityPost).filter(CommunityPost.community_post_id == postId).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community post not found"
        )

    # Ownership check
    if post.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post"
        )

    db.delete(post)
    db.commit()
    return None
