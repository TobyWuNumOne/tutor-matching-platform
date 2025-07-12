<script setup>
import { reactive, ref, computed } from 'vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

const teachers = reactive({
  name: "老師 A",
  email: "teachera@test.com",
  country: "臺北 Taipei",
  course: "國文",
})

const bookedStudents = ref([
  { name: "學生 A", course: "國文", time: "09:00 - 10:00", status: "線上" },
  { name: "學生 B", course: "英文", time: "10:00 - 11:00", status: "離線" },
  { name: "學生 C", course: "數學", time: "14:00 - 15:00", status: "線上" },
  { name: "學生 D", course: "社會", time: "17:00 - 18:00", status: "離線" },
  { name: "學生 E", course: "自然", time: "20:00 - 21:00", status: "線上" },
])

const showAllStudents = ref(false)
const showCalendar = ref(false)
const showBulletin = ref(false)
const showModal = ref(false)
const selectedDate = ref('')
const selectedPeriod = ref('')
const scheduleStatus = ref('')

// 2025年7月固定示範，可改成動態邏輯
const currentYear = ref(2025)
const currentMonth = ref(7) // 7月

// 上午下午晚上狀態資料，格式：{ 'YYYY-MM-DD': { morning: true/false, afternoon: true/false, evening: true/false } }
const availability = reactive({})

// 公告欄相關
const newAnnouncement = reactive({
  title: '',
  content: '',
})

const announcements = reactive([])

// 判斷該日期的星期幾 0(日)~6(六)
function getDayOfWeek(year, month, day) {
  return new Date(year, month - 1, day).getDay()
}

// 該月份天數
function getDaysInMonth(year, month) {
  return new Date(year, month, 0).getDate()
}

// 生成完整月曆格子 (陣列內元素是日期號碼或空字串代表空格)
const calendarDays = computed(() => {
  const days = []
  const firstDayWeek = getDayOfWeek(currentYear.value, currentMonth.value, 1)
  const totalDays = getDaysInMonth(currentYear.value, currentMonth.value)

  // 月曆起始空白格(第一天是星期幾，前面空幾格)
  for (let i = 0; i < firstDayWeek; i++) {
    days.push('')
  }
  // 月份日期
  for (let d = 1; d <= totalDays; d++) {
    days.push(d)
  }
  // 補足尾部空白(不一定要，讓每週7天整齊)
  while (days.length % 7 !== 0) {
    days.push('')
  }
  return days
})

// 周日固定灰色且不可點擊
function isSunday(day) {
  if (!day) return false
  return getDayOfWeek(currentYear.value, currentMonth.value, day) === 0
}

// 該日期是否所有時段都是不可預約(默認為可預約)
function isAllUnavailable(day) {
  if (!day) return false
  const dateKey = `${currentYear.value}-${String(currentMonth.value).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  const dayStatus = availability[dateKey]
  if (!dayStatus) return false // 無設定代表可預約
  return !dayStatus.morning && !dayStatus.afternoon && !dayStatus.evening
}

// 格子底色判斷
function getDayBgColor(day) {
  if (!day) return 'bg-transparent'
  if (isSunday(day)) return 'bg-gray-300 cursor-not-allowed'
  if (isAllUnavailable(day)) return 'bg-red-300 cursor-pointer'
  return 'bg-green-300 cursor-pointer'
}

// 點日期時，設定 selectedDate 且 showModal 打開
function onClickDate(day) {
  if (!day) return
  if (isSunday(day)) return
  selectedDate.value = `${currentYear.value}-${String(currentMonth.value).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  showModal.value = false
}

// 打開modal設定時段狀態
function openSchedule(period) {
  selectedPeriod.value = period
  if (!selectedDate.value) return
  // 讀取現有狀態或預設true（可預約）
  const dateKey = selectedDate.value
  const dayStatus = availability[dateKey] || { morning: true, afternoon: true, evening: true }
  scheduleStatus.value = dayStatus[periodMapToKey(period)]
  showModal.value = true
}

// 確認狀態(可預約或不可預約)
function confirmStatus(status) {
  if (!selectedDate.value) return
  const dateKey = selectedDate.value
  if (!availability[dateKey]) {
    availability[dateKey] = { morning: true, afternoon: true, evening: true }
  }
  availability[dateKey][periodMapToKey(selectedPeriod.value)] = (status === '可預約')
  scheduleStatus.value = status
  showModal.value = false
}

// 取消modal
function cancelModal() {
  showModal.value = false
}

// period 字串對應 availability key
function periodMapToKey(period) {
  switch (period) {
    case '上午': return 'morning'
    case '下午': return 'afternoon'
    case '晚上': return 'evening'
  }
  return ''
}

// 讀取某天某時段狀態
function getPeriodStatus(dateStr, period) {
  const dayStatus = availability[dateStr]
  if (!dayStatus) return '可預約'
  return dayStatus[periodMapToKey(period)] ? '可預約' : '不可預約'
}

// 切換月份
function prevMonth() {
  if (currentMonth.value === 1) {
    currentYear.value--
    currentMonth.value = 12
  } else {
    currentMonth.value--
  }
  selectedDate.value = ''
  showModal.value = false
}

function nextMonth() {
  if (currentMonth.value === 12) {
    currentYear.value++
    currentMonth.value = 1
  } else {
    currentMonth.value++
  }
  selectedDate.value = ''
  showModal.value = false
}

// 公告欄相關功能
function clearAnnouncement() {
  newAnnouncement.title = ''
  newAnnouncement.content = ''
}

function publishAnnouncement() {
  if (!newAnnouncement.title.trim() || !newAnnouncement.content.trim()) {
    alert('請輸入標題與內容')
    return
  }
  announcements.push({
    title: newAnnouncement.title,
    content: newAnnouncement.content,
    date: new Date().toLocaleString(),
    editable: false,
  })
  clearAnnouncement()
}

function toggleEdit(i) {
  announcements[i].editable = !announcements[i].editable
}

function deleteAnnouncement(i) {
  announcements.splice(i, 1)
}

// 修改按鈕點擊事件修正(直接呼叫方法)
function openCalendar() {
  showCalendar.value = true
  showBulletin.value = false
}
function openBulletin() {
  showBulletin.value = true
  showCalendar.value = false
}
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />
    <main class="flex-1 bg-gray-50 p-6 pt-[110px] mt-4 relative">
      <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-10 gap-6">
        <!-- 左側資訊 -->
        <div class="md:col-span-3 bg-white p-4 rounded-lg shadow flex flex-col items-center">
          <img src="https://source.unsplash.com/random/180x200" alt="avatar" class="w-[180px] h-[200px] rounded-lg mb-4 object-cover" />
          <p class="text-xl font-bold mb-2">{{ teachers.name }}</p>
          <p class="text-sm text-gray-600 mb-4">{{ teachers.email }}</p>
          <p class="text-gray-600 mb-2"><span class="font-bold">來自：</span>{{ teachers.country }}</p>
          <p class="text-gray-600"><span class="font-bold">教學科目：</span>{{ teachers.course }}</p>

          <div class="grid gap-4 mt-2 w-full">
            <button @click="openCalendar" class="bg-gray-200 hover:bg-gray-300 py-2 rounded-md cursor-pointer w-full text-center">安排行事曆</button>
            <button @click="openBulletin" class="bg-gray-200 hover:bg-gray-300 py-2 rounded-md cursor-pointer w-full text-center">公告欄</button>
            <button class="bg-gray-200 hover:bg-gray-300 py-2 rounded-md cursor-pointer w-full text-center">線上教學課程</button>
          </div>
        </div>

        <!-- 右側主體區域 -->
        <div class="md:col-span-7 space-y-6 relative">
          <!-- 預約 & 設定 -->
          <div v-if="!showCalendar && !showBulletin">
            <!-- 預約學生區塊 -->
            <div class="bg-white p-4 rounded-lg shadow space-y-4">
              <div class="flex justify-between items-center border-b pb-2">
                <p class="font-semibold text-xl">與您預約的學生：</p>
              </div>
              <div
                v-for="(student, i) in (showAllStudents ? bookedStudents : bookedStudents.slice(0, 3))"
                :key="i"
                class="bg-gray-100 p-3 rounded-lg mb-2 text-sm md:text-base grid grid-cols-2 grid-rows-2 gap-2 items-center md:flex md:justify-between"
              >
                <p class="font-medium text-left md:w-1/4">{{ student.name }}</p>
                <p class="text-right md:text-left md:w-1/4"><span class="font-bold">狀態：</span><span :class="student.status === '線上' ? 'text-green-600' : 'text-gray-600'">{{ student.status }}</span></p>
                <p class="text-left md:w-1/4"><span class="font-bold">預約課程：</span>{{ student.course }}</p>
                <p class="text-left md:w-1/4"><span class="font-bold">預約時間：</span>{{ student.time || '未填寫' }}</p>
              </div>
              <div v-if="bookedStudents.length > 3" class="text-center">
                <button @click="showAllStudents = !showAllStudents" class="text-blue-500 hover:underline cursor-pointer">{{ showAllStudents ? '顯示較少' : '查看更多...' }}</button>
              </div>
            </div>

            <!-- 設定選單 -->
            <div class="bg-white p-4 rounded-lg shadow">
              <p class="font-semibold text-xl mb-3">設定：</p>
              <div class="space-y-2 text-sm">
                <div class="bg-gray-100 hover:bg-gray-200 p-2 rounded cursor-pointer text-base">編輯個人資料</div>
                <div class="bg-gray-100 hover:bg-gray-200 p-2 rounded cursor-pointer text-base">安全性</div>
                <div class="bg-gray-100 hover:bg-gray-200 p-2 rounded cursor-pointer text-base">通知</div>
                <div class="bg-gray-100 hover:bg-gray-200 p-2 rounded cursor-pointer text-base">回報問題</div>
              </div>
            </div>
          </div>

          <!-- 行事曆區塊 -->
          <div v-if="showCalendar" class="bg-white p-4 rounded-lg shadow space-y-6 relative">
            <!-- 月份切換 -->
            <div class="flex justify-between items-center mb-4">
              <button @click="prevMonth" class="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 cursor-pointer">上一月</button>
              <h2 class="text-xl font-bold">{{ currentYear }} 年 {{ currentMonth }} 月</h2>
              <button @click="nextMonth" class="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 cursor-pointer">下一月</button>
            </div>

            <!-- 月曆表 -->
            <table class="w-full border-collapse border border-gray-300 text-center">
              <thead>
                <tr>
                  <th class="border border-gray-300 p-2 bg-gray-200">日</th>
                  <th class="border border-gray-300 p-2 bg-gray-200">一</th>
                  <th class="border border-gray-300 p-2 bg-gray-200">二</th>
                  <th class="border border-gray-300 p-2 bg-gray-200">三</th>
                  <th class="border border-gray-300 p-2 bg-gray-200">四</th>
                  <th class="border border-gray-300 p-2 bg-gray-200">五</th>
                  <th class="border border-gray-300 p-2 bg-gray-200">六</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(week, wIndex) in Math.ceil(calendarDays.length / 7)" :key="wIndex">
                  <td
                    v-for="d in 7"
                    :key="d"
                    :class="[ 
                      'border border-gray-300 p-3',
                      getDayBgColor(calendarDays[wIndex * 7 + d - 1]),
                      calendarDays[wIndex * 7 + d - 1] ? 'cursor-pointer' : '',
                      isSunday(calendarDays[wIndex * 7 + d - 1]) ? 'cursor-not-allowed' : ''
                    ]"
                    @click="onClickDate(calendarDays[wIndex * 7 + d - 1])"
                  >
                    {{ calendarDays[wIndex * 7 + d - 1] || '' }}
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- 點選日期後的上午下午晚上狀態設定 -->
            <div v-if="selectedDate" class="mt-6 bg-gray-100 p-4 rounded shadow">
              <h3 class="font-semibold mb-3">設定 {{ selectedDate }} 時段狀態</h3>
              <div class="space-y-3">
                <div v-for="period in ['上午', '下午', '晚上']" :key="period" class="flex items-center gap-3">
                  <p class="w-16 font-semibold">{{ period }}</p>
                  <p>狀態：
                    <span class="font-bold text-green-600" v-if="getPeriodStatus(selectedDate, period) === '可預約'">可預約</span>
                    <span class="font-bold text-red-600" v-else>不可預約</span>
                  </p>
                  <button
                    class="ml-auto px-3 py-1 rounded bg-blue-500 text-white hover:bg-blue-600 cursor-pointer"
                    @click="openSchedule(period)"
                  >修改</button>
                </div>
              </div>
            </div>

            <!-- 右下角離開按鈕 -->
            <button
                @click="showCalendar = false"
                class="mt-6 ml-auto px-5 py-2 bg-gray-200 hover:bg-gray-300 rounded shadow block cursor-pointer"
                >
                離開
            </button>

            <!-- modal: 確認時段狀態 -->
            <div
              v-if="showModal"
              class="fixed inset-0 bg-black bg-opacity-30 flex justify-center items-center z-50"
              @click.self="cancelModal"
            >
              <div class="bg-white rounded-lg p-6 w-80">
                <h3 class="text-lg font-bold mb-4">設定 {{ selectedDate }} {{ selectedPeriod }} 狀態</h3>
                <div class="flex justify-around mb-4">
                  <button
                    class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 cursor-pointer"
                    @click="confirmStatus('可預約')"
                  >
                    可預約
                  </button>
                  <button
                    class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 cursor-pointer"
                    @click="confirmStatus('不可預約')"
                  >
                    不可預約
                  </button>
                </div>
                <button class="block mx-auto px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 cursor-pointer" @click="cancelModal">取消</button>
              </div>
            </div>
          </div>

          <!-- 公告欄 -->
          <div v-if="showBulletin" class="bg-white p-4 rounded-lg shadow space-y-6">
            <h2 class="text-xl font-bold">發佈公告內容</h2>
            <div class="border border-black rounded-md overflow-hidden">
              <input v-model="newAnnouncement.title" placeholder="輸入標題" class="w-full p-2 bg-gray-100 focus:outline-none placeholder:font-semibold" />
              <textarea v-model="newAnnouncement.content" rows="4" placeholder="輸入內容" class="w-full p-2 bg-gray-100 focus:outline-none placeholder:font-semibold"></textarea>
            </div>
            <div class="flex justify-end gap-4">
              <button @click="clearAnnouncement" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded cursor-pointer">取消</button>
              <button @click="publishAnnouncement" class="px-4 py-2 bg-blue-500 text-white hover:bg-blue-600 rounded cursor-pointer">發佈</button>
            </div>
            <hr />

            <div class="space-y-3">
              <h3 class="text-lg font-bold">已發佈消息</h3>
              <div v-for="(a, i) in announcements" :key="i" class="border border-black p-3 rounded">
                <div v-if="!a.editable">
                  <p class="font-semibold">{{ a.title }}</p>
                  <p class="text-sm text-gray-600">{{ a.content }}</p>
                  <p class="text-xs text-right text-gray-400">{{ a.date }}</p>
                </div>
                <div v-else>
                  <input v-model="a.title" class="w-full p-1 border rounded mb-2" />
                  <textarea v-model="a.content" class="w-full p-1 border rounded"></textarea>
                </div>
                <div class="flex justify-end gap-2 mt-2">
                  <button @click="toggleEdit(i)" class="text-blue-600 hover:underline cursor-pointer">{{ a.editable ? '完成' : '編輯' }}</button>
                  <button @click="deleteAnnouncement(i)" class="text-red-500 hover:underline cursor-pointer">刪除</button>
                </div>
              </div>
            </div>

            <div class="flex justify-end mt-4">
              <button @click="showBulletin = false" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded cursor-pointer">離開</button>
            </div>
          </div>
        </div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<style scoped>
/* 讓不可點的日曆格子無法點擊，cursor 是 not-allowed */
.cursor-not-allowed {
  cursor: not-allowed !important;
}
</style>
