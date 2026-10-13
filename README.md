# Anamorphic Fluid Room

A working TouchDesigner installation prototype with a metre-scale Blender room and mannequin. The projection is an ideal virtual preview: one image spans a corner, an inward-curved wall, and a protrusion when seen from a fixed sweet spot.

## Open the project

Open **`Anamorphic_Fluid_Room.toe`** in TouchDesigner 2025.33230 or newer. Open the viewer of `/fluid_room`, or press **F1** for its interface. Escape returns from Perform mode. The saved default is the microphone source, 512 × 512 simulation, and side-by-side views. No microphone playback or audio output operator is present.

The original `Anamorphic_Ring.toe` is preserved. Its network is also retained, with cooking disabled, inside the new project. TouchDesigner may display an incremented `.1.toe` project name; the explicitly named `Anamorphic_Fluid_Room.toe` is the delivery file.

If the editor opens inside `/anamorphic`, press **U** over the network to return to the root and enter **`/fluid_room`** for the new system. The repository tracks the canonical fluid-room and ring-demo saves. Automatic numbered saves, development checkpoints, Python caches, and local MCP runtime logs remain local.

Files:

- `Anamorphic_Fluid_Room.blend`: editable named room surfaces and neutral mannequin.
- `assets/room_and_person.glb`: packaged glTF exchange asset.
- `assets/geometry_contract.json`: units and geometry contract.
- `src/`: readable source of the embedded Python and GLSL.
- `tools/build_td_room.py`: reproducible native-network builder, executed inside TouchDesigner.
- `assets/*validation.json`: measured acceptance evidence.

The TOE embeds its runtime, shaders, geometry generator, and callbacks. It does not need an external Python installation or Blender running. The Blender file and GLB are editable/exchange companions; the native TD SOP surfaces use the same mesh generator so the room dimensions remain adjustable. Editing the Blender mesh does **not** automatically replace TD's procedural room.

## Controls

The right-hand buttons select control pages. The buttons below the image switch views, re-anchor, audition silence, or toggle the clearly labelled synthetic voice source.

| Page | Controls |
| --- | --- |
| Experience | First person / third person / comparison; ink / checkerboard / circle; source; audition silence; pause; reset fluid; cutaway; set sweet spot here |
| Voice | Microphone device, input gain, noise gate, full-response level, overall audio sensitivity, independent colour sensitivity, palette smoothing, noise-floor calibration, pitch mapping range, restart synthetic voice |
| Fluid | 512 default / 256 performance; saturation, brightness, viscosity, force and injection multipliers; curl strength, filament detail, surface sheen and palette audition |
| Room | Width, depth, height, inward curve depth, protrusion depth, all in metres |
| Person | Position, heading, look pitch, eye height, FOV, walk speed, orbit angle/distance/height, reset person |
| Anchor | Independent sweet-spot position, heading, pitch, horizontal FOV, aspect |
| Emitters | Three emitter positions, strengths, and radii in normalized simulation coordinates |

**Navigation:** Hover/focus the image and use WASD to walk. Drag the image to look in first-person/comparison mode, or orbit in third-person mode. Numeric controls are also available. Movement is constrained by the room perimeter, curved wall and protrusion. The mannequin is excluded from first-person rendering. Third-person cutaway hides the ceiling, left wall and back wall for inspection.

**Set sweet spot here** copies the person's eye pose and FOV, with the eye view's 16:9 aspect. It leaves the running fluid intact. Moving the person, changing the orbit or switching views leaves the anchor fixed. Reset person does not re-anchor automatically.

The last saved inspection pose and live control settings are retained, including any audition controls. Turn **Audition silence** off to resume microphone response, and set **Fluid → Palette audition → Follow voice** for voice-driven colour. To return to the original aligned view, use **Person → Reset person**, then **Set sweet spot here**. `assets/saved_controls.json` records the delivered settings.

Comparison displays both full 16:9 views with letterboxing; the image is not stretched. View renders are 960 × 540. A 1360 × 840 native panel contains the controls.

## Microphone calibration

1. Select **Microphone** as the source and choose the intended device on the Voice page. The status text reports the active device or an unavailable-device fallback.
2. Turn **Audition silence** off. Leave input gain at 0 dB initially.
3. Keep the room quiet and press **Calibrate noise floor (2 s)**. The gate is set 6 dB above the 90th percentile of measured ambient levels. Recalibrate when the room or device changes.
4. Speak at an ordinary level. Adjust gain and the full-response dBFS value so normal speech has useful movement without spending all its time at maximum loudness. The on-screen meter and numerical dBFS display show the input.
5. Hum a sustained note to inspect pitch and confidence. Unpitched speech keeps the last reliable pitch; loudness still responds.
6. Use **Audition silence** to feed a nonzero level 10 dB below the current gate. Use **Synthetic demo** to test without a microphone. Restart synthetic voice resets its repeatable input sequence.

Mic samples are mono at 48 kHz. RMS response uses approximately 30 ms attack and 250 ms release. NumPy YIN analyses a decimated window over 80–1,000 Hz, using a confidence threshold of 0.8. The default **colour/movement mapping spans 85–255 Hz**, logarithmically, to give conversational pitch changes more of the available range. These adjustable endpoints are independent of the detector bounds; tones outside the mapping range stay at its low/high palette endpoint. The combined range is an artistic response range, not a classification of the speaker. The supplied [speaking-frequency reference](https://voicefrequencytest.com/voice-frequency-chart/) informed these defaults. The loudest FFT bin is not used. No audio is recorded to disk.

## Colour and silence

Mood labels describe the artwork, not inferred human emotions. Loudness and pitch form continuous weights:

| Mood | Acoustic tendency | Palette |
| --- | --- | --- |
| Calm | Quiet / lower pitch | Deep blue, teal, cyan |
| Wonder | Quiet / higher pitch | Indigo, lavender, pale pink |
| Joy | Louder / higher pitch | Coral, gold, magenta |
| Intensity | Louder / lower pitch | Burgundy, amber, violet |

**Voice → Colour sensitivity** defaults to **1.8**. It gives ordinary loudness changes more colour response and increases the contrast between neighbouring pitch palettes, while keeping continuous weights. It changes the colour mapping independently of fluid force and injection. A value of 1 restores the linear palette response; higher values give stronger changes. Overall audio sensitivity still controls the general audio response.

**Palette smoothing** defaults to a **one-second time constant** (about 86% of a fixed target change in two seconds). This replaces the previously saved 5.99-second setting. Colours are mixed in OKLab, then applied to advected pigment density and pigment identity. Existing fluid changes colour along with newly injected ink. Confidence filtering, unpitched pitch-hold, and the eight-second Calm return remain active.

The fluid was refined using the supplied [Refractiv visual reference](https://www.instagram.com/p/DMsZkRgsG5n/?img_index=1): rolling billows, thin pigment trails, and pale ink folding into coloured ink. **Fluid → Palette audition → Intensity** previews the red/pale treatment. Return this control to **Follow voice** for the emotional journey. Curl strength changes eddy retention; filament detail changes the injected layers and stirring; surface sheen adds subtle relief from pigment gradients. The default sheen is deliberately restrained.

Idle always supplies 12% force and 8% injection before the user multipliers. After one second below the gate, an eight-second return toward Calm begins. A bounded 20-second breathing cycle modulates the circulation. Moderately high idle viscosity and density-dependent pigment dissipation keep the image alive without accumulating opaque colour. Speech smoothly restores the additional forces; it does not reset simulation buffers.

## Network and simulation

`/fluid_room` contains separate `audio`, `emotion`, `fluid`, `room`, `projection`, `viewing` and `interface` components.

- `audio/microphone`: selected device; runtime analysis is embedded in the root `runtime` and `audio_emotion` DATs.
- `emotion/OUT`: stable channels `loudness`, `pitch_hz`, `pitch_norm`, `pitch_confidence`, `voiced`, `idle_mix`, `calm`, `wonder`, `joy`, `intensity`, plus force/injection/viscosity/onset and diagnostic channels.
- `fluid`: floating-point velocity and three pigment quantities (density, colour identity, pale-ink concentration). Velocity uses semi-Lagrangian advection, multi-scale stirring, curl and bounded vorticity confinement. Pigment uses forward/backward RK2 transport and a locally clamped MacCormack correction to retain filaments. There are 12 Jacobi viscosity iterations and 24 pressure iterations with a previous-frame pressure estimate, followed by pressure projection and solid normal-velocity boundaries. Drag and pigment fading are independent of viscosity.
- `projection`: world-position projection into the sweet-spot basis, equivalent to the camera view/projection transform; reference-depth rejection and frustum clipping; perceptual palette material.
- `viewing`: separate sweet-spot, eye, and orbit cameras. The reference depth excludes the mannequin so this prototype shows ideal mapped imagery.

The simulation takes one fixed **1/60 second** step per rendered project frame. At the measured 60 FPS it runs in real time. If a heavily loaded machine drops to 30 FPS, the fluid slows rather than using an unstable larger step; use the 256 preset. Pause holds the GPU state while camera and audio controls stay available. Reset fluid explicitly resets its feedback textures; view changes and re-anchoring do not.

## Geometry and site preparation

The default room is **6 × 5 × 3 m**, with a 0.4 m inward curve and a 0.55 m protrusion. Mannequin height is 1.76 m; eye height defaults to 1.65 m. Blender uses Z-up; glTF and TD use Y-up. The verified conversion is **Blender `(x, y, z)` → TD/glTF `(x, z, -y)`**, with metre scale 1.0. Surfaces are named `floor`, `ceiling`, `front_wall`, `back_wall`, `left_wall`, `curved_wall`, and `protrusion`.

For a real site, supply a dimensioned `.blend` or clean mesh with known scale, wall names, and proposed viewer/projector locations. A Gaussian splat can help with visual context but is not a replacement for clean projection and collision surfaces. Integrating an arbitrary scanned site mesh is a separate next step.

## Verification

Tested on **NVIDIA GeForce RTX 4060 Laptop GPU, 8 GB**, driver 596.36, TouchDesigner 2025.33230; Blender 5.2.2 LTS.

- The refined solver's 65.6-second idle run used a calibrated gate of approximately −49.89 dBFS and a nonzero input of −59.89 dBFS. All 64 samples were finite; mean pigment density stayed approximately 0.24–0.48 and remained moving. Detailed samples are in `assets/refined_fluid_validation.json`; the earlier solver's baseline report is preserved separately.
- Default 512 quality with the refined solver: approximately **60.02 FPS** average in comparison and **60.08 FPS** in single view; measured minimum smoothed rates were 59.32 and 59.95 FPS respectively. These are project-frame measurements on this machine, not a guarantee for additional outputs or other hardware.
- Harmonic test signals at 110, 220 and 440 Hz, at −48/−30/−12 dB amplitude levels, resolved within about 1.1 cents. Additional 80, 880 and 1,000 Hz tests passed within one semitone. Seeded noise was rejected; sustained harmonic signals and pitch-hold behaviour passed. An in-room human humming check remains part of microphone calibration.
- Speech colour regression checks covered 85/110/150/165/180/220/255/440 Hz tones at three levels, smooth monotonic colour response to pitch and volume, held colour during unpitched input, independent colour gain, and a modelled 60-second below-gate idle return. In the stepped speech test, the palette completed **85%** of its transition after two seconds, versus **27%** with the previous saved settings. See `assets/speech_colour_validation.json`.
- Increasing viscosity reduced the test velocity's spatial variation by approximately **29%**, independently of drag. Pressure projection reduced measured divergence on every refined idle sample, averaging about **13.7%** reduction per step. Pigment/velocity produced no NaNs or infinities.
- Both 512 and 256 presets ran without operator errors. The checkerboard matched its intended screen-space grid at **100% of sampled pixels** both at the original sweet spot and after re-anchoring; moving away reduced agreement to 57.4%. The reference depth was identical before and after person movement. View buttons and keyboard/mouse callbacks were exercised. Images and staged pixel checks are in `assets/`.
- The saved TOE reopened with controls restored, microphone recovered, assets available, and no operator errors. The `.blend` also reopened and its bounding dimensions and mannequin scale were verified.

Physical projector coverage, calibration, brightness, real visitor shadows, occlusion by real people, and live person tracking are outside this virtual version. A single sweet spot is intentional: moving away reveals the anamorphic distortion.

## Existing TouchDesigner MCP

The installed official TDMCP connection is reused at `http://127.0.0.1:13316/mcp`, embedded as `/TDMCP` in the saved project. Open the TOE before using it. `tools/td_client.py` is a small local JSON-RPC client for that existing connection; no replacement MCP server is needed. The project remains usable without Codex or the MCP client.

The bundled [TDMCP](https://github.com/TouchDesigner/TDMCP) component is by **Derivative Inc.** Its upstream license and terms are retained in [tools/LICENSE.md](tools/LICENSE.md), and apply to TDMCP rather than the original artwork and project scripts.

To rebuild from source in this folder, open the preserved ring project with TDMCP active, then execute `tools/build_td_room.py` through the existing `execute_code` tool. To regenerate Blender assets in a separate background process, run Blender with `--background --python tools/create_blender_room.py`. The verification scripts deliberately exercise controls; run them when the interface is not being used for a live demonstration.
