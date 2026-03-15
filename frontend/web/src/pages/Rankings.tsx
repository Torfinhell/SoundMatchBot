import React, { useEffect, useState } from 'react';
import { getLeaderboard } from '../services/api';
import UserCard from '../components/Rankings/UserCard';

export default function Rankings() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    getLeaderboard().then(setUsers);
  }, []);

  return (
    <div style={{ padding: 20, background: '#111', color: '#fff', minHeight: '100vh' }}>
      <h1>Global Leaderboard</h1>
      {users.map((u: any) => <UserCard key={u.user_id} user={u} />)}
    </div>
  );
}