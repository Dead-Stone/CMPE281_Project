# Robot Patrol Path Optimization System

A comprehensive system for optimizing security robot patrol paths with multiple optimization criteria.

## Prerequisites

- Docker
- Docker Compose
- Git

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd BackendSystem
```

2. Configure Environment Variables:
- Copy `.env.example` to `.env`
- Update the values in `.env` with your configuration

3. Build and Start the Services:
```bash
docker-compose up --build
```

The application will be available at:
- Backend API: http://localhost:5000
- MongoDB: localhost:27017
- MySQL: localhost:3306

## API Endpoints

### Create Patrol Path
```
POST /api/patrol/path

Payload:
{
  "robot_id": 1,
  "staff_id": 2,
  "waypoints": [
    { "latitude": 37.7749, "longitude": -122.4194 },
    { "latitude": 37.7750, "longitude": -122.4189 }
  ],
  "start_time": "2024-01-01T08:00:00",
  "end_time": "2024-01-01T10:00:00",
  "repeat": false,
  "frequency": "once"
}
```

### Optimize Patrol Path
```
PUT /api/paths/{path_id}/optimize

Payload:
{
  "criteria": ["battery", "coverage", "time", "obstacles"],
  "area_bounds": {
    "min_x": 0,
    "max_x": 100,
    "min_y": 0,
    "max_y": 100
  },
  "speed_limit": 5.0,
  "obstacles": [
    {"x": 50, "y": 50}
  ]
}
```

## Development

### Running Tests
```bash
docker-compose exec backend pytest
```

### Code Formatting
```bash
docker-compose exec backend black .
docker-compose exec backend flake8
```

## Deployment

### Production Deployment

1. Update environment variables for production:
```bash
cp .env.example .env
# Edit .env with production values
```

2. Deploy using Docker Compose:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Monitoring

- Application logs: `docker-compose logs -f backend`
- MongoDB logs: `docker-compose logs -f mongodb`
- MySQL logs: `docker-compose logs -f mysql`

## Security Notes

1. Change default passwords in production
2. Update SECRET_KEY in .env
3. Configure proper firewall rules
4. Set up SSL/TLS for production

## Backup

### Database Backups

MongoDB:
```bash
docker-compose exec mongodb mongodump --out /backup
```

MySQL:
```bash
docker-compose exec mysql mysqldump -u root -p robot_patrol > backup.sql
```

## Troubleshooting

1. If containers don't start:
   - Check logs: `docker-compose logs`
   - Verify port availability
   - Check environment variables

2. If database connection fails:
   - Verify credentials in .env
   - Check if databases are running
   - Verify network connectivity

## License

MIT License
