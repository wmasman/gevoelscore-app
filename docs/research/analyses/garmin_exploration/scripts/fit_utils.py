"""Shared helpers for decoding monitoring_b FIT files in this research
project.

## The `timestamp_16` gotcha (read this before writing new FIT scripts)

In `monitoring` messages, most heart_rate / activity samples carry only
a 16-bit `timestamp_16` field instead of a full `timestamp`. To resolve
it to a real datetime, three things have to be correct simultaneously
or the result will be off by hours:

1. `timestamp_16` is the lower 16 bits of seconds-since-**FIT epoch**
   (1989-12-31 00:00 UTC = Unix epoch 631065600), NOT Unix epoch
   seconds. Using `datetime.timestamp() & 0xFFFF` directly is wrong
   and gives misaligned results (off by ~12h in the H02d calibration
   run that discovered this).
2. `fitdecode` does **not** auto-resolve `timestamp_16`. It exposes
   the raw 16-bit int. You have to maintain rolling reference state
   yourself.
3. The rolling reference must update on **every resolve**, not only
   on full `monitoring_info.timestamp` or `monitoring.timestamp`
   frames. Otherwise sequences crossing a 65536-second rollover get
   mis-decoded.

This module bakes those three rules in. New scripts: import
`Monitoring16Resolver` instead of re-implementing.

## Example

```python
from fit_utils import Monitoring16Resolver
import fitdecode

resolver = Monitoring16Resolver()
hr_samples: list[tuple[datetime, int]] = []
with fitdecode.FitReader(buf) as fit:
    for frame in fit:
        if not isinstance(frame, fitdecode.FitDataMessage):
            continue
        if frame.name == "monitoring_info":
            for f in frame.fields:
                if f.name == "timestamp" and isinstance(f.value, datetime):
                    resolver.set_reference(f.value)
        elif frame.name == "monitoring":
            ts = resolver.resolve_frame(frame)
            hr = next((f.value for f in frame.fields
                       if f.name == "heart_rate" and isinstance(f.value, int)),
                      None)
            if ts is not None and hr is not None:
                hr_samples.append((ts, hr))
```
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

# 1989-12-31 00:00:00 UTC in Unix seconds. The FIT format's reference
# epoch. `timestamp_16` fields are the lower 16 bits of (Unix seconds
# minus this offset).
FIT_EPOCH_OFFSET = 631065600


class Monitoring16Resolver:
    """Stateful resolver for `monitoring` frames carrying timestamp_16.

    Usage pattern:
      - call `set_reference(dt)` whenever you see a full timestamp
        (monitoring_info.timestamp, or a monitoring frame's own
        timestamp field) — this anchors the lower-16 rollover.
      - call `resolve_frame(frame)` for each `monitoring` frame; it
        will use the full `timestamp` if present, otherwise expand
        `timestamp_16` against the running reference, and return
        the resolved datetime (or None if no anchor has been set yet).

    The resolver updates its internal reference on every successful
    resolution so cross-rollover sequences stay aligned.
    """

    def __init__(self) -> None:
        self._reference: datetime | None = None

    def set_reference(self, dt: datetime) -> None:
        self._reference = dt

    def reference(self) -> datetime | None:
        return self._reference

    def _expand_ts16(self, t16: int) -> datetime | None:
        if self._reference is None:
            return None
        base_fit = int(self._reference.timestamp()) - FIT_EPOCH_OFFSET
        base_lower = base_fit & 0xFFFF
        if t16 >= base_lower:
            delta = t16 - base_lower
        else:
            delta = (t16 + 0x10000) - base_lower
        resolved = self._reference + timedelta(seconds=delta)
        self._reference = resolved
        return resolved

    def resolve_frame(self, frame: Any) -> datetime | None:
        """Resolve the timestamp of a `monitoring` frame.

        Prefers a full `timestamp` field if present (also updates the
        rolling reference). Falls back to `timestamp_16` expansion.
        Returns None if the frame has neither and no prior anchor.
        """
        full_ts: datetime | None = None
        t16: int | None = None
        for f in frame.fields:
            if f.name == "timestamp" and isinstance(f.value, datetime):
                full_ts = f.value
            elif f.name == "timestamp_16" and isinstance(f.value, int):
                t16 = f.value
        if full_ts is not None:
            self._reference = full_ts
            return full_ts
        if t16 is not None:
            return self._expand_ts16(t16)
        return None
