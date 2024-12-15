import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

createApp(App).use(router).mount('#app');

async function fetchCsrfToken() {
    const response = await fetch('http://127.0.0.1:8000/users/csrf/', {
        credentials: 'include', // Include cookies
    });
    const data = await response.json();
    console.log('CSRF Token fetched:', data.csrfToken); // Debug
    document.cookie = `csrftoken=${data.csrfToken}; path=/`; // Save token in cookies
}

// Call this function during initialization
fetchCsrfToken();

