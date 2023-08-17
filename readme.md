**Prerequisites:**
- Make sure you have Python (version 3.6 or newer) installed on your machine.
- Install pip, which is the package installer for Python.
- Ensure you have virtualenv installed. If not, install it using `pip install virtualenv`.

**Steps to setup and run the application:**

1. **Create a virtual environment:** Create a new virtual environment to manage the project's dependencies. Run the following command in the terminal:
```shell
virtualenv venv
```

2. **Activate the virtual environment:** Before you start working on the project, activate the virtual environment:
- On Windows: `venv\Scripts\activate`
- On macOS and Linux: `source venv/bin/activate`

3. **Clone the project repository:** Clone the Django project repository to your local machine. If it's hosted on GitHub, you can use the following command:
```shell
git clone https://github.com/vivek-pr/social_media_analytics.git
```

4. **Navigate to the project directory:** Use the terminal to navigate to the directory where you cloned the project.

5. **Install project dependencies:** Install the required packages using pip by running:
```shell
pip install -r requirements.txt
```
6. **Install Redis:** Install Redis as a message broker for Celery and as a cache backend for Django.
- On Ubuntu: `sudo apt-get install redis-server`
- On macOS using Homebrew: `brew install redis`
- On Windows: Download the installer from https://github.com/tporadowski/redis/releases

7. **Run the Redis server:** Start the Redis server:
```shell
redis-server
```

8. **Run migrations:** Apply the database migrations using the following command:
```shell
python manage.py migrate
```

9. **Run the Celery worker:** Open a new terminal window, activate the virtual environment, and start the Celery worker:
```shell
celery -A social_media_analytics worker --loglevel=info
```

10. **Run the Django development server:** Finally, run the Django development server with the following command:
```shell
python manage.py runserver
```

12. **Access the application:** Open your web browser and navigate to `http://localhost:8000/api/v1/posts/` to interact with the social media analytics platform's API endpoints.

**Using the Analysis API Endpoint:**
1. **Create a post:** Use the POST creation API (`POST /api/v1/posts/`) to create a post. This will accept a JSON payload with text content.
2. **Get the unique identifier:** After creating a post, you will receive a unique identifier in the response.
3. **Perform post analysis:** Use the Post Analysis API (`GET /api/v1/posts/{id}/analysis/`) and replace `{id}` with the unique identifier received from the post creation. This will return the word count and average word length of the post.

---

### Infrastructure

1. **Web Servers**: Start with multiple web server instances behind a load balancer to distribute incoming traffic. Use an auto-scaling group to add more web server instances as traffic increases. Popular web servers include NGINX or Apache. A common practice is to run your Django application with Gunicorn as the application server, and use NGINX as the reverse proxy server.

2. **Load Balancer**: Implement a load balancer like Amazon ELB or HAProxy to distribute incoming traffic across your web servers. It can also perform health checks to ensure that traffic is only directed to healthy instances.

3. **Database**: Consider using a database like PostgreSQL, which supports a high degree of concurrency and performs well under high traffic loads. You could use Amazon RDS or another cloud provider's managed database service for automatic backups, patches, and scaling. Additionally, implement database replication (master-slave setup) to offload read queries to the read replicas and improve performance.

4. **Message Broker**: Use Redis or RabbitMQ as a message broker for Celery to offload the task of post analysis. This will enable the app to handle a high volume of post creation and analysis requests without overloading the web servers.

5. **Cache**: Implement caching with Redis to store the results of post analysis, reducing the need to recompute the analysis for repeated requests. This will significantly speed up response times and reduce the load on the system.

6. **Content Delivery Network (CDN)**: Utilize a CDN to serve static assets (e.g., images, stylesheets, JavaScript files) closer to the users, reducing the load on your servers and improving user experience.

7. **Monitoring & Logging**: Implement monitoring and logging solutions (e.g., CloudWatch, Datadog, Prometheus, ELK Stack) to keep track of the application's performance and troubleshoot any issues that arise.

### Scaling

1. **Vertical Scaling**: As a starting point, you can vertically scale the web servers and database by increasing the resources (CPU, memory, disk space) on the instances.

2. **Horizontal Scaling**: When vertical scaling is no longer sufficient, horizontally scale your web servers by adding more instances. Use an auto-scaling group to automate this process based on CPU utilization or other metrics.

3. **Database Sharding**: Consider database sharding, which involves splitting the database into smaller chunks (shards) that can be distributed across multiple servers. This helps distribute the load and improve query performance.

4. **Microservices**: As the application grows, break it down into microservices to isolate different functionalities. This will enable you to scale individual components independently, optimize resources, and improve the overall maintainability of the system.

5. **Task Queue Scaling**: Scale the Celery workers to handle a high volume of post analysis tasks. Consider using dedicated worker instances or containers to process different types of tasks.

6. **Cache Eviction Policies**: Implement cache eviction policies like LRU (Least Recently Used) or LFU (Least Frequently Used) to manage the cache effectively and ensure that frequently accessed data remains available in the cache.

7. **Geographical Distribution**: If your users are spread across different regions, consider deploying the application in multiple data centers or cloud regions. This will reduce latency and provide a better user experience.

By following these infrastructure and scaling strategies, your social media analytics platform should be able to handle a significant amount of traffic and provide a responsive and reliable user experience.

---
## Assumptions
Here are the assumptions and decisions I made while working on this project and the reasons behind them:

1. **Choice of Django and Django REST framework**: I assumed that the microservice needs to be developed using Python and the Django framework as per the project requirements. Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design, and it comes with a lot of built-in features. Django REST framework makes it easier to build robust web APIs with Django.

2. **SQLite as the Database**: The choice of SQLite for the database was made based on the project requirements, which specified using SQLite for simplicity. SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine. It is ideal for smaller applications or when starting the development process.

3. **Unique ID Generation**: Initially, it was suggested that the client would provide a unique identifier for each post. However, to simplify the post creation process for the client, I decided that the backend should generate the unique identifier. This avoids potential collisions if clients accidentally provide the same identifier for different posts.

4. **Analysis Endpoint**: For the analysis endpoint, I chose to provide both word count and average word length for a given post as per the project requirements. These metrics are commonly used in text analysis and can provide valuable insights into the content of the posts.

5. **Use of Celery**: I decided to use Celery for asynchronous task processing to handle the post analysis computation. This approach allows the application to offload the analysis tasks to background workers, improving the overall responsiveness of the API and enabling it to handle a higher volume of requests.

6. **Cache Implementation**: To optimize the analysis endpoint's performance, I decided to implement caching using Redis. By caching the results of post analysis, the application can quickly serve repeated requests without recomputing the analysis, improving the response times.

7. **Throttling**: In the test cases, I included a throttle test case to demonstrate the implementation of request rate limiting. Throttling is essential to protect the application from being overwhelmed by too many requests in a short amount of time.

8. **Test Cases**: I created test cases to cover the main functionalities of the API, including post creation, analysis, retrieval, and throttling. These test cases help ensure that the application works as expected and allow for easy regression testing when making changes.

9. **Analysis Computation**: The `analyze_post` method calculates the word count and average word length in O(n) time complexity, where n is the length of the post content. This approach was chosen for its simplicity and efficiency.

10. **Parallelization**: I suggested parallelizing or distributing the analysis computation to handle large volumes of data. This can be achieved using techniques like map-reduce or by distributing the computation across multiple Celery workers.

These assumptions and decisions were made based on the project requirements, best practices, and a desire to optimize the performance, scalability, and reliability of the social media analytics platform.
