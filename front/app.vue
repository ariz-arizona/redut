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
    <div class="bg-primary-800 text-white">
      <div class="container flex items-center gap-4 p-2 py-8">
        <div class="grid grid-cols-3">
          <div class="col-span-2">
            <div class="text-sm">
              Информация о ценах, планировках, а также специальных предложениях, размещённых на данном сайте, носит
              исключительно ознакомительный характер, не является публичной офертой, определяемой положениями Статьи 437
              Гражданского кодекса Российской Федерации. Представленные на сайте изображения объектов долевого
              строительства носят предварительный ознакомительный характер и могут отличаться от фактических проектных
              решений, реализуемых застройщиком.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
