import { describe, expect, it } from 'vitest';
import { createPendingTfaStore } from '../pending-tfa';

describe('pending-tfa', () => {
  describe('createPendingTfaStore', () => {
    it('stores and retrieves a pending entry by session id', () => {
      const store = createPendingTfaStore();
      store.create('s-1', { secret: 'JBSWY', expiresAt: Date.now() + 60_000 });
      const got = store.get('s-1');
      expect(got?.secret).toBe('JBSWY');
    });

    it('returns undefined for an unknown session id', () => {
      const store = createPendingTfaStore();
      expect(store.get('nope')).toBeUndefined();
    });

    it('expires entries past expiresAt and removes them on read', () => {
      const now = 1_000_000;
      let clock = now;
      const store = createPendingTfaStore({ now: () => clock });
      store.create('s-1', { secret: 'JBSWY', expiresAt: now + 1_000 });
      clock = now + 2_000;
      expect(store.get('s-1')).toBeUndefined();
      expect(store.size()).toBe(0);
    });

    it('delete removes the entry', () => {
      const store = createPendingTfaStore();
      store.create('s-1', { secret: 'JBSWY', expiresAt: Date.now() + 60_000 });
      store.delete('s-1');
      expect(store.get('s-1')).toBeUndefined();
    });

    it('cleanupExpired drops all past-TTL entries', () => {
      const now = 1_000_000;
      let clock = now;
      const store = createPendingTfaStore({ now: () => clock });
      store.create('s-1', { secret: 'A', expiresAt: now + 500 });
      store.create('s-2', { secret: 'B', expiresAt: now + 5_000 });
      clock = now + 1_000;
      store.cleanupExpired();
      expect(store.size()).toBe(1);
      expect(store.get('s-2')?.secret).toBe('B');
    });

    it('overwrites a prior entry for the same session id', () => {
      const store = createPendingTfaStore();
      store.create('s-1', { secret: 'OLD', expiresAt: Date.now() + 60_000 });
      store.create('s-1', { secret: 'NEW', expiresAt: Date.now() + 60_000 });
      expect(store.get('s-1')?.secret).toBe('NEW');
      expect(store.size()).toBe(1);
    });
  });
});
