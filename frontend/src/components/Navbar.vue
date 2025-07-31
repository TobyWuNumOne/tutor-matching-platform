<script setup>
import { ref, onMounted, watch } from "vue";
import { RouterLink, useRouter, useRoute } from "vue-router";

const languages = ["繁體中文(TW)", "簡體中文(CN)", "英文 (ENG)", "日文 (JPN)"];
const selectedLang = ref(localStorage.getItem("lang") || languages[0]);
const login = ref(false);
const role = ref("both"); // 可從後端或登入狀態取得
const userAccount = ref("");
const userName = ref("");
const showMenu = ref(false);
const router = useRouter();
const route = useRoute();

function toggleMobileMenu() {
    showMenu.value = !showMenu.value;
}

function handleLanguageChange() {
    localStorage.setItem("lang", selectedLang.value);
    console.log("切換語言為：", selectedLang.value);
    // i18n 切換可在這裡實現
}

function checkLogin() {
    const jwt = localStorage.getItem("jwt");
    login.value = !!jwt;
    if (jwt) {
        try {
            const payload = JSON.parse(atob(jwt.split(".")[1]));
            // 假設 payload 有 account, username 欄位，請根據實際欄位調整
            userAccount.value =
                payload.account || payload.email || payload.sub || "";
            userName.value = payload.username || payload.name || "";
        } catch (e) {
            userAccount.value = "";
            userName.value = "";
        }
    } else {
        userAccount.value = "";
        userName.value = "";
    }
}

function handleLogout() {
    localStorage.removeItem("jwt");
    login.value = false;
    router.push("/login");
}

onMounted(() => {
    checkLogin();
});

watch(
    () => route.fullPath,
    () => {
        checkLogin();
    }
);
</script>

<template>
    <nav
        class="fixed top-0 w-full h-[80px] bg-[#3F3FF0] flex justify-between items-center px-4 z-50"
    >
        <!-- 左側 logo -->
        <div class="flex items-center gap-2 sm:gap-5">
            <img
                src="../assets/customer-service-headset.png"
                class="w-10 h-10 invert"
            />
            <p class="text-white text-base sm:text-2xl">
                <RouterLink to="/">家教媒合平台</RouterLink>
            </p>
        </div>
        <!-- 桌機版導覽與按鈕 -->
        <div class="hidden md:flex items-center gap-5">
            <div
                class="text-white flex items-center gap-3"
                v-if="role === 'student' && $route.path !== '/'"
            >
                <RouterLink to="/search">預約老師</RouterLink>
                <span class="text-white">｜</span>
                <RouterLink to="/personaldashboard">學生個人頁面</RouterLink>
            </div>

            <!-- 老師 -->
            <div
                class="text-white flex items-center gap-3"
                v-else-if="role === 'teacher' && $route.path !== '/'"
            >
                <RouterLink to="/teacherdashboard">教師個人頁面</RouterLink>
            </div>

            <!-- 既是老師也是學生 -->
            <div
                class="text-white flex items-center gap-3"
                v-else-if="role === 'both' && $route.path !== '/'"
            >
                <RouterLink to="/search">預約老師</RouterLink>
                <span class="text-white">｜</span>
                <RouterLink to="/personaldashboard">學生個人頁面</RouterLink>
                <span class="text-white">｜</span>
                <RouterLink to="/teacherdashboard">教師個人頁面</RouterLink>
            </div>

            <!-- 管理者 -->
            <div
                class="text-white flex items-center gap-3"
                v-else-if="role === 'admin' && $route.path !== '/'"
            >
                <RouterLink to="/">管理者頁面</RouterLink>
            </div>

            <RouterLink to="/register-teacher">
                <button
                    class="w-[140px] h-[40px] border border-white text-white bg-transparent rounded-md hover:bg-white hover:text-[#3F3FF0] transition cursor-pointer"
                >
                    註冊成為老師
                </button>
            </RouterLink>

            <template v-if="!login">
                <RouterLink to="/login">
                    <button
                        class="w-[98px] h-[40px] border border-white text-white bg-[#3F3FF0] rounded-md hover:bg-white hover:text-[#3F3FF0] transition cursor-pointer"
                    >
                        登入
                    </button>
                </RouterLink>
            </template>
            <template v-else>
                <span class="text-white mr-2 flex flex-col items-end text-xs">
                    <span v-if="userAccount">帳號：{{ userAccount }}</span>
                    <span v-if="userName">使用者名稱：{{ userName }}</span>
                </span>
                <button
                    @click="handleLogout"
                    class="w-[98px] h-[40px] border border-white text-white bg-[#3F3FF0] rounded-md hover:bg-white hover:text-[#3F3FF0] transition cursor-pointer"
                >
                    登出
                </button>
            </template>
        </div>

        <!-- 手機版漢堡選單 -->
        <button
            class="md:hidden text-white"
            @click="toggleMobileMenu"
            aria-label="Toggle Menu"
        >
            <svg
                class="w-8 h-8"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M4 6h16M4 12h16M4 18h16"
                />
            </svg>
        </button>

        <!-- 手機版展開選單 -->
        <div
            v-if="showMenu"
            class="absolute top-[110px] right-4 bg-white shadow-lg rounded-md w-52 sm:hidden z-50 text-sm divide-y divide-gray-200"
        >
            <div class="flex flex-col text-[#3F3FF0] font-medium">
                <RouterLink
                    to="/search"
                    class="px-4 py-3 hover:bg-[#f0f4ff] transition"
                >
                    預約老師
                </RouterLink>

                <RouterLink
                    to="/personaldashboard"
                    v-if="role === 'student' && $route.path !== '/'"
                    class="px-4 py-3 hover:bg-[#f0f4ff] transition"
                >
                    學生個人頁面
                </RouterLink>

                <RouterLink
                    to="/teacherdashboard"
                    v-else-if="role === 'teacher' && $route.path !== '/'"
                    class="px-4 py-3 hover:bg-[#f0f4ff] transition"
                >
                    教師個人頁面
                </RouterLink>

                <RouterLink
                    to="/"
                    v-else-if="role === 'admin' && $route.path !== '/'"
                    class="px-4 py-3 hover:bg-[#f0f4ff] transition"
                >
                    管理者頁面
                </RouterLink>

                <template v-else-if="role === 'both' && $route.path !== '/'">
                    <RouterLink
                        to="/personaldashboard"
                        class="px-4 py-3 hover:bg-[#f0f4ff] transition"
                    >
                        學生個人頁面
                    </RouterLink>
                    <RouterLink
                        to="/teacherdashboard"
                        class="px-4 py-3 hover:bg-[#f0f4ff] transition"
                    >
                        教師個人頁面
                    </RouterLink>
                </template>
            </div>

            <div class="px-4 py-3">
                <RouterLink to="/register-teacher">
                    <button
                        class="w-full border border-[#3F3FF0] text-[#3F3FF0] bg-white rounded-md px-4 py-2 hover:bg-[#3F3FF0] hover:text-white transition cursor-pointer"
                    >
                        註冊成為老師
                    </button>
                </RouterLink>
            </div>

            <div class="px-4 py-3">
                <RouterLink to="/login">
                    <button
                        class="w-full border border-[#3F3FF0] text-[#3F3FF0] bg-white rounded-md px-4 py-2 hover:bg-[#3F3FF0] hover:text-white transition cursor-pointer"
                    >
                        {{ login ? "登出" : "登入" }}
                    </button>
                </RouterLink>
            </div>
        </div>
    </nav>
</template>

<style></style>
