/**
 * Boring task: Continuous Performance Task (letter stream).
 * Target appears ~15% of the time; participant presses SPACEBAR for target only.
 * Tracks hits, misses, false alarms, mean RT.
 */
const BoringTask = (() => {
  const LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWYZ'.split(''); // X removed; added back as target
  const TARGET_PROB  = 0.15;
  const DISPLAY_MS   = 500;
  const MIN_ISI_MS   = 1500;
  const MAX_ISI_MS   = 2500;
  const HIT_WINDOW   = 1000; // ms after letter onset to count as hit

  let cfg, taskRunning, taskStarted;
  let hits = 0, misses = 0, falseAlarms = 0;
  let rts = [];
  let currentLetter = null;
  let letterOnset = null;
  let letterTimeout = null;
  let taskEndTimeout = null;
  let totalDuration = 0;

  function randInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  function showLetter() {
    if (!taskRunning) return;

    const isTarget = Math.random() < TARGET_PROB;
    const letter   = isTarget
      ? cfg.target
      : LETTERS[Math.floor(Math.random() * LETTERS.length)];

    currentLetter = letter;
    letterOnset   = Date.now();

    const el = document.getElementById('letter-display');
    el.textContent  = letter;
    el.className    = 'letter-display' + (isTarget ? ' target' : '');

    // Hide letter after DISPLAY_MS
    setTimeout(() => {
      if (el.textContent === letter) el.textContent = '';
    }, DISPLAY_MS);

    // Miss detection: if no spacebar within HIT_WINDOW after target onset
    if (isTarget) {
      letterTimeout = setTimeout(() => {
        if (currentLetter === letter) {
          misses++;
          currentLetter = null;
        }
      }, HIT_WINDOW);
    }

    // Schedule next letter
    const isi = randInt(MIN_ISI_MS, MAX_ISI_MS);
    setTimeout(showLetter, DISPLAY_MS + isi);
  }

  function handleKeydown(e) {
    if (e.code !== 'Space') return;
    e.preventDefault();

    if (!taskStarted) {
      startTask();
      return;
    }

    if (!taskRunning) return;

    const now = Date.now();

    if (currentLetter === cfg.target && (now - letterOnset) <= HIT_WINDOW) {
      hits++;
      rts.push(now - letterOnset);
      clearTimeout(letterTimeout);
      currentLetter = null;
    } else if (currentLetter !== cfg.target) {
      falseAlarms++;
    }
    // Spacebar after hit window on target: already counted as miss via timeout
  }

  function updateTimer() {
    if (!taskRunning) return;
    const elapsed   = (Date.now() - window._taskStartTime) / 1000;
    const remaining = Math.max(0, cfg.duration - elapsed);
    const m = Math.floor(remaining / 60);
    const s = Math.floor(remaining % 60);
    document.getElementById('task-timer').textContent =
      m + ':' + String(s).padStart(2, '0');
    if (remaining > 0) {
      requestAnimationFrame(updateTimer);
    }
  }

  function startTask() {
    taskStarted = true;
    taskRunning = true;
    window._taskStartTime = Date.now();

    document.getElementById('task-instructions').style.display = 'none';
    document.getElementById('task-area').style.display = 'block';

    requestAnimationFrame(updateTimer);
    showLetter();

    taskEndTimeout = setTimeout(endTask, cfg.duration * 1000);
  }

  function endTask() {
    taskRunning = false;
    totalDuration = (Date.now() - window._taskStartTime) / 1000;
    document.removeEventListener('keydown', handleKeydown);

    const rtMean = rts.length > 0
      ? (rts.reduce((a, b) => a + b, 0) / rts.length).toFixed(1)
      : 0;

    document.getElementById('f_duration').value     = totalDuration.toFixed(1);
    document.getElementById('f_hits').value          = hits;
    document.getElementById('f_misses').value        = misses;
    document.getElementById('f_false_alarms').value  = falseAlarms;
    document.getElementById('f_rt_mean').value       = rtMean;

    document.getElementById('task-area').style.display = 'none';
    document.getElementById('task-done').style.display  = 'block';
  }

  function init(options) {
    cfg        = options;
    taskRunning = false;
    taskStarted = false;
    document.addEventListener('keydown', handleKeydown);
  }

  return { init };
})();
