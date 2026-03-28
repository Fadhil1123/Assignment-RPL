# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **FastAPI docs, SQLAlchemy docs, Pydantic v2 docs, pytest docs**

This assignment took me about **TODO** hours to do.


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> Branch: `feat/week7-task1-endpoints-validations`
> 
> Commit: `0f9c1dc` (week7 task1: add endpoint validation and error handling)
>
> Compare URL: `https://github.com/Fadhil1123/Assignment-RPL/compare/master...feat/week7-task1-endpoints-validations?expand=1`
>
> PR: `https://github.com/Fadhil1123/Assignment-RPL/pull/2`

b. PR Description
> Implemented additional API endpoints and stricter validation/error handling across notes and action-items routes.
>
> Scope:
> - Added new endpoints: get by id and delete for notes/action-items.
> - Enforced stronger payload validation (trim whitespace, non-empty text, length constraints).
> - Added strict pagination and sorting validation (`skip`, `limit`, allowed sort fields).
> - Standardized error responses for invalid sort fields and missing resources.
>
> Testing performed:
> - `python -m black .`
> - `python -m ruff check . --fix`
> - `python -m pytest -q backend/tests`
> - Result: all tests passed.

c. Graphite Diamond generated code review
> Graphite provided one concrete comment on this PR: the PATCH flow for action items could not explicitly clear/unassign `project_id` because update logic only ran when the value was not `None`.
>
> My assessment of the comment:
> - Type: correctness / potential edge-case behavior
> - Quality: useful and specific
> - Action taken: recorded as a valid follow-up item and included in review notes for API patch semantics.

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> Branch: `feat/week7-task2-extend-extraction`
>
> Commit: `5c3741e` (week7 task2: extend extraction patterns and dedup logic)
>
> Compare URL: `https://github.com/Fadhil1123/Assignment-RPL/compare/feat/week7-task1-endpoints-validations...feat/week7-task2-extend-extraction?expand=1`
>
> PR: `https://github.com/Fadhil1123/Assignment-RPL/pull/1`

b. PR Description
> Extended extraction logic to detect action items using richer patterns and reduce duplicates.
>
> Scope:
> - Added regex-based pattern matching for actionable language (e.g., "need to", "must", "please", "follow up", owner markers, due/before/by date expressions).
> - Added line normalization for bullets and numbered lines.
> - Added de-duplication to avoid repeated extracted items.
> - Preserved legacy behavior for TODO/ACTION prefixes and exclamation-mark actionable lines.
>
> Testing performed:
> - Added tests for extended patterns, de-duplication, and empty input.
> - Ran full backend test suite.
> - Result: all tests passed.

c. Graphite Diamond generated code review
> No additional Graphite comments were generated on this PR.
>
> Interpretation:
> - Either no actionable issues were detected in this diff, or the review did not emit additional findings beyond checks.
> - I still performed manual review on regex precision/recall and dedup behavior.

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> Branch: `feat/week7-task3-project-model-relationship`
>
> Commit: `56c347a` (week7 task3: add project model relationships and project endpoints)
>
> Compare URL: `https://github.com/Fadhil1123/Assignment-RPL/compare/feat/week7-task2-extend-extraction...feat/week7-task3-project-model-relationship?expand=1`
>
> PR: `https://github.com/Fadhil1123/Assignment-RPL/pull/3`

b. PR Description
> Added a new `Project` model and linked it to existing entities.
>
> Scope:
> - Added `Project` model with timestamps and unique name.
> - Added nullable `project_id` relationships for `Note` and `ActionItem`.
> - Added a full `/projects` router (list/create/get/patch/delete).
> - Added relation-aware validation when assigning `project_id` to notes and action-items.
> - Updated app router wiring and seed SQL schema to include project table and foreign keys.
>
> Testing performed:
> - Added dedicated tests for project CRUD and uniqueness constraints.
> - Added relation tests for assigning valid/invalid project references.
> - Ran full backend test suite.
> - Result: all tests passed.

c. Graphite Diamond generated code review
> No additional Graphite comments were generated on this PR.
>
> Interpretation:
> - No model/relationship issues were surfaced by AI review for this diff.
> - Manual review remained the main signal for relation integrity and endpoint consistency.

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> Branch: `feat/week7-task4-pagination-sorting-tests`
>
> Commit: `dac39bb` (week7 task4: improve pagination and sorting test coverage)
>
> Compare URL: `https://github.com/Fadhil1123/Assignment-RPL/compare/feat/week7-task3-project-model-relationship...feat/week7-task4-pagination-sorting-tests?expand=1`
>
> PR: `https://github.com/Fadhil1123/Assignment-RPL/pull/4`

b. PR Description
> Expanded test coverage for pagination and sorting behavior on notes, action-items, and projects.
>
> Scope:
> - Added test scenarios for `skip`/`limit` combinations.
> - Added explicit ascending/descending sort assertions.
> - Added invalid sort-field tests returning 422.
> - Added filtering + sorting checks and post-delete behavior checks.
>
> Testing performed:
> - Updated test files for notes/action-items/extract and added project tests.
> - Ran full backend test suite.
> - Result: all tests passed (`10 passed`).

c. Graphite Diamond generated code review
> No additional Graphite comments were generated on this PR.
>
> Interpretation:
> - AI review did not flag test-coverage issues in this change set.
> - I relied on manual review to verify assertion strength and edge-case coverage.

## Brief Reflection 
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> My manual review comments usually focused on correctness and API contract clarity first (status codes, validation semantics, missing-resource behavior), then maintainability (naming, route consistency, and schema readability), and finally test gaps (edge cases for invalid sort, whitespace-only input, and relation integrity). I also looked for practical robustness issues such as deduplication logic and accidental fallback behavior.

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> Task 1: Graphite produced one concrete edge-case comment (PATCH unassign `project_id` semantics), while my manual comments were broader around validation consistency and error shape. Here Graphite was better at pinpointing a narrow behavioral gap.
>
> Task 2: Graphite produced no extra comments. My manual review contributed the main feedback on extraction precision/recall tradeoffs and dedup expectations.
>
> Task 3: Graphite produced no extra comments. My manual review remained primary for relationship design and endpoint consistency checks.
>
> Task 4: Graphite produced no extra comments. My manual review drove confidence in test coverage quality (skip/limit/sort/error-path assertions).

c. When the AI reviews were better/worse than yours (cite specific examples)
> Better example: In PR Task 1 (`/pull/2`), Graphite highlighted a specific PATCH edge case where `project_id` could not be explicitly cleared. That was more precise than my initial high-level validation review.
>
> Worse/limited example: In PR Task 2, 3, and 4, Graphite did not provide additional comments. In those PRs, manual review gave more practical value for deciding whether behavior and tests matched assignment intent.

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
> I am comfortable using AI review as a second-pass reviewer for consistency checks and broad issue scanning, but I do not fully trust it for product-context or intent-sensitive decisions. My current heuristic is: trust AI for mechanical checks (validation, missing tests, obvious edge cases), and rely on manual review for behavior expectations, tradeoffs, and domain-specific correctness.



