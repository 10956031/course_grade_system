// 表格 hover 高亮（保險用，部分瀏覽器支援度不同）
document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll("table tbody tr");

    rows.forEach(row => {
        row.addEventListener("mouseenter", () => {
            row.style.backgroundColor = "#eef4ff";
        });

        row.addEventListener("mouseleave", () => {
            row.style.backgroundColor = "";
        });
    });
});
