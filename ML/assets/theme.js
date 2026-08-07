/* ============================================================
   Manuel Informatique MPSI/PCSI — bascule clair / sombre
   ------------------------------------------------------------
   Ce fichier est charge de facon SYNCHRONE dans le <head> :
   l'attribut data-theme est pose avant le premier rendu, ce qui
   evite tout clignotement blanc au chargement d'une page sombre.

   Ordre de priorite du theme :
     1. le choix explicite de l'utilisateur (localStorage) ;
     2. sinon, la preference du systeme (prefers-color-scheme) ;
     3. sinon, le theme clair.
   ============================================================ */
(function () {
  "use strict";

  var CLE = "mpsi-theme";
  var racine = document.documentElement;

  function stockage(action, valeur) {
    // le protocole file:// peut refuser localStorage selon le navigateur
    try {
      if (action === "lire") return window.localStorage.getItem(CLE);
      if (action === "ecrire") window.localStorage.setItem(CLE, valeur);
    } catch (e) {
      return null;
    }
    return null;
  }

  function systemeSombre() {
    return window.matchMedia &&
           window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function themeCourant() {
    return racine.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }

  function appliquer(theme) {
    if (theme === "dark") racine.setAttribute("data-theme", "dark");
    else racine.removeAttribute("data-theme");
    majBouton(theme);
  }

  // --- 1. application immediate, avant le rendu ---------------------
  var choix = stockage("lire");
  appliquer(choix === "dark" || choix === "light"
            ? choix
            : (systemeSombre() ? "dark" : "light"));

  // --- 2. construction du bouton -----------------------------------
  var SOLEIL =
    '<svg class="ico ico-soleil" viewBox="0 0 24 24" fill="none" ' +
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" ' +
    'aria-hidden="true"><circle cx="12" cy="12" r="4.2"/>' +
    '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4' +
    'M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';

  var LUNE =
    '<svg class="ico ico-lune" viewBox="0 0 24 24" fill="currentColor" ' +
    'aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 ' +
    '9.8z"/></svg>';

  var bouton = null;

  function majBouton(theme) {
    if (!bouton) return;
    var sombre = theme === "dark";
    bouton.setAttribute("aria-pressed", sombre ? "true" : "false");
    bouton.setAttribute(
      "title",
      sombre ? "Passer au theme clair" : "Passer au theme sombre"
    );
    var lbl = bouton.querySelector(".lbl");
    if (lbl) lbl.textContent = sombre ? "Clair" : "Sombre";
  }

  function creerBouton() {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "theme-toggle";
    b.setAttribute("aria-label", "Basculer entre theme clair et theme sombre");
    b.innerHTML = SOLEIL + LUNE + '<span class="lbl"></span>';
    b.addEventListener("click", function () {
      // on n'anime qu'apres le chargement, jamais au premier rendu
      racine.classList.add("theme-anime");
      var nouveau = themeCourant() === "dark" ? "light" : "dark";
      appliquer(nouveau);
      stockage("ecrire", nouveau);
    });
    return b;
  }

  function installer() {
    if (document.querySelector(".theme-toggle")) return;
    bouton = creerBouton();

    var conteneur = document.querySelector(".site-header .container");
    if (conteneur) {
      // on regroupe le code du cours et le bouton a droite de l'en-tete
      var code = conteneur.querySelector(".course-code");
      var actions = document.createElement("div");
      actions.className = "header-actions";
      if (code) {
        conteneur.insertBefore(actions, code);
        actions.appendChild(code);
      } else {
        conteneur.appendChild(actions);
      }
      actions.appendChild(bouton);
    } else {
      // page sans en-tete : bouton flottant en haut a droite
      bouton.style.position = "fixed";
      bouton.style.top = "14px";
      bouton.style.right = "14px";
      bouton.style.zIndex = "999";
      bouton.style.background = "var(--primary)";
      document.body.appendChild(bouton);
    }
    majBouton(themeCourant());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", installer);
  } else {
    installer();
  }

  // --- 3. suivi de la preference systeme ----------------------------
  // tant que l'utilisateur n'a pas choisi explicitement, on suit l'OS
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    var reagir = function (e) {
      if (stockage("lire")) return;          // choix explicite : on ne touche pas
      racine.classList.add("theme-anime");
      appliquer(e.matches ? "dark" : "light");
    };
    if (mq.addEventListener) mq.addEventListener("change", reagir);
    else if (mq.addListener) mq.addListener(reagir);
  }

  // --- 4. raccourci clavier : Maj + D -------------------------------
  document.addEventListener("keydown", function (e) {
    if (e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey &&
        (e.key === "D" || e.key === "d")) {
      var cible = e.target || {};
      var nom = (cible.tagName || "").toLowerCase();
      if (nom === "input" || nom === "textarea" || nom === "select" ||
          cible.isContentEditable) {
        return;                              // on n'interfere pas avec la saisie
      }
      racine.classList.add("theme-anime");
      var nouveau = themeCourant() === "dark" ? "light" : "dark";
      appliquer(nouveau);
      stockage("ecrire", nouveau);
    }
  });
})();
