<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";

const router = useRouter();

const review = ref({
    course_id: "", // 可根據情境動態傳入
    rating: "",
    comment: "",
});

const errors = ref({
    course_id: false,
    rating: false,
});

const successMessage = ref("");
const errorMessage = ref("");

const submitReview = () => {
    errors.value = {
        course_id: !review.value.course_id,
        rating: !review.value.rating,
    };

    const hasError = Object.values(errors.value).some((v) => v);
    if (hasError) {
        errorMessage.value = "❗請填寫所有必填欄位";
        successMessage.value = "";
        return;
    }

    const formData = {
        ...review.value,
        created_at: new Date().toISOString(),
    };

    console.log("📦 評價送出:", formData);

    successMessage.value = "✅ 評價送出成功！";
    errorMessage.value = "";
    // 這裡可改為實際 API 發送程式碼
};

const goBack = () => {
    router.back();
};
</script>

<template>
    <Navbar />
    <div class="review-form">
        <h2 class="form-title">課程評價</h2>

        <div class="form-group">
            <label>課程 ID：</label>
            <input
                type="number"
                v-model="review.course_id"
                :class="{ 'input-error': errors.course_id }"
                placeholder="請輸入課程編號"
            />
        </div>

        <div class="form-group">
            <label>評分：</label>
            <select
                v-model="review.rating"
                :class="{ 'input-error': errors.rating }"
            >
                <option value="">請選擇星等</option>
                <option value="1">⭐</option>
                <option value="2">⭐⭐</option>
                <option value="3">⭐⭐⭐</option>
                <option value="4">⭐⭐⭐⭐</option>
                <option value="5">⭐⭐⭐⭐⭐</option>
            </select>
        </div>

        <div class="form-group">
            <label>評論（選填）：</label>
            <textarea
                v-model="review.comment"
                placeholder="請輸入你的想法..."
            ></textarea>
        </div>

        <div class="form-actions">
            <button @click="submitReview">送出評價</button>
            <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
            <p v-if="successMessage" class="success-message">
                {{ successMessage }}
            </p>
            <button @click="goBack">返回上一頁</button>
        </div>
    </div>
    <Footer />
</template>

<style scoped>
.review-form {
    max-width: 600px;
    margin: 120px auto 40px;
    padding: 24px;
    background: #f8fafc;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.form-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
}

.form-group {
    margin-bottom: 16px;
}

label {
    font-weight: bold;
    margin-bottom: 6px;
    display: block;
}

input,
select,
textarea {
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

.input-error {
    border: 2px solid #dc2626;
    background-color: #fef2f2;
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

.form-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 24px;
}

.error-message {
    color: #dc2626;
    text-align: center;
    font-weight: bold;
}

.success-message {
    color: #10b981;
    text-align: center;
    font-weight: bold;
}
</style>
