from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, BigInteger, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.database import Base


class DockApp(Base):
    __tablename__ = "dock_apps"

    id = Column(String, primary_key=True)
    org_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    vendor = Column(String, default="")
    description = Column(String, default="")
    url = Column(String, nullable=True)
    advertised = Column(Boolean, default=True)
    license_model = Column(String, default="per_user")
    integrations = Column(JSONB, default=list)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class License(Base):
    __tablename__ = "dock_licenses"

    id = Column(String, primary_key=True)
    org_id = Column(String, nullable=False, index=True)
    app_id = Column(String, ForeignKey("dock_apps.id"), nullable=False)
    seats_purchased = Column(Integer, default=1)
    seats_assigned = Column(Integer, default=0)
    currency = Column(String, default="USD")
    total_cost = Column(Float, default=0.0)
    renewal_date = Column(String, nullable=True)
    status = Column(String, nullable=False, default="active")
    purchased_by = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Assignment(Base):
    __tablename__ = "dock_assignments"

    id = Column(String, primary_key=True)
    org_id = Column(String, nullable=False, index=True)
    app_id = Column(String, ForeignKey("dock_apps.id"), nullable=False)
    user_id = Column(String, nullable=False, index=True)
    access_level = Column(String, default="user")
    status = Column(String, default="active")
    assigned_by = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class DockRequest(Base):
    __tablename__ = "dock_requests"

    id = Column(String, primary_key=True)
    org_id = Column(String, nullable=False, index=True)
    requester_user_id = Column(String, nullable=False)
    app_name = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    requested_seats = Column(Integer, default=1)
    business_justification = Column(String, default="")
    status = Column(String, default="pending")
    reviewer_user_id = Column(String, nullable=True)
    review_notes = Column(String, nullable=True)
    linked_app_id = Column(String, nullable=True)
    automation_ticket_id = Column(String, nullable=True)
    automation_status = Column(String, default="idle")
    automation_last_error = Column(String, nullable=True)
    automation_hint = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class DockPackage(Base):
    __tablename__ = "dock_packages"

    id = Column(String, primary_key=True)
    org_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    version = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    size_bytes = Column(BigInteger, nullable=False, default=0)
    checksum = Column(String, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class DockAuditEvent(Base):
    __tablename__ = "dock_audit_events"

    id = Column(String, primary_key=True)
    event_type = Column(String, nullable=False)
    org_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False)
    role = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String, nullable=False)
    request_id = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    metadata_json = Column(JSONB, default=dict)


class BudgetPolicy(Base):
    __tablename__ = "dock_budget_policies"

    id = Column(String, primary_key=True)
    org_id = Column(String, nullable=False, index=True)
    department_id = Column(String, nullable=True, index=True)
    monthly_limit = Column(Float, nullable=False, default=0.0)
    currency = Column(String, nullable=False, default="USD")
    alert_threshold_pct = Column(Float, nullable=False, default=80.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProcurementConfig(Base):
    __tablename__ = "dock_procurement_configs"

    id = Column(String, primary_key=True)
    org_id = Column(String, nullable=False, index=True, unique=True)
    require_manager_approval = Column(Boolean, nullable=False, default=True)
    auto_approve_threshold = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
