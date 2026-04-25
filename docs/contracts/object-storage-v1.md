# Object Storage Contract v1

Status: Baseline  
Date: 2026-03-02

## Purpose

Define a shared object-storage contract for attachment/file workflows across RM Orbit services.

## Backends

- `local` for development
- `s3` for S3-compatible providers (AWS S3, MinIO, R2 with S3 API compatibility)

## Canonical Environment Variables

- `STORAGE_BACKEND` (`local` or `s3`)
- `STORAGE_LOCAL_BASE_PATH` (local storage root directory)
- `STORAGE_BUCKET` (S3 bucket/container)
- `S3_ENDPOINT_URL` (optional; required for MinIO/custom endpoints)
- `S3_REGION` (default `us-east-1`)
- `S3_ACCESS_KEY_ID`
- `S3_SECRET_ACCESS_KEY`
- `S3_FORCE_PATH_STYLE` (`true` for MinIO/path-style setups)

## Object Key Shape

Use scoped keys in the pattern:

`<project_or_tenant_scope>/<object_name>`

Examples:

- `project-42/0af2f4f0a5ff4c35b7a0f2c1f8afc6f1.pdf`
- `tenant-7/email-9001/3f7f...png`

## Runtime Requirements

1. Upload paths must enforce tenant/org/project access checks before write.
2. Downloads must enforce the same scope checks before read.
3. Deletions must be idempotent and safe when object is already absent.
4. Metadata in application DB should retain:
   - logical owner scope
   - original filename
   - content type
   - byte size

## Current Adoption

- Mail: presigned upload/download flow with local+S3 providers.
- Atlas: attachment upload/download/delete now routed through pluggable object storage providers (local+S3).
