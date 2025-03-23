<script setup lang="ts">
import("assets/tailwind.scss");
</script>
<template>
  <div>
    <div class="bg-primary-800 text-white">
      <div class="container flex items-center gap-4 p-2">
        <HeaderLogo />
        <HeaderMenu class="grow" />
        <HeaderPhone />
      </div>
    </div>
    <NuxtLayout>
      <Suspense>
        <NuxtPage />
      </Suspense>
    </NuxtLayout>
  </div>
</template>
