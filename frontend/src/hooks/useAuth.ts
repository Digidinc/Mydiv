import { create } from 'zustand';

interface User {
  id: string;
  name: string;
  email: string;
  image?: string;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  signUp: (email: string, password: string, name: string) => Promise<void>;
}

export const useAuth = create<AuthState>((set) => ({
  user: null,
  isLoading: false,
  error: null,
  signIn: async (email: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      // TODO: Implement actual authentication
      const response = await fetch('/api/auth/signin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      
      if (!response.ok) {
        throw new Error('Authentication failed');
      }

      const user = await response.json();
      set({ user, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },
  signOut: async () => {
    set({ isLoading: true, error: null });
    try {
      // TODO: Implement actual sign out
      await fetch('/api/auth/signout', { method: 'POST' });
      set({ user: null, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },
  signUp: async (email: string, password: string, name: string) => {
    set({ isLoading: true, error: null });
    try {
      // TODO: Implement actual sign up
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        throw new Error('Registration failed');
      }

      const user = await response.json();
      set({ user, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },
}));