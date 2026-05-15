/**
 * Tab navigation – VII Congreso Patagónico EF Bariloche 2026
 */
(function () {
  'use strict';

  const tabs   = document.querySelectorAll('.tab-btn');
  const panels = document.querySelectorAll('.tab-panel');

  function activateTab(tabId) {
    tabs.forEach(function (btn) {
      var active = btn.dataset.tab === tabId;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-selected', active ? 'true' : 'false');
    });

    panels.forEach(function (panel) {
      panel.classList.toggle('active', panel.id === tabId);
    });
  }

  tabs.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var tabId = btn.dataset.tab;
      activateTab(tabId);
      // Keep URL in sync without forcing a scroll jump
      history.replaceState(null, '', '#' + tabId);
    });
  });

  // Restore tab from URL hash on load
  var hash = window.location.hash.replace('#', '');
  if (hash && document.getElementById(hash)) {
    activateTab(hash);
  }
})();
