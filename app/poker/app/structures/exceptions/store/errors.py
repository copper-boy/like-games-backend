from __future__ import annotations


class BaseStoreError(Exception):
    ...


class AccessorError(BaseStoreError):
    ...


class DatabaseError(BaseStoreError):
    ...


class DatabaseAccessorError(AccessorError, DatabaseError):
    ...
