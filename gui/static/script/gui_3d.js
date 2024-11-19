import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.outputColorSpace = THREE.SRGBColorSpace;

renderer.setSize(500, 500);
renderer.setClearColor("white");
renderer.setPixelRatio(window.devicePixelRatio);

renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const threeDHtml = document.getElementById("model")
threeDHtml.appendChild(renderer.domElement);

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(45, 500 / 500, 1, 1000);
camera.position.set(0, 5, 11);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.enablePan = false;
controls.minDistance = 5;
controls.maxDistance = 20;
controls.minPolarAngle = 0.5;
controls.maxPolarAngle = 1.5;
controls.autoRotate = false;
controls.target = new THREE.Vector3(0, 1, 0);
controls.update();

const groundGeometry = new THREE.PlaneGeometry(20, 20, 32, 32);
groundGeometry.rotateX(-Math.PI / 2);
const groundMaterial = new THREE.MeshStandardMaterial({
  color: 0x555555,
  side: THREE.DoubleSide
});
const groundMesh = new THREE.Mesh(groundGeometry, groundMaterial);
groundMesh.castShadow = false;
groundMesh.receiveShadow = true;
scene.add(groundMesh);

const spotLight = new THREE.SpotLight(0xffffff, 3000, 100, 0.22, 1);
spotLight.position.set(0, 25, 0);
spotLight.castShadow = true;
spotLight.shadow.bias = -0.0001;
scene.add(spotLight);
let car;
const loader = new GLTFLoader().setPath('../static/models/dodge/');
loader.load('scene.gltf', (gltf) => {
  console.log('loading model');
  car = gltf.scene;

  car.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });

  car.position.set(0, 1.05, 0);
  scene.add(car);

  document.getElementById('progress-container').style.display = 'none';
}, (xhr) => {
  console.log(`loading ${xhr.loaded / xhr.total * 100}%`);
}, (error) => {
  console.error(error);
});

window.addEventListener('resize', () => {
  camera.aspect = 500 / 500;
  camera.updateProjectionMatrix();
  renderer.setSize(500, 500);
});
let pitch = 34;
let yaw = 213;
let roll = 15;
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  /* const timer = Date.now() * 0.0001; */
  if (car) {
    car.rotation.x = pitch * (Math.PI/180); /* pitch */
    car.rotation.y = yaw * (Math.PI/180); /* Yaw (i think we won't need it) */
    car.rotation.z = roll * (Math.PI/180); /* roll */
  }
  renderer.render(scene, camera);
}

animate();