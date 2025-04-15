<script setup>
import { ref } from 'vue';

// Реактивные данные формы
const formData = ref({
    name: '',
    phone: '',
    acceptance: false,
});

// Хранилище ошибок
const errors = ref({
    name: '',
    phone: '',
    acceptance: '',
});

// Флаг для отслеживания состояния отправки
const isFormSubmitted = ref(false);

// Метод для отправки формы
const submitForm = async () => {
    // Сброс ошибок перед проверкой
    resetErrors();

    // Проверка имени
    if (!formData.value.name.trim()) {
        errors.value.name = 'Поле "Имя" обязательно';
    }

    // Проверка телефона
    const isValidPhone = validatePhoneNumber(formData.value.phone);
    if (!isValidPhone) {
        errors.value.phone = 'Неверный формат телефона';
    }

    // Проверка согласия
    if (!formData.value.acceptance) {
        errors.value.acceptance = 'Необходимо подтвердить согласие';
    }

    // Если есть ошибки, не отправляем форму
    if (Object.values(errors.value).some((error) => error)) {
        return;
    }

    // Отправка данных на сервер
    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData.value),
        });

        if (response.ok) {
            // Устанавливаем флаг успешной отправки
            isFormSubmitted.value = true;
            formData.value = {
                name: '',
                phone: '',
                acceptance: false,
            };
            resetErrors();
        } else {
            alert('Ошибка при отправке формы. Попробуйте позже.');
        }
    } catch (error) {
        console.error('Ошибка при отправке:', error);
        alert('Произошла ошибка. Попробуйте позже.');
    }
};

// Валидация телефона
const validatePhoneNumber = (phone) => {
    // Очищаем номер от всех символов, кроме цифр
    const cleanedPhone = phone.replace(/[^0-9]/g, '');

    // Проверяем, что длина номера равна 11 цифрам
    return cleanedPhone.length === 11;
};

// Сброс всех ошибок
const resetErrors = () => {
    errors.value = {
        name: '',
        phone: '',
        acceptance: '',
    };
};

// Очистка конкретной ошибки
const clearError = (field) => {
    errors.value[field] = '';
};
</script>

<template>
    <form v-if="!isFormSubmitted" class="prose flex flex-col gap-8" @submit.prevent="submitForm">
        <!-- Поле "Имя" -->
        <label for="name" :data-error="errors.name" class="flex flex-col justify-center items-start"
            :class="{ 'text-red-500': errors.name }">
            <div>
                <template v-if="errors.name">Пожалуйста, укажите имя</template>
                <template v-else>Ваше имя:</template>
            </div>
            <input id="name" v-model="formData.name" type="text" placeholder="Введите ваше имя" class="input w-full"
                :class="{ 'border-red-500': errors.name }" @keydown="clearError('name')" />
        </label>

        <!-- Поле "Телефон" -->
        <label for="phone" :data-error="errors.phone" class="flex flex-col justify-center items-start"
            :class="{ 'text-red-500': errors.phone }">
            <div>
                <template v-if="errors.phone">Укажите телефон</template>
                <template v-else>Телефон:</template>
            </div>
            <input id="phone" v-model="formData.phone" type="tel" placeholder="Введите ваш телефон" class="input w-full"
                :class="{ 'border-red-500': errors.phone }" @keydown="clearError('phone')" />
        </label>

        <!-- Согласие на обработку данных -->
        <label :data-error="errors.acceptance" class="flex gap-2 justify-start items-center"
            :class="{ 'text-red-500': errors.acceptance }">
            <input v-model="formData.acceptance" type="checkbox" class="input" @change="clearError('acceptance')" />
            <span>Принимаю <NuxtLink to="policy">условия обработки персональных данных</NuxtLink></span>
        </label>

        <!-- Кнопка отправки -->
        <button class="leadbtn p-4">
            Отправить
        </button>
    </form>

    <!-- Сообщение об успешной отправке -->
    <div v-else class="prose text-center text-2xl">
        Ваше сообщение успешно отправлено!
    </div>
</template>