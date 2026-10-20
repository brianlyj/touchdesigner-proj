# Progress slides

Black 16:9 presentation, 9 slides, prepared on 16 October 2026 using the implementation and recorded tests from 13 October 2026.

- **Anamorphic_Fluid_Room_Progress.slides.md** is the editable source, with Marp-style frontmatter, embedded styling, HTML layout blocks and speaker notes. Images reference `../assets/`, so keep the source in this repository's folder structure.
- **Anamorphic_Fluid_Room_Progress.html** is a self-contained presentation with its images embedded. Share this single file and open it in a desktop browser. Use the arrow keys or the navigation buttons, **F** for fullscreen and **N** for speaker notes.
- **Anamorphic_Fluid_Room_Progress.pdf** is a self-contained version for easy viewing and sharing. It contains the slides, without speaker notes.

The deck uses actual prototype captures, identifies the physical installation work still outstanding and keeps test conditions with the reported results. Repository links require access to the private GitHub repository.

To regenerate HTML and PDF after editing the Markdown, run `node tools/render_progress_slides.mjs` from the project root. The renderer needs Node.js, the `marked` and `playwright` packages, and Chrome. It also supports the installed Codex dependency bundle. Set `CODEX_RUNTIME_NODE_MODULES` to an alternative dependency directory if needed, or `SLIDES_BROWSER=msedge` to use Edge. It writes temporary rendering checks to `output/playwright/progress-slides/`.
