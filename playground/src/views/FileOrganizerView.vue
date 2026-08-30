<script setup lang="ts">
import '../styles/FileOrganizerView.css'
</script>

<template>
  <main class="file-organizer-page">
    <RouterLink to="/" class="back-link">
      ← Back to Overview
    </RouterLink>

    <header class="lab-header">
      <div>
        <p class="eyebrow">LAB · PYTHON ENGINEERING</p>

        <h1>File Organizer</h1>

        <p class="lab-description">
          A production-minded CLI tool that automatically organizes files
          into configurable subfolders based on sorting rules.
        </p>
      </div>
    </header>

    <section class="lab-meta">
      <span>PYTHON</span>
      <span>CLI</span>
      <span>AUTOMATION</span>
    </section>

    <section class="content-section">
      <div class="section-heading">
        <span class="section-label">01</span>
        <h2>Purpose</h2>
      </div>

      <p class="section-description">
        Automate the repetitive task of cleaning directories while keeping
        filesystem operations predictable, configurable, and safe.
      </p>
    </section>

    <section class="content-section">
      <div class="section-heading">
        <span class="section-label">02</span>
        <h2>Workflow</h2>
      </div>

      <div class="workflow-grid">
        <article class="workflow-card">
          <span class="workflow-number">01</span>
          <h3>Scan</h3>
          <p>
            Inspect the target directory and discover files that can be
            organized.
          </p>
        </article>

        <article class="workflow-card">
          <span class="workflow-number">02</span>
          <h3>Classify</h3>
          <p>
            Match files against the configured extension rules and determine
            their destination.
          </p>
        </article>

        <article class="workflow-card">
          <span class="workflow-number">03</span>
          <h3>Plan</h3>
          <p>
            Build the set of filesystem operations before modifying anything.
          </p>
        </article>

        <article class="workflow-card">
          <span class="workflow-number">04</span>
          <h3>Execute</h3>
          <p>
            Move files safely while handling duplicates, permissions, and
            filesystem errors.
          </p>
        </article>
      </div>
    </section>

    <section class="content-section split-section">
      <article class="feature-panel">
        <span class="section-label">03</span>
        <h2>Dry Run</h2>

        <p>
          Preview the planned filesystem changes without modifying the target
          directory.
        </p>

        <code>python main.py --path ~/Downloads --dry-run</code>
      </article>

      <article class="feature-panel">
        <span class="section-label">04</span>
        <h2>Configuration</h2>

        <p>
          Sorting rules are defined independently from the organizer logic.
        </p>

        <pre><code>{
  "images": [".jpg", ".png", ".gif"],
  "documents": [".pdf", ".docx", ".txt"],
  "code": [".py", ".js", ".html"],
  "others": []
}</code></pre>
      </article>
    </section>

    <section class="content-section">
      <div class="section-heading">
        <span class="section-label">05</span>
        <h2>Architecture</h2>
      </div>

      <div class="architecture-list">
        <div>
          <strong>main.py</strong>
          <span>Application orchestration</span>
        </div>

        <div>
          <strong>cli.py</strong>
          <span>Arguments and user input</span>
        </div>

        <div>
          <strong>config_loader.py</strong>
          <span>Sorting rule configuration</span>
        </div>

        <div>
          <strong>scanner.py</strong>
          <span>Directory scanning and classification</span>
        </div>

        <div>
          <strong>organizer.py</strong>
          <span>Filesystem operations</span>
        </div>

        <div>
          <strong>logger.py</strong>
          <span>Console and persistent logging</span>
        </div>
      </div>
    </section>

    <section class="content-section">
      <div class="section-heading">
        <span class="section-label">06</span>
        <h2>Engineering Practices</h2>
      </div>

      <div class="practice-grid">
        <span>Clean Architecture</span>
        <span>Single Responsibility</span>
        <span>Dependency Injection</span>
        <span>Type Hints</span>
        <span>Pathlib</span>
        <span>Exception Handling</span>
        <span>Dry Run</span>
        <span>Logging</span>
      </div>
    </section>

    <section class="content-section usage-section">
      <div class="section-heading">
        <span class="section-label">07</span>
        <h2>Usage</h2>
      </div>

      <div class="terminal">
        <span class="terminal-prompt">$</span>
        <code>python main.py --path ~/Downloads --dry-run --recursive</code>
      </div>

      <div class="terminal">
        <span class="terminal-prompt">$</span>
        <code>python main.py --path ~/Downloads --recursive</code>
      </div>
    </section>

    <footer class="lab-footer">
      <span>PYTHON · CLI · AUTOMATION</span>
      <span>PHOENIX ENGINEERING PLAYGROUND</span>
    </footer>
  </main>
</template>
