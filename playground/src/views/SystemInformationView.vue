<script setup lang="ts">
import { onMounted, ref } from 'vue'
import '../styles/SystemInformationView.css'

interface SystemInformation {
  'Operating System': string
  'OS Version': string
  Architecture: string
  Processor: string
  Memory: string
  Python: string
  'Current Time': string
}

const information = ref<SystemInformation | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const lastUpdated = ref<string | null>(null)

async function loadSystemInformation() {
  loading.value = true
  error.value = null

  try {
    const response = await fetch(
      'http://127.0.0.1:8000/system-information',
    )

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`)
    }

    information.value = await response.json()
    lastUpdated.value = new Date().toLocaleTimeString()
  } catch {
    error.value = 'Unable to connect to the System Information API.'
  } finally {
    loading.value = false
  }
}

onMounted(loadSystemInformation)
</script>

<template>
  <main class="system-information-page">
    <header class="system-header">
      <div>
        <p class="eyebrow">LAB · PYTHON ENGINEERING</p>

        <h1>System Information Inspector</h1>

        <p class="system-description">
          Inspect the current system environment through a Python and
          FastAPI service.
        </p>
      </div>

      <button
        class="refresh-button"
        type="button"
        :disabled="loading"
        @click="loadSystemInformation"
      >
        Refresh
      </button>
    </header>

    <section class="api-status">
      <div class="status-indicator">
        <span
          class="status-dot"
          :class="{ online: information && !error }"
        />

        <span>
          API {{ information && !error ? 'ONLINE' : 'OFFLINE' }}
        </span>
      </div>

      <span v-if="lastUpdated" class="last-updated">
        Last updated {{ lastUpdated }}
      </span>
    </section>

    <section v-if="error" class="state-panel state-error">
      <span class="state-label">CONNECTION ERROR</span>

      <p>{{ error }}</p>

      <button type="button" @click="loadSystemInformation">
        Try again
      </button>
    </section>

    <section v-else-if="information" class="information-grid">
      <article class="information-card">
        <span class="card-label">Operating System</span>
        <strong>{{ information['Operating System'] }}</strong>
      </article>

      <article class="information-card">
        <span class="card-label">OS Version</span>
        <strong>{{ information['OS Version'] }}</strong>
      </article>

      <article class="information-card">
        <span class="card-label">Architecture</span>
        <strong>{{ information.Architecture }}</strong>
      </article>

      <article class="information-card information-card-wide">
        <span class="card-label">Processor</span>
        <strong>{{ information.Processor }}</strong>
      </article>

      <article class="information-card">
        <span class="card-label">Memory</span>
        <strong class="accent-value">{{ information.Memory }}</strong>
      </article>

      <article class="information-card">
        <span class="card-label">Python</span>
        <strong>{{ information.Python }}</strong>
      </article>

      <article class="information-card">
        <span class="card-label">Current Time</span>
        <strong>{{ information['Current Time'] }}</strong>
      </article>
    </section>

    <footer class="system-footer">
      <span>PYTHON · FASTAPI · SYSTEM INSPECTION</span>
      <span>PHOENIX ENGINEERING PLAYGROUND</span>
    </footer>
  </main>
</template>
