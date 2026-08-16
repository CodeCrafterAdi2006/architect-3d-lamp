import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import deskLampUrl from './assets/desk_lamp.glb?url';

// -----------------------------------------------------------------------------
// 1. SETUP CANVAS, RENDERER & SCENE
// -----------------------------------------------------------------------------
const canvas = document.getElementById('webgl-canvas');
const loaderElement = document.getElementById('loader');

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111218);
scene.fog = new THREE.FogExp2(0x111218, 0.025);

const renderer = new THREE.WebGLRenderer({
  canvas,
  antialias: true,
  powerPreference: 'high-performance'
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.30;

// -----------------------------------------------------------------------------
// 2. STUDIO REFLECTION ENVIRONMENT
// -----------------------------------------------------------------------------
const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();

function createStudioEnvMap() {
  const envScene = new THREE.Scene();
  const envGeo = new THREE.SphereGeometry(10, 32, 16);

  const canvasTex = document.createElement('canvas');
  canvasTex.width = 512;
  canvasTex.height = 256;
  const ctx = canvasTex.getContext('2d');

  const grad = ctx.createLinearGradient(0, 0, 0, 256);
  grad.addColorStop(0.0, '#353c48');
  grad.addColorStop(0.5, '#181e28');
  grad.addColorStop(1.0, '#0a0d12');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 512, 256);

  ctx.fillStyle = '#ffffff';
  ctx.filter = 'blur(16px)';
  ctx.fillRect(80, 40, 140, 80);
  ctx.fillRect(320, 50, 100, 70);

  const tex = new THREE.CanvasTexture(canvasTex);
  tex.mapping = THREE.EquirectangularReflectionMapping;

  const envMat = new THREE.MeshBasicMaterial({ map: tex, side: THREE.BackSide });
  const envMesh = new THREE.Mesh(envGeo, envMat);
  envScene.add(envMesh);

  const renderTarget = pmremGenerator.fromScene(envScene);
  scene.environment = renderTarget.texture;
}

createStudioEnvMap();

// -----------------------------------------------------------------------------
// 3. CAMERA & CONTROLS
// -----------------------------------------------------------------------------
const camera = new THREE.PerspectiveCamera(
  35,
  window.innerWidth / window.innerHeight,
  0.1,
  100
);
camera.position.set(0.9, 2.3, 4.4);

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.maxPolarAngle = Math.PI / 2 - 0.02;
controls.minDistance = 1.6;
controls.maxDistance = 8.5;
controls.target.set(0.1, 0.95, -0.25);

// -----------------------------------------------------------------------------
// 4. POST-PROCESSING BLOOM COMPOSER
// -----------------------------------------------------------------------------
const renderScene = new RenderPass(scene, camera);

const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  0.42,  // bloom strength
  0.38,  // bloom radius
  0.82   // bloom threshold
);

const composer = new EffectComposer(renderer);
composer.addPass(renderScene);
composer.addPass(bloomPass);

// -----------------------------------------------------------------------------
// 5. STUDIO LIGHTING RIG (Moody Atmospheric Baseline)
// -----------------------------------------------------------------------------
const hemiLight = new THREE.HemisphereLight(0x3a3028, 0x080605, 0.65);
scene.add(hemiLight);

const ambientKey = new THREE.DirectionalLight(0xffecd6, 0.35);
ambientKey.position.set(3.0, 5.0, 3.0);
scene.add(ambientKey);

const subtleRim = new THREE.DirectionalLight(0x8899bb, 0.40);
subtleRim.position.set(-4.0, 3.5, -3.0);
scene.add(subtleRim);

// -----------------------------------------------------------------------------
// 6. EXPANSIVE DARK WALNUT DESK
// -----------------------------------------------------------------------------
function createWoodTexture() {
  const canvasTex = document.createElement('canvas');
  canvasTex.width = 1024;
  canvasTex.height = 1024;
  const ctx = canvasTex.getContext('2d');

  ctx.fillStyle = '#221711';
  ctx.fillRect(0, 0, 1024, 1024);

  for (let i = 0; i < 900; i++) {
    const y = Math.random() * 1024;
    const h = 1 + Math.random() * 3;
    const opacity = 0.04 + Math.random() * 0.07;
    ctx.fillStyle = Math.random() > 0.5 ? `rgba(60, 42, 28, ${opacity})` : `rgba(14, 8, 4, ${opacity})`;
    ctx.fillRect(0, y, 1024, h);
  }

  const texture = new THREE.CanvasTexture(canvasTex);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(6, 4);
  return texture;
}

const deskGeo = new THREE.BoxGeometry(14.0, 0.15, 9.0);
const deskMat = new THREE.MeshStandardMaterial({
  map: createWoodTexture(),
  color: 0x322219,
  roughness: 0.42,
  metalness: 0.08
});
const deskMesh = new THREE.Mesh(deskGeo, deskMat);
deskMesh.position.set(0.0, -0.075, 0.0);
deskMesh.receiveShadow = true;
scene.add(deskMesh);

// -----------------------------------------------------------------------------
// 6B. PROCEDURAL 3D DESK PROPS (Sketchbook, Books Stack, Ceramic Mug, Pen)
// -----------------------------------------------------------------------------
function createSketchbookTexture() {
  const c = document.createElement('canvas');
  c.width = 1024;
  c.height = 512;
  const ctx = c.getContext('2d');

  // Aged warm paper
  ctx.fillStyle = '#eeddc3';
  ctx.fillRect(0, 0, 1024, 512);

  // Center binding shadow
  const spineGrad = ctx.createLinearGradient(490, 0, 534, 0);
  spineGrad.addColorStop(0, 'rgba(0,0,0,0.0)');
  spineGrad.addColorStop(0.5, 'rgba(0,0,0,0.35)');
  spineGrad.addColorStop(1, 'rgba(0,0,0,0.0)');
  ctx.fillStyle = spineGrad;
  ctx.fillRect(480, 0, 64, 512);

  // Grid lines
  ctx.strokeStyle = 'rgba(160, 140, 110, 0.25)';
  ctx.lineWidth = 1;
  for (let x = 40; x < 984; x += 32) {
    if (Math.abs(x - 512) < 24) continue;
    ctx.beginPath();
    ctx.moveTo(x, 30);
    ctx.lineTo(x, 482);
    ctx.stroke();
  }
  for (let y = 30; y < 490; y += 32) {
    ctx.beginPath();
    ctx.moveTo(40, y);
    ctx.lineTo(480, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(544, y);
    ctx.lineTo(984, y);
    ctx.stroke();
  }

  // Left Page: Technical Cantilever / Crane schematic
  ctx.strokeStyle = '#2b231c';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  // Base & arm schematic
  ctx.strokeRect(120, 360, 160, 20);
  ctx.moveTo(200, 360); ctx.lineTo(200, 260);
  ctx.lineTo(340, 150); ctx.lineTo(420, 190);
  ctx.stroke();

  // Dimension lines & arcs
  ctx.strokeStyle = '#7c6652';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.arc(200, 260, 30, 0, Math.PI * 0.6);
  ctx.moveTo(110, 360); ctx.lineTo(110, 260);
  ctx.stroke();

  ctx.fillStyle = '#4a3b2c';
  ctx.font = '14px "JetBrains Mono", monospace';
  ctx.fillText('FIG. 04 — ARTICULATION JOINT', 120, 100);
  ctx.fillText('θ = 38.0° [± 153° SWIVEL]', 120, 124);
  ctx.fillText('TENSION EQUILIBRIUM: 12.4 N', 120, 430);

  // Right Page: Lamp Shade Section & Isometric Notes
  ctx.strokeStyle = '#2b231c';
  ctx.lineWidth = 2.0;
  ctx.beginPath();
  // Lamp shade bell cone profile
  ctx.moveTo(680, 180); ctx.lineTo(840, 280);
  ctx.lineTo(820, 320); ctx.lineTo(650, 200); ctx.closePath();
  ctx.stroke();
  // Bulb curve
  ctx.beginPath();
  ctx.arc(710, 220, 24, 0, Math.PI * 2);
  ctx.stroke();

  ctx.fillStyle = '#4a3b2c';
  ctx.fillText('SECT. B-B : REFLECTOR DRAFT', 620, 100);
  ctx.fillText('CURVATURE: PARABOLIC r=0.62m', 620, 380);
  ctx.fillText('ANODIZED MATTE FINISH', 620, 404);

  const tex = new THREE.CanvasTexture(c);
  return tex;
}

// 1. Open Sketchbook
const bookCoverMat = new THREE.MeshStandardMaterial({ color: 0x1c1713, roughness: 0.85 });
const bookPageMat = new THREE.MeshStandardMaterial({
  map: createSketchbookTexture(),
  roughness: 0.92,
  metalness: 0.0
});

const openBookGroup = new THREE.Group();
const leftPage = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.02, 1.15), [bookCoverMat, bookCoverMat, bookPageMat, bookCoverMat, bookCoverMat, bookCoverMat]);
leftPage.position.set(-0.43, 0.01, 0);
leftPage.rotation.y = 0.03;
leftPage.receiveShadow = true;
openBookGroup.add(leftPage);

const rightPage = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.02, 1.15), [bookCoverMat, bookCoverMat, bookPageMat, bookCoverMat, bookCoverMat, bookCoverMat]);
rightPage.position.set(0.43, 0.01, 0);
rightPage.rotation.y = -0.03;
rightPage.receiveShadow = true;
openBookGroup.add(rightPage);

openBookGroup.position.set(-0.45, 0.001, -1.05);
openBookGroup.rotation.y = 0.12;
scene.add(openBookGroup);

// Stylus / drafting pen resting across the sketchbook
const penMat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.35, metalness: 0.8 });
const penGeo = new THREE.CylinderGeometry(0.012, 0.012, 0.55, 16);
const penMesh = new THREE.Mesh(penGeo, penMat);
penMesh.rotation.z = Math.PI / 2.2;
penMesh.rotation.y = 0.45;
penMesh.position.set(0.05, 0.032, -0.95);
penMesh.castShadow = true;
scene.add(penMesh);

// 2. Stack of Hardcover Architecture Books (Bauhaus & Kinfolk)
function createBookTexture(title, subtitle, colorBg, colorTxt) {
  const c = document.createElement('canvas');
  c.width = 512; c.height = 128;
  const ctx = c.getContext('2d');
  ctx.fillStyle = colorBg;
  ctx.fillRect(0, 0, 512, 128);
  ctx.fillStyle = colorTxt;
  ctx.font = 'bold 24px "Cinzel", serif';
  ctx.letterSpacing = '6px';
  ctx.fillText(title, 40, 72);
  ctx.font = '12px "Plus Jakarta Sans", sans-serif';
  ctx.letterSpacing = '2px';
  ctx.fillText(subtitle, 260, 70);
  return new THREE.CanvasTexture(c);
}

const bookStackGroup = new THREE.Group();
const book1Mat = new THREE.MeshStandardMaterial({ map: createBookTexture('BAUHAUS', 'MAGDALENA DROSTE', '#282422', '#dcd4c8'), roughness: 0.7 });
const book1 = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.14, 0.95), book1Mat);
book1.position.set(0, 0.07, 0);
book1.receiveShadow = true;
book1.castShadow = true;
bookStackGroup.add(book1);

const book2Mat = new THREE.MeshStandardMaterial({ map: createBookTexture('KINFOLK', 'ENTREPRENEUR', '#1c1b1a', '#b8ae9e'), roughness: 0.65 });
const book2 = new THREE.Mesh(new THREE.BoxGeometry(1.35, 0.13, 0.92), book2Mat);
book2.position.set(0.02, 0.205, -0.01);
book2.rotation.y = -0.04;
book2.receiveShadow = true;
book2.castShadow = true;
bookStackGroup.add(book2);

bookStackGroup.position.set(-1.6, 0.001, -1.35);
bookStackGroup.rotation.y = 0.08;
scene.add(bookStackGroup);

// 3. Matte Ceramic Coffee Mug in ambient shadow
const mugGroup = new THREE.Group();
const mugMat = new THREE.MeshStandardMaterial({ color: 0x222120, roughness: 0.55, metalness: 0.1 });
const mugGeo = new THREE.CylinderGeometry(0.18, 0.16, 0.38, 24);
const mugMesh = new THREE.Mesh(mugGeo, mugMat);
mugMesh.position.y = 0.19;
mugMesh.castShadow = true;
mugGroup.add(mugMesh);

// Coffee liquid top
const liquidMat = new THREE.MeshStandardMaterial({ color: 0x110a05, roughness: 0.15 });
const liquidGeo = new THREE.CylinderGeometry(0.16, 0.16, 0.02, 24);
const liquidMesh = new THREE.Mesh(liquidGeo, liquidMat);
liquidMesh.position.y = 0.36;
mugGroup.add(liquidMesh);

mugGroup.position.set(-0.85, 0.001, -2.1);
scene.add(mugGroup);

// -----------------------------------------------------------------------------
// 7. FEATHERED RADIAL POOL OF LIGHT ON DESK
// -----------------------------------------------------------------------------
function createRadialLightTexture() {
  const canvasTex = document.createElement('canvas');
  canvasTex.width = 512;
  canvasTex.height = 512;
  const ctx = canvasTex.getContext('2d');

  const grad = ctx.createRadialGradient(256, 256, 10, 256, 256, 250);
  grad.addColorStop(0.0, 'rgba(255, 185, 90, 0.90)');
  grad.addColorStop(0.30, 'rgba(255, 155, 55, 0.55)');
  grad.addColorStop(0.65, 'rgba(255, 120, 30, 0.20)');
  grad.addColorStop(1.0, 'rgba(255, 100, 20, 0.0)');

  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 512, 512);

  const texture = new THREE.CanvasTexture(canvasTex);
  return texture;
}

const poolGeo = new THREE.PlaneGeometry(3.4, 3.8);
const poolMat = new THREE.MeshBasicMaterial({
  map: createRadialLightTexture(),
  transparent: true,
  opacity: 0.85,
  blending: THREE.AdditiveBlending,
  depthWrite: false
});
const poolMesh = new THREE.Mesh(poolGeo, poolMat);
poolMesh.rotation.x = -Math.PI / 2;
scene.add(poolMesh);

// -----------------------------------------------------------------------------
// 8. EXACT HIERARCHICAL KINEMATICS ENGINE
// -----------------------------------------------------------------------------
let lampModel = null;
let bulbMesh = null;
let shadeBellMesh = null;
let shadeRimMesh = null;
let lampPointLight = null;
let lampSpotLight = null;
let bulbMaterial = null;

let isLightOn = true;
let isFlickerEnabled = true;

// Hierarchical kinematic pivot nodes
const swivelPivot = new THREE.Object3D();
const lowerArmPivot = new THREE.Object3D();
const upperArmPivot = new THREE.Object3D();
const shadePivot = new THREE.Object3D();

swivelPivot.name = 'Pivot_Swivel';
lowerArmPivot.name = 'Pivot_LowerArm';
upperArmPivot.name = 'Pivot_UpperArm';
shadePivot.name = 'Pivot_Shade';

const allLampMeshes = [];
const meshToPartType = new Map();

// Helper to categorize every mesh strictly by its mechanical joint parent
function classifyPart(name) {
  if (name.includes('Base') && !name.includes('Bolt') && !name.includes('Cap')) {
    return 'base';
  } else if (
    name.includes('Stem') ||
    name.includes('JointBolt_Bottom_0') ||
    name.includes('BoltCap_0_')
  ) {
    return 'swivel';
  } else if (
    name.includes('LowerArm') ||
    name.includes('JointBolt_Bottom_1') ||
    name.includes('BoltCap_1_') ||
    name.includes('LowerArmPin')
  ) {
    return 'lowerArm';
  } else if (
    name.includes('UpperArm') ||
    name.includes('MiddleElbow') ||
    name.includes('CenterPivot') ||
    name.includes('UpperArmPin') ||
    name.includes('ThumbScrew')
  ) {
    return 'upperArm';
  } else {
    // Shade Bell, Rim, TopCap, Neck, Bulb Socket, Bulb, Top Joint Bolt & Caps (TopBoltCap_-1, TopBoltCap_1)
    return 'shade';
  }
}

const gltfLoader = new GLTFLoader();
gltfLoader.load(
  deskLampUrl || './assets/desk_lamp.glb',
  (gltf) => {
    lampModel = gltf.scene;

    const parts = {};

    lampModel.traverse((child) => {
      if (child.isMesh) {
        // Hide static rigid power cord and its top grommet collar for clean artifact-free articulation
        if (child.name.includes('PowerCord') || child.name.includes('Curve') || child.name.includes('Grommet')) {
          child.visible = false;
          return;
        }

        child.castShadow = true;
        child.receiveShadow = true;
        parts[child.name] = child;
        allLampMeshes.push(child);

        // Dull steel grey for bolts & springs
        if (child.name.includes('Bolt') || child.name.includes('Cap') || child.name.includes('Spring') || child.name.includes('ThumbScrew')) {
          if (child.material) {
            const steelMat = child.material.clone();
            steelMat.color = new THREE.Color(0x8e949c);
            steelMat.metalness = 0.82;
            steelMat.roughness = 0.38;
            steelMat.envMapIntensity = 1.0;
            child.material = steelMat;
          }
        }

        if (child.name.includes('Bulb') && !child.name.includes('Socket')) {
          bulbMesh = child;
          if (child.material) {
            bulbMaterial = child.material.clone();
            child.material = bulbMaterial;
            bulbMaterial.emissive = new THREE.Color(0xffaa44);
            bulbMaterial.emissiveIntensity = 3.0;
          }
        }

        if (child.name.includes('Shade_Bell')) {
          shadeBellMesh = child;
        }
        if (child.name.includes('Shade_Rim')) {
          shadeRimMesh = child;
        }
      }
    });

    scene.add(lampModel);

    // 1. Exact Hinge Joint World Positions
    const bottomHingePos = new THREE.Vector3();
    const elbowHingePos = new THREE.Vector3();
    const topHingePos = new THREE.Vector3();

    if (parts['Lamp_JointBolt_Bottom_0']) {
      parts['Lamp_JointBolt_Bottom_0'].getWorldPosition(bottomHingePos);
    } else {
      bottomHingePos.set(0.0, 0.465, 0.0);
    }

    if (parts['Lamp_ElbowBolt_CenterPivot']) {
      parts['Lamp_ElbowBolt_CenterPivot'].getWorldPosition(elbowHingePos);
    } else {
      elbowHingePos.set(0.0, 1.967, 0.646);
    }

    if (parts['Lamp_TopJoint_Bolt']) {
      parts['Lamp_TopJoint_Bolt'].getWorldPosition(topHingePos);
    } else {
      topHingePos.set(0.0, 2.503, -0.215);
    }

    // 2. Build the Kinematic Tree
    scene.add(swivelPivot);
    swivelPivot.position.set(0, 0, 0);

    lowerArmPivot.position.copy(bottomHingePos);
    swivelPivot.add(lowerArmPivot);

    upperArmPivot.position.copy(elbowHingePos);
    scene.add(upperArmPivot);
    lowerArmPivot.attach(upperArmPivot);

    shadePivot.position.copy(topHingePos);
    scene.add(shadePivot);
    upperArmPivot.attach(shadePivot);

    // 3. Attach every part to its exact structural parent
    for (const [name, mesh] of Object.entries(parts)) {
      const category = classifyPart(name);
      meshToPartType.set(mesh, category);

      if (category === 'swivel') {
        swivelPivot.attach(mesh);
      } else if (category === 'lowerArm') {
        lowerArmPivot.attach(mesh);
      } else if (category === 'upperArm') {
        upperArmPivot.attach(mesh);
      } else if (category === 'shade') {
        shadePivot.attach(mesh);
      }
      // 'base' stays at the root of lampModel
    }

    scene.updateMatrixWorld(true);

    // 4. Studio Lights
    const bulbWorldPos = new THREE.Vector3();
    if (bulbMesh) {
      bulbMesh.getWorldPosition(bulbWorldPos);
    } else {
      bulbWorldPos.set(0.0, 2.15, -0.66);
    }

    lampPointLight = new THREE.PointLight(0xffb566, 1.5, 7.5, 1.3);
    lampPointLight.position.copy(bulbWorldPos);
    lampPointLight.castShadow = false;
    scene.add(lampPointLight);

    lampSpotLight = new THREE.SpotLight(0xff9933, 6.0, 8.5, Math.PI / 3.2, 0.45, 1.2);
    lampSpotLight.position.copy(bulbWorldPos);
    lampSpotLight.target.position.set(0, 0, -2);
    lampSpotLight.castShadow = true;
    lampSpotLight.shadow.mapSize.width = 2048;
    lampSpotLight.shadow.mapSize.height = 2048;
    lampSpotLight.shadow.bias = -0.001;
    scene.add(lampSpotLight);
    scene.add(lampSpotLight.target);

    // Hide loader
    if (loaderElement) {
      loaderElement.classList.add('hidden');
    }
  },
  undefined,
  (error) => {
    console.error('Error loading GLB:', error);
  }
);

// -----------------------------------------------------------------------------
// 9. INTUITIVE DRAG CONTROLLER WITH NATURAL DIRECTION MAPPING
// -----------------------------------------------------------------------------
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

let isDraggingPart = false;
let activeDragPart = null;
// Per-frame previous pointer position (eliminates accumulated delta "debt" at clamp limits)
let prevPointerX = 0;
let prevPointerY = 0;

// Natural angular limits (radians)
const LIMITS = {
  swivel: { min: -Math.PI * 0.85, max: Math.PI * 0.85 }, // ±153° swivel
  lowerArm: { min: -0.80, max: 0.72 },                      // Lower arm pitch — stays within natural visual horizon
  upperArm: { min: -0.75, max: 0.75 },                      // Elbow joint pitch
  shade: { min: -0.90, max: 0.60 }                       // Shade tilt
};

function onPointerDown(event) {
  if (event.button !== 0) return; // Left click only

  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(allLampMeshes, true);

  if (intersects.length > 0) {
    const hitMesh = intersects[0].object;
    let partType = meshToPartType.get(hitMesh);

    // Base can initiate swivel
    if (partType === 'base') partType = 'swivel';

    if (partType) {
      isDraggingPart = true;
      activeDragPart = partType;
      controls.enabled = false;
      canvas.style.cursor = 'grabbing';

      // Seed previous pointer at the exact click position
      prevPointerX = event.clientX;
      prevPointerY = event.clientY;

      event.preventDefault();
    }
  }
}

function onPointerMove(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  if (isDraggingPart) {
    // Per-frame delta: only the movement since the last event, not since drag start.
    // This means hitting a clamp limit never creates accumulated "debt" —
    // as soon as the cursor reverses, movement resumes immediately.
    const dx = event.clientX - prevPointerX;
    const dy = event.clientY - prevPointerY;
    prevPointerX = event.clientX;
    prevPointerY = event.clientY;

    if (activeDragPart === 'swivel') {
      const angle = swivelPivot.rotation.y + dx * 0.008;
      swivelPivot.rotation.y = THREE.MathUtils.clamp(angle, LIMITS.swivel.min, LIMITS.swivel.max);
    } else if (activeDragPart === 'lowerArm') {
      const angle = lowerArmPivot.rotation.x + dy * 0.008;
      lowerArmPivot.rotation.x = THREE.MathUtils.clamp(angle, LIMITS.lowerArm.min, LIMITS.lowerArm.max);
    } else if (activeDragPart === 'upperArm') {
      const angle = upperArmPivot.rotation.x - dy * 0.007;
      upperArmPivot.rotation.x = THREE.MathUtils.clamp(angle, LIMITS.upperArm.min, LIMITS.upperArm.max);
    } else if (activeDragPart === 'shade') {
      const angle = shadePivot.rotation.x - dy * 0.007;
      shadePivot.rotation.x = THREE.MathUtils.clamp(angle, LIMITS.shade.min, LIMITS.shade.max);
    }
    return;
  }

  // Hover cursor feedback
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(allLampMeshes, true);
  if (intersects.length > 0) {
    canvas.style.cursor = 'grab';
  } else {
    canvas.style.cursor = 'default';
  }
}

function onPointerUp() {
  if (isDraggingPart) {
    isDraggingPart = false;
    activeDragPart = null;
    controls.enabled = true;
    canvas.style.cursor = 'grab';
  }
}

window.addEventListener('pointerdown', onPointerDown);
window.addEventListener('pointermove', onPointerMove);
window.addEventListener('pointerup', onPointerUp);

// -----------------------------------------------------------------------------
// 10. FLICKER TIMELINE (4s ON -> 1s OFF -> 6s ON -> 1s OFF)
// -----------------------------------------------------------------------------
function calculateFlicker(t) {
  if (!isLightOn) return 0.0;
  if (!isFlickerEnabled) return 1.0;

  const cycleDuration = 12.0;
  const cycleTime = t % cycleDuration;

  if (cycleTime < 4.0) {
    const hum = Math.sin(t * 18.0) * 0.04;
    return 1.0 + hum;
  } else if (cycleTime < 5.0) {
    const sputter = Math.sin(t * 40.0);
    return sputter > 0.85 ? 0.25 : 0.02;
  } else if (cycleTime < 11.0) {
    const hum = Math.sin(t * 12.0) * 0.03;
    return 1.0 + hum;
  } else {
    const sputter = Math.sin(t * 50.0);
    return sputter > 0.90 ? 0.30 : 0.02;
  }
}

// -----------------------------------------------------------------------------
// 11. INTERACTIVE BUTTON HANDLERS
// -----------------------------------------------------------------------------
// 11. INTERACTIVE BUTTON HANDLERS & MODAL CONTROLS
// -----------------------------------------------------------------------------
const togglePowerBtn = document.getElementById('btn-toggle-power');
const toggleFlickerBtn = document.getElementById('btn-toggle-flicker');
const aboutBtn = document.getElementById('btn-about');
const menuBtn = document.getElementById('btn-menu');
const closeModalBtn = document.getElementById('btn-close-modal');
const aboutModal = document.getElementById('about-modal');

function updatePowerState(newState) {
  isLightOn = newState;
  if (togglePowerBtn) {
    togglePowerBtn.classList.toggle('active', isLightOn);
    const stateText = togglePowerBtn.querySelector('.state-text');
    if (stateText) stateText.textContent = isLightOn ? 'ON' : 'OFF';
  }
}

function updateFlickerState(newState) {
  isFlickerEnabled = newState;
  if (toggleFlickerBtn) {
    toggleFlickerBtn.classList.toggle('active', isFlickerEnabled);
    const stateText = toggleFlickerBtn.querySelector('.state-text');
    if (stateText) stateText.textContent = isFlickerEnabled ? 'ON' : 'OFF';
  }
}

if (togglePowerBtn) {
  togglePowerBtn.addEventListener('click', () => {
    updatePowerState(!isLightOn);
  });
}

if (toggleFlickerBtn) {
  toggleFlickerBtn.addEventListener('click', () => {
    updateFlickerState(!isFlickerEnabled);
  });
}

// Modal Drawer Controls
function openModal() {
  if (aboutModal) aboutModal.classList.remove('hidden');
}

function closeModal() {
  if (aboutModal) aboutModal.classList.add('hidden');
}

if (menuBtn) menuBtn.addEventListener('click', openModal);
if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
if (aboutModal) {
  aboutModal.addEventListener('click', (e) => {
    if (e.target === aboutModal) closeModal();
  });
}

// -----------------------------------------------------------------------------
// 12. ANIMATION & LIVE BEAM TRACKING
// -----------------------------------------------------------------------------
const clock = new THREE.Clock();
const tempBulbWorldPos = new THREE.Vector3();
const tempBellWorldPos = new THREE.Vector3();
const tempRimWorldPos = new THREE.Vector3();
const tempBeamDir = new THREE.Vector3();

function animate() {
  requestAnimationFrame(animate);

  const elapsedTime = clock.getElapsedTime();
  const flicker = calculateFlicker(elapsedTime);

  // Dynamic real-time light steering
  if (bulbMesh && lampPointLight && lampSpotLight) {
    bulbMesh.getWorldPosition(tempBulbWorldPos);
    lampPointLight.position.copy(tempBulbWorldPos);
    lampSpotLight.position.copy(tempBulbWorldPos);

    // Use the mathematically correct local direction of the shade cone (38-deg tilt)
    // and transform it by the shadePivot's absolute world rotation.
    // This perfectly synchronizes the light beam with the physical geometry,
    // avoiding any GLTF mesh origin offsets.
    tempBeamDir.set(0, -0.6157, -0.7880);
    tempBeamDir.applyQuaternion(shadePivot.getWorldQuaternion(new THREE.Quaternion())).normalize();

    // Intersect shade beam with table plane (Y = 0)
    // Clamp effective beam downward vector to ensure pool remains naturally anchored on the desk
    const effectiveBeamY = Math.min(tempBeamDir.y, -0.22);
    const t = Math.min(-tempBulbWorldPos.y / effectiveBeamY, 4.2);

    const targetX = THREE.MathUtils.clamp(tempBulbWorldPos.x + tempBeamDir.x * t, -5.5, 5.5);
    const targetZ = THREE.MathUtils.clamp((tempBulbWorldPos.z + tempBeamDir.z * t) - 0.4, -4.0, 4.0);

    // Physically intuitive pool scaling based on lamp height
    const poolScale = THREE.MathUtils.clamp(tempBulbWorldPos.y * 0.50, 0.60, 1.35);
    poolMesh.scale.set(poolScale, poolScale, poolScale);

    lampSpotLight.target.position.set(targetX, 0.0, targetZ);
    poolMesh.position.set(targetX, 0.002, targetZ);
    poolMesh.visible = isLightOn;

    // Intensity modulation
    lampPointLight.intensity = 1.5 * flicker;
    lampSpotLight.intensity = 6.0 * flicker;
    if (bulbMaterial) {
      bulbMaterial.emissiveIntensity = 2.0 * flicker;
    }
    poolMat.opacity = THREE.MathUtils.clamp(0.85 / (poolScale * 0.9), 0.35, 0.90) * flicker;
  }

  controls.update();
  composer.render();
}

animate();

// -----------------------------------------------------------------------------
// 13. RESPONSIVE RESIZE
// -----------------------------------------------------------------------------
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  composer.setSize(window.innerWidth, window.innerHeight);
});
