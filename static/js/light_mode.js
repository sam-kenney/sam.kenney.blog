const lightMode = localStorage.getItem("light");
const root = document.documentElement;
const checkbox = document.querySelector("input[name=light-mode]");

if (lightMode) {
  root.classList.add("light");
  checkbox.checked = false;
} else {
  root.classList.remove("light");
  checkbox.checked = true;
}

checkbox.addEventListener("change", () => {
  root.classList.toggle("light");
  if (root.classList.contains("light")) {
    localStorage.setItem("light", true);
  } else {
    localStorage.removeItem("light");
  }
});
