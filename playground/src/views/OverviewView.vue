<template>
  <div class="playground">
    <header class="header">
      <a class="brand" href="/">
        <span class="brand-mark">🐍</span>
        <span>Python Engineering Playground</span>
      </a>

      <nav class="navigation" aria-label="Main navigation">
        <a href="#overview">Overview</a>
        <a href="#concepts">Concepts</a>
        <a href="#labs">Labs</a>
      </nav>
    </header>

    <main>
      <section id="overview" class="hero">
        <p class="eyebrow">PHOENIX · PYTHON ENGINEERING</p>

        <h1>
          Learn Python by
          <span>building systems.</span>
        </h1>

        <p class="hero-description">
          A hands-on engineering playground focused on Python,
          APIs, automation, architecture, and production-oriented practices.
        </p>
      </section>

      <section id="concepts" class="section">
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

      <section id="labs" class="section">
        <div class="section-heading">
          <p class="eyebrow">LABS</p>
          <h2>Projects</h2>
        </div>

        <article class="lab-card">
          <div>
            <span class="status">IN PROGRESS</span>
            <h3>System Information Inspector</h3>
            <p>
              A Python utility and FastAPI service for inspecting the current
              system environment.
            </p>
          </div>

          <span class="arrow">→</span>
        </article>
      </section>
    </main>

    <footer>
      <span>Phoenix Engineering Playground</span>
      <span>Python · FastAPI · Engineering</span>
    </footer>
  </div>
</template>
