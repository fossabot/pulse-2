# Grafana Loki

Loki is a horizontally-scalable, highly-available, multi-tenant log aggregation system inspired by Prometheus. It is designed to be very cost-effective and easy to operate. It does not index the contents of the logs, but rather a set of labels for each log stream.

```
loki
├── README.md
├── docker-compose.yaml
├── loki-config.yaml
├── otelcol-config.yaml
└── otelcol.Dockerfile

1 directory, 5 files
```

## Installation

### Prerequisites
- Docker
- Docker Compose
- Git

## Usage

### Start the Loki stack
```bash
docker-compose up -d
```

### Access the Grafana dashboard
- Open a browser and navigate to `http://localhost:3000`
- Login with the default credentials `admin:admin`
- Add a new data source with the URL `http://loki:3100`
- Import the dashboard from the file `grafana-dashboard.json`
- Explore the logs
- Enjoy!
- :tada:

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

---
© 2024 Open Source at Machani Robotics
