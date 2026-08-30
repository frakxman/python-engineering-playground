import { createRouter, createWebHistory } from 'vue-router'

import OverviewView from '../views/OverviewView.vue'
import SystemInformationView from '../views/SystemInformationView.vue'

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
  ],
})

export default router
