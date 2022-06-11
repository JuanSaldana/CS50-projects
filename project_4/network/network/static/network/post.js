document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#collapsable-button")
    .addEventListener("click", () => {
      document.querySelector("#collapseExample").collapse.show;
    });
});
