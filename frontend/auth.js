const API = "http://127.0.0.1:8000";

(function() {
  const t = localStorage.getItem("oncho_token");
  const path = window.location.pathname;
  const onLoginPage = path.endsWith("login.html") || path.endsWith("/app/");
  if (t && onLoginPage) {
    window.location.replace("dashboard.html");
  }
})();

// Tab switching
function switchTab(tab) {
  document.querySelectorAll(".auth-tab").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".auth-form").forEach(f => f.classList.remove("active"));
  const idx = tab === "login" ? 0 : 1;
  document.querySelectorAll(".auth-tab")[idx].classList.add("active");
  document.getElementById(tab === "login" ? "loginForm" : "registerForm").classList.add("active");
  clearErrors();
}

function clearErrors() {
  ["loginError","regError","regSuccess"].forEach(id => {
    const el = document.getElementById(id);
    if (el) { el.textContent = ""; el.classList.add("hidden"); }
  });
}
function showError(id, msg)   { const e = document.getElementById(id); e.textContent = msg; e.classList.remove("hidden"); }
function showSuccess(id, msg) { const e = document.getElementById(id); e.textContent = msg; e.classList.remove("hidden"); }

function togglePass(inputId, btn) {
  const inp = document.getElementById(inputId);
  inp.type = inp.type === "password" ? "text" : "password";
  btn.textContent = inp.type === "password" ? "👁" : "🙈";
}

//  LOGIN 
async function doLogin(e) {
  if (e) e.preventDefault();
  clearErrors();

  const username = document.getElementById("loginUsername").value.trim();
  const password = document.getElementById("loginPassword").value;

  if (!username || !password) {
    showError("loginError", "Please enter username and password.");
    return;
  }

  const btn = document.querySelector("#loginForm .btn-primary");
  btn.querySelector("span").textContent = "Signing in…";
  btn.disabled = true;

  try {
    const form = new URLSearchParams();
    form.append("username", username);
    form.append("password", password);

    const res  = await fetch(`${API}/login`, {
      method:  "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body:    form
    });

    const data = await res.json();

    if (!res.ok) {
      showError("loginError", data.detail || "Login failed.");
      btn.querySelector("span").textContent = "Sign In";
      btn.disabled = false;
      return;
    }

    localStorage.setItem("oncho_token", data.access_token);
    localStorage.setItem("oncho_user",  data.username);
    localStorage.setItem("oncho_name",  data.full_name || data.username);


    window.location.assign("dashboard.html");

  } catch(err) {
    showError("loginError", "Cannot connect to server. Is it running?");
    btn.querySelector("span").textContent = "Sign In";
    btn.disabled = false;
  }
}

// REGISTER 
async function doRegister(e) {
  if (e) e.preventDefault();
  clearErrors();

  const full_name = document.getElementById("regFullName").value.trim();
  const email     = document.getElementById("regEmail").value.trim();
  const username  = document.getElementById("regUsername").value.trim();
  const password  = document.getElementById("regPassword").value;

  if (!username || !email || !password) {
    showError("regError", "Please fill all required fields.");
    return;
  }
  if (password.length < 6) {
    showError("regError", "Password must be at least 6 characters.");
    return;
  }

  const btn = document.querySelector("#registerForm .btn-primary");
  btn.querySelector("span").textContent = "Creating account…";
  btn.disabled = true;

  try {
    const res  = await fetch(`${API}/register`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ username, email, password, full_name })
    });

    const data = await res.json();

    if (!res.ok) {
      showError("regError", data.detail || "Registration failed.");
      btn.querySelector("span").textContent = "Create Account";
      btn.disabled = false;
      return;
    }

    localStorage.setItem("oncho_token", data.access_token);
    localStorage.setItem("oncho_user",  data.username);
    localStorage.setItem("oncho_name",  data.full_name || data.username);

    showSuccess("regSuccess", "Account created! Redirecting…");
    setTimeout(() => window.location.assign("dashboard.html"), 700);

  } catch(err) {
    showError("regError", "Cannot connect to server. Is it running?");
    btn.querySelector("span").textContent = "Create Account";
    btn.disabled = false;
  }
}
document.addEventListener("DOMContentLoaded", function() {
  
  const loginBtn    = document.querySelector("#loginForm .btn-primary");
  const registerBtn = document.querySelector("#registerForm .btn-primary");

  if (loginBtn)    loginBtn.addEventListener("click",    doLogin);
  if (registerBtn) registerBtn.addEventListener("click", doRegister);

  
  document.addEventListener("keydown", function(e) {
    if (e.key !== "Enter") return;
    e.preventDefault();
    const loginActive = document.getElementById("loginForm").classList.contains("active");
    if (loginActive) doLogin();
    else doRegister();
  });


  document.querySelectorAll(".inp").forEach(inp => {
    inp.addEventListener("keydown", function(e) {
      if (e.key === "Enter") {
        e.preventDefault();
        e.stopPropagation();
        const loginActive = document.getElementById("loginForm").classList.contains("active");
        if (loginActive) doLogin();
        else doRegister();
      }
    });
  });
});
