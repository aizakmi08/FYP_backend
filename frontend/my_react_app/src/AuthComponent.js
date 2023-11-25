import React, { useState } from 'react';
import { auth } from './firebase';
import { useHistory } from 'react-router-dom';

const AuthComponent = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const history = useHistory();

  const handleSignup = async () => {
    try {
      await auth.createUserWithEmailAndPassword(email, password);
      // User successfully signed up
      history.push('/'); // Redirect to home page after signup
    } catch (error) {
      // Handle signup errors
      console.error(error.message);
    }
  };

  const handleLogin = async () => {
    try {
      await auth.signInWithEmailAndPassword(email, password);
      // User successfully logged in
      history.push('/'); // Redirect to home page after login
    } catch (error) {
      // Handle login errors
      console.error(error.message);
    }
  };

  return (
    <div>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleSignup}>Sign Up</button>
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default AuthComponent;
