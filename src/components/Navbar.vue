<template>
  <nav class="fixed top-0 w-full h-[110px] bg-[#3F3FF0] rounded-b-xl flex justify-between items-center px-4 z-50">
    <!-- 左側 logo -->
    <div class="flex items-center gap-2 sm:gap-5">
      <img src="../assets/customer-service-headset.png" class="w-10 h-10 sm:w-[90px] sm:h-[90px] invert" />
      <p class="text-white text-base sm:text-2xl">家教媒合平台</p>
    </div>

    <!-- 中間語言選單 -->
    <select
      class="ml-auto bg-[#3F3FF0] text-white text-sm sm:text-lg border-0 hover:cursor-pointer focus:outline-none mr-4"
      v-model="selectedLang"
      @change="handleLanguageChange"
    >
      <option v-for="(item, i) in languages" :key="i" :value="item">{{ item }}</option>
    </select>

    <!-- 桌機版導覽與按鈕 -->
    <div class="hidden sm:flex items-center gap-5">
      <div class="text-white flex items-center gap-3" v-if="role === 'student' && $route.path !== '/'">
        <Router-link to="/personaldashboard">學生個人頁面</Router-link>
      </div>
      <div class="text-white flex items-center gap-3" v-else-if="role === 'teacher' && $route.path !== '/'">
        <Router-link to="/teacherdashboard">教師個人頁面</Router-link>
      </div>
      <div class="text-white flex items-center gap-3" v-else-if="role === 'both' && $route.path !== '/'">
        <Router-link to="/personaldashboard">學生個人頁面</Router-link>
        <span class="text-white">｜</span>
        <Router-link to="/teacherdashboard">教師個人頁面</Router-link>
      </div>
      <div class="text-white flex items-center gap-3" v-else-if="role === 'admin' && $route.path !== '/'">
        <Router-link to="/">管理者頁面</Router-link>
      </div>

      <Router-link to="/login">
        <button
          v-if="login === false"
          class="w-[98px] h-[40px] border border-white text-white bg-[#3F3FF0] rounded-md hover:bg-white hover:text-[#3F3FF0] transition cursor-pointer"
        >
          登入
        </button>
        <button
          v-else
          class="w-[98px] h-[40px] border border-white text-white bg-[#3F3FF0] rounded-md hover:bg-white hover:text-[#3F3FF0] transition cursor-pointer"
        >
          登出
        </button>
      </Router-link>
    </div>

    <!-- 手機版漢堡選單 -->
    <button class="sm:hidden text-white" @click="toggleMobileMenu" aria-label="Toggle Menu">
      <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>

    <!-- 手機版展開選單 -->
    <div
      v-if="showMenu"
      class="absolute top-[110px] right-4 bg-white shadow-lg rounded-md w-52 sm:hidden z-50 text-sm divide-y divide-gray-200"
    >
      <div class="flex flex-col text-[#3F3FF0] font-medium">
        <Router-link
          v-if="role === 'student' && $route.path !== '/'"
          to="/personaldashboard"
          class="px-4 py-3 hover:bg-[#f0f4ff] transition"
        >
          學生個人頁面
        </Router-link>

        <Router-link
          v-else-if="role === 'teacher' && $route.path !== '/'"
          to="/teacherdashboard"
          class="px-4 py-3 hover:bg-[#f0f4ff] transition"
        >
          教師個人頁面
        </Router-link>

        <Router-link
          v-else-if="role === 'admin' && $route.path !== '/'"
          to="/"
          class="px-4 py-3 hover:bg-[#f0f4ff] transition"
        >
          管理者頁面
        </Router-link>

        <template v-else-if="role === 'both' && $route.path !== '/'">
          <Router-link to="/personaldashboard" class="px-4 py-3 hover:bg-[#f0f4ff] transition">
            學生個人頁面
          </Router-link>
          <Router-link to="/teacherdashboard" class="px-4 py-3 hover:bg-[#f0f4ff] transition">
            教師個人頁面
          </Router-link>
        </template>
      </div>

      <div class="px-4 py-3">
        <Router-link to="/login">
          <button
            class="w-full border border-[#3F3FF0] text-[#3F3FF0] bg-white rounded-md px-4 py-2 hover:bg-[#3F3FF0] hover:text-white transition cursor-pointer"
          >
            {{ login ? '登出' : '登入' }}
          </button>
        </Router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      languages: ['繁體中文(TW)', '簡體中文(CN)', '英文 (ENG)', '日文 (JPN)'],
      selectedLang: '',
      login: false,
      role: 'both', // 可改為從後端或登入狀態取得
      showMenu: false,
    }
  },
  mounted() {
    const savedLang = localStorage.getItem('lang')
    this.selectedLang = savedLang || this.languages[0]
  },
  methods: {
    toggleMobileMenu() {
      this.showMenu = !this.showMenu
    },
    handleLanguageChange() {
      localStorage.setItem('lang', this.selectedLang)
      console.log('切換語言為：', this.selectedLang)
      // i18n 切換可在這裡實現
    },
  },
}
</script>

<style scoped></style>
