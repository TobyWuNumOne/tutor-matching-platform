<script setup>
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import { reactive } from 'vue'
import { RouterLink } from 'vue-router'  // 這裡新增 import

const stdfeedbacks = reactive([
  {
    title: '非常完美!!',
    content: '「這個平台幫我找到超合適的數學家教，才幾個禮拜，我的成績就大大進步了！」',
    student: 'Cody',
    role: 'std',
  },
  {
    title: '精準媒合!!',
    content:
      '「作為一位家教老師，我非常欣賞這個平台的便利性，能輕鬆與學生互動並追蹤他們的學習成果，值得推薦！',
    tutor: 'Shen',
    role: 'teacher',
  },
  {
    title: '有許多人受惠!!',
    content: '「互動式工具加上量身打造的課程，讓學習變得超有趣，真的是我做過最棒的決定！」',
    student: 'Alex',
    role: 'std',
  },
])
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <!-- 固定導覽列 -->
    <Navbar />

    <!-- 主內容區 -->
    <main class="pt-[110px] flex-1 md:h-screen-navbar-footer md:flex md:flex-col md:overflow-hidden overflow-auto">
      <!-- 標語 -->
      <div class="h-[100px] flex justify-center items-center shrink-0 px-4">
        <h1 class="text-3xl font-semibold text-center">"引導學生，成就未來"</h1>
      </div>

      <!-- 評價卡片 -->
      <div class="flex-1 overflow-auto flex flex-col md:flex-row justify-center items-center gap-6 px-4 py-6">
        <div v-for="(item, i) in stdfeedbacks" :key="i" class="relative w-[90%] md:w-[300px] h-[200px] bg-white border border-black rounded-2xl p-4 shadow-md">
          <h3 class="text-indigo-600 text-xl font-semibold text-center mb-2">{{ item.title }}</h3>
          <p class="text-base break-words text-center">{{ item.content }}</p>

          <p class="absolute bottom-2 right-4 text-sm text-gray-600" v-if="item.role === 'std'">
            -- {{ item.student }} 同學
          </p>
          <p class="absolute bottom-2 right-4 text-sm text-gray-600" v-else>
            -- {{ item.tutor }} 家教
          </p>
        </div>
      </div>

      <!-- CTA 按鈕 -->
      <div class="h-[90px] flex justify-center items-center shrink-0 px-4 mb-4 md:mb-6">
        <RouterLink to="/search">
          <button class="w-[300px] md:w-[600px] h-[60px] md:h-[90px] bg-[#3F3FF0] text-white rounded-xl text-lg hover:brightness-110 transition cursor-pointer">
            立即開始，與你的專屬家教見面！
          </button>
        </RouterLink>
      </div>
    </main>

    <!-- 頁腳 -->
    <Footer />
  </div>
</template>

<style scoped></style>
