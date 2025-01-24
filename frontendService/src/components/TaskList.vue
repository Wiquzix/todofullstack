    <template>
        <ul class="list">
            <TaskItem v-for="task in tasks" :key="task.id" :task="task" @task-toggle="onTaskToggle" @task-delete="onDelete" />
        </ul>
    </template>

    <script>
    import TaskItem from './TaskItem.vue';
    export default {
        components: {
            TaskItem
        },
        props: ['tasks'],
        emits: ['task-toggle', 'task-delete'],
        methods: {
            onTaskToggle(id, completed) {
                this.$emit('task-toggle', id, completed);
            },
            onDelete(id) {
                this.$emit('task-delete',id);
            }
        }
    }
    </script>
    <style scoped>
    .list {
        padding: 0;
        list-style: none;
    }
    </style>
