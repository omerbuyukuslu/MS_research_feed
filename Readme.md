# **Materials Science Research Feed**

#### Video Demo: [<URL NOT YET AVAILABLE>](#)

#### Description:  
Materials Science Research Feed is a web-based platform designed to help material scientists stay up to date with recent publications in the field. Instead of visiting individual journal websites, this platform fetches **recent articles** from **23 high impact journals** and stores up to 30 days in materials science. Journals that are published older than 30 days will be deleted per database update. The tool focuses on improving productivity by reducing the time scientists spend searching for articles, while focusing on only the most recent articles.  

**Key Features:**  
- **Fetch Recent Articles**:  
   The **Update** button fetches articles published **yesterday** from 23 different journals. The data is aggregated in one SQlite database.  
- **Search Functionality**:  
   A **real-time search bar** allows users to filter articles based on keywords, searching across titles, abstracts, and journal names.  
- **Focus on Now**:  
   Only articles published in the **last 30 days** are displayed, ensuring scientists don´t miss current trends.  
- **Streamlined Viewing**:  
   Each article displays its title, authors, journal name, publication date, DOI link, and abstract (expandable). Journals are linked to their respective websites.  

---

## **How It Works**

### **Backend**  
- **Framework**: Django  
- **Database**: SQLite for local storage  
- **Data Sources**:  
   Articles are fetched using RSS feeds from 23 selected journals. Article metadata (authors, abstract, etc.) is enriched using the **CrossRef API**.  

- **`.env` File Configuration**:  
   The backend requires a `User-Agent` configuration for the CrossRef API:  
   ```dotenv
   USER_AGENT='ExampleProject (mailto:example@gmail.com)'
   ```

### **Frontend**  
- **Framework**: Vue.js  
- **Markup and styling**: HTML + CSS
---

## **Features**

1. **Update Articles**:  
   - The Update button fetches new articles using the CrossRef API and journal RSS feeds.  
   - The backend processes and stores only unique articles, ensuring no duplicates.  

2. **Search Bar**:  
   - Allows **real-time filtering** of articles.  
   - Filters articles based on **keywords** in title, abstract, and journal name.  

3. **Article Listing**:  
   - Displays article details:  
     - Title  
     - Authors  
     - Journal name (linked to the journal's official webpage)  
     - DOI link (searchable on Google)  
     - Abstract (expandable on demand)  

4. **Clean Data Management**:  
   - Articles older than **30 days** are automatically deleted from the database.  

---

## **Installation & Execution**

### Prerequisites:  
- Python 3.x  
- Node.js  
- Vue.js CLI  
- SQLite  

### Steps:  

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/omerbuyukuslu/MS_research_feed.git
   cd ms-research-feed
   ```

2. **Setup Backend**:  
   - Create a virtual environment:  
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - Install dependencies:  
     ```bash
     pip install -r requirements.txt
     ```
   - Add `.env` file with:  
     ```dotenv
     USER_AGENT='ExampleProject (mailto:example@gmail.com)'
     ```
   - Migrate and run the server:  
     ```bash
     python manage.py migrate
     python manage.py runserver
     ```

3. **Setup Frontend**:  
   - Navigate to the frontend folder:  
     ```bash
     cd frontend
     ```
   - Install dependencies and run the Vue app:  
     ```bash
     npm install
     npm run dev
     ```

4. **Access the App**:  
   - Open `http://127.0.0.1:8000` in your browser.  

---

## **Project Goals**

1. **What Will the Software Do?**  
   - Aggregate and display recent materials science articles.  
   - Reduce time spent by researchers visiting multiple journal websites.  
   - Provide a simple and efficient interface for searching and viewing articles.

2. **Features**:
   - Real-time search filtering.  
   - Update button to fetch recent articles.  
   - Articles displayed with clean formatting and linked resources.  

3. **Skills Acquired and Researched**:  
   - Backend: Django and SQLite for efficient data storage and API integration.  
   - Frontend: Vue.js for dynamic user interfaces.  
   - API Integration: RSS feeds and CrossRef API.  
   - Deployment and configuration: Managing environment variables and databases.

---

## **Project Outcomes**

1. **Good Outcome**:  
   - Fetch and display recent articles from 23 journals.  
   - Basic search and display functionality works smoothly.  

2. **Better Outcome**:  
   - Implement real-time feedback during updates.
   - Allow users to create accounts with email and password.
   - Add error handling for failed API requests or incomplete data.  

3. **Best Outcome**:  
   - Expand the platform to include more journals.  
   - Add user accounts to allow saved articles or custom preferences.  
   - Deploy the application for global access.  

---

## **License**  
This project is licensed under the MIT License.  

