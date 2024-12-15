<template>
    <div class="navigation-bar">
      <h1>Research Feed</h1>
      <ul>
        <li>
          <router-link to="/" class="nav-link">Home</router-link>
        </li>
        <li>
          <router-link to="/login" class="nav-link">Login</router-link>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NavigationBar',
  };
  </script>
  
  <style scoped>
  .navigation-bar {
    width: 100%; /* Takes up the entire assigned flex width */
  }
  
  h1 {
    margin-bottom: 20px;
  }
  
  ul {
    list-style: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 10px;
  }
  
  .nav-link {
    color: white;
    text-decoration: none;
  }
  
  .nav-link:hover {
    text-decoration: underline;
  }
  </style>
  