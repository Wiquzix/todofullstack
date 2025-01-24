    <template>
        <form class="form" @submit.prevent="handleSubmit">
            <input class="input" type="text" placeholder="Add task" v-model="title" />
            <button class="button" type="submit">Add</button>
        </form>
    </template>

    <script>
    import { ref } from 'vue';
    export default {
        setup(props, { emit }){
            const title = ref('');
            const handleSubmit = () => {
                if(title.value.trim()){
                   emit('task-create', {title: title.value});
                   title.value = '';
                }
            };
            return {
              title,
              handleSubmit
            }
        },
        emits: ['task-create']
    }
    </script>

    <style scoped>
    .form {
        display: flex;
        margin-bottom: 20px;
        gap: 10px;
    }
    
    .input {
        flex: 1;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    
    .button {
        padding: 10px 15px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    
    .button:hover {
        background-color: #0056b3;
    }
    </style>
