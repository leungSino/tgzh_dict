<template>
  <div class="min-h-screen flex flex-col">
    <Navbar />
    <router-view class="flex-1" />
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
</script>
