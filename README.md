# ARCHITECT — Precision in Motion

> An interactive 3D articulated architect desk lamp web experience featuring real-time forward kinematics, procedural warm lighting, and a luxury editorial UI built with **Three.js** and **Blender**.

---

## ✨ Features

- **4-DOF Hierarchical Kinematics:** Live articulated forward kinematics supporting horizontal base swivel, lower arm pitch, elbow flexion/extension, and shade tilt with realistic physical angle limits.
- **Dynamic Light Beam & Pool Tracking:** Live ray-plane intersection calculating the shade's physical 38° cone orientation to dynamically project and scale an incandescent light pool on the desk.
- **Editorial Luxury HUD:** Typography (`Cinzel`, `Plus Jakarta Sans`, `JetBrains Mono`), vertical dashed gesture legend, and tactile glass control capsule for Power and Filament Flicker.
- **3D Desk Environment & Props:** Procedural open architect sketchbook with technical schematics, hardcover architecture volumes (*Bauhaus*, *Kinfolk*), and matte ceramic coffee mug.
- **Post-Processing Pipeline:** ACESFilmic tone mapping, UnrealBloom, and soft shadows.

---

## 🛠️ Tech Stack

- **3D Modeling & Procedural Rigging:** Blender (Python API `bpy`)
- **3D Web Engine:** Three.js + Postprocessing (UnrealBloomPass)
- **Bundler & Dev Server:** Vite
- **Styling:** Vanilla CSS (Glassmorphic Luxury Design System)

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/CodeCrafterAdi2006/architect-3d-lamp.git
cd architect-3d-lamp/web
```

### 2. Install dependencies
```bash
npm install
```

### 3. Run development server
```bash
npm run dev
```

### 4. Build for production
```bash
npm run build
```

---

## 📂 Project Structure

```
├── blender_scripts/      # Procedural Blender Python pipeline scripts (01-08)
├── exports/              # Exported GLB binary assets
├── web/                  # Interactive Three.js web application
│   ├── assets/           # GLB model and textures
│   ├── index.html        # Main HTML structure & editorial HUD
│   ├── style.css         # Luxury glassmorphism design system
│   ├── main.js           # Three.js kinematics engine & light steering
│   └── package.json      # Vite & Three.js dependencies
└── README.md
```

---

## 👤 Author

- **Portfolio:** [aditya1952-portfolio.vercel.app](https://aditya1952-portfolio.vercel.app/)
- **GitHub:** [@CodeCrafterAdi2006](https://github.com/CodeCrafterAdi2006)
