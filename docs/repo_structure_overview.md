# Ignition Demo Project Overview

This document captures the layout and key conventions of the Ignition demo project to make it easier to navigate and extend.

## Top-level layout

- `MES_Project/` – Source code organized the way Ignition exports scripts, broken down into adapters, common utilities, domain cores, and infrastructure glue code.
- `tests/` – Python tests that exercise the Ignition modules via the infrastructure bootstrapper.

Within `MES_Project/`, each major business capability (production, energy, maintenance, quality, etc.) lives under `core/`, while shared functionality resides in `common/`, and integration points (messaging, cache providers) are exposed through `adapters/`. The `infrastructure/` package wires everything together at runtime.

## Script module convention

Every Ignition script package is represented as a directory that contains two files:

- `code.py` with the actual Python functions and classes.
- `resource.json` with Ignition-specific metadata (module name, enabled flag, timestamps).

For example, the production domain entities package contains both files, with `resource.json` storing the metadata Ignition needs to re-create the script module. 【F:MES_Project/core/production/domain/entities/resource.json†L1-L9】

Services typically expose Python classes with methods that publish events through the shared messaging router. For instance, the production service constructs messaging envelopes and sends them via the router whenever orders are created or updated. 【F:MES_Project/core/production/application/services/code.py†L2-L18】

## Infrastructure bootstrap

The `MES_Project/infrastructure/bootstrap` package provides an entry point for tests and runtime. Its `start` function registers messaging adapters, configures the cache provider, instantiates all core services, and wires up event-driven callbacks that coordinate modules such as inventory, planning, energy, KPI, alerts, quality, and maintenance. 【F:MES_Project/infrastructure/bootstrap/code.py†L2-L66】

This bootstrapper is used by the end-to-end test to verify that a material receipt flows through production, energy, and KPI services while reading and writing shared cache state. 【F:tests/test_e2e_flow.py†L2-L19】

## Shared utilities

Shared modules under `MES_Project/common/` provide reusable services like the cache provider. The cache module exposes a provider interface, an in-memory implementation, and helper functions for swapping providers and accessing cached data. This mirrors how Ignition projects abstract backend services behind script modules. 【F:MES_Project/common/cache/cache_provider/code.py†L2-L19】

With this structure in mind, new Ignition functionality can be added by introducing a new script package (directory with `code.py` and `resource.json`), wiring it through the bootstrapper, and extending the tests to cover the new flows.
