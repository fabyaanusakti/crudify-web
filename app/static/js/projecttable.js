class ProjekTable {
  constructor(tableContainerId) {
    try {
      // Initialize core elements
      this.container = document.getElementById(tableContainerId);
      if (!this.container) {
        throw new Error(`Container with ID ${tableContainerId} not found`);
      }

      // Table elements
      this.searchInput = this.container.querySelector("#searchInput");
      this.syncButton = this.container.querySelector("[data-sync-url]");
      this.table = this.container.querySelector("table");
      this.alertContainer = this.createAlertContainer();

      // Modal elements
      this.statusModal = document.getElementById('statusModal');
      this.statusForm = document.getElementById('statusForm');
      this.modalProjectId = document.getElementById('modalProjectId');
      this.statusDropdown = document.getElementById('statusDropdown');

      if (!this.searchInput || !this.syncButton || !this.table) {
        throw new Error("Required elements not found in container");
      }

      this.initEvents();
    } catch (error) {
      console.error("Initialization error:", error);
      this.showAlert("Gagal memuat tabel projek", "danger");
    }
  }

  initEvents() {
    // Search functionality
    this.searchInput.addEventListener("input", () => {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => this.filterRows(), 300);
    });

    // Sync button
    this.syncButton.addEventListener("click", (e) => {
      e.preventDefault();
      if (confirm("Apakah Anda yakin ingin menyinkronkan data projek?")) {
        this.syncProjects();
      }
    });

    // Status modal events
    if (this.statusModal) {
      // When modal opens
      this.statusModal.addEventListener('show.bs.modal', (event) => {
        const button = event.relatedTarget;
        const projectId = button.getAttribute('data-project-id');
        const currentStatus = button.getAttribute('data-current-status');
        
        // Update form action URL with the correct project ID
        const formAction = this.statusForm.getAttribute('action');
        this.statusForm.setAttribute('action', formAction.replace('/0/', `/${projectId}/`));
        
        this.modalProjectId.value = projectId;
        this.statusDropdown.value = currentStatus;
      });

      // Form submission loading state
      if (this.statusForm) {
        this.statusForm.addEventListener('submit', (e) => {
          const submitButton = this.statusForm.querySelector('button[type="submit"]');
          const originalText = submitButton.innerHTML;
          
          // Show loading state
          submitButton.disabled = true;
          submitButton.innerHTML = `
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Memproses...
          `;
          
          // The form will submit normally, no need for AJAX
          // The page will refresh after submission
        });
      }
    }
  }

  filterRows() {
    try {
      const keyword = this.searchInput.value.trim().toLowerCase();
      const rows = this.table.querySelectorAll("tbody tr");

      let visibleRows = 0;

      rows.forEach((row) => {
        if (row.querySelector("td[colspan]")) {
          row.style.display = "none";
          return;
        }

        const rowText = row.textContent.toLowerCase();
        const shouldShow = keyword === "" || rowText.includes(keyword);
        row.style.display = shouldShow ? "" : "none";

        if (shouldShow) visibleRows++;
      });

      this.showNoResultsMessage(visibleRows === 0 && keyword !== "");
    } catch (error) {
      console.error("Filter error:", error);
    }
  }

  async syncProjects() {
    const button = this.syncButton;
    const originalText = button.innerHTML;

    try {
      button.disabled = true;
      button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
        Memproses...
      `;

      const csrfToken = this.getCSRFToken();
      if (!csrfToken) {
        throw new Error("Token keamanan hilang. Silakan muat ulang halaman.");
      }

      const response = await fetch(button.dataset.syncUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/json",
        },
        credentials: "same-origin",
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Sinkronisasi gagal");
      }

      this.showAlert(
        `Sinkronisasi berhasil! ${data.created || 0} dibuat, ${
          data.updated || 0
        } diperbarui.`,
        "success"
      );

      if (data.refresh_needed) {
        setTimeout(() => location.reload(), 750);
      }
    } catch (error) {
      console.error("Sync error:", error);
      this.showAlert(error.message, "danger");
    } finally {
      button.disabled = false;
      button.innerHTML = originalText;
    }
  }

  getCSRFToken() {
    try {
      return (
        document.querySelector("[name=csrfmiddlewaretoken]")?.value ||
        document.cookie.match(/csrftoken=([^;]+)/)?.[1] ||
        null
      );
    } catch (error) {
      console.error("CSRF token error:", error);
      return null;
    }
  }

  createAlertContainer() {
    const alertDiv = document.createElement("div");
    alertDiv.className = "position-fixed top-0 end-0 p-3";
    alertDiv.style.zIndex = "1100";
    document.body.appendChild(alertDiv);
    return alertDiv;
  }

  showAlert(message, type) {
    const alert = document.createElement("div");
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = "alert";
    alert.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    this.alertContainer.innerHTML = "";
    this.alertContainer.appendChild(alert);

    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 5000);
  }

  showNoResultsMessage(show) {
    let noResultsRow = this.table.querySelector(".no-results-row");

    if (show && !noResultsRow) {
      noResultsRow = document.createElement("tr");
      noResultsRow.className = "no-results-row";
      noResultsRow.innerHTML = `
        <td colspan="${this.table.querySelectorAll("thead th").length}">
          <div class="text-center py-3 text-muted">
            Tidak ada projek yang cocok dengan pencarian Anda
          </div>
        </td>
      `;
      this.table.querySelector("tbody").appendChild(noResultsRow);
    } else if (!show && noResultsRow) {
      noResultsRow.remove();
    }
  }
}

// Initialize on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  try {
    if (document.getElementById("projekTableContainer")) {
      new ProjekTable("projekTableContainer");
    }
  } catch (error) {
    console.error("Initialization failed:", error);
  }
});