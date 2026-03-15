import axios from 'axios';
import { BACKEND_URL } from '../config';

const api = axios.create({ baseURL: BACKEND_URL });

export const getLeaderboard = () => api.get('/leaderboard').then(r => r.data);
export const createPoll = (title: string, questions: string[], pwd: string) => 
    api.post('/polls', { title, questions, admin_password: pwd });