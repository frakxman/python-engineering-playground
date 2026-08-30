<script setup lang="ts">
import { ref } from 'vue'
import '../styles/FileOrganizerView.css'

interface FileOperation {
  source: string
  destination: string
  category: string
}

interface FileOrganizerPreview {
  path: string
  recursive: boolean
  total_files: number
  categories: Record<string, number>
  operations: FileOperation[]
}

interface FileOrganizerResult {
  path: string
  recursive: boolean
  dry_run: boolean
  moved: number
  skipped: number
  errors: number
}

const API_BASE_URL = 'http://127.0.0.1:8001'

const path = ref('')
const recursive = ref(false)

const preview = ref<FileOrganizerPreview | null>(null)
const result = ref<FileOrganizerResult | null>(null)

const loading = ref(false)
const organizing = ref(false)
const error = ref<string | null>(null)
const lastUpdated = ref<string | null>(null)

async function previewFiles() {
  console.log('Preview recursive:', recursive.value)

  if (!path.value.trim()) {
    error.value = 'Please enter a target directory.'
    return
  }

  loading.value = true
  error.value = null

  try {
    const response = await fetch(
      `${API_BASE_URL}/file-organizer/preview`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          path: path.value.trim(),
          recursive: recursive.value,
        }),
      },
    )

    if (!response.ok) {
      const data = await response.json().catch(() => null)

      throw new Error(
        data?.detail ??
          `Request failed with status ${response.status}`,
      )
    }

    preview.value = await response.json()

    lastUpdated.value = new Date().toLocaleTimeString()
  } catch (err) {
    preview.value = null

    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to connect to the File Organizer API.'
  } finally {
    loading.value = false
  }
}

async function organizeFiles() {
  if (!path.value.trim()) {
    error.value = 'Please enter a target directory.'
    return
  }

  if (!preview.value || preview.value.total_files === 0) {
    error.value = 'There are no files available to organize.'
    return
  }

  organizing.value = true
  error.value = null

  try {
    const response = await fetch(
      `${API_BASE_URL}/file-organizer/organize`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          path: path.value.trim(),
          recursive: recursive.value,
        }),
      },
    )

    if (!response.ok) {
      const data = await response.json().catch(() => null)

      throw new Error(
        data?.detail ??
          `Request failed with status ${response.status}`,
      )
    }

    result.value = await response.json()

    lastUpdated.value = new Date().toLocaleTimeString()

    /*
     * Refresh the preview after organization.
     *
     * Important:
     * We do this manually instead of calling previewFiles()
     * because previewFiles() clears the execution result.
     */
    await refreshPreviewAfterOrganization()
  } catch (err) {
    error.value =
      err instanceof Error
        ? err.message
        : 'Unable to organize files.'
  } finally {
    organizing.value = false
  }
}

async function refreshPreviewAfterOrganization() {
  try {
    const response = await fetch(
      `${API_BASE_URL}/file-organizer/preview`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          path: path.value.trim(),
          recursive: recursive.value,
        }),
      },
    )

    if (!response.ok) {
      const data = await response.json().catch(() => null)

      throw new Error(
        data?.detail ??
          `Request failed with status ${response.status}`,
      )
    }

    preview.value = await response.json()

    lastUpdated.value = new Date().toLocaleTimeString()
  } catch (err) {
    /*
     * The organization itself already succeeded.
     *
     * If refreshing the preview fails, keep the execution
     * result visible and only report the refresh problem.
     */
    error.value =
      err instanceof Error
        ? `Files were organized, but the preview could not be refreshed: ${err.message}`
        : 'Files were organized, but the preview could not be refreshed.'
  }
}

function clearResults() {
  preview.value = null
  result.value = null
  error.value = null
  lastUpdated.value = null
}
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

    <!-- API CONTROL -->
    <section class="content-section organizer-console">
      <div class="section-heading">
        <span class="section-label">00</span>
        <h2>File Organizer Control</h2>
      </div>

      <div class="organizer-form">
        <label for="target-path">
          Target Directory
        </label>

        <input
          id="target-path"
          v-model="path"
          type="text"
          placeholder="C:\Users\YourName\Downloads"
          :disabled="loading || organizing"
          @keyup.enter="previewFiles"
        />

        <label class="recursive-option">
          <input
            v-model="recursive"
            type="checkbox"
            :disabled="loading || organizing"
          />

          <span>
            Scan subdirectories recursively
          </span>
        </label>

        <div class="organizer-actions">
          <button
            type="button"
            :disabled="loading || organizing"
            @click="previewFiles"
          >
            {{ loading ? 'Scanning...' : 'Preview' }}
          </button>

          <button
            type="button"
            :disabled="
              loading ||
              organizing ||
              !path.trim() ||
              !preview ||
              preview.total_files === 0
            "
            @click="organizeFiles"
          >
            {{ organizing ? 'Organizing...' : 'Organize Files' }}
          </button>

          <button
            v-if="preview || result || error"
            type="button"
            :disabled="loading || organizing"
            @click="clearResults"
          >
            Clear
          </button>
        </div>
      </div>

      <div class="api-status">
        <div class="status-indicator">
          <span
            class="status-dot"
            :class="{ online: preview || result }"
          />

          <span>
            API {{ preview || result ? 'ONLINE' : 'READY' }}
          </span>
        </div>

        <span
          v-if="lastUpdated"
          class="last-updated"
        >
          Last updated {{ lastUpdated }}
        </span>
      </div>
    </section>

    <!-- ERROR -->
    <section
      v-if="error"
      class="state-panel state-error"
    >
      <span class="state-label">
        OPERATION ERROR
      </span>

      <p>{{ error }}</p>

      <button
        type="button"
        :disabled="loading || organizing"
        @click="previewFiles"
      >
        Try again
      </button>
    </section>

    <!-- PREVIEW SUMMARY -->
    <section
      v-if="preview"
      class="content-section"
    >
      <div class="section-heading">
        <span class="section-label">01</span>
        <h2>Preview</h2>
      </div>

      <div class="preview-summary">
        <article class="information-card">
          <span class="card-label">
            Target
          </span>

          <strong>
            {{ preview.path }}
          </strong>
        </article>

        <article class="information-card">
          <span class="card-label">
            Total Files
          </span>

          <strong class="accent-value">
            {{ preview.total_files }}
          </strong>
        </article>

        <article class="information-card">
          <span class="card-label">
            Recursive
          </span>

          <strong>
            {{ preview.recursive ? 'YES' : 'NO' }}
          </strong>
        </article>
      </div>
    </section>

    <!-- CATEGORIES -->
    <section
      v-if="preview"
      class="content-section"
    >
      <div class="section-heading">
        <span class="section-label">02</span>
        <h2>Categories</h2>
      </div>

      <div class="category-grid">
        <article
          v-for="(count, category) in preview.categories"
          :key="category"
          class="category-card"
        >
          <span class="card-label">
            {{ category }}
          </span>

          <strong>
            {{ count }}
          </strong>
        </article>
      </div>
    </section>

    <!-- OPERATIONS -->
    <section
      v-if="preview && preview.operations.length"
      class="content-section"
    >
      <div class="section-heading">
        <span class="section-label">03</span>
        <h2>Planned Operations</h2>
      </div>

      <div class="operations-list">
        <article
          v-for="(operation, index) in preview.operations"
          :key="`${operation.source}-${index}`"
          class="operation-card"
        >
          <span class="operation-number">
            {{ String(index + 1).padStart(2, '0') }}
          </span>

          <div class="operation-content">
            <span class="operation-category">
              {{ operation.category }}
            </span>

            <strong>
              {{ operation.source }}
            </strong>

            <span class="operation-destination">
              → {{ operation.destination }}
            </span>
          </div>
        </article>
      </div>
    </section>

    <!-- EMPTY PREVIEW -->
    <section
      v-if="preview && preview.total_files === 0"
      class="state-panel"
    >
      <span class="state-label">
        NO FILES FOUND
      </span>

      <p>
        No files were found in the selected directory.
      </p>
    </section>

    <!-- RESULT -->
    <section
      v-if="result"
      class="content-section"
    >
      <div class="section-heading">
        <span class="section-label">04</span>
        <h2>Execution Result</h2>
      </div>

      <div class="result-grid">
        <article class="information-card">
          <span class="card-label">
            Moved
          </span>

          <strong class="accent-value">
            {{ result.moved }}
          </strong>
        </article>

        <article class="information-card">
          <span class="card-label">
            Skipped
          </span>

          <strong>
            {{ result.skipped }}
          </strong>
        </article>

        <article class="information-card">
          <span class="card-label">
            Errors
          </span>

          <strong>
            {{ result.errors }}
          </strong>
        </article>

        <article class="information-card">
          <span class="card-label">
            Mode
          </span>

          <strong>
            {{ result.dry_run ? 'DRY RUN' : 'EXECUTED' }}
          </strong>
        </article>
      </div>
    </section>

    <!-- ORIGINAL PROJECT DESCRIPTION -->
    <section class="content-section">
      <div class="section-heading">
        <span class="section-label">05</span>
        <h2>Purpose</h2>
      </div>

      <p class="section-description">
        Automate the repetitive task of cleaning directories while keeping
        filesystem operations predictable, configurable, and safe.
      </p>
    </section>

    <!-- WORKFLOW -->
    <section class="content-section">
      <div class="section-heading">
        <span class="section-label">06</span>
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

    <!-- DRY RUN / CONFIGURATION -->
    <section class="content-section split-section">
      <article class="feature-panel">
        <span class="section-label">07</span>

        <h2>Dry Run</h2>

        <p>
          Preview the planned filesystem changes without modifying the target
          directory.
        </p>

        <code>
          python main.py --path ~/Downloads --dry-run
        </code>
      </article>

      <article class="feature-panel">
        <span class="section-label">08</span>

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

    <!-- ARCHITECTURE -->
    <section class="content-section">
      <div class="section-heading">
        <span class="section-label">09</span>
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

    <!-- ENGINEERING PRACTICES -->
    <section class="content-section">
      <div class="section-heading">
        <span class="section-label">10</span>
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

    <!-- USAGE -->
    <section class="content-section usage-section">
      <div class="section-heading">
        <span class="section-label">11</span>
        <h2>Usage</h2>
      </div>

      <div class="terminal">
        <span class="terminal-prompt">$</span>

        <code>
          python main.py --path ~/Downloads --dry-run --recursive
        </code>
      </div>

      <div class="terminal">
        <span class="terminal-prompt">$</span>

        <code>
          python main.py --path ~/Downloads --recursive
        </code>
      </div>
    </section>

    <footer class="lab-footer">
      <span>
        PYTHON · CLI · AUTOMATION
      </span>

      <span>
        PHOENIX ENGINEERING PLAYGROUND
      </span>
    </footer>
  </main>
</template>
