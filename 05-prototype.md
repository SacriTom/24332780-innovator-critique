# Step E — Prototype + Design Specs

**Derived from:** 04-solution-design.md

---

## Product: HiveMap Platform

### 1. Core Features (MVP)

#### 1.1 Survey Mission Planner
- Define survey zone on a map (draw polygon or enter coordinates)
- Auto-generate optimal drone flight paths for thermal + multispectral coverage
- Estimate flight time, battery swaps, and sensor data volume
- Export mission plan to DJI or ArduPilot-compatible formats

#### 1.2 Site Detection Engine
- Ingest drone sensor data (thermal IR, NDVI multispectral, LiDAR point clouds)
- Automated detection algorithms:
  - **Structure Finder:** Identify ruins/abandoned buildings from LiDAR elevation data
  - **Moisture Mapper:** Subsurface water signatures from thermal differential analysis
  - **Pollinator Tracker:** Bee flight corridor detection from thermal motion analysis
  - **Vegetation Anomaly Detector:** Unexpected green patches via NDVI thresholding
- Output: georeferenced feature layer with detected assets

#### 1.3 TEK Annotation Interface
- Tablet-optimised (Android), works offline with sync-when-connected
- Displays drone imagery with detected features highlighted
- Knowledge holders can:
  - Confirm / reject / reclassify each detected feature
  - Add voice notes (transcribed to text via Whisper API)
  - Draw historical water routes, migration paths, seasonal patterns
  - Rate structural integrity (visual assessment scale 1–5)
- Available in French, Arabic, Hassaniya, Pulaar

#### 1.4 HiveMap Scoring Dashboard
- Each surveyed site receives a HiveMap Score (0–100) computed from:
  - Water availability index (30%)
  - Pollinator presence score (20%)
  - Structural reusability rating (15%)
  - Soil rehabilitation potential (15%)
  - Proximity to cooperative (10%)
  - Tenure clarity rating (10%)
- Interactive map view with colour-coded sites (red/amber/green)
- Drill-down to individual site profiles with sensor imagery, TEK annotations, score breakdown

#### 1.5 Activation Report Generator
- Select a scored site → auto-generate PDF activation plan
- Includes: recommended crops, apiary placement, rehabilitation cost, 3-year P&L projection
- Formatted for development funder submission (GIZ, USAID, AFD templates)

### 2. Architecture

```
┌─────────────────────────────────────────────────┐
│                   FRONTEND                       │
│  React + Mapbox GL JS + PWA (offline-capable)   │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Mission  │  │  Map     │  │  Dashboard   │  │
│  │ Planner  │  │  Viewer  │  │  & Reports   │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└──────────────────┬──────────────────────────────┘
                   │ REST API + WebSocket
┌──────────────────┴──────────────────────────────┐
│                   BACKEND                        │
│  Python (FastAPI) + Celery task queue           │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Auth &   │  │ Sensor   │  │  Scoring     │  │
│  │ Users    │  │ Pipeline │  │  Engine      │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────┐
│                DATA LAYER                        │
│  PostgreSQL + PostGIS │ MinIO (sensor files)    │
│  Redis (cache/queue)  │ SQLite (offline TEK)    │
└─────────────────────────────────────────────────┘
```

### 3. User Flows

#### Flow 1: Drone Operator — Survey Mission
1. Login → Mission Planner
2. Draw survey zone on map
3. Configure sensors (thermal + multispectral + LiDAR)
4. Generate flight plan → export to drone
5. Fly mission → upload data on return
6. System processes data → site features detected
7. Review detected features on map → flag any issues
8. Assign sites for TEK validation

#### Flow 2: TEK Knowledge Holder — Site Annotation
1. Open tablet app (offline mode)
2. View assigned sites with drone imagery
3. For each detected feature: confirm / reject / annotate
4. Record voice notes in local language
5. Draw historical features on map overlay
6. Sync data when connectivity available

#### Flow 3: Cooperative Leader — Dashboard Review
1. Login → Dashboard
2. View ranked site portfolio (HiveMap Scores)
3. Drill into top-scoring sites
4. Generate activation report
5. Download PDF → submit to funder

### 4. Brand Guidelines

#### Colour Palette
| Role | Colour | Hex | Usage |
|------|--------|-----|-------|
| Primary | Desert Gold | #D4A843 | Headers, CTAs, accents |
| Secondary | Sahel Green | #4A7C59 | Success states, vegetation data |
| Dark | Basalt | #2C2C2C | Body text, dark backgrounds |
| Light | Sand | #F5F0E8 | Backgrounds, cards |
| Accent | Honey Amber | #E8960C | Highlights, bee/pollinator features |
| Alert | Terracotta | #C65D3E | Warnings, high-risk indicators |

#### Typography
- **Headlines:** Inter Bold (700), 28–48px
- **Body:** Inter Regular (400), 16px, line-height 1.6
- **Data/Code:** JetBrains Mono, 14px
- **Arabic/Hassaniya:** Noto Sans Arabic

#### Logo Concept
Hexagonal beehive cell containing a simplified drone silhouette, with a subtle map pin at the centre. Rendered in Desert Gold on dark backgrounds, Basalt on light.

#### Tone of Voice
- Grounded, not grandiose
- Data-driven but human
- Respectful of traditional knowledge — never patronising
- "We see what satellites miss. We listen to what algorithms can't hear."

### 5. MVP Development Timeline

| Week | Milestone | Deliverables |
|------|-----------|-------------|
| 1–2 | Foundation | Auth, database schema, API scaffolding, map component |
| 3–4 | Sensor Pipeline | Data ingestion, structure detection, moisture mapping |
| 5–6 | TEK Interface | Offline-capable tablet app, annotation tools, voice notes |
| 7–8 | Scoring Engine | HiveMap Score algorithm, dashboard, site profiles |
| 9–10 | Report Generator | PDF activation plans, funder-ready templates |
| 11–12 | Integration & Testing | End-to-end flow, field testing with pilot cooperative |
| 13–14 | Pilot Launch | Deploy with 2 cooperatives in Adrar region |

**Total MVP timeline: 14 weeks / 3.5 months**

### 6. Hardware Requirements

| Component | Specification | Estimated Cost |
|-----------|--------------|----------------|
| Survey Drone | DJI Matrice 350 RTK | €10,500 |
| Thermal Camera | DJI Zenmuse H30T | €5,200 |
| Multispectral Sensor | MicaSense RedEdge-P | €5,500 |
| LiDAR Module | DJI Zenmuse L2 | €6,800 |
| Field Tablets (x5) | Samsung Galaxy Tab Active4 Pro | €3,250 |
| Edge Server | NVIDIA Jetson Orin (field processing) | €1,200 |
| **Total per survey kit** | | **€32,450** |
