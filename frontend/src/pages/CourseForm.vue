<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";

const router = useRouter();

const course = ref({
    subject: "",
    description: "",
    price: "",
    location: "",
    teacher_id: 1, // 假設為目前登入教師 ID
});

const startTime = ref("10:00");
const endTime = ref("11:00");

const tags = ref(["數學", "英文"]);
const tagInput = ref("");

const addTag = () => {
    if (tagInput.value.trim() && !tags.value.includes(tagInput.value.trim())) {
        tags.value.push(tagInput.value.trim());
        tagInput.value = "";
    }
};

const removeTag = (index) => {
    tags.value.splice(index, 1);
};

const successMessage = ref("");
const errorMessage = ref("");

// 每個欄位的錯誤狀態
const errors = ref({
    subject: false,
    price: false,
    location: false,
    startTime: false,
    endTime: false,
});

const submitForm = () => {
    // 初始化錯誤
    errors.value = {
        subject: !course.value.subject,
        price: !course.value.price,
        location: !course.value.location,
        startTime: !startTime.value,
        endTime: !endTime.value,
    };

    const hasError = Object.values(errors.value).some((v) => v);

    if (hasError) {
        errorMessage.value = "❗請填寫所有必填欄位（描述可選）";
        successMessage.value = "";
        return;
    }

    const formData = {
        ...course.value,
        start_time: startTime.value,
        end_time: endTime.value,
        tags: tags.value,
    };

    console.log("📦 課程資料送出:", formData);

    successMessage.value = "✅ 課程建立成功！";
    errorMessage.value = "";
};

import { watch } from "vue";

// 即時監控欄位輸入來移除錯誤框框
watch(
    course,
    (newVal) => {
        if (newVal.subject) errors.value.subject = false;
        if (newVal.price) errors.value.price = false;
        if (newVal.location) errors.value.location = false;
    },
    { deep: true }
);

watch(startTime, (val) => {
    if (val) errors.value.startTime = false;
});

watch(endTime, (val) => {
    if (val) errors.value.endTime = false;
});

const goBack = () => {
    router.push("/teacherdashboard");
};
</script>

<template>
    <Navbar />
    <div class="course-form">
        <h2 class="form-title">課程設定</h2>

        <div class="form-group">
            <label>標題：</label>
            <input
                v-model="course.subject"
                :class="{ 'input-error': errors.subject }"
                placeholder="請輸入課程名稱..."
            />
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>開始時間：</label>
                <input
                    type="time"
                    v-model="startTime"
                    :class="{ 'input-error': errors.startTime }"
                />
            </div>
            <div class="form-group">
                <label>結束時間：</label>
                <input
                    type="time"
                    v-model="endTime"
                    :class="{ 'input-error': errors.endTime }"
                />
            </div>
        </div>

        <div class="form-group">
            <label>價格：</label>
            <input
                type="number"
                v-model="course.price"
                :class="{ 'input-error': errors.price }"
                placeholder="請輸入價格，例如 600"
            />
        </div>

        <div class="form-group">
            <label>地點：</label>
            <select
                v-model="course.location"
                :class="{ 'input-error': errors.location }"
            >
                <option value="" disabled>請選擇地點</option>
                <option value="線上授課">線上授課</option>
                <option value="學生家">學生家</option>
                <option value="教師地點">教師地點</option>
            </select>
        </div>

        <div class="form-group">
            <label>描述：</label>
            <textarea
                v-model="course.description"
                placeholder="請輸入課程描述..."
            ></textarea>
        </div>

        <div class="form-group">
            <label>標籤：</label>
            <input
                v-model="tagInput"
                @keydown.enter.prevent="addTag"
                placeholder="輸入標籤後按 Enter"
            />
            <div class="tag-list">
                <span v-for="(tag, index) in tags" :key="index" class="tag">
                    {{ tag }}
                    <button @click="removeTag(index)">×</button>
                </span>
            </div>
        </div>

        <div class="form-actions">
            <button @click="submitForm">建立課程</button>
            <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
            <p v-if="successMessage" class="success-message">
                {{ successMessage }}
            </p>
            <button @click="goBack">回到個人檔案</button>
        </div>
    </div>
    <Footer />
</template>

<style scoped>
.course-form {
    max-width: 720px;
    margin: 0 auto;
    margin-top: 125px;
    margin-bottom: 25px;
    padding: 24px;
    border-radius: 16px;
    background: #f7f9fc;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.form-title {
    font-size: 24px;
    margin-bottom: 20px;
    font-weight: bold;
    text-align: center;
}

.form-group {
    margin-bottom: 16px;
}

label {
    display: block;
    margin-bottom: 6px;
    font-weight: bold;
}

input,
textarea,
select {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 16px;
}

textarea {
    min-height: 100px;
    resize: vertical;
}

.form-row {
    display: flex;
    gap: 20px;
}

.form-row .form-group {
    flex: 1;
}

.tag-list {
    margin-top: 8px;
}

.tag {
    display: inline-flex;
    align-items: center;
    background: #6366f1;
    color: #fff;
    padding: 4px 10px;
    border-radius: 12px;
    margin-right: 6px;
    margin-bottom: 6px;
    font-size: 14px;
}

.tag button {
    background: transparent;
    border: none;
    color: #fff;
    margin-left: 6px;
    cursor: pointer;
}

.form-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 24px;
}

button {
    padding: 10px 20px;
    font-size: 16px;
    background: #4f46e5;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
}

button:hover {
    background: #4338ca;
}
.error-message {
    margin-top: 10px;
    color: #dc2626; /* 紅色 */
    font-weight: bold;
    text-align: center;
}

.success-message {
    margin-top: 10px;
    color: #10b981; /* 綠色 */
    font-weight: bold;
    text-align: center;
}

.input-error {
    border: 2px solid #dc2626 !important;
    background-color: #fef2f2;
}
</style>
