// ---- un-authenticated users drawer alert ---- //
function handleMenuClick(element, isDisabled) {
  if (isDisabled === "true") {
    var loginModal = new bootstrap.Modal(
      document.getElementById("loginRequiredModal")
    );
    loginModal.show();
    return false;
  }
  return true;
}

// --- Charts --- //
function createBarChart(
  elementId,
  { labels, data, label, bgColors, borderColors }
) {
  const element = document.getElementById(elementId);
  if (!element) return null;

  return new Chart(element.getContext("2d"), {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: label,
          data: data,
          backgroundColor: bgColors,
          borderColor: borderColors,
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true },
      },
    },
  });
}