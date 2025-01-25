    <template>
        <li :style="{ textDecoration: task.completed ? 'line-through' : 'none' }" class="listItem">
            <input type="checkbox" :checked="task.completed" @change="toggleTask"/>
            {{ task.title }}
            <button @click="deleteTask">Delete</button>
        </li>
    </template>

    <script>
    export default {
        props: ['task'],
        emits: ['task-toggle','task-delete'],
        methods: {
            toggleTask(){
              this.$emit('task-toggle', this.task.id, !this.task.completed);
            },
            deleteTask(){
                this.$emit('task-delete', this.task.id);
            }
        }
    }
    </script>

    <style scoped>
    .listItem {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px;
        border-bottom: 1px solid #eee;
        background-color: white;
    }

    .listItem input {
        margin-right: 10px;
    }

    .listItem button {
        background-color: #dc3545;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        padding: 5px 10px;
    }

    .listItem button:hover {
      background-color: #c82333;
    }
    </style>
