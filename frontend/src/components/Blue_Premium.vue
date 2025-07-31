<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps({
    isPremium: {
        type: Boolean,
        required: true,
    },
});

const emit = defineEmits(["upgrade"]);

function handleUpgradeClick() {
    emit("upgrade");
}
</script>

<template>
    <span
        v-if="isPremium"
        class="bg-blue-500 text-white text-sm px-2 py-1 rounded"
    >
        Premium
    </span>
    <button
        v-else
        @click="handleUpgradeClick"
        class="bg-gray-300 text-gray-700 text-sm px-2 py-1 rounded hover:bg-gray-400 transition"
    >
        升級藍鑽會員
    </button>
</template>

<style scoped></style>
