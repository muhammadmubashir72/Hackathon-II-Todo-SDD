# Tasks: Phase I – In-Memory Todo Console Application

**Input**: Design documents from `/specs/1-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below DO NOT include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Create src/ directory with subdirectories (models/, services/, cli/, skills/, lib/)
- [ ] T003 Create __init__.py files for all src/ subdirectories
- [ ] T004 Create main.py entry point at repository root

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Models Layer

- [ ] T005 [P] Create Task entity in src/models/task.py with attributes (id, title, description, status, created_at, updated_at)
- [ ] T006 [P] Create TaskList collection in src/models/task.py with methods (add, get_by_id, update, delete, list_all, count_by_status)

### Skills Layer (Reusable Intelligence)

- [ ] T007 [P] Create task_validation skill in src/skills/task_validation.py with validation logic (title not empty, ID exists, prevent duplicates)
- [ ] T008 [P] Create input_parsing skill in src/skills/input_parsing.py with parsing logic (menu selections, text trimming, numeric validation)
- [ ] T009 [P] Create task_formatting skill in src/skills/task_formatting.py with formatting logic (ID, title, status, list layout)
- [ ] T010 [P] Create error_handling skill in src/skills/error_handling.py with error generation and display logic
- [ ] T011 [P] Create task_state_management skill in src/skills/task_state_management.py with state transition logic

### Utility Layer

- [ ] T012 [P] Create utils module in src/lib/utils.py with shared utilities (timestamp generation, ISO 8601 formatting)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks with titles/descriptions and view all tasks organized by completion status

**Independent Test**: Launch CLI, create multiple tasks with various titles, view task list, verify all tasks appear correctly with unique IDs and appropriate status indicators

### Implementation for User Story 1

- [ ] T013 [US1] Implement create_task operation in src/services/task_service.py (uses task_validation, input_parsing, task_state_management, task_formatting, error_handling)
- [ ] T014 [US1] Implement view_tasks operation in src/services/task_service.py (uses task_formatting, error_handling)
- [ ] T015 [US1] Implement TaskList.add method in src/models/task.py with sequential ID generation
- [ ] T016 [US1] Implement TaskList.list_all method in src/models/task.py
- [ ] T017 [US1] Implement TaskList.count_by_status method in src/models/task.py
- [ ] T018 [US1] Add "Add task" menu option in src/cli/main.py
- [ ] T019 [US1] Add "View tasks" menu option in src/cli/main.py
- [ ] T020 [US1] Wire create_task and view_tasks operations to CLI menu in src/cli/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Mark Tasks Complete or Incomplete (Priority: P2)

**Goal**: Users can indicate which tasks have been completed and can reopen completed tasks if needed

**Independent Test**: Create tasks, mark them complete, view updated status, then reopen completed tasks and verify state changes

### Implementation for User Story 2

- [ ] T021 [US2] Implement mark_complete operation in src/services/task_service.py (uses input_parsing, task_validation, task_state_management, error_handling, task_formatting)
- [ ] T022 [US2] Implement mark_incomplete operation in src/services/task_service.py (uses input_parsing, task_validation, task_state_management, error_handling, task_formatting)
- [ ] T023 [US2] Add "Mark complete" menu option in src/cli/main.py
- [ ] T024 [US2] Add "Mark incomplete" menu option in src/cli/main.py
- [ ] T025 [US2] Wire mark_complete and mark_incomplete operations to CLI menu in src/cli/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update and Delete Tasks (Priority: P3)

**Goal**: Users can correct mistakes in task information and remove tasks that are no longer relevant

**Independent Test**: Create tasks, update titles/descriptions, view changes, then delete tasks and verify removal

### Implementation for User Story 3

- [ ] T026 [US3] Implement update_task operation in src/services/task_service.py (uses input_parsing, task_validation, error_handling, task_formatting)
- [ ] T027 [US3] Implement delete_task operation in src/services/task_service.py (uses input_parsing, task_validation, error_handling, task_formatting)
- [ ] T028 [US3] Implement TaskList.get_by_id method in src/models/task.py
- [ ] T029 [US3] Implement TaskList.update method in src/models/task.py
- [ ] T030 [US3] Implement TaskList.delete method in src/models/task.py
- [ ] T031 [US3] Add "Update task" menu option in src/cli/main.py
- [ ] T032 [US3] Add "Delete task" menu option in src/cli/main.py
- [ ] T033 [US3] Wire update_task and delete_task operations to CLI menu in src/cli/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T034 [P] Add "Exit" menu option in src/cli/main.py with farewell message
- [ ] T035 [P] Implement main application loop in src/cli/main.py (while True with menu display and choice handling)
- [ ] T036 [P] Update main.py entry point to import and start CLI application from src/cli/main.py
- [ ] T037 [P] Update quickstart.md with actual file paths after implementation
- [ ] T038 [P] Add empty task list handling with clear message and create task option in src/services/task_service.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3, 4, 5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before CLI integration
- CLI integration in parallel after services ready
- Story complete before moving to next priority

### Parallel Opportunities

- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Tasks marked [P] within each user story can run in parallel

### Parallel Example: Phase 2 Foundational

```bash
# Launch all models together:
Task: "Create Task entity in src/models/task.py"
Task: "Create TaskList collection in src/models/task.py"

# Launch all skills together:
Task: "Create task_validation skill in src/skills/task_validation.py"
Task: "Create input_parsing skill in src/skills/input_parsing.py"
Task: "Create task_formatting skill in src/skills/task_formatting.py"
Task: "Create error_handling skill in src/skills/error_handling.py"
Task: "Create task_state_management skill in src/skills/task_state_management.py"
```

### Parallel Example: User Story 1 (Phase 3)

```bash
# Launch service operations together:
Task: "Implement create_task operation in src/services/task_service.py"
Task: "Implement view_tasks operation in src/services/task_service.py"

# Launch TaskList methods together:
Task: "Implement TaskList.add method in src/models/task.py"
Task: "Implement TaskList.list_all method in src/models/task.py"
Task: "Implement TaskList.count_by_status method in src/models/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently using quickstart.md scenarios
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- All operations MUST use reusable skills (task_validation, input_parsing, task_formatting, error_handling, task_state_management)
- No duplicate validation/parsing/formatting logic outside skills
- Verify manual testing with quickstart.md after implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
