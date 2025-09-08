const API_URL = "http://127.0.0.1:8000";  // your Django backend

// Get stored token from localStorage
function getToken() {
  return localStorage.getItem("token");
}

// Wrapper for requests
async function apiRequest(endpoint, method = "GET", body = null, auth = true) {
  const headers = {
    "Content-Type": "application/json",
  };

  if (auth && getToken()) {
    headers["Authorization"] = `Bearer ${getToken()}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  return response.json();
}

export { apiRequest, getToken };