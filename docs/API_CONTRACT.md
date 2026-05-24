# FormFlow API Contract

This document outlines the strict API boundaries between the React frontend (`/client`) and the Python FastAPI backend (`/server`). All payloads use standard JSON formatting, except for music uploading which uses a multi-part form.

## API Endpoint Reference

| Method | Path | Description | Response Status |
|---|---|---|---|
| **GET** | `/api/projects` | List all choreography projects. | `200 OK` |
| **GET** | `/api/projects/{id}` | Get detailed project data (including dancers/formations). | `200 OK`, `404 Not Found` |
| **POST** | `/api/projects` | Create a new project. | `201 Created` |
| **PUT** | `/api/projects/{id}` | Edit general project details. | `200 OK`, `404 Not Found` |
| **DELETE** | `/api/projects/{id}` | Delete a project and cascade all associations. | `204 No Content` |
| **GET** | `/api/projects/{project_id}/dancers` | List all dancers registered in a project. | `200 OK` |
| **POST** | `/api/projects/{project_id}/dancers` | Create/add a dancer to a project. | `201 Created` |
| **PUT** | `/api/projects/{project_id}/dancers/{dancer_id}` | Edit dancer metadata (e.g. name, color). | `200 OK` |
| **DELETE** | `/api/projects/{project_id}/dancers/{dancer_id}` | Remove a dancer from the project. | `204 No Content` |
| **DELETE** | `/api/projects/{project_id}/dancers/bulk` | Remove multiple dancers from the project. | `204 No Content` |
| **GET** | `/api/projects/{project_id}/formations` | List formations alongside positioning arrays. | `200 OK` |
| **POST** | `/api/projects/{project_id}/formations` | Create a new formation snapshot. | `201 Created` |
| **PUT** | `/api/projects/{project_id}/formations/{formation_id}` | Edit formation metadata (name, timing). | `200 OK` |
| **DELETE** | `/api/projects/{project_id}/formations/{formation_id}` | Remove a formation snapshot. | `204 No Content` |
| **POST** | `/api/projects/{project_id}/formations/{formation_id}/duplicate` | Duplicate a formation with all its positions. | `201 Created` |
| **PUT** | `/api/projects/{project_id}/formations/reorder` | Update the sorting order index of snapshots. | `200 OK` |
| **PUT** | `/api/projects/{project_id}/formations/{formation_id}/positions` | Batch update positioning coordinates for a snapshot. | `200 OK` |
| **POST** | `/api/projects/{project_id}/ai/generate` | Generate random/symmetric placements on the grid. | `200 OK` |
| **POST** | `/api/projects/{project_id}/ai/suggest-transitions` | Optimally route transitions to minimize crossing routes. | `200 OK` |
| **POST** | `/api/projects/{project_id}/ai/template` | Generate layout based on standard presets (e.g., V_SHAPE). | `200 OK` |
| **GET** | `/api/projects/{project_id}/center-time` | Obtain cumulative center-stage metrics for all dancers. | `200 OK` |
| **GET** | `/api/projects/{project_id}/center-time/{dancer_id}` | Retrieve history of center-stage residency for a dancer. | `200 OK` |
| **POST** | `/api/projects/{project_id}/center-time/rebalance` | Formulate a balanced layout structure based on weights. | `200 OK` |
| **POST** | `/api/projects/{project_id}/music/upload` | Upload audio file. | `200 OK` |
| **GET** | `/api/projects/{project_id}/music/markers` | Retrieve timeline timestamp annotations. | `200 OK` |
| **POST** | `/api/projects/{project_id}/music/markers` | Bind a timeline label to a specific second marker. | `201 Created` |
| **PUT** | `/api/projects/{project_id}/music/markers/{id}` | Edit timeline marker metadata. | `200 OK` |
| **DELETE** | `/api/projects/{project_id}/music/markers/{id}` | Remove a timeline marker. | `204 No Content` |
| **POST** | `/api/projects/{project_id}/export/image` | Render static formation graphics. | `200 OK` |
| **POST** | `/api/projects/{project_id}/export/pdf` | Build multi-page formation books. | `200 OK` |

---

## Data Contract Structures

### 1. Projects API

#### `GET /api/projects`
**Response:**
```json
{
  "projects": [
    {
      "id": 1,
      "name": "Confidence Show",
      "description": "Choreography for summer show case",
      "num_dancers": 21,
      "audio_file_path": "uploads/audio_17165849.mp3",
      "created_at": "2026-05-23T12:00:00Z",
      "updated_at": "2026-05-23T12:00:00Z"
    }
  ]
}
```

#### `GET /api/projects/{id}`
**Response:**
```json
{
  "id": 1,
  "name": "Confidence Show",
  "description": "Choreography for summer show case",
  "num_dancers": 21,
  "audio_file_path": "uploads/audio_17165849.mp3",
  "dancers": [
    { "id": 5, "number": 1, "name": "Ayman", "color": "#ff2a7f", "group": "leads" }
  ],
  "formations": [
    {
      "id": 12,
      "name": "Intro",
      "order_index": 0,
      "timestamp_start": 0.0,
      "timestamp_end": 4.5,
      "positions": [
        { "dancer_id": 5, "x": 0.0, "y": -2.0 }
      ]
    }
  ],
  "created_at": "2026-05-23T12:00:00Z",
  "updated_at": "2026-05-23T12:00:00Z"
}
```

#### `POST /api/projects`
**Request Payload:**
```json
{
  "name": "Confidence Show",
  "description": "Choreography for summer show case",
  "num_dancers": 21
}
```

---

### 2. Dancers API

#### `POST /api/projects/{project_id}/dancers`
**Request Payload:**
```json
{
  "name": "Patty",
  "color": "#3b82f6",
  "group": "ensemble"
}
```
**Response:**
```json
{
  "id": 19,
  "project_id": 1,
  "number": 19,
  "name": "Patty",
  "color": "#3b82f6",
  "group": "ensemble",
  "created_at": "2026-05-23T12:00:00Z"
}
```

---

### 3. Formations API

#### `POST /api/projects/{project_id}/formations`
**Request Payload:**
```json
{
  "name": "Intro",
  "order_index": 0,
  "timestamp_start": 0.0,
  "timestamp_end": 4.5,
  "positions": [
    { "dancer_id": 5, "x": 0.0, "y": -2.0 }
  ]
}
```

#### `PUT /api/projects/{project_id}/formations/reorder`
**Request Payload:**
```json
{
  "ordered_ids": [12, 14, 13, 15]
}
```

---

### 4. Positions API

#### `PUT /api/projects/{project_id}/formations/{formation_id}/positions`
**Request Payload:**
```json
{
  "positions": [
    { "dancer_id": 5, "x": -1.2, "y": 3.4 },
    { "dancer_id": 6, "x": 1.2, "y": 3.4 }
  ]
}
```

---

### 5. AI Formation API

#### `POST /api/projects/{project_id}/ai/generate`
**Request Payload:**
```json
{
  "style": "symmetric",
  "density": 0.5,
  "symmetry": true,
  "focal_point": { "x": 0.0, "y": 0.0 }
}
```
**Response:**
```json
{
  "formation": {
    "name": "AI Generated Formation",
    "positions": [
      { "dancer_id": 5, "x": -2.0, "y": 1.5 },
      { "dancer_id": 6, "x": 2.0, "y": 1.5 }
    ]
  }
}
```

#### `POST /api/projects/{project_id}/ai/suggest-transitions`
**Request Payload:**
```json
{
  "from_formation_id": 12,
  "to_formation_id": 13
}
```
**Response:**
```json
{
  "paths": [
    {
      "dancer_id": 5,
      "waypoints": [
        { "x": -2.0, "y": 1.5, "t": 0.0 },
        { "x": -1.0, "y": 0.8, "t": 0.5 },
        { "x": 0.0, "y": 0.0, "t": 1.0 }
      ]
    }
  ],
  "estimated_duration": 4.5
}
```

---

### 6. Center Time Tracking API

#### `GET /api/projects/{project_id}/center-time`
**Response:**
```json
{
  "center_point": { "x": 0.0, "y": 0.0 },
  "threshold_radius": 2.5,
  "stats": [
    {
      "dancer_id": 5,
      "dancer_name": "Chase",
      "total_time_near_center": 32.5,
      "percentage": 42.5,
      "target_percentage": 25.0,
      "deviation": 17.5,
      "is_flagged": true
    }
  ]
}
```
