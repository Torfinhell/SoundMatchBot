import React from 'react';
export default function UserCard({ user }: { user: any }) {
  return (
    <div style={{ border: '1px solid #333', padding: 10, margin: '5px 0' }}>
      <h3>#{user.rank} {user.username || 'Anon'}</h3>
      <p>Score: {user.score.toFixed(2)}</p>
    </div>
  );
}