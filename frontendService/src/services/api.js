   import axios from 'axios';
   const AUTH_BASE_URL = 'http://localhost:8001';
   const TASK_BASE_URL = 'http://localhost:8002';
  export const registerUser = async (user) => {
        return axios.post(`${AUTH_BASE_URL}/users`, user,  {
            headers: {
                "Content-Type": "application/json",
            },
        });
    };

    export const loginUser = async (user) => {
        return axios.post(`${AUTH_BASE_URL}/token`, new URLSearchParams(user).toString(),
        {
             headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });
    };

    export const fetchTasks = async (token) => {
        const response = await axios.get(`${TASK_BASE_URL}/tasks`, {
          headers: {
              Authorization: `Bearer ${token}`
            }
        });
        return response.data;
    };

    export const createTask = async (task, token) => {
        const response = await axios.post(`${TASK_BASE_URL}/tasks`, task, {
          headers: {
              Authorization: `Bearer ${token}`,
           }
        });
        return response.data;
    };

    export const updateTask = async (id, task, token) => {
        const response = await axios.put(`${TASK_BASE_URL}/tasks/${id}`, task, {
          headers: {
              Authorization: `Bearer ${token}`,
          }
        });
        return response.data;
     };

    export const deleteTask = async (id, token) => {
        await axios.delete(`${TASK_BASE_URL}/tasks/${id}`, {
          headers: {
              Authorization: `Bearer ${token}`,
           }
         });
    };
