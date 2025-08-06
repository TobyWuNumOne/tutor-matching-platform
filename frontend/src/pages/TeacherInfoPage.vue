<script setup>
    import { reactive } from 'vue';
    import { useRoute } from 'vue-router';
    import Navbar from '../components/Navbar.vue';
    import Footer from '../components/Footer.vue';

    // 路由參數
    const route = useRoute();
    const teacherName = route.params.teacherName;

    // 模擬資料，實際應從 API 抓取
    const teacher = reactive({
        avatar: 'https://via.placeholder.com/150', // 老師照片
        name: '王小明',
        email: 'teacher@example.com',
        phone: '0912-345-678',
        gender: 'Male',
        age: '35',
        education: '國立台灣大學 教育系 碩士',
        certifications: '教師資格證書 / TESOL / Google Educator',
        intro: '熱愛教學，擅長互動式學習，專注於學生的個別發展。',
        teaching_experience:
            '10年以上高中與成人英文教學經驗。\n曾任教於多間補習班及國際學校。',
        status: '在職',
        blue_premium: false,
        user_id: 1,
    });
</script>

<template>
    <Navbar />
    <div
        class="teacher-profile max-w-3xl mx-auto p-6 pt-[130px] bg-white rounded-lg shadow-md"
    >
        <div
            class="teacher-profile max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-md"
        >
            <!-- 大頭貼 + 名稱 -->
            <div class="flex items-center space-x-4">
                <img
                    :src="teacher.avatar"
                    alt="老師照片"
                    class="w-24 h-24 rounded-full object-cover border"
                />
                <div>
                    <h1 class="text-2xl font-bold">{{ teacher.name }}</h1>
                    <p class="text-gray-500">{{ teacher.status }}</p>
                </div>
            </div>

            <!-- 基本資料 -->
            <div class="mt-6 grid grid-cols-2 gap-4 text-gray-700">
                <div><strong>Email:</strong> {{ teacher.email }}</div>
                <div><strong>Phone:</strong> {{ teacher.phone }}</div>
                <div><strong>Gender:</strong> {{ teacher.gender }}</div>
                <div><strong>Age:</strong> {{ teacher.age }}</div>
            </div>

            <!-- 教育背景 -->
            <div class="mt-6">
                <h2 class="font-semibold text-lg">🎓 教育背景</h2>
                <p class="text-gray-700 mt-1 whitespace-pre-line">
                    {{ teacher.education }}
                </p>
            </div>

            <!-- 證照 -->
            <div v-if="teacher.certifications" class="mt-6">
                <h2 class="font-semibold text-lg">📜 證照</h2>
                <p class="text-gray-700 mt-1 whitespace-pre-line">
                    {{ teacher.certifications }}
                </p>
            </div>

            <!-- 簡介 -->
            <div class="mt-6">
                <h2 class="font-semibold text-lg">📖 簡介</h2>
                <p class="text-gray-700 mt-1 whitespace-pre-line">
                    {{ teacher.intro }}
                </p>
            </div>

            <!-- 教學經驗 -->
            <div class="mt-6">
                <h2 class="font-semibold text-lg">💼 教學經驗</h2>
                <p class="text-gray-700 mt-1 whitespace-pre-line">
                    {{ teacher.teaching_experience }}
                </p>
            </div>
        </div>
    </div>
    <Footer />
</template>

<style scoped>
    .teacher-profile {
        background-color: #f9fafb;
    }
</style>
