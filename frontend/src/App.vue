<script setup>
import NavigationBar from './components/NavigationBar.vue';
import { RouterView } from 'vue-router'; // Use RouterView for dynamic content like login or articles
</script>

<template>
  <div class="app-container">
    <!-- Navigation Bar (3/10 of screen width) -->
    <div class="nav-bar">
      <NavigationBar />
    </div>

    <!-- Main Content (7/10 of screen width) -->
    <div class="main-content">
      <RouterView /> <!-- Dynamically load pages (ArticlesFeed, LoginPage, etc.) -->
    </div>
  </div>
</template>

<style>
/* Layout styles */
.app-container {
  display: flex;
  flex-direction: row; /* Layout in a horizontal row */
  height: 100vh; /* Full viewport height */
}

.nav-bar {
  flex: 2; /* 2/10 of the screen width */
  background: #333; /* Dark background for the navigation bar */
  color: white;
  padding: 20px; /* Padding for the navigation bar */
}

.main-content {
  flex: 8; /* 8/10 of the screen width */
  overflow-y: auto; /* Enable vertical scrolling for the main content */
  padding: 20px; /* Padding for main content */
  background: #f9f9f9; /* Light background for content area */
}
</style>
