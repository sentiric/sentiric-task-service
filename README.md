# Sentiric Task Service

**Description:** Manages and executes long-running, asynchronous, or scheduled tasks (e.g., batch processing, AI model training, report generation) within the Sentiric platform.

**Core Responsibilities:**
*   Accepting and queuing task definitions.
*   Distributing tasks to appropriate workers and monitoring their execution status.
*   Providing features like automatic retries on failure, scheduling, and prioritization.
*   Integrating with message brokers (e.g., RabbitMQ, Kafka) for task queuing.

**Technologies:**
*   Python (e.g., Celery, FastAPI for task definition API) or Node.js (e.g., BullMQ).
*   Message Broker client libraries.

**API Interactions (As an API Provider & Client/Consumer):**
*   **As a Provider/Queue Consumer:** Receives tasks from various services (e.g., `sentiric-agent-service` for asynchronous AI operations, `sentiric-cdr-service` for batch reports).
*   **As a Client/Queue Publisher:** Triggers tasks in other services or consumes results from them.

**Local Development:**
1.  Clone this repository: `git clone https://github.com/sentiric/sentiric-task-service.git`
2.  Navigate into the directory: `cd sentiric-task-service`
3.  Install dependencies: `pip install -r requirements.txt` (Python) or `npm install` (Node.js).
4.  Create a `.env` file from `.env.example` to configure message broker connections and task definitions.
5.  Start the service: `python app.py` (or equivalent, potentially with a separate worker process).

**Configuration:**
Refer to `config/` directory and `.env.example` for service-specific configurations, including message broker connection details, task schedules, and worker settings.

**Deployment:**
Designed for containerized deployment (e.g., Docker, Kubernetes), often deployed with separate worker instances for task execution. Refer to `sentiric-infrastructure`.

**Contributing:**
We welcome contributions! Please refer to the [Sentiric Governance](https://github.com/sentiric/sentiric-governance) repository for coding standards and contribution guidelines.

**License:**
This project is licensed under the [License](LICENSE).
