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

  // Programa: detalle de talleres, mesas, libros y pósteres en ventana emergente
  var dialog = document.getElementById('prog-dialog');
  if (dialog && dialog.showModal) {
    var dlgTitle  = dialog.querySelector('.prog-dialog-title');
    var dlgPeople = dialog.querySelector('.prog-dialog-people');
    var dlgFacts  = dialog.querySelector('.prog-dialog-facts');
    var dlgBody   = dialog.querySelector('.prog-dialog-body');

    document.querySelectorAll('.prog-more').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var item = btn.closest('li');
        var isTaller = item.classList.contains('taller');
        dlgTitle.textContent = item.querySelector('h5').textContent;
        dlgFacts.innerHTML = '';
        dlgBody.innerHTML  = '';

        if (isTaller) {
          dlgPeople.innerHTML = item.querySelector('.taller-people').innerHTML;
          item.querySelectorAll('.taller-fact').forEach(function (f) {
            dlgFacts.appendChild(f.cloneNode(true));
          });
          dlgBody.textContent = item.querySelector('.taller-desc').textContent;
        } else {
          dlgPeople.textContent = item.querySelector('.prog-sub-meta span').textContent;
          dlgBody.innerHTML = item.querySelector('.prog-sub-detail').innerHTML;
        }

        dialog.classList.toggle('is-wide', !isTaller);
        dialog.showModal();
      });
    });

    dialog.querySelector('.prog-dialog-close').addEventListener('click', function () {
      dialog.close();
    });
    // Cerrar al hacer clic fuera del contenido
    dialog.addEventListener('click', function (e) {
      if (e.target !== dialog) return;
      var r = dialog.getBoundingClientRect();
      var inside = e.clientX >= r.left && e.clientX <= r.right &&
                   e.clientY >= r.top && e.clientY <= r.bottom;
      if (!inside) dialog.close();
    });
  } else {
    // Sin soporte de <dialog>: mostrar el detalle en línea
    document.querySelectorAll('.taller-desc, .prog-sub-detail').forEach(function (d) { d.hidden = false; });
    document.querySelectorAll('.prog-more').forEach(function (b) { b.hidden = true; });
  }

  // Restore tab from URL hash on load (also for anchors inside a tab)
  var hash = window.location.hash.replace('#', '');
  var target = hash && document.getElementById(hash);
  var panel = target && target.closest('.tab-panel');
  if (panel) {
    activateTab(panel.id);
    if (panel !== target) target.scrollIntoView();
  }
})();
