



const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container_login = document.querySelector(".container_login");

sign_up_btn.addEventListener("click", () => {
  container_login.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container_login.classList.remove("sign-up-mode");
});