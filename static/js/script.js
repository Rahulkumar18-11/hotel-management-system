// Hotel Management System Front-End JavaScript Handler

document.addEventListener("DOMContentLoaded", function () {
    // 1. Live Clock initialization
    const clockEl = document.getElementById("liveClock");
    if (clockEl) {
        function updateClock() {
            const now = new Date();
            clockEl.innerText = now.toLocaleString("en-US", {
                weekday: "short",
                year: "numeric",
                month: "short",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit"
            });
        }
        updateClock();
        setInterval(updateClock, 1000);
    }

    // 2. Responsive Mobile Sidebar Toggle
    const sidebar = document.getElementById("sidebar");
    const sidebarToggle = document.getElementById("sidebarToggle");
    const sidebarClose = document.getElementById("sidebarClose");

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", function () {
            sidebar.classList.add("show");
        });
    }

    if (sidebarClose && sidebar) {
        sidebarClose.addEventListener("click", function () {
            sidebar.classList.remove("show");
        });
    }

    // 3. Auto-dismiss Flash Alerts after 5 seconds
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // 4. Chart.js Dashboard Visualizations
    if (window.dashboardChartData) {
        initDashboardCharts(window.dashboardChartData);
    }
});

function initDashboardCharts(data) {
    // Chart 1: Occupancy Doughnut Chart
    const ctxOcc = document.getElementById("chartOccupancy");
    if (ctxOcc) {
        new Chart(ctxOcc, {
            type: "doughnut",
            data: {
                labels: ["Available", "Booked", "Maintenance"],
                datasets: [{
                    data: data.occupancy,
                    backgroundColor: ["#198754", "#ffc107", "#dc3545"],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });
    }

    // Chart 2: Monthly Revenue Bar Chart
    const ctxRev = document.getElementById("chartRevenue");
    if (ctxRev) {
        new Chart(ctxRev, {
            type: "bar",
            data: {
                labels: data.monthlyLabels,
                datasets: [{
                    label: "Monthly Revenue (₹)",
                    data: data.monthlyRevenue,
                    backgroundColor: "#0d6efd",
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Chart 3: Booking Status Pie Chart
    const ctxStatus = document.getElementById("chartBookingStatus");
    if (ctxStatus) {
        new Chart(ctxStatus, {
            type: "pie",
            data: {
                labels: ["Reserved", "Checked In", "Checked Out", "Cancelled"],
                datasets: [{
                    data: data.bookingStatus,
                    backgroundColor: ["#0dcaf0", "#198754", "#6c757d", "#dc3545"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });
    }

    // Chart 4: Room Category Distribution Radar / Polar Area Chart
    const ctxTypes = document.getElementById("chartRoomTypes");
    if (ctxTypes) {
        new Chart(ctxTypes, {
            type: "polarArea",
            data: {
                labels: ["Single", "Double", "Deluxe", "Suite"],
                datasets: [{
                    data: data.roomTypes,
                    backgroundColor: ["#6f42c1", "#20c997", "#fd7e14", "#0d6efd"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });
    }
}
