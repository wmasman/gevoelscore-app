import { writeFile, mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
// @ts-expect-error — .mjs lib without type declarations is intentional.
import {
  MISSING_URL_MESSAGE,
  queryPg,
  runSqlFile,
} from '../lib/sql-migration.mjs';

type QueryRows = Array<Record<string, unknown>>;

function makeFakeClient(opts: {
  queryImpl?: (sql: string) => Promise<{ rows: QueryRows }> | { rows: QueryRows };
} = {}) {
  const calls: { connect: number; query: string[]; end: number } = {
    connect: 0,
    query: [],
    end: 0,
  };
  class FakeClient {
    constructor(public config: { connectionString: string }) {}
    async connect() {
      calls.connect += 1;
    }
    async query(sql: string) {
      calls.query.push(sql);
      if (opts.queryImpl) return await opts.queryImpl(sql);
      return { rows: [] };
    }
    async end() {
      calls.end += 1;
    }
  }
  return { FakeClient, calls };
}

let tmpDir: string;

beforeEach(async () => {
  tmpDir = await mkdtemp(join(tmpdir(), 'gv-sql-mig-'));
});

afterEach(async () => {
  await rm(tmpDir, { recursive: true, force: true });
  delete process.env.DATABASE_URL;
});

describe('sql-migration', () => {
  describe('runSqlFile', () => {
    it('given a valid SQL file and an injected Client, when run, then connects, runs the file content as one query, and closes', async () => {
      const sqlPath = join(tmpDir, 'mig.sql');
      await writeFile(sqlPath, 'CREATE UNIQUE INDEX IF NOT EXISTS foo ON bar (a, b);');
      const { FakeClient, calls } = makeFakeClient();

      await runSqlFile(sqlPath, {
        Client: FakeClient,
        databaseUrl: 'postgres://fake/test',
      });

      expect(calls.connect).toBe(1);
      expect(calls.query).toEqual([
        'CREATE UNIQUE INDEX IF NOT EXISTS foo ON bar (a, b);',
      ]);
      expect(calls.end).toBe(1);
    });

    it('given a SQL file whose query throws, when run, then wraps the error with the file path and re-throws and STILL calls end()', async () => {
      const sqlPath = join(tmpDir, 'broken.sql');
      await writeFile(sqlPath, 'NOT VALID SQL;');
      const { FakeClient, calls } = makeFakeClient({
        queryImpl: () => Promise.reject(new Error('syntax error at or near "NOT"')),
      });

      const promise = runSqlFile(sqlPath, {
        Client: FakeClient,
        databaseUrl: 'postgres://fake/test',
      });

      await expect(promise).rejects.toThrow(/broken\.sql/);
      await expect(promise).rejects.toThrow(/syntax error at or near "NOT"/);
      expect(calls.end).toBe(1);
    });

    it('given no DATABASE_URL and no databaseUrl opt, when run, then throws the actionable "get it from fly secrets" message before any client construction', async () => {
      const sqlPath = join(tmpDir, 'unused.sql');
      await writeFile(sqlPath, 'SELECT 1;');
      const constructed = vi.fn();
      class FakeClient {
        constructor() {
          constructed();
        }
        async connect() {}
        async query() {
          return { rows: [] };
        }
        async end() {}
      }

      await expect(
        runSqlFile(sqlPath, { Client: FakeClient }),
      ).rejects.toThrow(MISSING_URL_MESSAGE);
      expect(constructed).not.toHaveBeenCalled();
    });
  });

  describe('queryPg', () => {
    it('given a SELECT query and an injected Client, when run, then returns the result rows verbatim', async () => {
      const fakeRows: QueryRows = [{ indexname: 'foo_unique', is_unique: true }];
      const { FakeClient } = makeFakeClient({
        queryImpl: () => ({ rows: fakeRows }),
      });

      const rows = await queryPg('SELECT indexname FROM pg_indexes WHERE 1=1;', {
        Client: FakeClient,
        databaseUrl: 'postgres://fake/test',
      });

      expect(rows).toEqual(fakeRows);
    });
  });
});
