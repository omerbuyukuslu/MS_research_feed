<template>
    <div class="signup-container">
      <h2>Sign Up</h2>
      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" v-model="email" type="email" required />
          <p v-if="errors.email" class="error">{{ errors.email }}</p>
        </div>
        <div class="form-group">
          <label for="username">Username</label>
          <input id="username" v-model="username" type="text" required />
          <p v-if="errors.username" class="error">{{ errors.username }}</p>
        </div>
        <div class="form-group">
          <label for="password1">Password</label>
          <input id="password1" v-model="password1" type="password" required />
          <p v-if="errors.password1" class="error">{{ errors.password1 }}</p>
        </div>
        <div class="form-group">
          <label for="password2">Confirm Password</label>
          <input id="password2" v-model="password2" type="password" required />
          <p v-if="errors.password2" class="error">{{ errors.password2 }}</p>
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Signing Up...' : 'Sign Up' }}
        </button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        email: '',
        username: '',
        password1: '',
        password2: '',
        errors: {}, // Holds validation errors
        loading: false,
      };
    },
    methods: {
      async handleSignup() {
        this.loading = true;
  
        // Validate required fields
        if (!this.email || !this.username || !this.password1 || !this.password2) {
          alert('All fields are required.');
          this.loading = false;
          return;
        }
  
        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(this.email)) {
          this.errors = { email: 'Please enter a valid email address.' };
          this.loading = false;
          return;
        }
  
        // Validate passwords
        if (this.password1 !== this.password2) {
          this.errors = { password2: 'Passwords do not match.' };
          this.loading = false;
          return;
        }
  
        // Retrieve CSRF token
        const csrfToken = this.getCsrfToken();
  
        try {
          const response = await fetch('http://127.0.0.1:8000/users/signup/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
            credentials: 'include',
            body: JSON.stringify({
              email: this.email,
              username: this.username,
              password1: this.password1,
              password2: this.password2,
            }),
          });
  
          const contentType = response.headers.get('Content-Type');
  
          let responseData;
          if (contentType && contentType.includes('application/json')) {
            responseData = await response.json(); // Parse as JSON
          } else {
            responseData = await response.text(); // Parse as plain text
          }
  
          if (response.ok) {
            alert('Account created successfully! Please log in.');
            console.log('Server response:', responseData); // Debug server response
            this.errors = {};
            this.$router.push('/login');
          } else {
            console.error('Server error:', responseData);
            if (typeof responseData === 'string') {
              alert(`Server error: ${responseData}`); // Handle text error
            } else {
              this.errors = responseData.errors || {};
            }
          }
        } catch (error) {
          console.error('Unexpected error during signup:', error);
          alert('An unexpected error occurred. Please try again later.');
        } finally {
          this.loading = false;
        }
      },
      getCsrfToken() {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; csrftoken=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
      },
    },
  };
  </script>
  
  <style scoped>
  .signup-container {
    margin: 100px auto;
    width: 300px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background: #f9f9f9;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .error {
    color: red;
    font-size: 12px;
    margin-top: 5px;
  }
  </style>
  