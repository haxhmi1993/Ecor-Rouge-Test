# Ecor-Rouge-Test

### Overview
- Comsumer file is consumer.py, creates connection with RabbitMQ and starts listening
- Producer file is producer.py, creates connection and keeps sending messages with timke difference as set in poll time.
- Utils are contains in utils folder, contains logger to manage logs, also contains constants.py to store global project constants.


### Docker Compose to run all services:
```bash
docker compose up --build
```

### .env file
- The configurable options are present as Environmnet Variables in example.env file. Follow this example fine to create .env file in the root of your project
- RABBITMQ_HOST is rabbitmq host, can be configured to connect to some other RabbitMQ instance.
- POLL_INTERVAL is poll time between two messages.
