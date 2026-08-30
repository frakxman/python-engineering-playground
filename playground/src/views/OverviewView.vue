<template>
  <main class="overview-page">
    <section class="hero">
      <p class="eyebrow">PHOENIX · PYTHON ENGINEERING</p>

      <h1>
        Learn Python
        <span>by building systems.</span>
      </h1>

      <p class="hero-description">
        A hands-on engineering playground focused on Python, APIs,
        automation, architecture, and production-oriented practices.
      </p>
    </section>

    <section class="section">
      <div class="section-heading">
        <p class="eyebrow">CONCEPTS</p>
        <h2>Engineering foundations</h2>
      </div>

      <div class="concept-grid">
        <article class="card">
          <span class="card-number">01</span>

          <h3>Architecture</h3>

          <p>
            Separation of responsibilities, modularity, and maintainable
            application structure.
          </p>
        </article>

        <article class="card">
          <span class="card-number">02</span>

          <h3>APIs</h3>

          <p>
            Build and consume APIs using Python, FastAPI, validation,
            and typed contracts.
          </p>
        </article>

        <article class="card">
          <span class="card-number">03</span>

          <h3>Automation</h3>

          <p>
            Turn repetitive tasks into reliable and reusable engineering
            tools.
          </p>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <p class="eyebrow">LABS</p>
        <h2>Projects</h2>
      </div>

      <div class="labs-list">
        <RouterLink
          to="/labs/system-information"
          class="lab-card"
        >
          <div>
            <span class="status">IN PROGRESS</span>

            <h3>System Information Inspector</h3>

            <p>
              A Python utility and FastAPI service for inspecting the
              current system environment.
            </p>

            <div class="lab-tags">
              <span>Python</span>
              <span>FastAPI</span>
              <span>API</span>
            </div>
          </div>

          <span class="arrow">→</span>
        </RouterLink>

        <RouterLink
          to="/labs/file-organizer"
          class="lab-card"
        >
          <div>
            <span class="status">IN PROGRESS</span>

            <h3>File Organizer</h3>

            <p>
              A production-minded CLI tool for automatically organizing
              files using configurable rules.
            </p>

            <div class="lab-tags">
              <span>Python</span>
              <span>CLI</span>
              <span>Automation</span>
            </div>
          </div>

          <span class="arrow">→</span>
        </RouterLink>
      </div>
    </section>

    <footer>
      <span>PYTHON · ENGINEERING PLAYGROUND</span>
      <span>PHOENIX ENGINEERING PLAYGROUND</span>
    </footer>
  </main>
</template>
