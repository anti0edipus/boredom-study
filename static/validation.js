/**
 * Form validation: highlights unanswered required fields instead of
 * relying on the browser's native per-field tooltip.
 *
 * Any form with the attribute data-validate is auto-discovered on
 * DOMContentLoaded — no inline script calls needed.
 */

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('form[data-validate]').forEach(function (form) {
    form.setAttribute('novalidate', '');
    form.addEventListener('submit', function (e) {
      clearHighlights(form);

      const unanswered = findUnanswered(form);

      if (unanswered.length === 0) return; // all good — let submit proceed

      // TESTING MODE: highlight but do not block submission
      unanswered.forEach(el => el.classList.add('unanswered'));
      showBanner(form, unanswered.length);
    });
  });
});

function clearHighlights(form) {
  form.querySelectorAll('.unanswered').forEach(el => el.classList.remove('unanswered'));
  const banner = form.querySelector('.validation-banner');
  if (banner) banner.remove();
}

function findUnanswered(form) {
  const unanswered = [];

  // ── Radio groups ──────────────────────────────────────────────────────────
  const radioNames = new Set();
  form.querySelectorAll('input[type="radio"][required]')
      .forEach(r => radioNames.add(r.name));

  radioNames.forEach(name => {
    const radios = Array.from(form.querySelectorAll(`input[type="radio"][name="${name}"]`));
    if (!radios.some(r => r.checked)) {
      const container = radios[0].closest('.item-row, .form-group, .ladder-group');
      if (container && !unanswered.includes(container)) {
        unanswered.push(container);
      }
    }
  });

  // ── Text inputs, number inputs, textareas ─────────────────────────────────
  form.querySelectorAll('input[required]:not([type="radio"]), textarea[required]')
      .forEach(el => {
        if (!el.value.trim()) {
          const container = el.closest('.form-group') || el.parentElement;
          if (!unanswered.includes(container)) unanswered.push(container);
        }
      });

  // ── Selects ───────────────────────────────────────────────────────────────
  form.querySelectorAll('select[required]').forEach(el => {
    if (!el.value) {
      const container = el.closest('.form-group') || el.parentElement;
      if (!unanswered.includes(container)) unanswered.push(container);
    }
  });

  // Sort by document order so scrolling goes top-to-bottom
  unanswered.sort((a, b) =>
    a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1
  );

  return unanswered;
}

function showBanner(form, count) {
  const banner = document.createElement('div');
  banner.className = 'validation-banner';
  banner.textContent = count === 1
    ? 'Please answer the highlighted question before continuing.'
    : `Please answer the ${count} highlighted questions before continuing.`;
  form.prepend(banner);
  banner.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
