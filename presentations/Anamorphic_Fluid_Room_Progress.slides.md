---
marp: true
theme: default
size: 16:9
paginate: true
backgroundColor: '#000000'
color: '#f3f4f5'
title: Anamorphic Fluid Room — Progress Review
description: A voice-responsive projection prototype in TouchDesigner and Blender
style: |
  section { box-sizing: border-box; width: 1280px; height: 720px; padding: 52px 64px 48px; background: #000 !important; color: #f3f4f5; font: 25px/1.35 'Segoe UI', Arial, sans-serif; position: relative; display: flex; flex-direction: column; overflow: hidden; }
  h1, h2, h3, p, ul, ol, table, figure { margin: 0; }
  h1, h2 { font-weight: 600; letter-spacing: -1.8px; line-height: 1.07; }
  h1 { font-size: 68px; }
  h2 { font-size: 48px; margin-bottom: 26px; }
  h3 { font-size: 29px; font-weight: 600; margin-bottom: 12px; }
  p { margin-bottom: 18px; }
  a { color: #86e8e3; text-decoration: none; }
  strong { font-weight: 600; color: #fff; }
  ul, ol { padding-left: 28px; }
  li { margin: 0 0 15px; padding-left: 6px; }
  code { font: 0.88em Consolas, monospace; color: #c7f2ef; background: transparent; }
  img { max-width: 100%; object-fit: contain; }
  .muted, figcaption { color: #aeb7bd; }
  .lead { font-size: 29px; color: #c2c9ce; max-width: 960px; }
  .eyebrow { font-size: 19px; letter-spacing: 2px; text-transform: uppercase; color: #9fb7be; }
  .note { font-size: 19px; line-height: 1.35; color: #aeb7bd; margin-top: auto; max-width: 1080px; }
  .columns { display: grid; grid-template-columns: 1fr 1fr; gap: 44px; align-items: start; }
  .split { display: grid; grid-template-columns: 0.85fr 1.35fr; gap: 38px; align-items: center; flex: 1; }
  .split.image-left { grid-template-columns: 0.9fr 1.1fr; }
  .split .room { width: 100%; }
  .picture-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 22px; }
  .picture-pair img { width: 100%; height: 306px; }
  figcaption { font-size: 20px; margin-top: 13px; line-height: 1.3; }
  .square { height: 445px; width: 445px; }
  .cover { justify-content: center; padding-top: 40px; }
  .cover h1 { width: 620px; font-size: 76px; line-height: 1.01; position: relative; z-index: 1; }
  .cover .eyebrow { margin-bottom: 26px; position: relative; z-index: 1; }
  .cover .subtitle { width: 465px; font-size: 28px; color: #c6cdd2; margin-top: 28px; position: relative; z-index: 1; }
  .cover .cover-art { position: absolute; width: 730px; right: -24px; top: 142px; }
  .cover .date { position: absolute; bottom: 57px; font-size: 21px; color: #aeb7bd; }
  .cover .image-label { position: absolute; bottom: 89px; right: 64px; font-size: 17px; color: #aeb7bd; }
  table { width: 100%; border-collapse: collapse; background: transparent; font-size: 24px; }
  th { color: #9eafb7; font-size: 18px; text-transform: uppercase; letter-spacing: 1px; font-weight: 500; }
  th, td { border: none; border-bottom: 1px solid #30383e; text-align: left; padding: 17px 18px 17px 0; vertical-align: top; background: #000; }
  tr { background: #000 !important; }
  .pipeline td:first-child { color: #6de0da; width: 60px; font-size: 28px; }
  .pipeline td:nth-child(2) { width: 285px; font-weight: 600; }
  .pipeline td:last-child { color: #c1c9ce; }
  .moods td:first-child { width: 160px; font-weight: 600; font-size: 28px; }
  .moods td { padding-top: 24px; padding-bottom: 24px; }
  .moods .calm { color: #63e1e0; }
  .moods .wonder { color: #c3a5ff; }
  .moods .joy { color: #ffac8a; }
  .moods .intensity { color: #ee789e; }
  .big { font-size: 80px; font-weight: 600; letter-spacing: -3px; line-height: 1.03; color: #83e6df; }
  .metric-label { font-size: 22px; color: #aeb7bd; margin-top: 9px; }
  .idle-stats { display: flex; gap: 44px; margin-bottom: 30px; }
  .idle-stats .big { font-size: 62px; }
  .chart { padding-top: 12px; }
  .bar-caption { display: flex; justify-content: space-between; font-size: 23px; margin: 14px 0 9px; }
  .bar-track { height: 38px; background: #182026; margin-bottom: 30px; }
  .bar { height: 100%; background: #769098; }
  .bar.new { background: #78e1da; }
  .chart-label { font-size: 20px; color: #b6c0c6; margin-top: 22px; }
  .performance .big { font-size: 100px; margin: 3px 0 0; }
  .performance table { margin-top: 8px; font-size: 24px; }
  .performance th, .performance td { padding: 15px 20px 15px 0; }
  .agenda { display: grid; grid-template-columns: 55px 1fr; gap: 18px 24px; margin-top: 12px; }
  .agenda .number { font-size: 34px; color: #75ddd7; line-height: 1.2; }
  .agenda p { font-size: 24px; color: #bac4cb; margin-bottom: 0; }
  .agenda h3 { margin-bottom: 5px; }
  .closing { justify-content: center; align-items: center; text-align: center; }
  .closing h2 { font-size: 88px; margin: 0; }
  .closing .page-number, .closing::after { display: none; }
  .repo { margin-top: 22px; font-size: 23px; }
  section::after { font-size: 16px; color: #7c8b94; right: 26px; bottom: 16px; }
---

<!-- _class: cover -->

<p class="eyebrow">Prototype progress</p>

# Anamorphic<br>Fluid Room

<p class="subtitle">A room-scale image that responds to voice and keeps moving through silence.</p>

<img class="cover-art" src="../assets/refined_room.png" alt="Virtual room with a red and pale fluid projection and a neutral mannequin">

<p class="image-label">Intensity palette audition in TouchDesigner</p>
<p class="date">16 October 2026</p>

<!--
Speaker notes:
This is a progress review of the working virtual prototype, not a photograph of a physical projection installation. The cover shows the Intensity palette audition. Recorded implementation and test evidence dates from 13 October 2026.
Sources: ../README.md; ../assets/refined_room.png; repository commit 8a322e5372098724cccbc71efe64deabe0b8b952.
-->

---

## The virtual room is working

<div class="split">
<div>

- **6 × 5 × 3 metre room** with a sharp corner, inward curve and protrusion.
- **Movable mannequin** with eye-level and orbit inspection.
- **Live microphone input** changes the fluid and its palette.
- **Editable Blender asset** accompanies the native TD project.

</div>
<figure>
<img class="room" src="../assets/delivered_room.png" alt="Blue fluid imagery projected across the virtual room with a mannequin in the foreground">
<figcaption>Third-person cutaway reveals the geometry and viewing position.</figcaption>
</figure>
</div>

<p class="note">The current prototype previews ideal mapped imagery. Physical projector calibration comes later.</p>

<!--
Speaker notes:
The cutaway is for inspection. The scene still models an enclosed room. The live room uses native procedural TouchDesigner surfaces so dimensions remain adjustable. Blender and glTF use the same geometry definition. Arbitrary Blender mesh edits do not sync automatically into TD.
Sources: ../README.md; ../src/room_geometry.py; ../assets/blender_validation.json; ../assets/delivered_room.png.
-->

---

## Alignment depends on the sweet spot

<p class="lead">One fixed projection camera aligns the image across uneven surfaces.</p>

<div class="picture-pair">
<figure>
<img src="../assets/alignment_sweet.png" alt="Checkerboard appearing as a regular grid from the designated sweet spot">
<figcaption><strong>At the sweet spot</strong><br>The checkerboard reads as a continuous grid.</figcaption>
</figure>
<figure>
<img src="../assets/alignment_off_axis.png" alt="The same checkerboard appearing distorted after moving away from the sweet spot">
<figcaption><strong>After moving away</strong><br>The room geometry becomes visible through distortion.</figcaption>
</figure>
</div>

<p class="note">Moving the person leaves projection alignment fixed. “Set sweet spot here” re-anchors the image without resetting the fluid.</p>

<!--
Speaker notes:
The shader derives projective coordinates from each surface's world position. A reference depth map excludes room surfaces hidden from the sweet spot. A staged pixel check found 100% agreement with the intended checker at sampled pixels at the sweet spot and after re-anchoring, versus 57.4% off axis. This is a virtual image comparison, not a physical calibration-accuracy measurement.
Sources: ../assets/alignment_validation.json; ../assets/alignment_sweet.png; ../assets/alignment_off_axis.png; ../src/room_pixel.glsl.
-->

---

## The audio-to-image pipeline

<table class="pipeline">
<thead><tr><th>Step</th><th>Stage</th><th>What it contributes</th></tr></thead>
<tbody>
<tr><td>01</td><td>Microphone analysis</td><td>RMS loudness and confidence-filtered fundamental pitch.</td></tr>
<tr><td>02</td><td>Emotional mapping</td><td>Continuous weights for Calm, Wonder, Joy and Intensity.</td></tr>
<tr><td>03</td><td>GPU fluid simulation</td><td>Voice adds force and ink to persistent idle circulation.</td></tr>
<tr><td>04</td><td>Colour mapping</td><td>The palette changes across existing pigment as well as new ink.</td></tr>
<tr><td>05</td><td>Room projection</td><td>The sweet spot aligns imagery. Independent cameras inspect it.</td></tr>
</tbody>
</table>

<p class="note">TouchDesigner embeds the shaders, Python callbacks and interface in one working TOE file.</p>

<!--
Speaker notes:
The project separates audio, emotion, fluid, room, projection, viewing and interface components. YIN estimates pitch rather than selecting the loudest FFT bin. The GPU solver uses a fixed 1/60-second step per project frame, floating-point textures, 12 viscosity iterations and 24 pressure iterations. The existing TDMCP connection allowed Python to build and inspect real TD operators. TDMCP and Codex are not required to run the saved artwork.
Sources: ../src/audio_emotion.py; ../src/runtime.py; ../tools/build_td_room.py; ../tools/refine_fluid.py; ../README.md.
-->

---

## Mood follows the character of the voice

<table class="moods">
<thead><tr><th>Artistic mood</th><th>Acoustic tendency</th><th>Palette direction</th><th>Movement direction</th></tr></thead>
<tbody>
<tr><td class="calm">Calm</td><td>Quiet, lower pitch</td><td>Deep blue and teal</td><td>Gentle circulation</td></tr>
<tr><td class="wonder">Wonder</td><td>Quiet, higher pitch</td><td>Indigo and lavender</td><td>Delicate curls</td></tr>
<tr><td class="joy">Joy</td><td>Louder, higher pitch</td><td>Coral and gold</td><td>Faster swirls</td></tr>
<tr><td class="intensity">Intensity</td><td>Louder, lower pitch</td><td>Burgundy and red</td><td>Denser streams</td></tr>
</tbody>
</table>

<p class="note">These names describe the artwork’s expression. They do not identify the speaker’s emotions. Neighbouring moods blend continuously.</p>

<!--
Speaker notes:
Loudness and logarithmic pitch define the mood coordinates. The latest palette uses perceptual OKLab mixing and pale-ink concentration. Movement descriptions express the intended character of the shared continuous solver, rather than four separate simulations. The Intensity treatment moved toward red and pale ink during the fluid refinement.
Sources: ../src/audio_emotion.py; ../src/palette.glsl; ../src/force.glsl; ../README.md.
-->

---

## The fluid now holds finer detail

<div class="split image-left">
<figure>
<img class="square" src="../assets/refined_intensity.png" alt="Detailed red and pale fluid with rolling eddies and thin layered trails">
<figcaption>Refined solver capture in Intensity audition.</figcaption>
</figure>
<div>

### Recent improvements

- Curl forces help retain rolling eddies.
- Corrected pigment transport preserves thin trails.
- Pale ink folds into coloured pigment.
- Viscosity stays separate from drag and colour fading.

</div>
</div>

<!--
Speaker notes:
The earlier prototype produced broad, smooth colour fields. The refinement added vorticity confinement, multiscale stirring, pressure history and locally clamped MacCormack pigment transport. The visual direction draws from the Refractiv reference shared during development. This is an independently implemented approximation of that direction, not an exact reproduction.
Sources: ../tools/refine_fluid.py; ../src/pigment_correct.glsl; ../src/vorticity.glsl; ../assets/refined_intensity.png.
Visual reference: https://www.instagram.com/p/DMsZkRgsG5n/?img_index=1
-->

---

<!-- _class: performance -->

## Measured prototype performance

<div class="columns">
<div>
<div class="big">≈60 FPS</div>
<p class="metric-label">512 × 512 fluid on an RTX 4060 Laptop GPU</p>

<table>
<thead><tr><th>View</th><th>Average</th><th>Minimum*</th></tr></thead>
<tbody>
<tr><td>Comparison</td><td>60.02</td><td>59.32</td></tr>
<tr><td>First person</td><td>60.08</td><td>59.95</td></tr>
</tbody>
</table>
</div>
<div>

### Recorded checks

- **65.6 seconds** of below-gate idle with finite, bounded fluid data.
- **Tone tests** resolve within one semitone across the tested speech range.
- **Higher viscosity** reduces velocity-field variation by about 29%.
- **Camera movement** preserves the fixed projection anchor.

</div>
</div>

<p class="note">Recorded 13 Oct 2026 in TouchDesigner 2025.33230. *Minimum sampled, smoothed project FPS. These short runs do not establish installation endurance or performance with physical projector outputs.</p>

<!--
Speaker notes:
The refined idle report contains 64 samples. Comparison: 33 samples, mean 60.0233 FPS, minimum 59.3204 FPS. First person: 31 samples, mean 60.0844 FPS, minimum 59.9538 FPS. Mean pigment density ranged roughly 0.24–0.48. Pressure projection reduced divergence on every sample, averaging around 13.7%. The viscosity comparison held the test field and drag constant and measured spatial gradient RMS. Speech-tone checks used synthetic harmonic signals at three levels. In-room human humming remains a calibration check. Native saves and live operator checks passed, while a final independently confirmed cold reopen and longer unattended run remain sensible handoff checks.
Sources: ../assets/refined_fluid_validation.json; ../assets/speech_colour_validation.json; ../assets/viscosity_validation.json; ../assets/alignment_validation.json; ../assets/speech_colour_delivery.json.
-->

---

## Next checks on a real site

<div class="agenda">
<div class="number">01</div><div><h3>Measured room geometry</h3><p>Replace the example room with a clean, dimensioned mesh and agree on the intended viewing position.</p></div>
<div class="number">02</div><div><h3>Voices in the actual space</h3><p>Calibrate the noise floor, try different speakers and test how room acoustics affect pitch confidence.</p></div>
<div class="number">03</div><div><h3>Projector coverage and calibration</h3><p>Check throw, surface brightness, overlapping coverage and the shadows cast by visitors.</p></div>
<div class="number">04</div><div><h3>Installation endurance</h3><p>Confirm a cold reopen, microphone recovery and longer unattended operation with the final output setup.</p></div>
</div>

<p class="note">Physical projection and real-person tracking remain outside this virtual prototype.</p>

<!--
Speaker notes:
These are proposed next checks, not completed work. The saved native project, editable Blender file, glTF companion and source code already exist. The current person is a manually controlled virtual mannequin. A Gaussian splat could add visual context for a site, while clean scaled meshes remain useful for projection and collision surfaces.
Sources: ../README.md; project scope and acceptance plan in the development conversation.
-->

---

<!-- _class: closing -->
<!-- _paginate: false -->

## Live Demo
