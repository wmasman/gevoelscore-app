'use client';

// EpisodeFormSheet — single composite for both create + edit of an Episode.
// Lives behind the BottomSheet primitive so it shares the thumb-first
// drag-to-dismiss / Escape / focus-trap / iOS-keyboard-anchor behaviour
// with the QuickEntryFlow daily popout.
//
// Explicit-save semantics: typing stays in local state; only the Bewaar
// button commits. Dismiss (✕ / Escape / drag-down) discards the unsaved
// changes silently — no confirmation dialog (per the brief's "no friction"
// rule and the locked Q3 audit decision in step-4 plan).
//
// Validation mirrors the server: validateEpisodeLabel (1-40 chars after
// trim+normalise), validateDateRange (end_date null OR >= start_date),
// validateEpisodeDescription (≤ 10,000 chars). Client-side gates surface
// inline errors as the user types; submit attempt on an invalid form
// forces all errors visible. The server is the final word — if a server
// error comes back it surfaces in the top-of-form banner.
//
// Archive button only renders in edit mode. One-tap action (the data
// layer is reversible; surfaced + un-archived in v1.5b).

import { useEffect, useRef, useState } from 'react';
import { BottomSheet } from '@/components/lab/bottom-sheet';
import { copy } from '@/copy';
import { useEpisodeUpsert } from '@/hooks/use-episode-upsert';
import type { Episode } from '@/lib/domain/episode';
import type { EpisodeCategory } from '@/lib/domain/episode-category';
import { MAX_EPISODE_DESCRIPTION_LENGTH } from '@/lib/domain/episode-description';
import { MAX_EPISODE_LABEL_LENGTH } from '@/lib/domain/episode-label';
import { cn } from '@/lib/ui/cn';

type Mode = 'create' | 'edit';

type LabelErrorKey = 'labelEmpty' | 'labelTooLong';
type DateErrorKey = 'startDateInvalid' | 'endDateInvalid' | 'endBeforeStart';
type DescriptionErrorKey = 'descriptionTooLong';

type Props = {
  mode: Mode;
  category: EpisodeCategory;
  /** Pre-fill source for edit mode. Must be the same episode whose id we PATCH. */
  initialEpisode: Episode | null;
  /** Default start_date in create mode (page-level today, ISO YYYY-MM-DD). */
  today: string;
  open: boolean;
  onClose: () => void;
  onSaved: (ep: Episode) => void;
  onArchived: (ep: Episode) => void;
};

const ISO_DATE_REGEX = /^\d{4}-\d{2}-\d{2}$/;

export function EpisodeFormSheet({
  mode,
  category,
  initialEpisode,
  today,
  open,
  onClose,
  onSaved,
  onArchived,
}: Props) {
  // Form state — local only; commits to the server on Bewaar.
  const [label, setLabel] = useState<string>('');
  const [startDate, setStartDate] = useState<string>('');
  const [lopend, setLopend] = useState<boolean>(true);
  const [endDate, setEndDate] = useState<string>('');
  const [description, setDescription] = useState<string>('');

  // Error-visibility gates: error messages stay hidden on first render
  // (no aggressive validation on mount); they flip visible on the first
  // interaction OR on submit attempt.
  const [showLabelError, setShowLabelError] = useState<boolean>(false);
  const [showDateError, setShowDateError] = useState<boolean>(false);
  const [showDescriptionError, setShowDescriptionError] = useState<boolean>(false);

  const { create, update, archive, status, lastError } = useEpisodeUpsert();

  // Closed → open edge: re-sync state from props. The sheet is mounted
  // for the lifetime of the parent; without this guard the user would
  // see stale form values after opening the sheet for a different
  // episode (same pattern as QuickEntryFlow). prevOpenRef starts at
  // `false` so a component that mounts with open=true ALSO triggers
  // the initial sync — useState's empty defaults above are placeholders
  // until this effect fires.
  const prevOpenRef = useRef<boolean>(false);
  useEffect(() => {
    if (open && !prevOpenRef.current) {
      const initLabel = initialEpisode?.label ?? '';
      const initStart = initialEpisode?.start_date ?? today;
      const initEnd = initialEpisode?.end_date ?? '';
      setLabel(initLabel);
      setStartDate(initStart);
      // create mode defaults to "lopend ON". edit mode mirrors the
      // initialEpisode's end_date — null → ON, set → OFF.
      setLopend(mode === 'create' ? true : initialEpisode?.end_date === null);
      setEndDate(initEnd);
      setDescription(initialEpisode?.description ?? '');
      setShowLabelError(false);
      setShowDateError(false);
      setShowDescriptionError(false);
    }
    prevOpenRef.current = open;
  }, [open, initialEpisode, mode, today]);

  // Derived: normalisation + per-field error state.
  const normalisedLabel = label.trim().replace(/\s+/g, ' ');
  const labelError: LabelErrorKey | null =
    normalisedLabel.length === 0
      ? 'labelEmpty'
      : normalisedLabel.length > MAX_EPISODE_LABEL_LENGTH
        ? 'labelTooLong'
        : null;

  const startDateError: DateErrorKey | null = ISO_DATE_REGEX.test(startDate)
    ? null
    : 'startDateInvalid';
  const endDateError: DateErrorKey | null = lopend
    ? null
    : !ISO_DATE_REGEX.test(endDate)
      ? 'endDateInvalid'
      : endDate < startDate
        ? 'endBeforeStart'
        : null;

  const descriptionError: DescriptionErrorKey | null =
    description.length > MAX_EPISODE_DESCRIPTION_LENGTH ? 'descriptionTooLong' : null;

  const canSubmit =
    !labelError && !startDateError && !endDateError && !descriptionError;

  const title =
    mode === 'create'
      ? category === 'interventie'
        ? copy.context.form.titleNewInterventie
        : copy.context.form.titleNewPeriode
      : category === 'interventie'
        ? copy.context.form.titleEditInterventie
        : copy.context.form.titleEditPeriode;

  async function handleSubmit(e: React.FormEvent): Promise<void> {
    e.preventDefault();
    if (!canSubmit) {
      // Submit-attempt forces ALL errors visible — the user gets the full
      // picture of what's blocking the save, not just the first field.
      setShowLabelError(true);
      setShowDateError(true);
      setShowDescriptionError(true);
      return;
    }
    const payload = {
      label: normalisedLabel,
      category,
      start_date: startDate,
      end_date: lopend ? null : endDate,
      // Description: empty string → null at the wire. Multi-line
      // whitespace is preserved (validateEpisodeDescription doesn't
      // trim) for non-empty values.
      description: description.length === 0 ? null : description,
    };
    let ep: Episode | null;
    if (mode === 'create') {
      ep = await create(payload);
    } else if (initialEpisode) {
      ep = await update(initialEpisode.id, payload);
    } else {
      ep = null;
    }
    if (ep) onSaved(ep);
  }

  async function handleArchive(): Promise<void> {
    if (!initialEpisode) return;
    const ep = await archive(initialEpisode.id);
    if (ep) onArchived(ep);
  }

  const labelInputId = 'ep-form-label';
  const startInputId = 'ep-form-start';
  const endInputId = 'ep-form-end';
  const descInputId = 'ep-form-description';

  return (
    <BottomSheet
      open={open}
      onClose={onClose}
      ariaLabel={copy.context.form.sheetAriaLabel}
    >
      <form
        onSubmit={handleSubmit}
        // noValidate disables the browser's native required/pattern
        // validation so our custom Dutch error messages own the surface.
        // aria-required + aria-invalid on the inputs preserve the
        // screen-reader contract.
        noValidate
        className="flex flex-col gap-4 overflow-y-auto px-6 pb-4"
      >
        <header className="flex items-baseline justify-between pt-1">
          <h2 className="text-lg font-semibold text-fg">{title}</h2>
          <button
            type="button"
            onClick={onClose}
            aria-label={copy.context.form.close}
            className="inline-flex min-h-11 min-w-11 items-center justify-center rounded-md text-fg-muted hover:bg-surface-muted focus-visible:outline-2 focus-visible:outline-accent"
          >
            ✕
          </button>
        </header>

        {/* Server-error banner — only renders when the last API call set lastError. */}
        {lastError !== null && (
          <div
            role="alert"
            className="rounded-md border border-error bg-error-soft px-3 py-2 text-sm text-error"
          >
            {copy.context.form.error.serverError}
          </div>
        )}

        {/* Label */}
        <div className="flex flex-col gap-1">
          <label htmlFor={labelInputId} className="text-sm font-medium text-fg">
            {copy.context.form.labelField}
            <span className="ml-1 text-xs font-normal text-fg-muted">
              ({copy.context.form.requiredMarker})
            </span>
          </label>
          <input
            id={labelInputId}
            type="text"
            value={label}
            onChange={(e) => {
              setLabel(e.target.value);
              setShowLabelError(true);
            }}
            onBlur={() => setShowLabelError(true)}
            required
            aria-required="true"
            aria-invalid={showLabelError && labelError ? 'true' : 'false'}
            // No `autoFocus` prop: jsx-a11y forbids it (forced focus
            // shifts can disorient screen-reader users). The BottomSheet
            // primitive's useFocusTrap focuses the close ✕ on open; one
            // tab/swipe reaches the label input. Acceptable tradeoff in
            // exchange for the a11y guarantee.
            maxLength={MAX_EPISODE_LABEL_LENGTH}
            className="rounded-md border border-border bg-surface px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-accent"
          />
          {showLabelError && labelError !== null && (
            <p role="alert" className="text-sm text-error">
              {labelError === 'labelEmpty'
                ? copy.context.form.error.labelEmpty
                : copy.context.form.error.labelTooLong}
            </p>
          )}
          {normalisedLabel.length >= 30 && (
            <p className="text-xs text-fg-subtle">
              {copy.context.form.labelCountSuffix(normalisedLabel.length)}
            </p>
          )}
        </div>

        {/* Start date */}
        <div className="flex flex-col gap-1">
          <label htmlFor={startInputId} className="text-sm font-medium text-fg">
            {copy.context.form.startDateField}
            <span className="ml-1 text-xs font-normal text-fg-muted">
              ({copy.context.form.requiredMarker})
            </span>
          </label>
          <input
            id={startInputId}
            type="date"
            value={startDate}
            onChange={(e) => {
              setStartDate(e.target.value);
              setShowDateError(true);
            }}
            required
            aria-required="true"
            aria-invalid={showDateError && startDateError ? 'true' : 'false'}
            className="rounded-md border border-border bg-surface px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-accent"
          />
          {showDateError && startDateError !== null && (
            <p role="alert" className="text-sm text-error">
              {copy.context.form.error.startDateInvalid}
            </p>
          )}
        </div>

        {/* Lopend toggle */}
        <label className="flex items-center gap-3 text-base">
          <input
            type="checkbox"
            checked={lopend}
            onChange={(e) => {
              const next = e.target.checked;
              setLopend(next);
              setShowDateError(true);
              if (next) setEndDate('');
            }}
            className="h-5 w-5"
          />
          <span>{copy.context.form.ongoingToggle}</span>
        </label>

        {/* End date (conditional on lopend OFF) */}
        {!lopend && (
          <div className="flex flex-col gap-1">
            <label htmlFor={endInputId} className="text-sm font-medium text-fg">
              {copy.context.form.endDateField}
            </label>
            <input
              id={endInputId}
              type="date"
              value={endDate}
              onChange={(e) => {
                setEndDate(e.target.value);
                setShowDateError(true);
              }}
              aria-invalid={showDateError && endDateError ? 'true' : 'false'}
              className="rounded-md border border-border bg-surface px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-accent"
            />
            {showDateError && endDateError !== null && (
              <p role="alert" className="text-sm text-error">
                {endDateError === 'endDateInvalid'
                  ? copy.context.form.error.endDateInvalid
                  : copy.context.form.error.endBeforeStart}
              </p>
            )}
          </div>
        )}

        {/* Description */}
        <div className="flex flex-col gap-1">
          <label htmlFor={descInputId} className="text-sm font-medium text-fg">
            {copy.context.form.descriptionField}
          </label>
          <textarea
            id={descInputId}
            value={description}
            onChange={(e) => {
              setDescription(e.target.value);
              if (e.target.value.length > MAX_EPISODE_DESCRIPTION_LENGTH) {
                setShowDescriptionError(true);
              }
            }}
            rows={3}
            placeholder={copy.context.form.descriptionPlaceholder}
            maxLength={MAX_EPISODE_DESCRIPTION_LENGTH}
            aria-invalid={
              showDescriptionError && descriptionError ? 'true' : 'false'
            }
            className="rounded-md border border-border bg-surface px-3 py-2 text-base focus-visible:outline-2 focus-visible:outline-accent"
          />
          {showDescriptionError && descriptionError !== null && (
            <p role="alert" className="text-sm text-error">
              {copy.context.form.error.descriptionTooLong}
            </p>
          )}
          {description.length >= 9000 && (
            <p className="text-xs text-fg-subtle">
              {copy.context.form.descriptionCountSuffix(description.length)}
            </p>
          )}
        </div>

        {/* Action row */}
        <div className="flex items-center justify-between gap-3 pt-2">
          {/* Archive (edit mode only) — one-tap, no confirm. Action is
              reversible at the data layer; v1.5b tag-management-settings
              surfaces archived episodes for un-archive. */}
          {mode === 'edit' && initialEpisode !== null ? (
            <button
              type="button"
              onClick={() => void handleArchive()}
              disabled={status === 'saving'}
              aria-busy={status === 'saving' ? 'true' : 'false'}
              className="inline-flex min-h-11 items-center rounded-md px-3 py-2 text-sm text-error hover:bg-error-soft focus-visible:outline-2 focus-visible:outline-accent"
            >
              {copy.context.archive.button}
            </button>
          ) : (
            <span />
          )}
          <button
            type="submit"
            disabled={status === 'saving'}
            aria-busy={status === 'saving' ? 'true' : 'false'}
            className={cn(
              'inline-flex min-h-11 items-center rounded-md px-4 py-2 text-base font-medium focus-visible:outline-2 focus-visible:outline-accent',
              status === 'saving'
                ? 'cursor-not-allowed bg-surface-muted text-fg-muted'
                : 'bg-accent-hover text-bg',
            )}
          >
            {status === 'saving'
              ? copy.context.form.saving
              : copy.context.form.save}
          </button>
        </div>
      </form>
    </BottomSheet>
  );
}
