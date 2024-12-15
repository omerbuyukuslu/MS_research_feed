import { createRouter, createWebHistory } from 'vue-router';
import ArticlesFeed from '../components/ArticlesFeed.vue';
import LoginPage from '../components/LoginPage.vue';
import SignupPage from '../components/SignupPage.vue';

const routes = [
  { path: '/', component: ArticlesFeed },
  { path: '/login', component: LoginPage },
  { path: '/signup', component: SignupPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
