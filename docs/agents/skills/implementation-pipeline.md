# implementation pipeline

## Overview

A deterministic, low-branching pipeline for delivering code changes.

## Phase 1: scope

- restate requirement in precise terms
- identify constraints (performance, API, environment)

## Phase 2: locate

- search only for symbols and files directly related
- read minimal code necessary to understand flow

## Phase 3: plan

- ≤ 5 concrete steps
- include where changes will occur

## Phase 4: implement

- write code in smallest viable diff
- avoid opportunistic refactors

## Phase 5: verify

- run targeted tests or commands
- add tests if missing

## Phase 6: finalize

- summarize changes and evidence
- note risks and follow-ups

## Failure handling

If verification fails:

- capture exact error
- trace to root cause
- modify only relevant code

Do not restart from scratch unless the model of the system is invalid.
