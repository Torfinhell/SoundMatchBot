import React, { useState } from 'react';
import { createPoll } from '../services/api';

export default function AdminPanel() {
  const [title, setTitle] = useState('');
  const [q1, setQ1] = useState('');
  const [pwd, setPwd] = useState('');

  const submit = async () => {
    await createPoll(title, [q1], pwd);
    alert('Poll Created');
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Create Poll</h2>
      <input placeholder="Title" onChange={e => setTitle(e.target.value)} /><br/>
      <input placeholder="Question" onChange={e => setQ1(e.target.value)} /><br/>
      <input type="password" placeholder="Admin Password" onChange={e => setPwd(e.target.value)} /><br/>
      <button onClick={submit}>Create</button>
    </div>
  );
}