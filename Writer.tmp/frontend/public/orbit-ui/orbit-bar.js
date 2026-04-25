(function orbitShellBootstrap() {
  if (typeof window === "undefined") {
    return;
  }

  var STORAGE_KEYS = {
    authUser: "auth_user",
    orgId: "orbit_org_id",
    orgOptions: "orbit_org_options",
  };

  var TOKEN_KEYS = [
    "auth_token",
    "gate_access_token",
    "gate_refresh_token",
    "access_token",
  ];

  var DEFAULT_APPS = [
    { id: "control-center", label: "Control Center", url: "http://localhost:45011" },
    { id: "atlas", label: "Atlas", url: "http://localhost:5173" },
    { id: "calendar", label: "Calendar", url: "http://localhost:45005" },
    { id: "planet", label: "Planet", url: "http://localhost:45006" },
    { id: "meet", label: "Meet", url: "http://localhost:45003" },
    { id: "mail", label: "Mail", url: "http://localhost:45004" },
    { id: "connect", label: "Connect", url: "http://localhost:45008" },
    { id: "learn", label: "Learn", url: "http://localhost:45009" },
    { id: "writer", label: "Writer", url: "http://localhost:45010" },
    { id: "secure", label: "Secure", url: "http://localhost:45012" },
    { id: "capital-hub", label: "Capital Hub", url: "http://localhost:45013" },
    { id: "turbotick", label: "TurboTick", url: "http://localhost:45018" },
    { id: "wallet", label: "RM Wallet", url: "http://localhost:45019" },
    { id: "dock", label: "RM Dock", url: "http://localhost:45020" },
    { id: "fitterme", label: "FitterMe", url: "http://localhost:45016" },
    { id: "gate-admin", label: "Gate Admin", url: "http://localhost:45022" },
    { id: "orbit-shell", label: "Orbit Shell", url: "http://localhost:6300" },
  ];

  var DEFAULT_ORGS = [
    { id: "org-enterprise", label: "Enterprise" },
    { id: "org-product", label: "Product" },
    { id: "org-engineering", label: "Engineering" },
  ];

  function safeParseJson(raw) {
    if (!raw) {
      return null;
    }
    try {
      return JSON.parse(raw);
    } catch (_err) {
      return null;
    }
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function readUser() {
    var parsed = safeParseJson(window.localStorage.getItem(STORAGE_KEYS.authUser));
    if (!parsed || typeof parsed !== "object") {
      return { name: "R&M Product", email: "guest@orbit.local", orgId: "" };
    }
    var name = parsed.name || parsed.display_name || parsed.username || parsed.sub || "R&M Product";
    var email = parsed.email || parsed.username || "user@orbit.local";
    var orgId = parsed.org_id || parsed.orgId || "";
    return { name: name, email: email, orgId: orgId };
  }

  function readOrgOptions() {
    var saved = safeParseJson(window.localStorage.getItem(STORAGE_KEYS.orgOptions));
    if (Array.isArray(saved) && saved.length) {
      return saved
        .map(function mapOrg(entry) {
          if (!entry || typeof entry !== "object") {
            return null;
          }
          var id = String(entry.id || entry.org_id || "").trim();
          var label = String(entry.label || entry.name || entry.org_name || "").trim();
          if (!id || !label) {
            return null;
          }
          return { id: id, label: label };
        })
        .filter(Boolean);
    }
    return DEFAULT_ORGS.slice();
  }

  function ensureOrg(orgId, orgOptions) {
    if (!orgId) {
      return orgOptions[0] ? orgOptions[0].id : "";
    }
    var found = orgOptions.some(function hasOrg(option) {
      return option.id === orgId;
    });
    if (!found) {
      orgOptions.unshift({ id: orgId, label: orgId });
    }
    return orgId;
  }

  function getInitials(name) {
    var parts = String(name || "")
      .trim()
      .split(/\s+/)
      .filter(Boolean);
    if (!parts.length) {
      return "RM";
    }
    if (parts.length === 1) {
      return parts[0].slice(0, 2).toUpperCase();
    }
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }

  function withOrg(url, orgId) {
    if (!orgId) {
      return url;
    }
    try {
      var parsed = new URL(url, window.location.origin);
      parsed.searchParams.set("org", orgId);
      return parsed.toString();
    } catch (_err) {
      return url;
    }
  }

  function parseApps(raw) {
    var parsed = safeParseJson(raw);
    if (!Array.isArray(parsed) || !parsed.length) {
      return DEFAULT_APPS.slice();
    }
    var normalized = parsed
      .map(function normalize(entry) {
        if (!entry || typeof entry !== "object") {
          return null;
        }
        var id = String(entry.id || "").trim();
        var label = String(entry.label || "").trim();
        var url = String(entry.url || "").trim();
        if (!id || !label || !url) {
          return null;
        }
        return { id: id, label: label, url: url };
      })
      .filter(Boolean);

    return normalized.length ? normalized : DEFAULT_APPS.slice();
  }

  function closeAllPanels(root) {
    root.querySelectorAll("[data-orbit-panel]").forEach(function closePanel(panel) {
      panel.setAttribute("data-open", "0");
    });
  }

  function togglePanel(root, panelName) {
    var target = root.querySelector('[data-orbit-panel="' + panelName + '"]');
    if (!target) {
      return;
    }
    var shouldOpen = target.getAttribute("data-open") !== "1";
    closeAllPanels(root);
    target.setAttribute("data-open", shouldOpen ? "1" : "0");
  }

  function currentAppFallbackFromLocation() {
    var href = window.location.href;
    var matched = DEFAULT_APPS.find(function findCurrent(app) {
      return href.indexOf(app.url) === 0;
    });
    return matched ? matched.id : "";
  }

  function emit(name, detail) {
    window.dispatchEvent(new CustomEvent(name, { detail: detail }));
  }

  var THEME_KEY = "orbit-theme";

  function readTheme() {
    try { return localStorage.getItem(THEME_KEY) || "system"; } catch (_) { return "system"; }
  }

  function applyTheme(theme) {
    try {
      var prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      var isDark = theme === "dark" || (theme === "system" && prefersDark);
      document.documentElement.classList.toggle("dark", isDark);
      localStorage.setItem(THEME_KEY, theme);
      emit("orbit:theme-change", { theme: theme, isDark: isDark });
    } catch (_) {}
  }

  function nextTheme(current) {
    if (current === "light") return "dark";
    if (current === "dark") return "system";
    return "light";
  }

  function themeIcon(theme) {
    var prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    var isDark = theme === "dark" || (theme === "system" && prefersDark);
    return isDark
      ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/></svg>'
      : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32 1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>';
  }

  if (!customElements.get("orbit-shell-bar")) {
    customElements.define(
      "orbit-shell-bar",
      class OrbitShellBar extends HTMLElement {
        connectedCallback() {
          if (this.dataset.orbitMounted === "1") {
            return;
          }
          this.dataset.orbitMounted = "1";
          this.render();
          this.bind();
        }

        disconnectedCallback() {
          if (this._onDocumentClick) {
            document.removeEventListener("click", this._onDocumentClick, true);
          }
          if (this._onEscape) {
            window.removeEventListener("keydown", this._onEscape);
          }
        }

        render() {
          var user = readUser();
          var orgOptions = readOrgOptions();
          var storedOrg = window.localStorage.getItem(STORAGE_KEYS.orgId);
          var orgId = ensureOrg(storedOrg || user.orgId || "", orgOptions);
          var appId = (this.getAttribute("app-id") || currentAppFallbackFromLocation() || "").trim();
          var appName = (this.getAttribute("app-name") || "Workspace").trim();
          var homeHref = this.getAttribute("home-href") || "/";
          var searchHref = this.getAttribute("search-href") || "http://localhost:45009/search.html";
          var apps = parseApps(this.getAttribute("apps-json"));
          var theme = readTheme();

          this._orgId = orgId;
          this._apps = apps;

          var appLinksHtml = apps
            .map(function makeAppLink(app) {
              var isCurrent = app.id === appId ? "1" : "0";
              return (
                '<a class="orbit-shell__app-link" data-current="' +
                isCurrent +
                '" href="' +
                escapeHtml(withOrg(app.url, orgId)) +
                '">' +
                '<span>' +
                escapeHtml(app.label) +
                "</span>" +
                '<span class="orbit-shell__app-meta">' +
                escapeHtml(app.id) +
                "</span>" +
                "</a>"
              );
            })
            .join("");

          var orgOptionsHtml = orgOptions
            .map(function makeOrgOption(option) {
              var selected = option.id === orgId ? ' selected="selected"' : "";
              return (
                '<option value="' +
                escapeHtml(option.id) +
                '"' +
                selected +
                ">" +
                escapeHtml(option.label) +
                "</option>"
              );
            })
            .join("");

          var initials = getInitials(user.name);

          this.innerHTML =
            '<div class="orbit-shell-root">' +
            '<div class="orbit-shell">' +
            '<a class="orbit-shell__brand" href="' +
            escapeHtml(homeHref) +
            '">' +
            '<span class="orbit-shell__brand-icon">RM</span>' +
            '<span class="orbit-shell__brand-label">Orbit</span>' +
            "</a>" +
            '<div class="orbit-shell__section">' +
            '<button class="orbit-shell__chip" type="button" data-orbit-toggle="apps">' +
            '<span class="material-symbols-outlined">apps</span>' +
            "<span>Apps</span>" +
            "</button>" +
            '<div class="orbit-shell__panel" data-orbit-panel="apps">' +
            '<p class="orbit-shell__panel-title">App Launcher</p>' +
            appLinksHtml +
            "</div>" +
            "</div>" +
            '<div class="orbit-shell__section">' +
            '<span class="orbit-shell__org-label">Org</span>' +
            '<label class="orbit-shell__org-wrap">' +
            '<select class="orbit-shell__org-select" data-orbit-org="1">' +
            orgOptionsHtml +
            "</select>" +
            "</label>" +
            "</div>" +

            '<span class="orbit-shell__spacer"></span>' +
            '<div class="orbit-shell__section">' +
            '<button class="orbit-shell__theme-toggle" type="button" data-orbit-action="toggle-theme" aria-label="Toggle theme (' + theme + ')">' +
            themeIcon(theme) +
            '</button>' +
            '</div>' +
            '<div class="orbit-shell__section">' +
            '<button class="orbit-shell__identity-toggle" type="button" data-orbit-toggle="identity">' +
            '<span class="orbit-shell__avatar">' +
            escapeHtml(initials) +
            "</span>" +
            '<span class="orbit-shell__identity-text">' +
            '<span class="orbit-shell__identity-name">' +
            escapeHtml(user.name) +
            "</span>" +
            '<span class="orbit-shell__identity-meta">' +
            escapeHtml(appName) +
            "</span>" +
            "</span>" +
            '<span class="material-symbols-outlined">expand_more</span>' +
            "</button>" +
            '<div class="orbit-shell__panel orbit-shell__panel--right" data-orbit-panel="identity">' +
            '<p class="orbit-shell__panel-title">' +
            escapeHtml(user.email) +
            "</p>" +
            '<button type="button" class="orbit-shell__action" data-orbit-action="profile">Profile</button>' +
            '<button type="button" class="orbit-shell__action orbit-shell__action-danger" data-orbit-action="signout">Sign out</button>' +
            "</div>" +
            "</div>" +
            "</div>" +
            "</div>";
        }

        bind() {
          var root = this;

          if (this._onDocumentClick) {
            document.removeEventListener("click", this._onDocumentClick, true);
          }
          if (this._onEscape) {
            window.removeEventListener("keydown", this._onEscape);
          }

          root.querySelectorAll("[data-orbit-toggle]").forEach(function bindToggle(button) {
            button.addEventListener("click", function onToggle(event) {
              event.stopPropagation();
              var panelName = button.getAttribute("data-orbit-toggle");
              togglePanel(root, panelName);
            });
          });

          var orgSelect = root.querySelector("[data-orbit-org='1']");
          if (orgSelect) {
            orgSelect.addEventListener("change", function onOrgChange() {
              var orgId = orgSelect.value;
              window.localStorage.setItem(STORAGE_KEYS.orgId, orgId);
              root._orgId = orgId;

              var rawUser = safeParseJson(window.localStorage.getItem(STORAGE_KEYS.authUser));
              if (rawUser && typeof rawUser === "object") {
                rawUser.org_id = orgId;
                rawUser.orgId = orgId;
                window.localStorage.setItem(STORAGE_KEYS.authUser, JSON.stringify(rawUser));
              }

              emit("orbit:org-change", { orgId: orgId });
              root.render();
              root.bind();
            });
          }

          root.querySelectorAll("[data-orbit-action]").forEach(function bindAction(button) {
            button.addEventListener("click", function onAction() {
              var action = button.getAttribute("data-orbit-action");
              if (action === "toggle-theme") {
                var current = readTheme();
                var next = nextTheme(current);
                applyTheme(next);
                root.render();
                root.bind();
                return;
              }
              if (action === "profile") {
                closeAllPanels(root);
                emit("orbit:profile-click", {});
                return;
              }
              if (action === "signout") {
                TOKEN_KEYS.forEach(function removeToken(key) {
                  window.localStorage.removeItem(key);
                  window.sessionStorage.removeItem(key);
                });
                emit("orbit:signed-out", {});

                var signoutUrl = root.getAttribute("signout-url");
                if (signoutUrl) {
                  window.location.href = signoutUrl;
                } else {
                  window.location.reload();
                }
              }
            });
          });

          this._onDocumentClick = function onDocumentClick(event) {
            if (!root.contains(event.target)) {
              closeAllPanels(root);
            }
          };
          document.addEventListener("click", this._onDocumentClick, true);

          this._onEscape = function onEscape(event) {
            if (event.key === "Escape") {
              closeAllPanels(root);
            }
          };
          window.addEventListener("keydown", this._onEscape);
        }
      }
    );
  }

  window.createOrbitShellBar = function createOrbitShellBar(options) {
    var existing = document.querySelector("orbit-shell-bar[data-orbit-global='1']");
    if (existing) {
      return existing;
    }
    var element = document.createElement("orbit-shell-bar");
    element.dataset.orbitGlobal = "1";

    if (options && typeof options === "object") {
      Object.keys(options).forEach(function setAttr(key) {
        var value = options[key];
        if (value === undefined || value === null) {
          return;
        }
        var attr = key
          .replace(/([a-z0-9])([A-Z])/g, "$1-$2")
          .replace(/_/g, "-")
          .toLowerCase();
        if (attr === "apps" && Array.isArray(value)) {
          element.setAttribute("apps-json", JSON.stringify(value));
          return;
        }
        element.setAttribute(attr, String(value));
      });
    }

    document.body.prepend(element);
    return element;
  };
})();
