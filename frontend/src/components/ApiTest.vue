<template>
  <div class="api-test-container p-6 bg-gray-100 min-h-screen">
    <h1 class="text-3xl font-bold mb-6">🔗 前後端串接測試</h1>
    
    <!-- 連線狀態 -->
    <div class="mb-6 p-4 rounded-lg" :class="connectionStatus.class">
      <h2 class="text-xl font-semibold mb-2">連線狀態</h2>
      <p>{{ connectionStatus.message }}</p>
      <button @click="testConnection" class="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
        重新測試連線
      </button>
    </div>

    <!-- 註冊測試 -->
    <div class="mb-6 p-4 bg-white rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">用戶註冊測試</h2>
      <div class="grid grid-cols-2 gap-4 mb-4">
        <input v-model="registerForm.name" placeholder="姓名" class="p-2 border rounded">
        <input v-model="registerForm.account" type="email" placeholder="Email" class="p-2 border rounded">
        <input v-model="registerForm.password" type="password" placeholder="密碼" class="p-2 border rounded">
        <select v-model="registerForm.gender" class="p-2 border rounded">
          <option value="">選擇性別</option>
          <option value="male">男</option>
          <option value="female">女</option>
        </select>
        <input v-model.number="registerForm.age" type="number" placeholder="年齡" class="p-2 border rounded">
      </div>
      <button @click="testRegister" :disabled="registerLoading" 
              class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50">
        {{ registerLoading ? '註冊中...' : '測試註冊' }}
      </button>
      <div v-if="registerResult" class="mt-4 p-3 rounded" :class="registerResult.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
        <pre>{{ JSON.stringify(registerResult, null, 2) }}</pre>
      </div>
    </div>

    <!-- 登入測試 -->
    <div class="mb-6 p-4 bg-white rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">用戶登入測試</h2>
      <div class="grid grid-cols-2 gap-4 mb-4">
        <input v-model="loginForm.account" type="email" placeholder="Email" class="p-2 border rounded">
        <input v-model="loginForm.password" type="password" placeholder="密碼" class="p-2 border rounded">
      </div>
      <button @click="testLogin" :disabled="loginLoading"
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50">
        {{ loginLoading ? '登入中...' : '測試登入' }}
      </button>
      <div v-if="loginResult" class="mt-4 p-3 rounded" :class="loginResult.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
        <pre>{{ JSON.stringify(loginResult, null, 2) }}</pre>
      </div>
    </div>

    <!-- 課程資料測試 -->
    <div class="mb-6 p-4 bg-white rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">課程資料測試</h2>
      <button @click="testGetCourses" :disabled="coursesLoading"
              class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 disabled:opacity-50">
        {{ coursesLoading ? '載入中...' : '獲取課程列表' }}
      </button>
      <div v-if="coursesResult" class="mt-4 p-3 rounded" :class="coursesResult.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
        <pre>{{ JSON.stringify(coursesResult, null, 2) }}</pre>
      </div>
    </div>

    <!-- 認證測試 -->
    <div class="mb-6 p-4 bg-white rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">認證測試</h2>
      <p class="mb-2">Token狀態: {{ authToken ? '✅ 已設置' : '❌ 未設置' }}</p>
      <button @click="testAuthRequest" :disabled="authLoading || !authToken"
              class="px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 disabled:opacity-50">
        {{ authLoading ? '測試中...' : '測試認證請求' }}
      </button>
      <div v-if="authResult" class="mt-4 p-3 rounded" :class="authResult.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
        <pre>{{ JSON.stringify(authResult, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { authAPI, courseAPI, userAPI } from '../utils/api.js'

// 連線狀態
const connectionStatus = ref({
  class: 'bg-yellow-100 text-yellow-800',
  message: '正在檢測連線...'
})

// 註冊表單
const registerForm = reactive({
  name: '測試用戶',
  account: 'test@example.com',
  password: 'test123',
  gender: 'male',
  age: 25,
  role: 'student'
})

// 登入表單
const loginForm = reactive({
  account: 'test@example.com',
  password: 'test123'
})

// 狀態
const registerLoading = ref(false)
const loginLoading = ref(false)
const coursesLoading = ref(false)
const authLoading = ref(false)

// 結果
const registerResult = ref(null)
const loginResult = ref(null)
const coursesResult = ref(null)
const authResult = ref(null)
const authToken = ref(null)

// 測試連線
async function testConnection() {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ account: 'test', password: 'test' })
    })
    
    connectionStatus.value = {
      class: 'bg-green-100 text-green-800',
      message: '✅ 後端服務正常運行'
    }
  } catch (error) {
    connectionStatus.value = {
      class: 'bg-red-100 text-red-800',
      message: '❌ 無法連接後端服務'
    }
  }
}

// 測試註冊
async function testRegister() {
  registerLoading.value = true
  registerResult.value = null
  
  try {
    const response = await authAPI.register(registerForm)
    registerResult.value = {
      success: true,
      data: response.data,
      message: '註冊成功'
    }
  } catch (error) {
    registerResult.value = {
      success: false,
      error: error.response?.data || error.message,
      message: '註冊失敗'
    }
  } finally {
    registerLoading.value = false
  }
}

// 測試登入
async function testLogin() {
  loginLoading.value = true
  loginResult.value = null
  
  try {
    const response = await authAPI.login(loginForm)
    authToken.value = response.data.access_token
    localStorage.setItem('jwt', authToken.value)
    
    loginResult.value = {
      success: true,
      data: response.data,
      message: '登入成功，Token已保存'
    }
  } catch (error) {
    loginResult.value = {
      success: false,
      error: error.response?.data || error.message,
      message: '登入失敗'
    }
  } finally {
    loginLoading.value = false
  }
}

// 測試獲取課程
async function testGetCourses() {
  coursesLoading.value = true
  coursesResult.value = null
  
  try {
    const response = await courseAPI.getAllCourses()
    coursesResult.value = {
      success: true,
      data: response.data,
      message: '課程資料獲取成功'
    }
  } catch (error) {
    coursesResult.value = {
      success: false,
      error: error.response?.data || error.message,
      message: '課程資料獲取失敗'
    }
  } finally {
    coursesLoading.value = false
  }
}

// 測試認證請求
async function testAuthRequest() {
  authLoading.value = true
  authResult.value = null
  
  try {
    // 測試一個簡單的認證端點
    const response = await authAPI.getCurrentUser()
    authResult.value = {
      success: true,
      data: response.data,
      message: '認證請求成功'
    }
  } catch (error) {
    authResult.value = {
      success: false,
      error: error.response?.data || error.message,
      message: '認證請求失敗'
    }
  } finally {
    authLoading.value = false
  }
}

// 頁面載入時測試連線
onMounted(() => {
  testConnection()
  // 檢查是否已有token
  const savedToken = localStorage.getItem('jwt')
  if (savedToken) {
    authToken.value = savedToken
  }
})
</script>