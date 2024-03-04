// document.getElementById('loginForm').addEventListener('submit', async function(event) {
//     event.preventDefault(); // Prevent default form submission
    
//     const username = document.getElementById('id_login').value;
//     const password = document.getElementById('id_password').value;

//     try {
//         const response = await fetch('/accounts/login/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/x-www-form-urlencoded',
//             },
//             body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
//         });
        
//         if (response.ok) {
//             // Handle successful login, e.g., redirect to dashboard
//             window.location.href = '/dashboard/';
//         } else {
//             // Handle failed login, e.g., display error message
//             console.error('Login failed');
//         }
//     } catch (error) {
//         console.error('Error:', error);
//     }
// });

// function updateDateTime() {
//     const now = new Date();
//     const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true };
//     const dateTimeString = now.toLocaleDateString('en-US', options);
//     document.getElementById('datetime').textContent = dateTimeString;
// }

// updateDateTime();
// setInterval(updateDateTime, 1000); // Update every second