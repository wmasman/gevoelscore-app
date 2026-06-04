// Renders a Dutch relative time like "2 uur geleden", "5 min geleden",
// "gisteren", "3 dagen geleden". Pure function — caller supplies `now`
// (no Date.now() call inside) so tests stay deterministic.
//
// Brainfog-friendly: rounded, single-unit. No "2 uur 14 min geleden"
// precision.

export function relativeDutchTime(target: Date, now: Date): string {
  const diffMs = now.getTime() - target.getTime();
  if (diffMs < 0) {
    // Future timestamps shouldn't happen for last_synced_at but
    // be defensive.
    return 'zojuist';
  }
  const seconds = Math.floor(diffMs / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (seconds < 60) return 'zojuist';
  if (minutes < 60) return `${minutes} min geleden`;
  if (hours < 24) return hours === 1 ? '1 uur geleden' : `${hours} uur geleden`;
  if (days === 1) return 'gisteren';
  if (days < 7) return `${days} dagen geleden`;
  if (days < 14) return '1 week geleden';
  if (days < 30) {
    const weeks = Math.floor(days / 7);
    return `${weeks} weken geleden`;
  }
  const months = Math.floor(days / 30);
  if (months < 12) return months === 1 ? '1 maand geleden' : `${months} maanden geleden`;
  const years = Math.floor(days / 365);
  return years === 1 ? '1 jaar geleden' : `${years} jaar geleden`;
}
