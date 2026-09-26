
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    String,
    Text,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pgvector.sqlalchemy import Vector

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    source_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    source_uri: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    version: Mapped[str] = mapped_column(
        String(100),
        default="1.0"
    )

    content_hash: Mapped[Optional[str]] = mapped_column(
        String(128),
        nullable=True,
        index=True
    )

    effective_from: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    effective_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan"
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
        index=True
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    embedding: Mapped[Optional[list]] = mapped_column(
        Vector(1536),
        nullable=True
    )

    metadata_json: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    document = relationship(
        "Document",
        back_populates="chunks"
    )


class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    entity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        index=True
    )

    external_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    properties: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    version: Mapped[str] = mapped_column(
        String(100),
        default="1.0"
    )

    source_document_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("documents.id"),
        nullable=True
    )

    authority_level: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    effective_from: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    effective_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    policy_id: Mapped[int] = mapped_column(
        ForeignKey("policies.id"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    condition: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    action: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=1.0
    )

    requires_human_validation: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    source_document_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("documents.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    skill_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    version: Mapped[str] = mapped_column(
        String(100),
        default="1.0"
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="draft"
    )

    risk_level: Mapped[str] = mapped_column(
        String(50),
        default="medium"
    )

    definition: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    requires_approval: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    steps = relationship(
        "SkillStep",
        back_populates="skill",
        cascade="all, delete-orphan"
    )


class SkillStep(Base):
    __tablename__ = "skill_steps"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        nullable=False,
        index=True
    )

    step_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    action: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    tool_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    requires_approval: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    skill = relationship(
        "Skill",
        back_populates="steps"
    )


class Execution(Base):
    __tablename__ = "executions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    execution_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    skill_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("skills.id"),
        nullable=True
    )

    agent_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    input_data: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )

    output_data: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="started"
    )

    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    execution_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        index=True,
        nullable=True
    )

    actor_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    actor_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    action: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    reasoning: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    source_references: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )

    result: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )
