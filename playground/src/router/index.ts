import { createRouter, createWebHistory } from 'vue-router'

import OverviewView from '../views/OverviewView.vue'
import SystemInformationView from '../views/SystemInformationView.vue'
import FileOrganizerView from '../views/FileOrganizerView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: OverviewView,
    },
    {
      path: '/labs/system-information',
      component: SystemInformationView,
    },
    {
      path: '/labs/file-organizer',
      component: FileOrganizerView,
    }
  ],
})

export default router
