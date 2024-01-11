import * as THREE from 'https://threejsfundamentals.org/threejs/resources/threejs/r132/build/three.module.js';

    const cursor = document.getElementById('cursor');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const holographicMaterial = new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 1.0 },
      },
      vertexShader: `
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform float time;
        varying vec2 vUv;
        void main() {
          vec2 uv = vUv;
          uv.x += time * 0.1; // Adjust the speed of background movement
          vec3 color = vec3(0.5 + 0.5 * sin(time), 0.5 + 0.5 * cos(time), 1.0);
          vec3 gradientColor = mix(vec3(0.0, 0.0, 1.0), color, uv.y);
          gl_FragColor = vec4(gradientColor, 1.0);
        }
      `,
    });

    const particleMaterial = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 0.2,
      map: new THREE.TextureLoader().load('https://threejsfundamentals.org/threejs/resources/images/w.png'),
      blending: THREE.AdditiveBlending,
      transparent: true,
    });

    const cubes = [];
    const particles = new THREE.Group();
    scene.add(particles);

    function createCube() {
      const maxSize = 10;
      const cubeSize = Math.random() * (maxSize - 2) + 2; // Random size between 2 and maxSize

      const cubeGeometry = new THREE.BoxGeometry(cubeSize, cubeSize, cubeSize);
      const cubeMesh = new THREE.Mesh(cubeGeometry, holographicMaterial);
      scene.add(cubeMesh);
      resetCubePosition(cubeMesh);
      cubes.push(cubeMesh);

      // Set initial scale to make it appear small
      cubeMesh.scale.set(0.1, 0.1, 0.1);
    }

    function resetCubePosition(cube) {
      const sectionWidth = window.innerWidth / 3; // Divide the width into three equal sections
      const spawnDistance = 50; // Set a distance for spawning cubes

      const section = Math.floor(Math.random() * 3); // Choose one of the three sections randomly

      if (section === 0) {
        // Left section
        cube.position.x = -spawnDistance;
      } else if (section === 1) {
        // Center section
        cube.position.x = 0;
      } else {
        // Right section
        cube.position.x = spawnDistance;
      }

      cube.position.y = Math.random() * spawnDistance * 2 - spawnDistance;
      cube.position.z = -spawnDistance; // Ensure cubes are generated at one end
    }

    function createParticle(position) {
      const particleGeometry = new THREE.BufferGeometry();
      const vertices = [];

      for (let i = 0; i < 100; i++) {
        const x = (Math.random() - 0.5) * 2;
        const y = (Math.random() - 0.5) * 2;
        const z = (Math.random() - 0.5) * 2;

        vertices.push(x, y, z);
      }

      particleGeometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));

      const particle = new THREE.Points(particleGeometry, particleMaterial);
      particle.position.copy(position);
      particles.add(particle);
    }

    function detectCollisions() {
      for (let i = 0; i < cubes.length; i++) {
        for (let j = i + 1; j < cubes.length; j++) {
          const cube1 = cubes[i];
          const cube2 = cubes[j];

          const distance = cube1.position.distanceTo(cube2.position);

          if (distance < cube1.scale.x + cube2.scale.x) {
            // Collision detected
            createParticle(cube1.position);
            createParticle(cube2.position);
          }
        }
      }
    }

    function animate() {
      requestAnimationFrame(animate);

      cubes.forEach((cube) => {
        cube.rotation.x += 0.001; // Adjusted rotation speed
        cube.rotation.y += 0.001; // Adjusted rotation speed

        // Adjusted movement speed and added logic to reposition cubes when out of bounds
        cube.position.z += 0.01; // Reduced the speed (adjust this value as needed)

        // Gradually increase the size as it moves closer
        cube.scale.x += 0.0005;
        cube.scale.y += 0.0005;
        cube.scale.z += 0.0005;

        // Check and reset position if cube is out of bounds
        if (cube.position.z > 25) {
          resetCubePosition(cube);
          // Reset scale when cube is repositioned
          cube.scale.set(0.1, 0.1, 0.1);
        }
      });

      detectCollisions();

      holographicMaterial.uniforms.time.value += 0.01;

      renderer.render(scene, camera);
    }

    document.addEventListener('mousemove', (e) => {
      const x = e.clientX - cursor.offsetWidth / 2;
      const y = e.clientY - cursor.offsetHeight / 2;
      cursor.style.transform = 'translate(${x}px, ${y}px)';
    });

    window.addEventListener('resize', () => {
      const newWidth = window.innerWidth;
      const newHeight = window.innerHeight;

      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();

      renderer.setSize(newWidth, newHeight);
    });

    animate();

    function clearInput() {
      document.getElementById('userInput').value = '';
    }

    function scan() {
      console.log('Scanning...');
    }

    // Create initial cubes
    for (let i = 0; i < 5; i++) {
      createCube();
    }

    // Create new cubes every 3 seconds
    setInterval(createCube, 3000);