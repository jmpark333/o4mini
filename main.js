// 생성: main.js 작성 2025-04-17 20:23:30
const canvas = document.getElementById('canvas');
const renderer = new THREE.WebGLRenderer({canvas, antialias: true});
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 1, 10000);
camera.position.set(0, 200, 500);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 50;
controls.maxDistance = 2000;

const ambient = new THREE.AmbientLight(0x333333);
scene.add(ambient);
const pointLight = new THREE.PointLight(0xffffff, 2);
pointLight.position.set(0, 0, 0);
scene.add(pointLight);

// 태양
const sunRadius = 20;
const sunGeo = new THREE.SphereGeometry(sunRadius, 32, 32);
const sunMat = new THREE.MeshBasicMaterial({color: 0xffff00});
const sun = new THREE.Mesh(sunGeo, sunMat);
scene.add(sun);

// 행성 데이터
const scale = 50;            // AU 단위를 가시적 거리로 변환
const earthOrbitSec = 60;    // 지구 공전 1주기 시뮬레이션 시간(초)
const planetData = [
  {name:'Mercury', color:0xbfbfbf, size:3,  semiMajor:0.39*scale, eccentricity:0.205, orbitPeriod:88,    rotationPeriod:58.6, moons:0,  features:'극심한 온도 변화'},
  {name:'Venus',   color:0xffcc88, size:7,  semiMajor:0.72*scale, eccentricity:0.0068, orbitPeriod:225,   rotationPeriod:-243, moons:0,  features:'두꺼운 황산 구름'},
  {name:'Earth',   color:0x5599ff, size:8,  semiMajor:1.0*scale,  eccentricity:0.0167, orbitPeriod:365,   rotationPeriod:1,    moons:1,  features:'생명 존재'},
  {name:'Mars',    color:0xff5533, size:6,  semiMajor:1.52*scale, eccentricity:0.0934, orbitPeriod:687,   rotationPeriod:1.03, moons:2,  features:'붉은 모래, 고대 하천'},
  {name:'Jupiter', color:0xffaa33, size:14, semiMajor:5.2*scale,  eccentricity:0.0489, orbitPeriod:4333,  rotationPeriod:0.41, moons:79, features:'대적반'},
  {name:'Saturn',  color:0xddddaa, size:12, semiMajor:9.58*scale, eccentricity:0.0565, orbitPeriod:10759, rotationPeriod:0.45, moons:82, features:'아름다운 고리'},
  {name:'Uranus',  color:0x88ddff, size:10, semiMajor:19.2*scale, eccentricity:0.0472, orbitPeriod:30687, rotationPeriod:-0.72, moons:27, features:'옆으로 기운 자전축'},
  {name:'Neptune', color:0x3366ff, size:10, semiMajor:30.05*scale, eccentricity:0.0086, orbitPeriod:60190, rotationPeriod:0.67, moons:14, features:'강력한 바람'}
];
const planets = [];
planetData.forEach(data => {
  const geo = new THREE.SphereGeometry(data.size, 32, 32);
  const mat = new THREE.MeshPhongMaterial({color: data.color});
  const mesh = new THREE.Mesh(geo, mat);
  scene.add(mesh);
  // 궤도선 생성
  const a = data.semiMajor;
  const b = a * Math.sqrt(1 - data.eccentricity * data.eccentricity); // 수정: 정확한 준최소축 계산, 2025-04-17 20:29:36
  const curve = new THREE.EllipseCurve(0,0,a,b,0,2*Math.PI,false,0);
  const points = curve.getPoints(100);
  const orbitGeo = new THREE.BufferGeometry().setFromPoints(points.map(p => new THREE.Vector3(p.x, 0, p.y)));
  const orbitMat = new THREE.LineBasicMaterial({color:0x444444});
  const orbitLine = new THREE.Line(orbitGeo, orbitMat);
  orbitLine.rotation.x = Math.PI/2;
  scene.add(orbitLine);
  planets.push({mesh, data});
});

// 정보 팝업
const infoDiv = document.getElementById('info');
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  const elapsed = clock.getElapsedTime();
  let nearest = null;
  let minDist = Infinity;
  planets.forEach(p => {
    const {mesh, data} = p;
    const a = data.semiMajor;
    const b = a * Math.sqrt(1 - data.eccentricity * data.eccentricity); // 수정: 정확한 준최소축 계산, 2025-04-17 20:29:36
    const periodSec = earthOrbitSec * data.orbitPeriod / 365;
    const angle = elapsed * 2 * Math.PI / periodSec;
    const x = a * Math.cos(angle);
    const z = b * Math.sin(angle);
    mesh.position.set(x, 0, z);
    const dist = camera.position.distanceTo(mesh.position);
    const threshold = data.size * 20; // 수정: 정보 팝업 거리 임계값 확대, 2025-04-17 20:29:36
    if (dist < threshold && dist < minDist) {
      nearest = p;
      minDist = dist;
    }
  });
  if (nearest) {
    showInfo(nearest);
  } else {
    infoDiv.className = 'hidden';
  }
  renderer.render(scene, camera);
}

function showInfo(p) {
  const {data, mesh} = p;
  const vec = mesh.position.clone().project(camera);
  const x = (vec.x * 0.5 + 0.5) * window.innerWidth;
  const y = (-vec.y * 0.5 + 0.5) * window.innerHeight;
  infoDiv.style.left = x + 'px';
  infoDiv.style.top = y + 'px';
  infoDiv.innerHTML = `<strong>${data.name}</strong><br>
    궤도 장반경: ${(data.semiMajor/scale).toFixed(2)} AU<br>
    자전주기: ${data.rotationPeriod} 일<br>
    위성 개수: ${data.moons}<br>
    특징: ${data.features}`;
  infoDiv.className = 'visible';
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}
window.addEventListener('resize', onWindowResize);
animate();
