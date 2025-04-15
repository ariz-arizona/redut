<script setup>
const { fetchData } = useApiFetch()

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
    submit: '',
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
        const { data, status } = await fetchData('feedback',
            'post',
            undefined,
            formData.value,
        );

        if (status.value == 'success') {
            // Устанавливаем флаг успешной отправки
            isFormSubmitted.value = true;
            formData.value = {
                name: '',
                phone: '',
                acceptance: false,
            };
            resetErrors();
        }
        if (status.value == 'error') {
            errors.value.submit = 'Ошибка при отправке'
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
        submit: '',
    };
};

// Очистка конкретной ошибки
const clearError = (field) => {
    errors.value['submit'] = '';
    errors.value[field] = '';
};
</script>

<template>
    <form class="prose relative" @submit.prevent="submitForm">
        <!-- Поле "Имя" -->
        <div class="flex flex-col gap-8" :class="{ 'invisible': isFormSubmitted }">
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
                <input id="phone" v-model="formData.phone" type="tel" placeholder="Введите ваш телефон"
                    class="input w-full" :class="{ 'border-red-500': errors.phone }" @keydown="clearError('phone')" />
            </label>

            <!-- Согласие на обработку данных -->
            <label :data-error="errors.acceptance" class="flex gap-2 justify-start items-center"
                :class="{ 'text-red-500': errors.acceptance }">
                <input v-model="formData.acceptance" type="checkbox" class="input" @change="clearError('acceptance')" />
                <span>Принимаю <NuxtLink to="policy">условия обработки персональных данных</NuxtLink></span>
            </label>

            <!-- Кнопка отправки -->
            <button class="leadbtn p-4" :class="{ 'ring-red-500 text-red-500': errors.submit }">
                <span v-if="errors.submit !== ''">Ошибка при отправке</span>
                <span v-else>Отправить</span>
            </button>
        </div>
        <!-- Сообщение об успешной отправке -->
        <div v-if="isFormSubmitted" class="prose text-center text-2xl absolute top-0">
            Ваше сообщение успешно отправлено!
        </div>
    </form>

</template>