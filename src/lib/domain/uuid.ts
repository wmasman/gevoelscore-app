// UUID-shape utility for boundary-layer id validation. Liberal on the
// case + version byte — the goal is "is this a UUID-looking thing?",
// not strict RFC 4122 v4 conformance. The Directus DB enforces the real
// constraint; this gate keeps non-UUID input out of the SDK + the wire.

export const UUID_REGEX =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export function isUuidShape(value: unknown): value is string {
  return typeof value === 'string' && UUID_REGEX.test(value);
}
