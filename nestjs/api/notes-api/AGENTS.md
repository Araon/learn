# AGENTS.md for notes-api

## Project summary
- NestJS API for notes (CRUD, minimal template).
- Core folders: `src/notes`, `src/common`, `test`.
- Uses TypeORM + PostgreSQL config likely via `.env` in real environments; however this learning project has no DB config in repo.

## Primary goals for AI assistance
- Implement endpoints in `src/notes/` following NestJS convention.
- Add DTOs/validation and service logic.
- Write/maintain unit tests under `src/**/*.spec.ts` and e2e tests under `test/`.
- Update docs/README as needed.

## Setup and useful commands
- `pnpm install` (or `npm install` if not using pnpm)
- `pnpm start:dev` run local server with hot reload
- `pnpm build` compile TypeScript
- `pnpm lint` run ESLint + auto-fix
- `pnpm format` run Prettier

## Test commands
- `pnpm test` run unit tests
- `pnpm test:e2e` run integration tests
- `pnpm test:cov` coverage
- `pnpm test:watch` watch mode

## Conventions
- TypeScript, NestJS decorators (`@Controller`, `@Get`, `@Post`, etc.)
- Use validation pipes and class-validator on DTOs
- Keep controllers thin: delegate to service methods
- Keep business logic in services with pure functions where possible

## Branch/commit style
- Keep changes small and focused; one feature/bug per commit
- Include tests for behavior updates

## Known considerations
- No environment config file committed; for DB tests use in-memory or mocked patterns.
- If adding `.env`, document it in README.

## Helpful user prompts (examples)
- "Add a `GET /notes` endpoint that returns all notes and include unit tests in `notes.controller.spec.ts`."
- "Implement `UpdateNoteDto`, validate `title` as non-empty string, and wire it into `notes.controller.ts` with PATCH route."
- "Write an e2e test for creating a note then fetching it by id using `supertest` and `test/jest-e2e.json`."

## Next agent-customization suggestions
- Create an `agent` for backend API feature work: `create-agent notes-api-backend`.
- Create a `hook` for custom lint/test precommit actions: `create-hook notes-api-precommit`.
- Add `applyTo` scoped rules for `src/notes/**` and `test/**` when project expands.
