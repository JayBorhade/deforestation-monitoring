# 🌍 Deforestation Monitoring Dashboard

An AI-powered satellite monitoring system for real-time deforestation detection, historical change analysis, and predictive hotspot identification.

## 🎯 Features

- **🛰️ Satellite Image Processing**: Automated ingestion and processing of satellite imagery from Sentinel-2, Landsat, and other sources
- **🤖 AI Deforestation Detection**: U-Net based deep learning model for accurate deforestation segmentation
- **📊 Historical Change Detection**: Track deforestation trends over time
- **🗺️ Interactive GIS Map**: Real-time map visualization with layer controls
- **📈 Analytics Dashboard**: Comprehensive statistics and insights
- **🚨 Alert System**: Automated alerts for significant deforestation events
- **🎯 Predictive Hotspots**: ML-based prediction of future deforestation risk areas
- **🔐 Authentication-Ready**: Secure API with JWT authentication support
- **🐳 Docker Ready**: Complete containerization with Docker Compose
- **🚀 CI/CD Pipeline**: GitHub Actions for automated testing and deployment

## 🏗️ Architecture

### Technology Stack

**Frontend:**
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Leaflet (GIS Maps)
- Chart.js (Analytics)

**Backend:**
- FastAPI
- Python 3.10+
- SQLAlchemy ORM
- PostgreSQL + PostGIS
- Alembic (Migrations)

**AI/ML:**
- PyTorch
- U-Net Architecture
- ResNet50 Backbone
- OpenCV
- Rasterio
- GDAL

**Deployment:**
- Docker & Docker Compose
- GitHub Actions
- Vercel (Frontend)
- Railway/Render (Backend)

## 📁 Project Structure

```
deforestation-monitoring/
├── frontend/                    # Next.js React frontend
├── backend/                     # FastAPI Python backend
├── ai-models/                   # ML model training and inference
├── docker-compose.yml           # Docker orchestration
├── docs/                        # Documentation
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+ (for local development)
- Node.js 18+ (for frontend development)
- Git

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/JayBorhade/deforestation-monitoring.git
cd deforestation-monitoring

# Start all services
docker compose up -d

# Services will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/api/docs
# - Database: localhost:5432
```

### Local Development

#### Backend Setup

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev
```

## 📚 Documentation

- [Architecture Guide](./ARCHITECTURE.md)
- [API Documentation](./docs/API.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
- [Setup Instructions](./docs/SETUP.md)

## 🔌 API Endpoints

### Health & Status
- `GET /api/health` - Health check
- `GET /` - API info

### Satellite Images
- `POST /api/satellite-images` - Upload satellite image
- `GET /api/satellite-images` - List images
- `GET /api/satellite-images/{id}` - Get image details

### Analysis Results
- `POST /api/analysis-results` - Create analysis
- `GET /api/analysis-results` - List results
- `GET /api/analysis-results/{id}` - Get result details

### Alerts
- `POST /api/alerts` - Create alert
- `GET /api/alerts` - List alerts
- `GET /api/alerts/{id}` - Get alert details
- `PATCH /api/alerts/{id}` - Update alert
- `GET /api/alerts/stats/summary` - Alert statistics

### Predictions
- `GET /api/predictions` - List predictions
- `GET /api/predictions/{id}` - Get prediction
- `GET /api/predictions/stats/risk-distribution` - Risk statistics

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

## 📊 Database

The application uses PostgreSQL with PostGIS extension for geospatial queries.

### Key Tables

- **satellite_images**: Satellite imagery metadata
- **analysis_results**: AI model predictions and analysis
- **alerts**: Deforestation alerts
- **predictions**: Hotspot predictions

## 🔐 Security Considerations

- JWT authentication ready
- CORS configured
- Environment-based configuration
- Secure password handling
- SQL injection prevention via SQLAlchemy ORM

## 🚀 Deployment

### Cloud Deployment

The application can be deployed to:

- **Vercel** (Frontend)
- **Railway** (Backend)
- **AWS** (Full Stack)
- **Google Cloud** (Full Stack)
- **Azure** (Full Stack)

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed instructions.

## 📈 Performance

- Async API endpoints for high throughput
- Database query optimization with proper indexing
- Caching strategies for satellite imagery
- Efficient ML inference pipeline

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review API documentation at `/api/docs`

## 🎓 Related Resources

- [Sentinel-2 Data](https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2)
- [PostGIS Documentation](https://postgis.net/)
- [PyTorch Documentation](https://pytorch.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)

---

**Made with ❤️ for environmental conservation**
