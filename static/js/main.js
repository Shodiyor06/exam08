const API = "http://127.0.0.1:8000";

// ===== LOGIN =====
function login() {
    fetch("/api/accounts/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem("access", data.access);

            // 🔐 ME tekshirish
            fetch("/api/accounts/me/", {
                headers: {
                    "Authorization": "Bearer " + data.access
                }
            })
            .then(res => {
                if (res.status === 200) {
                    window.location.href = "/events/";
                } else {
                    alert("Token yaroqsiz");
                }
            });

        } else {
            alert("Login yoki parol xato");
        }
    });
}


// ===== LOGOUT =====
function logout() {
    localStorage.clear();
    window.location.href = "/login/";
}

// ===== LOAD EVENTS =====
function loadEvents() {
    const token = localStorage.getItem("access");

    fetch("/api/events/", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => {
        if (res.status === 401) {
            alert("Login qiling");
            window.location.href = "/login/";
            return;
        }
        return res.json();
    })
    .then(events => {
        const box = document.getElementById("events");
        box.innerHTML = "";

        if (!events || events.length === 0) {
            box.innerHTML = "<p>Eventlar mavjud emas</p>";
            return;
        }

        events.forEach(e => {
            box.innerHTML += `
                <div class="event">
                    <b>${e.title}</b><br>
                    Capacity: ${e.capacity}
                </div>
            `;
        });
    });
}



// ===== REGISTER EVENT =====
function registerEvent(eventId) {
    const token = localStorage.getItem("access");

    fetch(API + "/api/registrations/register/", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ event: eventId })
    })
    .then(res => res.json())
    .then(data => {
        alert("Registered");
    });
}

// ===== CANCEL EVENT =====
function cancelEvent(eventId) {
    const token = localStorage.getItem("access");

    fetch(API + `/api/registrations/cancel/${eventId}/`, {
        method: "PATCH",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {
        alert("Cancelled");
    });
}

// 1️⃣ Registrations count
function loadRegistrationsCount() {
    const id = document.getElementById("eventId").value;
    const token = localStorage.getItem("access");

    fetch(`/api/events/${id}/registrations-count/`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("regCount").innerText =
            "Ro‘yxatdan o‘tganlar soni: " + data.registrations_count;
    })
    .catch(() => {
        document.getElementById("regCount").innerText = "Xato yoki event topilmadi";
    });
}


// 2️⃣ Available seats
function loadAvailableSeats() {
    const id = document.getElementById("eventIdSeats").value;
    const token = localStorage.getItem("access");

    fetch(`/api/events/${id}/available-seats/`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("seatCount").innerText =
            "Bo‘sh joylar: " + data.available_seats;
    })
    .catch(() => {
        document.getElementById("seatCount").innerText = "Xato yoki event topilmadi";
    });
}


// 3️⃣ Top 5 events
function loadTopEvents() {
    const token = localStorage.getItem("access");

    if (!token) {
        alert("Login qiling");
        return;
    }

    fetch("/api/events/top-registrations/", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => {
        if (res.status === 401) {
            alert("Token yaroqsiz");
            return;
        }
        return res.json();
    })
    .then(events => {
        console.log("TOP EVENTS:", events); // 👈 MUHIM

        const ul = document.getElementById("topEvents");
        ul.innerHTML = "";

        if (!events || events.length === 0) {
            ul.innerHTML = "<li>Ma'lumot yo‘q</li>";
            return;
        }

        events.forEach(e => {
            ul.innerHTML += `
                <li>
                    <b>${e.title}</b> — ${e.registrations_count} ta
                </li>
            `;
        });
    })
    .catch(err => {
        console.error("XATO:", err);
    });
}
