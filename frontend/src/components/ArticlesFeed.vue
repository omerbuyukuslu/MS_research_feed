<template>
  <div>
    <!-- Update Articles Section -->
    <div class="update-section">
      <button :disabled="isUpdating" @click="startUpdate">
        {{ isUpdating ? "Updating..." : "Update Articles" }}
      </button>
      <p>Last update: {{ lastUpdated || "Not updated yet" }}</p>
      <div class="output-log">
        <p v-for="line in log" :key="line">{{ line }}</p>
      </div>
    </div>

    <!-- Search Bar -->
    <div class="search-bar">
      <input 
        v-model="searchQuery"
        type="text" 
        placeholder="Search articles by title, abstract, or journal..." 
      />
    </div>

    <!-- Filter Info -->
    <div class="filter-info">
      <p>{{ filteredArticles.length }} articles filtered out of {{ articles.length }}</p>
      <p>Oldest publication date: {{ oldestPublicationDate }}</p>
    </div>

    <!-- Articles -->
    <div class="articles-container">
      <div v-for="article in filteredArticles" :key="article.doi" class="article-box">
        <!-- Title -->
        <h2>{{ article.title }}</h2>

        <!-- Authors -->
        <h3>Authors: {{ article.authors }}</h3>

        <!-- Publication Date -->
        <h3>Publication Date: {{ article.published_date }}</h3>

        <!-- Journal -->
        <h3>
          Journal: 
          <a 
            :href="getJournalUrl(article.journal)" 
            target="_blank" 
            rel="noopener noreferrer">
            {{ article.journal }}
          </a>
        </h3>

        <!-- DOI -->
        <h3>
          DOI: 
          <a 
            :href="'https://www.google.com/search?q=' + article.doi" 
            target="_blank" 
            rel="noopener noreferrer">
            {{ article.doi }}
          </a>
        </h3>

        <!-- Abstract -->
        <div>
          <button @click="toggleAbstract(article.doi)">
            {{ article.showAbstract ? "Hide Abstract" : "Show Abstract" }}
          </button>
          <div 
            v-if="article.showAbstract" 
            class="abstract">
            {{ article.abstract }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';

export default {
  name: 'ArticlesFeed',
  setup() {
    const articles = ref([]);
    const searchQuery = ref('');
    const lastUpdated = ref('');
    const log = ref([]);
    const isUpdating = ref(false);

    // Fetch articles from the backend
    const fetchArticles = async () => {
      const response = await fetch('http://127.0.0.1:8000/api/articles/');
      const data = await response.json();
      articles.value = data.map((article) => ({
        ...article,
        showAbstract: false,
      }));
    };

    // Fetch the last updated timestamp from the backend
    const fetchLastUpdated = async () => {
      const response = await fetch('http://127.0.0.1:8000/api/last-updated/');
      const data = await response.json();
      lastUpdated.value = data.last_updated || "Not updated yet";
    };

    // Start streaming log messages from the backend
    const startUpdate = () => {
      if (isUpdating.value) return; // Prevent multiple clicks
      isUpdating.value = true; // Disable the button
      log.value = []; // Clear previous logs

      // Immediately update the last updated field on the frontend
      const now = new Date();
      lastUpdated.value = now.toISOString().replace('T', ' ').split('.')[0]; // Format as YYYY-MM-DD HH:MM:SS

      const eventSource = new EventSource('http://127.0.0.1:8000/api/stream-output/');

      eventSource.onmessage = (event) => {
        log.value.push(event.data);
      };

      eventSource.onopen = () => {
        log.value.push('Update process started...');
      };

      eventSource.onerror = (event) => {
        if (eventSource.readyState !== EventSource.CLOSED) {
          log.value.push('Error: Unable to connect to server.');
        }
        eventSource.close();
        isUpdating.value = false; // Re-enable the button
      };

      eventSource.addEventListener('done', () => {
        log.value.push('Update process completed.');
        eventSource.close();
        isUpdating.value = false; // Re-enable the button
        fetchArticles(); // Refresh articles list
        fetchLastUpdated(); // Sync with backend for accuracy
      });
    };


    onMounted(async () => {
      await fetchArticles();
      await fetchLastUpdated();
    });

    const filteredArticles = computed(() => {
      const query = searchQuery.value.toLowerCase();
      return articles.value.filter((article) =>
        article.title.toLowerCase().includes(query) ||
        article.abstract.toLowerCase().includes(query) ||
        article.journal.toLowerCase().includes(query)
      );
    });

    const oldestPublicationDate = computed(() => {
      if (articles.value.length === 0) return "N/A";
      const dates = articles.value.map((article) => new Date(article.published_date));
      return new Date(Math.min(...dates)).toISOString().split("T")[0];
    });

    const toggleAbstract = (doi) => {
      const article = articles.value.find((article) => article.doi === doi);
      if (article) {
        article.showAbstract = !article.showAbstract;
      }
    };

    const getJournalUrl = (journalName) => {
      const journal = articles.value.find((article) => article.journal === journalName);
      return journal ? journal.journal_url || '#' : '#';
    };


    return {
      articles,
      searchQuery,
      filteredArticles,
      oldestPublicationDate,
      toggleAbstract,
      getJournalUrl,
      startUpdate,
      lastUpdated,
      log,
      isUpdating,
    };
  },
};
</script>

<style>
.search-bar input {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.filter-info {
  margin-bottom: 20px;
}

/* Articles container */
.articles-container {
  display: flex;
  flex-direction: column; /* One article per row */
  gap: 20px;
}

/* Individual article box */
.article-box {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.article-box h2 {
  font-size: 18px;
  margin-bottom: 10px;
}

.article-box h3 {
  font-size: 14px;
  margin: 5px 0;
}

.article-box button {
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.article-box button:hover {
  background-color: #0056b3;
}

.article-box .abstract {
  margin-top: 10px;
  overflow-y: auto;
  background: #f9f9f9;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Update section */
.update-section {
  margin-bottom: 20px;
  text-align: center;
}

.update-section button {
  padding: 10px 20px;
  font-size: 18px;
  color: white;
  background-color: #28a745;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.update-section button:hover {
  background-color: #218838;
}

.update-section button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.update-section p {
  margin-top: 10px;
  font-size: 14px;
  color: #555;
}

/* Output log */
.output-log {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background: #f9f9f9;
  max-height: 300px;
  overflow-y: auto;
  font-family: monospace;
}

.output-log p {
  margin: 0;
}
</style>
